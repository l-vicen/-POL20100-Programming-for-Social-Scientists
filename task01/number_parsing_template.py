""" Dependencies from within the
python library.
"""
import re

OPERATION_SYSTEM_DICT = {
    'plus': '+',
    'minus': '-',
    'multiplied': '*',
    'divided': '/',
    'by': 'by',
    '(': '(',
    ')': ')',
    'times': '*',
    'divided by': '/'
}

NUMBER_SYSTEM_DICT = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
}

TYPE_ONE = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}

TYPE_TWO = {
    'hundred': 100
}

TYPE_THREE = {
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
}

def tokenize(sentence):

    sentence = sentence.lower()

    sentence = re.sub(r'\(','( ', sentence)
    sentence = re.sub(r'\)',' )', sentence)

    sentence = sentence.replace('-', ' ')

    tmpTokenList = sentence.split()

    numericalValues = list(NUMBER_SYSTEM_DICT.keys())
    opsValues = list(OPERATION_SYSTEM_DICT.keys())

    tokenList = []
    for i in range(len(tmpTokenList)):
        if tmpTokenList[i] in opsValues:
            tokenList.append(tmpTokenList[i])
        
        if tmpTokenList[i] in numericalValues:
            number = tmpTokenList[i]
            count = i + 1
            while (count < len(tmpTokenList)):
                
                if tmpTokenList[count] in numericalValues:
                    number += ' ' + tmpTokenList[count]
                    count += 1
                
                else:
                    break
            
            tokenList.append(number)
            # print('Number is {}'.format(number))

    cleaner = []
    for k in tokenList:
        cleaner.append(len(k.split()))
    # print('Lengths: {}'.format(cleaner))

    cleanedTokenList = []

    control = 0
    while control < len(cleaner):
        if (cleaner[control] > 1):
            cleanedTokenList.append(tokenList[control])
            control += cleaner[control]
        else:
            cleanedTokenList.append(tokenList[control])
            control += 1

    if ('divided' in cleanedTokenList):
        cleanedTokenList = [w.replace('divided', 'divided by') for w in cleanedTokenList]
        cleanedTokenList.remove('by')

    if ('multiplied' in cleanedTokenList):
        cleanedTokenList = [w.replace('multiplied', 'multiplied by') for w in cleanedTokenList]
        cleanedTokenList.remove('by')

    cleanedTokenList = [re.sub('y ', 'y-', token) for token in cleanedTokenList]

    # print('------------------------------')
    # print('TMP Token List: {}'.format(tmpTokenList))
    # print('Token List: {}'.format(tokenList))
    # print('Cleaned Token List: {}'.format(cleanedTokenList))
    # print('------------------------------')

    return cleanedTokenList

def normalize_number(number_word):

    if (number_word.startswith('hundred')):
        number_word = re.sub('hundred', 'one hundred', number_word)
    elif (number_word.startswith('thousand')):
        number_word = re.sub('thousand', 'one thousand', number_word)
    elif (number_word.startswith('million')):
        number_word = re.sub('million', 'one million', number_word)
    elif(number_word.startswith('billion')):
        number_word = re.sub('billion', 'one billion', number_word)

    number_word = number_word.replace('-', ' ')
    number_word_array = number_word.split()

    tmpNumber = 0
    number = 0
    for w in number_word_array:

        for keyOne, valueOne in TYPE_ONE.items():
            if (w == keyOne):
                tmpNumber += valueOne
        
        for keyTwo, valueTwo in TYPE_TWO.items():
            if (w == keyTwo):
                tmpNumber *= valueTwo

        for keyThree, valueThree in TYPE_THREE.items():
            if (w == keyThree):
                tmpNumber *= valueThree
                number += tmpNumber
                tmpNumber = 0
        
    number += tmpNumber
    tmpNumber = 0

    # print('Tmp Number: {}'.format(tmpNumber))
    # print('----')
    # print('OUTPUT {}'.format(number))
    # print('----')

    return number


def normalize(tokens):

    # print('INPUTS: {}'.format(tokens))

    normalizedList = []
    for i in range(len(tokens)):

        match = False
        for key, value in OPERATION_SYSTEM_DICT.items():
            if (tokens[i] == key):
                normalizedList.append(value)
                match = True
                # print('Found operation {} and match is {}'.format(value, match))

        if (match == False):
            # print('Appending number {} and match is {}'.format(tokens[i], match))
            normalizedList.append(normalize_number(tokens[i]))

    # print('NORMALIZED LIST ORIGINAL {}'.format(normalizedList))

    # normalizedList = [x for x in normalizedList if x != 0]
    normalizedList = list(map(str, normalizedList))

    # print('NORMALIZED LIST FINAL: {}'.format(normalizedList))
    # print('----')

    return normalizedList

def evaluate(expression):

    print('INPUTS: {}'.format(expression))

    # Tokenizing expression
    listTokens = tokenize(expression)
    print('OUTPUT Tokenized String: {}'.format(listTokens))

    # Storage list
    parsedList = normalize(listTokens)
    print('OUTPUT Parsed String: {}'.format(parsedList))

    for value in parsedList:
        if (re.search('[a-zA-Z]', value)):
            parsedList.remove(value)

    print('OUTPUT Parsed String: {}'.format(parsedList))

    # print('OUTPUT: {}'.format(eval(''.join(parsedList))))
    # Concatenating list of parsed strings into single string which is evaluated using eval()
    return eval(''.join(parsedList))

if __name__ == "__main__":
    print('TASK 1: Tokenize')
    tokenize("one plus two")
    tokenize("minus (forty-five minus five) divided by five")
    tokenize("six hundred forty-five minus nine hundred")
    print('==============================================')
    print('TASK 2: Normalize Number')
    normalize_number("seven")
    normalize_number("six hundred forty-five")
    normalize_number("one hundred eleven thousand one hundred eleven")
    normalize_number("one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine")
    print('==============================================')
    print('TASK 3: Normalize')
    normalize(["seven"])
    normalize(["six", "minus", "(", "three", "plus", "five", ")", "times", "two"])
    normalize(["eleven", "times", "four"])
    normalize(["ninety-nine", "divided by", "nine"])
    normalize(['one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine', 'plus', 'one'])
    normalize(['zero', 'minus', 'zero'])
    print('==============================================')
    print('TASK 4: Evaluate')
    evaluate("seven")
    evaluate("six minus (three plus five) times two")
    evaluate("five divided by two")
    evaluate("hundred thousand times (one divided by hundred thousand)")