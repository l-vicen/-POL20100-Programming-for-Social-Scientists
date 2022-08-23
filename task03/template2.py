# Dependencies
from __future__ import annotations
from typing import Optional
from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
import re
import io
PARTIES = ["spd","csu","freie wähler","bündnis 90/die grünen","fraktionslos"]
ZERO_TUPLE_LIST = [("0.00%", "bündnis 90/die grünen"), ("0.00%", "csu"),  ("0.00%", "fraktionslos"), ("0.00%", "freie wähler"), ("0.00%", "spd")]
EDGES = ['plpr', '(drs.', '(änderung', 'hier', 'kap.', 'bundesautobahnen', ') öffentlichkeitsarbeit', 'infrastrukturgesellschaft für autobahnen']
SPECIAL_MARKS = ["(spd)\n",  "(csu)\n", "(freie wähler)\n", "(bündnis 90/die grünen)\n", "(fraktionslos)\n"]
def _load_html_pages(register="A") -> list[str]:
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
    return 0 if len(html_list) == 0 else len(_get_all_speakers(html_list))  if party is None else len(_get_all_speakers(html_list, party))
def count_speeches(html_list: list[str], party: Optional[str] = None) -> int:
    if (len(html_list) == 0):
        return 0
    all_counts_over_htmls = 0
    party_specific_counts_over_htmls = 0
    for html in html_list:
        soup = BeautifulSoup(html, 'lxml-xml')
        l1 = soup.dl.get_text("\n").lower().replace('\n\n', '')
        targets_list = []
        multi_line_uncleaned = io.StringIO(l1)
        for line in multi_line_uncleaned:
            line = line.replace('\n', '').lower()
            if line.endswith("(spd)") or line.endswith("(csu)") or line.endswith("(freie wähler)") or line.endswith("(bündnis 90/die grünen)") or line.endswith("(fraktionslos)") or line.startswith('plpr'):
                targets_list.append(line + '\n')
        targets = ''.join(targets_list)
        multi_line_pseudo_clean = io.StringIO(targets)
        tmp_speaker = ''
        cleaned_line_list = []
        for line in multi_line_pseudo_clean:
            if line.startswith('plpr') == False:
                tmp_speaker = line.replace('\n', ' ')
                continue
            else:
                line = tmp_speaker + line
                cleaned_line_list.append(line)
        cleaned_line = ''.join(cleaned_line_list)  
        final_clean = io.StringIO(cleaned_line)
        if party is None:
            all_speeches = 0
            for line in final_clean:
                all_speeches += 1
            all_counts_over_htmls += all_speeches
        else:
            party_count = 0
            party = party.lower()
            for line in final_clean:
                if "("+party+")" in line:    
                    party_count += 1
            party_specific_counts_over_htmls += party_count
    return all_counts_over_htmls if party is None else party_specific_counts_over_htmls
def most_speeches(html_list: list[str], n: Optional[int] = None, party: Optional[str] = None) -> list[tuple[int, str]]:
    list_with_all = _get_list_of_speakers_with_count(html_list, n, party)
    list_with_all.sort(key = lambda element: element[0], reverse = True)
    return _return_case(n, list_with_all)

def fewest_speeches(html_list: list[str], n: Optional[int] = None, party: Optional[str] = None) -> list[tuple[int, str]]:
    list_with_all = _get_list_of_speakers_with_count(html_list, n, party)
    list_with_all.sort(key = lambda element: element[0])
    return _return_case(n, list_with_all)
    
def _get_list_of_speakers_with_count(html_list: list[str], n: Optional[int] = None, party: Optional[str] = None) -> list[tuple[int, str]]:
    if len(html_list)==0 or (n == 0): 
        return []

    speaker_list = _get_all_speakers(html_list, party)
    # speaker_list.sort()
    count_speeches = [0] * len(speaker_list)

    speeches = _extract_description(html_list, party)
    # speeches.sort()  

    final_clean = io.StringIO(speeches)
    for line in final_clean:
        for i in range(len(speaker_list)):
            if (line.startswith(speaker_list[i])):
                count_speeches[i] = count_speeches[i] + 1
                break
    ops_two = [re.sub(r' (\(.*?\))', '', s) for s in speaker_list]
    ops_three = []
    for element in ops_two:
        name = ' '
        tmpList = element.split(', ')
        tmpList.sort(reverse=True)
        name = name.join(tmpList)
        ops_three.append(name.title())
    speakers_edge = [s if s.find('Von Brunn Florian') == -1 else 'Florian von Brunn' for s in ops_three]
    speakers_final = [s.replace('Prof. Dr. ', '') if s.startswith('Prof. Dr. ') else s for s in speakers_edge]
    list_with_all = list(zip(count_speeches, speakers_final))
    return list_with_all
def count_terms(html_list: list[str], term_list: list[str], party: Optional[str] = None) -> dict[str, int]:
    if len(html_list) == 0:
        return dict((term,0) for term in term_list)
    words = _extract_description(html_list, party)      
    count_storage = [0] * len(term_list)
    for i in range(len(term_list)):
        appearances = 0
        lines = io.StringIO(words)    
        t = term_list[i].lower()
        for line in lines:
            if t in line:
                appearances += 1
        count_storage[i] += appearances
    return dict(zip(term_list, count_storage))

def compare_parties(html_list: list[str], term_list: list[str]) -> list[tuple[str, str]]:
    if len(html_list) == 0 or len(term_list) == 0:
        return ZERO_TUPLE_LIST

def _get_all_speakers(html_list: list[str], party: Optional[str] = None) -> list[str]:
    all_speakers = []
    for html in html_list:
        soup = BeautifulSoup(html, 'lxml-xml')
        speaker_set = soup.find_all(["dt"], class_="redner")
        for speaker in speaker_set:
            all_speakers.append(speaker.get_text())
    all_speakers = [s.lower() for s in all_speakers]
    if party is None:
        return list(set(all_speakers)) 
    else: 
        return list(set([party_specific_speaker for party_specific_speaker in all_speakers if party_specific_speaker.lower().find(party.lower()) != -1]))
def _extract_description(html_list: list[str], party: Optional[str] = None) -> str:
    targets_list = []
    for html in html_list:
        soup = BeautifulSoup(html, 'lxml-xml')
        l1 = soup.dl.get_text("\n").lower().replace('\n\n', '')
        multi_line_uncleaned = io.StringIO(l1)
        for line in multi_line_uncleaned:
            line = line.replace('\n', '').lower()
            if line.startswith('zu'): 
                continue
            targets_list.append(line + '\n')
        targets = ''.join(targets_list)
        tmp_speaker = ''
        multi_line_pseudo_clean = io.StringIO(targets)
        cleaned_line_list = []
        for line in multi_line_pseudo_clean:
            speaker_flag = False
            for s in SPECIAL_MARKS:
                if line.endswith(s): speaker_flag = True
            if speaker_flag == True:
                tmp_speaker = line.replace('\n', ' ')
                continue
            else:
                line = tmp_speaker + line
                cleaned_line_list.append(line)
        cleaned_line = ''.join(cleaned_line_list)
        third_ops = io.StringIO(cleaned_line)
        very_clean_line_list = []
        for line in third_ops:
            if len(line.split()) <= 5:
                continue 
            else:
                flag = False
                for e in EDGES:
                    if e in line:
                        flag = True
                if flag == True:
                    continue
                else:
                    very_clean_line_list.append(line)
        very_clean_line = ''.join(very_clean_line_list)           
    if party is None: 
        return _helper_last_formatting(very_clean_line)
    else:
        party = party.lower()
        party_specific = ''
        fourth_ops = io.StringIO(very_clean_line)
        for line in fourth_ops: 
            if "(" + party + ")" in line: party_specific += line
        return _helper_last_formatting(party_specific)
def _get_all_speakers(html_list: list[str], party: Optional[str] = None) -> list[str]:
    if (len(html_list) == 0):
        return 0 
    else:
        all_speakers = []
        for html in html_list:
            soup = BeautifulSoup(html, 'lxml-xml')
            speaker_set = soup.find_all(["dt"], class_="redner")
            for speaker in speaker_set:
                all_speakers.append(speaker.get_text())
        all_speakers = [s.lower() for s in all_speakers]
        if party is None:
            return list(set(all_speakers)) 
        else: 
            return list(set([party_specific_speaker for party_specific_speaker in all_speakers if party_specific_speaker.lower().find(party.lower()) != -1]))
def _get_all_speeches(html_list: list[str]) -> str:
    targets = []
    for html in html_list:
        soup = BeautifulSoup(html, 'lxml-xml')
        l1 = soup.dl.get_text("\n").lower().replace('\n\n', '')
        multi_line_uncleaned = io.StringIO(l1)
        for line in multi_line_uncleaned:
            line = line.replace('\n', '').lower()
            if line.endswith("(spd)") or line.endswith("(csu)") or line.endswith("(freie wähler)") or line.endswith("(bündnis 90/die grünen)") or line.endswith("(fraktionslos)") or line.startswith('plpr'):
                targets.append(line + '\n')
        targets_string = ''.join(targets)
        tmp_speaker = ''
        multi_line_pseudo_clean = io.StringIO(targets_string)
        list_split = []
        for line in multi_line_pseudo_clean:
            if line.startswith('plpr') == False:
                tmp_speaker = line.replace('\n', ' ')
                continue
            else:
                line = tmp_speaker + line
                list_split.append(line)
    list_split.sort()
    speeches = [s for s in list_split if s != '']
    text = '\n'.join(speeches)
    return text
def _return_case(n: int, tuple_list: list[tuple[int, str]]) -> list[tuple[int, str]]:
    return tuple_list if n >= len(tuple_list) else tuple_list[:n]
def _helper_last_formatting(to_be_cleaned: str) -> str:
    list_split = to_be_cleaned.split('\n')
    list_split.sort()
    speeches = [s for s in list_split if s != '']
    text = '\n'.join(speeches)
    return text