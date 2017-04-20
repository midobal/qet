#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Miguel Domingo"
__license__ = "MIT License"
__email__ = "midobal@prhlt.upv.es"

import sys, os

def commonWords(hyp, pe):
    """
    This function computes the longest common subsequence between a translation hypothesis and
    its post-edited version. The function returns a list with the positions of the common words.
    """
    x_list = hyp.split()
    y_list = pe.split()
    m = len(x_list)
    n = len(y_list)
    x_path = [str(tr) for tr in range(m)]

    LCS = [['' for i in range(n + 1)] for j in range(m + 1)]
    LCS_xpath = [['' for i in range(n + 1)] for j in range(m + 1)]
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            LCS[i][j] = LCS[i + 1][j + 1]
            LCS_xpath[i][j] = LCS_xpath[i + 1][j + 1]

            if x_list[i] == y_list[j]:
                LCS[i][j] += ' ' + x_list[i]
                LCS_xpath[i][j] += ' ' + x_path[i]

            if len(LCS[i][j + 1]) > len(LCS[i][j]):
                LCS[i][j] = LCS[i][j + 1]
                LCS_xpath[i][j] = LCS_xpath[i][j + 1]
                
            if len(LCS[i + 1][j]) > len(LCS[i][j]):
                LCS[i][j] = LCS[i + 1][j]
                LCS_xpath[i][j] = LCS_xpath[i + 1][j]
                
    return [int(index) for index in list(reversed(LCS_xpath[0][0].split()))]

def wordLevelTagGeneration(hyp, pe):
    """
    This function generates word-level QE tags for a given translation hypothesis.
    The function prints the tags into the standard output.
    """
    correct_words = commonWords(hyp, pe)

    #Case in which all words are wrong.
    if correct_words == []:
        print ' '.join(['BAD' for word in hyp.split()])

    #General case.
    else:
        tags = ''
        
        #Words prior to the first correct word.
        for word in range(int(correct_words[0])):
            tags += 'BAD '
        tags += 'OK '

        #Words up to the last correct word.
        for n in range(1, len(correct_words)):
            for word in range(int(correct_words[n - 1]) + 1, int(correct_words[n])):
                tags += 'BAD '
            tags += 'OK '

        #Words from the last correct word to the end of the sentence.
        for word in range(int(correct_words[-1]) + 1, len(hyp.split())):
            tags += 'BAD '

        print tags.strip()

def usage():
    """                                                                                                                                                                                                           
    This function shows the usage message.                                                                                                                                                                        
    """
    sys.stderr.write('Usage: ' + sys.argv[0] + ' -t translation_file -pe post-edited_file [options]\n\n')
    sys.stderr.write('Options: \n')
    sys.stderr.write('  -h     show this message.\n')
    sys.stderr.write('  -p     generate phrase-level QE tags (default: word-level).\n')
    sys.exit(-1)

def getArguments():
    """                                                                                                                                                                                                           
    This function checks the arguments and returns their value.                                                                                                                                                   
    """
    hyp = None
    pe = None
    phrase_level = False
    
    #Loop through the arguments.
    n = 1
    while n < len(sys.argv):

        if sys.argv[n] == '-t':
            hyp = sys.argv[n + 1]
            n += 2

        elif sys.argv[n] == '-pe':
            pe = sys.argv[n + 1]
            n += 2
            
        elif sys.argv[n] == '-p':
            phrase_level = True
            n += 1
            
        else:
            usage()
            
    #Check that mandatory arguments are present.
    if hyp == None or pe == None:
        usage()
                
    #Check all paths.
    if not os.path.isfile(hyp):
        sys.stderr.write('Error opening file ' + hyp + '.\n')
        sys.exit(-1)
                    
    if not os.path.isfile(pe):
        sys.stderr.write('Error opening file ' + pe + '.\n')
        sys.exit(-1)

    #Return arguments.
    return hyp, pe, phrase_level

if __name__ == "__main__":

    #Check arguments.
    hyp, pe, phrase_level = getArguments()

    #Check file lengths.
    hyp_sentences = sum(1 for line in open(hyp))
    pe_sentences = sum(1 for line in open(pe))
    if hyp_sentences != pe_sentences:
        sys.stderr.write('Files differ in number of sentences!\n')
        sys.exit(-1)

    #Loop the text sentence by sentence.
    pe_file = open(pe, 'r')
    for hyp_sentence in open(hyp):
        pe_sentence = pe_file.readline()

        #Generate word-level tags.
        if not phrase_level:
            wordLevelTagGeneration(hyp_sentence, pe_sentence)

        #Generate phrase-level tags.
        else:
            sys.stderr.write('Phrase-level tagger is under development.\n')
            sys.exit(-1)
