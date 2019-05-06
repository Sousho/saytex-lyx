import logging
import requests
import urllib
import re
import config

from saytex import Saytex

# used in all APIs
special_vocabulary = [
        ('open', '('),
        ('close', ')')
]

# used in all APIs
math_symbols = [
        ('plus', '+'),
        ('minus', '-'),
        ('factorial', '!'),
        ('divided by', '/'),
        ('to the power of', '^'),
        ('times', '*'),
        ('equals','='),
        ('squared','^2'),
        ('cubed','^3'),
        ('greater than','>'),
        ('less than','<'),
        ('< or equal to','<='),
        ('> or equal to','>='),
]

# used in all APIs
common_mischaracterizations = [
        ('see','c'),
        ('some','sum'), # dubious
        ('end','n'),
        ('hey','a'),
        ('day','a'),
        ('be','b'),
        ('overbyte','over b'),
        ('richer','greater'),
        ("I'm",'n'),
        ('clothes','close'),
        ('whole','close'),
        ('closed','close'),
        ('cosign','cosine'),
        ('quotes','close'),
        ('oakland','open'),
        ('eggs','x'),
        ('clubs','close'),
        ('eclipse','a plus'),
        ('aid','a'),
        ('beat','b'),
        ('nfinity','infinity'),
        ('sign','sine'),
        ('menace','minus'),
        ('age','h'),
]

# not used for wolfram alpha, but used for fast API
math_symbols_aggressive = [
        ('by', '*'),
        ('over', '/'),
]

# not used for wolfram alpha, but used for fast API
common_mischaracterizations_aggressive = [
        ('is',' '),
        ('the',' '),
        ('of',' '),
        ('such that','then'),
        ('we get','then'),
        ('dan','then'),
        ('done','then'),
        ('there exists','exists'),
        ('there exist','exists'),
        ('equivalent to','equiv'),
        ('equal to','equals'),
        ('for all','forall'),
        ('frale','forall'),
        ('integrate','integral'),
]


import json

class WolframError(Exception):
    pass

def wolframlatex(text):
    """
    convert text to latex using wolfram API.
    utilizes caching so as to minimize API usage.

    parameters:
        text: unprocessed spoken string

    returns:
        latex string
    """

    logging.info("start wolframlatex")


    if config.WOLFRAM_CACHING:
        with open('wolframcache.txt','r') as wolframcache:
            cache = json.load(wolframcache)
            if text in cache:
                logging.info("found string in cache; using that")
                return cache[text]

    preprocessed = preprocess(text)

    logging.debug(preprocessed)

    r = requests.get('https://www.wolframcloud.com/objects/arvid/latexdictation/stringtolatex?x=' + urllib.parse.quote_plus(preprocessed))
    latex = r.text

    logging.debug(latex)

    # clean up the result
    latex = latex.strip('"')

    # replace escaped backslashes with real ones
    latex = latex.replace('\\\\', '\\')

    # remove starting and ending brackets
    #latex = latex.lstrip('\\[').rstrip('\\]')
    if latex.startswith('\\['):
        latex = latex[2:]
    if latex.endswith('\\]'):
        latex = latex[:-2]
    latex = latex.lstrip('[').rstrip(']')
    
    if '$Failed' in latex:
        raise WolframError

    if config.WOLFRAM_CACHING:
        with open('wolframcache.txt','w') as wolframcache:
            cache[text] = latex
            json.dump(cache, wolframcache)


    return latex



def simplelatex(text):
    """
    convert text to latex using the saytex package

    parameters:
        text: unprocessed spoken string

    returns:
        latex string
    """
    saytex_compiler = Saytex()

    return saytex_compiler.to_latex(text)


# helper methods
def makeword(s):
    return ' ' + s + ' '
def replacelist(s, l):
    for replacetuple in l:
        nreptup = (makeword(replacetuple[0]), makeword(replacetuple[1]))
        if replacetuple[0][0] == ' ':
            # if replace begins with space, then we also want to replace the space
            nreptup = (nreptup[0][1:], nreptup[1][1:])
        s = s.replace(nreptup[0], nreptup[1])
    return s

def transformcapitals(text):
    # for every string capital letter, replace with Letter
    # include greek letters!
    return re.sub(r'capital (\D)', lambda x : x.group(1).upper(), text)



def preprocess(text):
    """
    replaces common mischaracterized words (eggs -> x)
    replaces simple math words (over -> divided by)

    parameters:
        text: unprocessed string of spoken math

    returns:
        string
    """
    # replace symbols!
    # order: mischaracterizations, uppercase to lowercase, vocabulary, math symbols

    # convert from lowercase to uppercase
    processedtext = text.lower()

    # make word, to add padding and make edge cases into non-edge cases
    processedtext = makeword(processedtext)

    # turn capital [letter] into [Letter]
    processedtext = transformcapitals(processedtext)

    # replace various things
    processedtext = replacelist(processedtext, common_mischaracterizations)
    processedtext = replacelist(processedtext, special_vocabulary)
    processedtext = replacelist(processedtext, math_symbols)
    
    return processedtext.strip()

def aggressive_preprocess(text):
    """
    used together with preprocess
    used for the simplelatex conversion
    produces a string that is NOT tailored to latex

    parameters:
        text: preprocessed string of spoken math

    returns:
        string
    """
    # replace symbols!
    # order: mischaracterizations, math symbols
    processedtext = makeword(text)
    processedtext = replacelist(processedtext, common_mischaracterizations_aggressive)
    processedtext = replacelist(processedtext, math_symbols_aggressive)
    
    return processedtext.strip()
