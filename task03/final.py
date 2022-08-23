# Dependencies
from __future__ import annotations
from typing import Any, Optional
from urllib.request import urlopen
import ssl
from xmlrpc.client import boolean
from bs4 import BeautifulSoup
from operator import itemgetter
import itertools
import io
import re
import datetime


PARTIES = ["spd","csu","freie wähler","bündnis 90/die grünen","fraktionslos"]
SPECIAL_MARKS = ["(spd)\n",  "(csu)\n", "(freie wähler)\n", "(bündnis 90/die grünen)\n", "(fraktionslos)\n"]

# ABCDEFGHIJKLMNOPRSTUVWZ
def _load_html_pages(register="ABCDE") -> list[str]:
    html_list = []
    for letter in register:
        try:
            with open(letter + ".html") as f:
                html = f.read()
            html_list.append(html)
        except IOError:
            url = "https://www.bayern.landtag.de/fileadmin/Sach_Sprechregister/WP17/HTML/Sprechregister/SprechReg_" + letter + ".html"
            fp = urlopen(url, context = ssl.SSLContext())
            html = fp.read().decode('utf-8')
            fp.close()
            html_list.append(html)
            with open(letter + ".html", "w") as f:
                f.write(html)
    return html_list

def count_speakers(html_list: list[str], party: Optional[str] = None) -> int:
    soups = [BeautifulSoup(html, 'lxml-xml') for html in html_list]
    return 0 if len(html_list) == 0 else len(_get_all_speakers(soups, None)) if party is None else len(_get_all_speakers(soups, party))

def _get_all_speakers(soups: list[BeautifulSoup], party: Optional[str] = None) -> list[str]:
    if party is not None:
        party = party.lower()
    all_speakers = [speaker.get_text().lower() for soup in soups for speaker in soup.find_all(["dt"], class_="redner")]
    return all_speakers if party is None else [party_specific_speaker for party_specific_speaker in all_speakers if party_specific_speaker.find(party) != -1]

def count_speeches(html_list: list[str], party: Optional[str] = None) -> int:
    soups = [BeautifulSoup(html, 'lxml-xml') for html in html_list]
    return 0 if len(html_list) == 0 else len(_extract_description(soups, None)) if party is None else len(_extract_description(soups, party))

def _extract_description(soups: list[BeautifulSoup], party: Optional[str] = None) -> list[str]:
    politicians = _get_all_speakers(soups, party)
    over_html_storage = []
    for soup in soups: 
        # descriptions = soup.dl.get_text('\n').lower().replace('\n\n', '')
        # # Get Titles
        # titles_unparsed = soup.find_all("dt")
        # cleaned_titles = []
        # for title in titles_unparsed:
        #     isSpeaker = False
        #     for s in PARTIES:
        #         if s in title.text.lower():
        #             isSpeaker = True
        #     if (isSpeaker == True):
        #         continue
        #     cleaned_titles.append(title.text)
        # titles = [t.lower() for t in cleaned_titles]

        # print(titles)

        # print("******")
 
        titles2 = [p.find_next_sibling("dd").find_all("dt") for soup in soups for p in soup.find_all("dt", class_="redner")]
        over_html_storage.append(titles2)
        # print(titles2)

        # Remove titles
        # lines = io.StringIO(descriptions)
        # tmp_storage = []
        # lines = [l.replace('\n', '') for l in lines]
        # for l in lines:
        #     isTitle = False
        #     for t in titles:
        #         if t == l:
        #             isTitle = True 
        #     if isTitle == True:
        #         continue
        #     tmp_storage.append(l)
        # descriptions_with_no_titles = '\n'.join(tmp_storage)

        # lines_with_no_title = io.StringIO(descriptions_with_no_titles)

        # cleaned_line_list = []
        # for line in lines_with_no_title:
        #     speaker_flag = False
        #     for s in SPECIAL_MARKS:
        #         if line.endswith(s):
        #                 speaker_flag = True
        #     if speaker_flag == True:
        #         tmp_speaker = line.replace('\n', ' ')
        #         continue
        #     else:
        #         line = tmp_speaker + line
        #         cleaned_line_list.append(line)
        # cleaned_line = ' '.join(cleaned_line_list)
        # lines_list = cleaned_line.splitlines()
        # flag = False
        # description = ''

        # d = []
        # for line in lines_list:
        #     if ') zu ' in line:
        #         flag = True
        #     description = description + line
        #     if flag == True:
        #         d.append(description)
        #         description = ''
        #         flag = False

        # if party is not None:
        #     party = party.lower()
        #     if party not in PARTIES:
        #         return []

        #     pattern = "("+party+")"
        #     politicians = [p for p in politicians if pattern in p]
        #     over_html_storage.append([descrip for descrip in d for p in politicians if p in descrip])
        # else:
        #     over_html_storage.append(d)
    
    d = list(itertools.chain(*over_html_storage))
    print(d)

    return d

def most_speeches(html_list: list[str], n: Optional[int] = None, party: Optional[str] = None) -> list[tuple[int, str]]:
    soups = [BeautifulSoup(html, 'lxml-xml') for html in html_list]
    return [] if len(html_list)==0 or (n == 0) else _get_list_of_speakers_with_count(True, soups, n, party)

def fewest_speeches(html_list: list[str], n: Optional[int] = None, party: Optional[str] = None) -> list[tuple[int, str]]:
    soups = [BeautifulSoup(html, 'lxml-xml') for html in html_list]
    return [] if len(html_list)==0 or (n == 0) else _get_list_of_speakers_with_count(False, soups, n, party)

def _get_list_of_speakers_with_count(sorted_status: boolean, soups: list[BeautifulSoup], n: Optional[int] = None, party: Optional[str] = None) -> list[tuple[int, str]]:
    speeches = _extract_description(soups, party)
    speaker_list = _get_all_speakers(soups, party)
    count_speeches = [0] * len(speaker_list)
    for i, speaker in enumerate(speaker_list):
            for s in speeches:
                if speaker in s:
                    count_speeches[i] += 1

    speakers = [_prepare_speaker_name(s) for s in speaker_list]
    all_speaker_counts = list(zip(count_speeches, speakers))
    sorted_acc = list(sorted(all_speaker_counts, key = itemgetter(0), reverse = sorted_status))
    return sorted_acc[:n]

def _prepare_speaker_name(name: str) -> str:
    name = re.sub(r' (\(.*?\))', '', name)
    n = name.split(', ')
    n.sort(reverse=True)
    politician = ' '.join(n)
    return politician.title() if politician != 'von brunn florian' else 'Florian von Brunn'

def count_terms(html_list: list[str], term_list: list[str], party: Optional[str] = None) -> dict[str, int]:
    if len(html_list) == 0:
        return dict((term,0) for term in term_list)
    else:
        soups = [BeautifulSoup(html, 'lxml-xml') for html in html_list]
        descriptions = _extract_description(soups, party)     
        count_storage = [0] * len(term_list)
        term_list = [t for t in term_list]
    
        for i, term in enumerate(term_list):
            t = term.lower()
            for d in descriptions:
                if t in d:
                    count_storage[i] += 1

        return dict(zip(term_list, count_storage)) 

def compare_parties(html_list: list[str], term_list: list[str]) -> list[tuple[str, str]]:
    if len(html_list) == 0 or len(term_list) == 0:
        return [("0.00%", "bündnis 90/die grünen"), ("0.00%", "csu"),  ("0.00%", "fraktionslos"), ("0.00%", "freie wähler"), ("0.00%", "spd")]

    s = [count_speeches(html_list, p) for p in PARTIES]
    # print(s)

    t = [sum(count_terms(html_list, term_list, p).values()) for p in PARTIES]
    # print(t)

    if (all(counts == 0 for counts in t)):
        return [("0.00%", "bündnis 90/die grünen"), ("0.00%", "csu"),  ("0.00%", "fraktionslos"), ("0.00%", "freie wähler"), ("0.00%", "spd")]

    rates = [t[i]/s[i] if s[i] !=0 else 0 for i in range(5)]
    # print(rates)

    tuple_list = [("{:.2%}".format(rates[0]), "spd"),
        ("{:.2%}".format(rates[1]), "csu"),
        ("{:.2%}".format(rates[2]), "freie wähler"),
        ("{:.2%}".format(rates[3]), "bündnis 90/die grünen"),
        ("{:.2%}".format(rates[4]), "fraktionslos")]

    return list(sorted(tuple_list, key = itemgetter(0), reverse = True))

if __name__ == "__main__":
    html_list = _load_html_pages()
    now = datetime.datetime.now()
    soups = [BeautifulSoup(html, 'lxml-xml') for html in html_list]
    # print(compare_parties(html_list, ["straße", "auto"]))
    print(_extract_description(soups))
    later = datetime.datetime.now()
    print('This method takes {}'.format(later - now))

    