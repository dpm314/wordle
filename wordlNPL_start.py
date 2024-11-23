# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 20:41:12 2023

@author: DrDave
"""
import re as re
import matplotlib.pyplot as plt
import nltk
#%%
#if re.search('[a-z]','abc123'):
#    print('yes')
#else:
#    print('no')
#%%
words = nltk.corpus.words
wordList = words.words()

#%%
# fiveLetterWords = []
# for word in wordList:
#     if(len(word) == 5):
#         fiveLetterWords.append(word)
# #%%
# #
# twentyFiveLetterWords = []
# for word in wordList:
#     if(len(word) <= 25):
#         twentyFiveLetterWords.append(word)
#%%

#if re.search('[a-z]','314156'):
##    print('yes')
#else:
#    print('no')

#%%
# def getWordsOfLength(wordList, targetLength):
#     return [w for w in wordList if len(w) == targetLength]
# #usage example
# targetLength = 5# can be anything
# myWords = getWordsOfLength(wordList, targetLength)

# #%%
# lowercaseLetters = list(map(chr, range(97,123)))
# hist = dict(zip(lowercaseLetters, [0]*26))
# #print(hist)

# for l in lowercaseLetters:
#     for word in fiveLetterWords:
#         if re.search(l, word):
#             hist[l] += 1
#     print("measuring letter: {}, got {}".format(l, hist[l]))
# #%%
# plt.close('all')
# #normalization = max(num for num in hist.values())
# for i,l in enumerate(lowercaseLetters):
#     #plt.plot(i, hist[l] / normalization, 'o', markerSize = 25)
#     plt.plot(i, hist[l], '.', markerSize = 20)
#     plt.ylabel("Instances", fontsize = 16)
# plt.xticks(range(26), lowercaseLetters, fontsize = 18)
# plt.yticks(fontsize = 18)
# plt.title("Instances of each letter \n in 25-letter or shorter English Words")
# plt.grid()
# plt.tight_layout()

#%%

##########################################################################%%

# class TXT_COLORS():
#     black = '\033[30m'
#     red = '\033[31m'
#     green = '\033[32m'
#     orange = '\033[33m'
#     blue = '\033[34m'
#     purple = '\033[35m'
#     cyan = '\033[36m'
#     lightgrey = '\033[37m'
#     darkgrey = '\033[90m'
#     lightred = '\033[91m'
#     lightgreen = '\033[92m'
#     yellow = '\033[93m'
#     lightblue = '\033[94m'
#     pink = '\033[95m'
#     lightcyan = '\033[96m'
# #%%
# print(TXT_COLORS.green , "Green!")
# print(TXT_COLORS.lightgrey , "gray!")
#%%
############################################################################
import numpy as np
import re as re
import matplotlib.pyplot as plt
import copy
import nltk
#%%
def getWordsOfLength(wordList, targetLength):
    return [str.lower(w) for w in wordList if len(w) == targetLength]

class singleHistogram():
    def __init__(self, wordList, letters, toPrint = False, toNormalize = True):

        self.words = wordList
        self.letters = letters

        self.hist = dict( zip(self.letters, [0]*len(self.letters)) )
        
        self.maxValue = 0.0

        self.calcHistogram(toPrint, toNormalize = toNormalize)
        if toPrint:
            self._print()

    def calcHistogram(self, toPrint = True, toNormalize = True):

        for l in self.letters:

            self.hist[l] = sum( [l in w for w in self.words])
            #for word in self.words:
            #    if re.search(l, word):
            #        self.hist[l] += 1


        self.maxValue = max( self.hist.values() )
        if toNormalize:

            for k in self.hist.keys():
                self.hist[k] = self.hist[k]/self.maxValue
            self.maxValue = 1.0

    def _print(self):
        for l in self.letters:
            print("letter: {}, frequency {}".format(l, self.hist[l]))

    def plotMe(self, clearAll = True):
        if clearAll: 
            plt.close('all')

        for i,l in enumerate(self.letters):
            
            plt.plot(i, self.hist[l], '.', markerSize = 20)
            plt.ylabel("Relative Frequency", fontsize = 16)
        plt.xticks(range(len(self.letters)), self.letters, fontsize = 18)

        plt.yticks(np.arange(0,self.maxValue + self.maxValue/ 4.0, self.maxValue/ 4.0  ), fontsize = 18)
        plt.ylim([0, self.maxValue])
        plt.title("Instances of each letter \n in {} letter English words".format(len(self.words[0])) )
        plt.grid()
        plt.tight_layout()

# #%%
# def getPossibleWords(allWords, possibleLetters):
#     "returns list of the words in allWords which have possible letters"

#     possibleWords = []
#     for word in allWords:
#         for l in possibleLetters:
#             if l in word:
#                 possibleWords.append(word)
#     return possibleWords


# #%%
# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, targetLength = 5)
# letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
h = singleHistogram(words, letters, toPrint = True, toNormalize=False)

#%%

# def getPossibleWords(allWords, possibleLetters):
#     "returns list of the words in allWords which have possible letters"

#     possibleWords = []
#     for word in allWords:
#         for l in possibleLetters:
#             if l in word:
#                 possibleWords.append(word)
#     return possibleWords

def getPossibleWordsFromRequiredLetters(allWords, requiredLetters, toPrint = False):
    "returns list of the words in allWords which *have all* of the required letters"
    possibleWords = []
    for word in allWords:
        iampossible = True
        #print("checking word {}".format(word))
        for l in requiredLetters:
            #print("    checking {}".format(l) )
            if l not in word:
                #print("        {} is not in {}".format(l, word) )
                iampossible = False
                break
        if iampossible: 
            possibleWords.append(word)
    if toPrint:
        print(possibleWords)
    return possibleWords

#todo: need a get possible words for a list of words at known locations or not allowed locations or unknown locations
#%%
# first start at wordGuess

# class TXT_COLORS():
#     black = '\033[30m'
#     red = '\033[31m'
#     green = '\033[32m'
#     orange = '\033[33m'
#     blue = '\033[34m'
#     purple = '\033[35m'
#     cyan = '\033[36m'
#     lightgrey = '\033[37m'
#     darkgrey = '\033[90m'
#     lightred = '\033[91m'
#     lightgreen = '\033[92m'
#     yellow = '\033[93m'
#     lightblue = '\033[94m'
#     pink = '\033[95m'
#     lightcyan = '\033[96m'
# #%%
# print(TXT_COLORS.green , "Green!")
# print(TXT_COLORS.lightgrey , "gray!")


class BoardLine():

    def __init__(self, myLetters = list(map(chr, range(97,123))),
                 lineLength = 5):
        self.available = [copy.copy(myLetters)] * lineLength

    def removeLetterAtLocation(self, letterToRemove, position):
        if letterToRemove in self.available[position]:
            self.available[position].remove(letterToRemove)

    def removeLettersEverywhere(self, lettersToRemove):
        for position_ in range(len(self.available)):
            for letterToRemove in list(lettersToRemove):
                self.removeLetterAtLocation(letterToRemove, position_)

    def setOnlyLetters(self, lettersToSet,   position):
        self.available[position] = list( lettersToSet )


def checkFits(word, aBoardLine):
    # Note len(word) and len(aBoardLine.available) must be same!
    fits = True
    for position in range(len(word)):
        if word[position] not in aBoardLine.available[position]:
            fits = False
    return fits

#%%
# Example checkFits:
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, targetLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"

b = BoardLine(lineLength = 5)
b.removeLettersEverywhere(letters[10:]) # cut all letters past 'j' out of all possibilities

b.setOnlyLetters(['a', 'b', 'c'], position = 0) # require first letter to be 'a-c'
b.setOnlyLetters('e', position = 4) # require last letter to be 'e'

#print all words which necessarily start with 'a' and end in 'e' and otherwise only have "a-j" in them
for w in words:
    if checkFits(w, b):
        print(w)

def printCheckFits(wordList, myBoardLine):
    possible = []
    for w in words:
        if checkFits(w, b):
            print(w)
            possible.append(w)
    return possible
#%%
"""
12/20/23 NTTimes
Have so far guesses 'SLATE' where S = loc 0, A = loc 2; T E out; L in but not loc 1
                    'SHAWL' where S = loc 0, A = loc 2, L = loc 5; H W out. 
"""
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, targetLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"

b = BoardLine(lineLength = 5)

b.removeLettersEverywhere(['t', 'e', 'h', 'w'])
b.setOnlyLetters('s', position = 0)
b.setOnlyLetters('a', position = 2)
b.setOnlyLetters('l', position = 0)































