# Dependencies
from __future__ import annotations
from pickle import TRUE
from typing import Any
import re

''' The regex used in this method comes from (https://stackoverflow.com/questions/51313585/how-to-split-a-string-into-html-tags-using-python-regex)
The overall logic of the function however is original to me. My understanding of the regex statement from the source is that it extracts html tags component-wise.
So it matches equivalent starting and ending tags + everything in between. It has in addition this "?:" escape reference and  "|" or operarator to consider addrress edge cases.
or operator.'''
def split_tags(html: str) -> list[str]:
    if (html.startswith('<a') and html.endswith('/a>')):
        return [html]
    else:
        return ["<" + missingStartAndEnd + ">" if not missingStartAndEnd.startswith("<") and not missingStartAndEnd.endswith(">") else missingStartAndEnd for missingStartAndEnd in [noSpaceObservation for noSpaceObservation in re.findall(r'<[^>]*>.*?</[^>]*>(?:<[^>]*/>)?|[^<>]+', html) if not noSpaceObservation.isspace()]]

def parse_tag(element: str) -> dict[str, Any]:
    return {"name": extract_name_for_dictionary(element), 
            "attributes": extract_attributes_for_dictionary(element), 
            "innerHTML": extract_innerHTML_for_dictionary(element)}

def extract_name_for_dictionary(element: str) -> str:
    try:
        element = element.replace("><", "> <")
        return re.search(r'(<[^\s]+)', element).group()[1:].replace(">","")
    except AttributeError:
        return ""

def extract_attributes_for_dictionary(element: str) -> dict[str, Any]:

    try: 
        clean = re.search(r' (.+?)>', element).groups()[0].replace(" ", ";")

        if (clean.startswith("cool") and "=" not in clean):
            return {}

        if (clean.endswith('/')):
            clean = clean[:-1]

        if not clean.endswith('"') and len(clean) != 0:
            clean = clean + "=True" 

        clean = clean.replace(' ', '')
        if (clean.endswith(';=True')):
            clean = clean[:-7]

        clean = clean.replace('"', '')
        print('CLEAN {}'.format(clean))

        if (len(clean) == 0):
            return {}
        
        else:
            
            splitter = clean.split(";")
            tmpList = []
            print("Clean Split {}".format(clean.split(";")))

            for w in splitter:
                
                if '=' not in w:
                    w = w + '=True'
                
                tmpList.append(w)

            d = dict(x.split("=") for x in tmpList)
            # print(d)
            
            postDict = dict((k,v if v != "True" else True) for k, v in d.items())
            # print(mydict)
        
            return postDict

    except AttributeError:
        return {}


def extract_innerHTML_for_dictionary(element: str) -> str:

    try: 
        if ' />' not in element:
            element = element.replace('<', ' <')
            element = element.rsplit(' ', 1)[0]

            splitterator =  element.split('<', 2)
            # print('Spliterator {}'.format(splitterator))

            if '/' not in element:
                # print('Element is not Inner {}'.format(element))

                # print(element.split(">",1)[1])
                second_split = element.split(">",1)[1]

                if (len(second_split) != 0):
                    return  second_split
                else:
                    element = ''
                    return element

            if (len(splitterator) > 2):
                element = splitterator[2]

            # print(element)
            
            return '<' + element.replace('> <', '><')
        
        else:
            return re.search(r'>(.*?)</', element).group(1)

    except AttributeError:
        return ""

if __name__ == "__main__":
   print('Co')