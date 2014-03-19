# Small NLP tools used in the main program of recipe transformation

import re

def to_singular(word):
#- convert the word to its singular form
#- only checks ending 's' and 'es'
#- may change MANY non-plural words, but it is OK as long as
#  all words are changed in the same way
#- more like cutting the singular and plural forms into the
#  same reduced form
#- e.g. 'classes' --> 'cla'
#       'class'   --> 'cla'
    try:
        while word[-1]=='s':
        # has to be a loop so that singular and plural forms
        # of the same word can end up the same
            if word[-2]=='e':
                word = word[:-2] # cut 'es'
            else:
                word = word[:-1] # cut 's'
    except:
        # in case word becomes too short to access index -2 or -1
        pass
    return word
#


def split(line):
#- split phrase into a list of words
    return re.findall(r"[\w\d]+", line)
#


def uni_rep(ingred_name):
#- generate a unique name id for an input phrase in order
#  to reduce multiple representation in natural language
#- done through 1) clean plural forms
#               2) reorder
#- note that this id will be less readible, but it is only
#  used as a unique identifier
    words = split(ingred_name)           # separate words
    for i in range(len(words)):
        words[i] = to_singular(words[i]) # singular form
    words.sort()                         # to make uniform ordering
                                         # of the same set of words
    return ' '.join(words)
#
