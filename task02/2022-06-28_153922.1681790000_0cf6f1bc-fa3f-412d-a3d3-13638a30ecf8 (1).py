# Dependencies
from __future__ import annotations
import re
from statistics import median

'''
In this exercise I worked with 3 concepts from own self-study that is
worth referencing. 

The first concept I researched and used (of course adapted to my own case / logic)
is the list Comprehension (https://www.w3schools.com/python/python_lists_comprehension.asp). I found 
it useful because I was stuggling to iterate over the lists while making changes to them at the same time.
I found that list comprehension in python was a way to work around this issue.

The second concept worth of referencing is the isalpha() method. I found the method under python doc. (https://docs.python.org/3/library/stdtypes.html#str.isalpha)
and realized that by using it I did not have to implement all rules of filter_tokens(...) explicitly. Specially, if I used the list comprehension technique with the
my own trick of encoding target values with "TOBEDELETED".

The third concept, is the method findall() from re package found at (https://docs.python.org/3/library/re.html#re.findall), which finds all strings matching
my searched pattern, returning a list of strings which is what the method looks for.
'''

CORPUS_FILENAME = "treaty_of_lisbon.txt"
STOPPWORDS_FILENAME = "terrier_stopwords.txt"
TARGET_WORDS = ["article", "title", "chapter", "paragraph", "subparagraph"]

def load_text(dateiname: str) -> str:
    try:
        return open(dateiname, "r").read()
    except FileNotFoundError:
        return ""


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w]+|[^\s\w]", text)

def filter_tokens(tokens: list[str]) -> list[str]:
    alphaTokens = [word if word.isalpha() else "TOBEDELETED" for word in tokens]
    lengthyTokens = [word if len(word) > 2 else "TOBEDELETED" for word in alphaTokens]
    lowerCase = [word.lower() for word in list(filter(lambda w: w.isupper() == False, lengthyTokens))]
    return [word for word in lowerCase if not word in TARGET_WORDS]

def load_stopwords(filename: str) -> list[str]:
    try:
        return open(filename, "r").read().replace("\n", " ").split()
    except FileNotFoundError:
        return []

def remove_stopwords(tokens: list[str], stopwords: list[str]) -> list[str]:
    return [word for word in tokens if not word in stopwords]

def bag_of_words(tokens: list[str]) -> dict[str, int]:
    return dict(zip(tokens, [tokens.count(word) for word in tokens]))

def most_frequent_words(word_bag: dict[str, int], n: int) -> list[str]:
    return sorted(word_bag, key = word_bag.get, reverse = True)[:n]

def longest_words(word_bag: dict[str, int], n: int) -> list[str]:
    return [word[0] for word in sorted(word_bag.items(), key = lambda f: len(f[0]), reverse = True)[:n]]

def statistics(word_bag: dict[str, int]) -> dict[str, float]:
    return {"count": 0.0} if len(word_bag) == 0 else {"count": count(word_bag), 
                                                      "average_length": averageLength(word_bag), 
                                                      "average_frequency": averageFrequency(word_bag),
                                                      "median_length": medianLength(word_bag), 
                                                      "median_frequency": medianFrequency(word_bag)}

# Helper 1: Sum over dict values
def count(word_bag: dict[str, int]) -> int:
    return sum(word_bag.values())

# Helper 2: Av. lengths of dict keys
def averageLength(word_bag: dict[str, int]) -> float:
    return sum(len(w[0]) * w[1] for w in word_bag.items()) / count(word_bag)

# Helper 3: Av. Frequency of dict keys
def averageFrequency(word_bag: dict[str, int]) -> float:
    return count(word_bag) / len(word_bag.keys())

# Helper 4: Median Length of dict keys
def medianLength(word_bag: dict[str, int]) -> float:
    return  float(median([len(word[0]) for word in sorted(word_bag.items(), key = lambda f: len(f[0]))]))

# Helper 5: Median Frequency of dict keys
def medianFrequency(word_bag: dict[str, int]) -> float:
    return  float(median([value[1] for value in sorted(word_bag.items(), key = lambda f: f[1])]))

if __name__ == "__main__":
    text = load_text(CORPUS_FILENAME)
    print(text)
    textList = load_stopwords(STOPPWORDS_FILENAME)
    print(textList)
    stopwords = load_stopwords(STOPPWORDS_FILENAME)
    test = "at the end of the first paragraph:\n\n‘on which the Member States confer competences to attain objectives they have in common.’"
    print(tokenize(test))
    tokens = [
           "The",
           "Union",
           "is",
           "founded",
           "on",
           "the",
           "values",
           "of",
           "respect",
           "for",
           "human",
           "dignity",
           ",",
           "freedom",
           ",",
           "democracy",
           ",",
           "equality",
           ",",
           "the",
           "rule",
           "of",
           "law",
           "and",
           "respect",
           "for",
           "human",
           "rights",
           ",",
           "including",
           "the",
           "rights",
           "of",
           "persons",
           "belonging",
           "to",
           "minorities",
           ".",
       ]
    print(filter_tokens(tokens))
    tokens = [
            "4",
            ".",
            "This",
            "Article",
            "shall",
            "be",
            "without",
            "prejudice",
            "to",
            "the",
            "other",
            "provisions",
            "of",
            "this",
            "Title",
            ".",
            "’",
        ]
    print(filter_tokens(tokens))
    stopwords = load_stopwords(STOPPWORDS_FILENAME)
    print(stopwords)
    tokens = [ "the", "union", "aim", "promote", "peace", "its",
    "values", "and", "the", "well", "being", "its", "peoples"]
    stopwords = ["the", "its", "and"]
    print(remove_stopwords(tokens, stopwords))
    tokens = [
        "union",
        "aim",
        "promote",
        "peace",
        "union",
        "promote",
        "war",
        "union",
    ]
    print(bag_of_words(tokens))
    dictionary = {
        "eins": 1,
        "zwei": 2,
        "drei": 3,
        "vier": 4,
        "fünf": 5,
        "sechs": 6,
        "sieben": 7,
        "acht": 8,
        "neun": 9,
        "zehn": 10,
    }
    print(most_frequent_words(dictionary, 5))
    dictionary = {
            "A": 1,
            "AB": 2,
            "ABC": 3,
            "ABCD": 4,
            "ABCDE": 5,
            "ABCDEF": 6,
            "ABCDEFG": 7,
            "ABCDEFGH": 8,
            "ABCDEFGHI": 9,
            "ABCDEFGHIJ": 10,
    }
    dictionary = {
            "A": 1,
            "AB": 1,
            "ABC": 1,
    }
    print(longest_words(dictionary, 3))
    dictionary = {
            "A": 10,
            "AB": 9,
            "ABC": 8,
            "ABCD": 7,
            "ABCDE": 6,
            "ABCDEF": 5,
            "ABCDEFG": 4,
            "ABCDEFGH": 3,
            "ABCDEFGHI": 2,
            "ABCDEFGHIJ": 1,
        }
    dictionary = { 'union': 3, 'aim': 1, 'promote': 2, 'peace': 1, 'war': 1 }
    print(statistics(dictionary))