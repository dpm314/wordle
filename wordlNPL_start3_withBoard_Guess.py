# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 20:41:12 2023

@author: DrDave
"""
#%%
#Utility Functions (to be moved into Classes later)
def getWordsOfLength(wordList, wordLength):
    return [str.lower(w) for w in wordList if len(w) == wordLength]

class singleLetterHistogram():
    def __init__(self, wordList, letters, toPrint = False, toNormalize = True):

        self.words = copy.copy(wordList)
        self.letters = letters

        self.hist = dict( zip(self.letters, [0]*len(self.letters)) )
        
        self.maxValue = 0.0

        self.calcHistogram(toPrint, toNormalize = toNormalize)
        if toPrint:
            self._print()

    def calcHistogram(self, toPrint = True, toNormalize = True):

        for l in self.letters:

            self.hist[l] = sum( [l in w for w in self.words])
            #^ equivalent to:
            #for word in self.words:
            #    if re.search(l, word):
            #        self.hist[l] += 1

        if toNormalize:

            for k in self.hist.keys():
                self.hist[k] = self.hist[k]/self.maxValue
            self.maxValue = 1.0
        else: 
            self.maxValue = max( self.hist.values() )


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

#%%
#allWords = nltk.corpus.words.words()
#words = getWordsOfLength(allWords, targetLength = 5)
#letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"

#%%
import matplotlib.pyplot as plt
import random
import nltk
import numpy as np
import re as re
import copy
#%%
class Board():

    def __init__(self, myLetters,
                 initialWordList,
                 theWord = None):

        self.lineLength = len(initialWordList[0])
        self.available = [copy.copy(myLetters)] * self.lineLength
        self.currentWordList = copy.copy(initialWordList)
        
        if theWord == None:
            index = random.randint(0, len(self.currentWordList))
            self.theWord = self.currentWordList[index]
        else:
            self.theWord = theWord

    def removeLetterAtLocation(self, letterToRemove, position):
        if letterToRemove in self.available[position]:
            self.available[position].remove(letterToRemove)
        self._update()
        #a debug: 
        print(len(b.currentWordList))

    def removeLettersEverywhere(self, lettersToRemove):
        for position_ in range(len(self.available)):
            for letterToRemove in list(lettersToRemove)[:]:
                self.removeLetterAtLocation(letterToRemove, position_)
        self._update()

    def setOnlyLetter(self, letterToSet, position):
        #likely lettersToSet is length 1, ie when we know a certain letter at a specific location
        self.available[position] = list( letterToSet )
        self._update()
        #a debug: 
        print(len(b.currentWordList))


    #This doesn't work either needs repeated calls!
    def mustHaveLetters(self, mustHaveLetters):
        mustHaveLetters = list(mustHaveLetters)
        for word in self.currentWordList[:]:
            print(" word: {}".format(word))
            for l in mustHaveLetters:
                print("    word:{} in mustHave: {}".format(word, l))
                if l not in word:
                    print("        letter {} NOT in {}, removing".format(l, word))
                    self.currentWordList.remove(word)
                    break
        self._update() # not sure this is needed
        #a debug: 
        print(len(b.currentWordList))

    def _checkFits(self, testWord):
        fits = True
        #print(testWord)
        #print(self.available)
        for position in range(self.lineLength):
            
            if testWord[position] not in self.available[position]:
                fits = False
                break
            #a debug:
        #self._update()
        return fits

    def _update(self):

        for word in self.currentWordList[:]:
            if not self._checkFits(word):
                self.currentWordList.remove(word)
        return len(self.currentWordList)

    def takeGuess(self, guessWord):
        pass
        """three steps: 
        1) loop on all pos's see if a winner then set only letter to that per pos
        2) % if letter doen't fit anywhere then make unavailble everywhere

        3) % if letter doesn't fit here but does somewhere make must have and can't have here
        
        """




#en(self
#    def orderCurrentByMostProbable(s
#    #todo combine with douplet probabelf, singleLetterHistogram, doubletLetterHistogram):
#        passility 
#    #todo sort by histogram probabilit word P(A|B) = P(B) * P(B|A) / P(A)
#    #  where A is a tuple of letters, any might only need to do tuplet not single
#    # use Bayesian prior on location ind B is the location in the word
#    # NOTE: will need to re-calculate and nordList
#    #todo -> sort/filter self.currentWordList irmalize after each self._update()
#    #   distributions based on self.currentWon order by highest probability
#    #todo add Histograms singlet and/or duplet to this class


#%%
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"

b = Board(myLetters = letters, initialWordList = words)
print( len(b.currentWordList) )# now words left 10422

#%%
















































































#%%
# Example checkFits: 
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"

b = Board(myLetters = letters, initialWordList = words)
print( len(b.currentWordList) )# now words left 10422
#%%
###############################################################################
###############################################################################

# NYT 1/28
# First Guess "slate"
b.removeLettersEverywhere(['s','l','a','t']) # now 2025 words left
print( len(b.currentWordList) )# 10422
#%%
b.mustHaveLetters('e')
print( len(b.currentWordList) )# now 1478 words left
#%% ###########################################################################
# Second Guess "coped"
b.removeLettersEverywhere(['c', 'o','p', 'd'])

print( len(b.currentWordList) )# now 425 words left
#%%
b.setOnlyLetter('e', position = 3)
print( len(b.currentWordList) )# now 249 words left
#%%

###### Jump ahead, last guess: 
b.removeLettersEverywhere(['s','l','a','t','c','o','p','d','i','k','w','f','u','n','y'])
print( len(b.currentWordList)) # 31 words remaining. 
# know that its ??BER
#%%
b.setOnlyLetter('b', 2)
print( len(b.currentWordList)) # 16 words remaining. 
b._update()
print( len(b.currentWordList)) # 8 words remaining. 
b._update()
print( len(b.currentWordList)) # 4 words remaining. 
b._update()
print( len(b.currentWordList)) # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
#%%
b.setOnlyLetter('e', 3)
print( len(b.currentWordList)) # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
#%%
b.setOnlyLetter('r', 4)
print( len(b.currentWordList)) # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
print( b.currentWordList )
#%%
# NYT 2/29
###############3 Turn #1 Guess "SLATE"
b.setOnlyLetter('a',2)
#%%
b.setOnlyLetter('e',4)
#%%
b.removeLettersEverywhere(['s', 'l', 't'])
#%%############## Turn 2 Guess "RIDGE"
b.setOnlyLetter('g', 3)
#%%
b.mustHaveLetters('i')
#%%
b.removeLettersEverywhere(['i', 'm', 'a', 'g', ' '])
#%%
################ AFTER update to fix behavior removing elements from list being iterated on simultaneously ...
# NYT 3/1/24
#########################################################################
import matplotlib.pyplot as plt
import nltk
import numpy as np
import re as re
import copy
#%%%
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
b = BoardLine(myLetters = letters, initialWordList = words)
print( len(b.currentWordList) )# now words left 10422
#%%Guess "SLATE"
# got expelled S L A T^1 E
b.removeLettersEverywhere(['s', 'l', 't', 'e'])
print('Remaining possible words {}'.format(b.currentWordList) )
print('    len: ' + str((len(b.currentWordList) ) ) )
#%% Guess "ORDER"b.cur
b.mustHaveLetters(['n','a', 'r']) #145
#%%
b.removeLettersEverywhere(['i', 'h', 'e', 'o'])
#%%########################################################################################################
Guess = "GRAIN"
b.removeLettersEverywhere(['g'])
b.setOnlyLetter('r', position=1)
b.setOnlyLetter('n', position =4)
# Need a "cant be here" indication too
#guess URBAN -> won

#%% NYT 3/3
b.removeLettersEverywhere(['l'])
#%%
b.setOnlyLetter('s',0)
b.setOnlyLetter('a',2)
b.setOnlyLetter('t',3)
b.setOnlyLetter('e',4)
#%%
b.removeLettersEverywhere('k')
#%%
#guess "state" -> won

#%% NYT 3/15/2024
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
b = BoardLine(myLetters = letters, initialWordList = words)
print( len(b.currentWordList) )# now words left 10422
#%%
#Guess SLATE
b.removeLettersEverywhere(['s', 'l', 'a'])
#%%
b.mustHaveLetters(['t', 'e'])
#%%
#Guess TREAT
b.setOnlyLetter('r', 1)
b.setOnlyLetter('t', 4) ## only 44 words remaining
#Guess ERUPT -> won
