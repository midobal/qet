#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Miguel Domingo"
__license__ = "MIT License"
__email__ = "midobal@prhlt.upv.es"

import sys, os, subprocess

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

def phraseLevelTagGeneration(hyp, pe, phrases):
    """
    This function generates phrase-level QE tags for a given translation hypothesis.
    The function prints the tags into the standard output.
    """
    tags = ['BAD' for word in range(len(hyp.split()))]
    correct_words = commonWords(hyp, pe)

    #Store word-level tags.
    for word in correct_words:
        tags[int(word)] = 'OK'

    #Compute phrase-level.
    for phrase in phrases.split('|'):
        tag = 'OK'

        #A phrase is tagged as 'BAD' if it contains 'BAD' words.
        for word in phrase.split():
            if tags[int(word) - 1] == 'BAD':
                tag = 'BAD'

        #Assign the tag to all the words in the phrase.
        for word in phrase.split():
            tags[int(word) - 1] = tag

    print ' '.join(tags)

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

def obtainPhrases(src, hyp, mgiza):
    """
    This function segments the translation hypothesis in phrases. The function returns
    the path to a file containing the phrase segmentation.
    """
    pa = os.path.dirname(sys.argv[0]) + '/phrase_alignments.sh'
    subprocess.call(pa + ' ' + src + ' ' +  hyp + ' ' +  mgiza, shell=True)
    
    return '/tmp/qet/phrases'

def usage():
    """                                                                                                                                                                                                           
    This function shows the usage message.                                                                                                                                                                        
    """
    sys.stderr.write('Usage: ' + sys.argv[0] + ' -t translation_file -pe post-edited_file [options]\n\n')
    sys.stderr.write('Options: \n')
    sys.stderr.write('  -h                         show this message.\n')
    sys.stderr.write('  -p source_file mgiza_path  generate phrase-level QE tags (default: word-level).\n')
    sys.exit(-1)

def getArguments():
    """                                                                                                                                                                                                           
    This function checks the arguments and returns their value.                                                                                                                                                   
    """
    hyp = None
    pe = None
    phrase_level = False
    src = None
    mgiza = None
    
    #Loop through the arguments.
    n = 1
    while n < len(sys.argv):

        if sys.argv[n] == '-t':
            try:
                hyp = sys.argv[n + 1]
            except:
                usage()
            n += 2

        elif sys.argv[n] == '-pe':
            try:
                pe = sys.argv[n + 1]
            except:
                usage()
            n += 2
            
        elif sys.argv[n] == '-p':
            phrase_level = True
            try:
                src = sys.argv[n + 1]
                mgiza = sys.argv[n + 2]
            except:
                usage()
            n += 3
            
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

    if phrase_level and not os.path.isfile(src):
        sys.stderr.write('Error opening file ' + src + '.\n')
        sys.exit(-1)

    if phrase_level and not os.path.isdir(mgiza):
        sys.stderr.write('Path ' + mgiza + ' does not exist.\n')
        sys.exit(-1)

    #Return arguments.
    return hyp, pe, phrase_level, src, mgiza

if __name__ == "__main__":

    #Check arguments.
    hyp, pe, phrase_level, src, mgiza = getArguments()

    #Check file lengths.
    hyp_sentences = sum(1 for line in open(hyp))
    pe_sentences = sum(1 for line in open(pe))
    if hyp_sentences != pe_sentences:
        sys.stderr.write('Files differ in number of sentences!\n')
        sys.exit(-1)

    #Obtain phrases.
    if phrase_level:
        phrases = obtainPhrases(src, hyp, mgiza)

    #Loop the text sentence by sentence.
    pe_file = open(pe, 'r')
    if phrase_level:
        phrases_file = open(phrases, 'r')
    for hyp_sentence in open(hyp):
        pe_sentence = pe_file.readline()
        if phrase_level:
            phrase_sentence = phrases_file.readline()

        #Generate word-level tags.
        if not phrase_level:
            wordLevelTagGeneration(hyp_sentence, pe_sentence)

        #Generate phrase-level tags.
        else:
            phraseLevelTagGeneration(hyp_sentence, pe_sentence, phrase_sentence)

    #Remove phrases' temporal files
    if phrase_level:
        subprocess.call('rm -r /tmp/qet', shell=True)
