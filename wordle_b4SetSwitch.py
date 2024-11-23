# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 20:41:12 2023
"""
# @author: DrDave

import matplotlib.pyplot as plt
import nltk
import numpy as np
import re as re
import copy
import random

class TXT_COLORS(): 
    #could do: class TXT_COLORS(Enum) #with apppropriate import Enum
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    BOLD = '\033[1m'

# print(TXT_COLORS.BOLD, TXT_COLORS.green , "G", end = "")
# print(TXT_COLORS.BOLD, TXT_COLORS.red , "R")
# print(TXT_COLORS.BOLD, TXT_COLORS.cyan , "C")
# print(TXT_COLORS.BOLD, TXT_COLORS.purple , "P")
# print(TXT_COLORS.BOLD, TXT_COLORS.orange , "O")
# Best probably green, red, orange

#from colorama import Fore, Back
#print( Fore.RED + "R" + Fore.LIGHTYELLOW_EX + "Y" + Fore.GREEN + "G" ) # works, not in black Spyder colorscheme
#print( "{}R{}Y{}G".format( Fore.RED, Fore.LIGHTYELLOW_EX. Fore.GREEN) ) #Doesnt work ?!?!
#print( "{}R{}Y{}G".format( TXT_COLORS.red, TXT_COLORS.yellow. TXT_COLORS.green ) ) #Doesnt work either ?!?!

# ToDo: make these class/static variables of Guess class

NOT       = 0
SOMEWHERE = 1
HERE      = 2


LETTER_COLOR_DICT = {
    NOT       : TXT_COLORS.red    ,
    SOMEWHERE : TXT_COLORS.orange ,
    HERE      : TXT_COLORS.green
    }

def getWordsOfLength(wordList, wordLength):
    return [str.lower(w) for w in wordList if len(w) == wordLength]

class Guess():

    def __init__(self, guessText = ""):
        self.text = guessText
        self.printText        = ""
        self.letterStatus = []
        self.setText(guessText)


    def setText(self, text):
        self.text = text

    def setLetterStatus(self, letterStatusList):
        self.letterStatus = letterStatusList

    def _genPrintText(self):
    #if len(self.text) == 0:
    #    return ""

        pstr = TXT_COLORS.BOLD + ""
        for i in range(len(self.text)):
            pstr += LETTER_COLOR_DICT[ self.letterStatus[i] ] + " " + self.text[i].upper()
        return pstr

class BoardLine():

    def __init__(self, myLetters, 
                 initialWordList, 
                 answer = None):

        self.lineLength = len(initialWordList[0])
        self.available = []
        self.guessList = []

        #self.ANSWER = ""
        if answer == None:
            self.ANSWER = self._getRandomWord()

        else:
            self.ANSWER = answer

        # WHY THIS DON'T WORK: self.available = [copy.copy(myLetters)] * self.lineLength
        for _ in range(self.lineLength):
            self.available.append( copy.copy(myLetters))

        self.currentWordList = copy.copy(initialWordList)

        print("The ANSWER is {} ".format(self.ANSWER) )
    #

    def _getRandomWord(self):
        return random.choice( list(self.currentWordList))

    def removeLetterAtLocation(self, letterToRemove, position):
        if letterToRemove in self.available[position]:
            self.available[position].remove(letterToRemove)
        self._update()

    def removeLettersAtLocations(self, lettersToRemove, positions):
        if any( [type(lettersToRemove) != type([]), type(positions) != type([]) ] ):
            lettersToRemove = list( [lettersToRemove] )
            positions       = list( [positions]    ) 
        print("\t Removing Letters {} at locations {}".format(lettersToRemove, positions ))
        for pos in positions:
            for l in lettersToRemove:
                self.removeLetterAtLocation(l,pos)
    #NOTE: len(lettersToRemove) MUST EQUAL len(positions)
    #IF in the strange case want to remove the same letter at multiple 
    #   positions (or viice versa)
    #   need redundant indices or latters 
    #       ex: .removeLettersAtLocations( ['a','a','z'], [0,1,4])
    #for pos in positions:
    #    self.available[pos].remove(lettersToRemove[pos])
    #    self._update()

    def mustHaveLetter(self, mustHaveLetter):
        print("\t Requiring letter {} somewhere". format( mustHaveLetter ) )
        for w in self.currentWordList:
            if mustHaveLetter not in w:
                self.currentWordList.remove( mustHaveLetter )

    def mustHaveLettersSomewhere(self, lettersMustHave):
        for l in list(lettersMustHave):
            self.mustHaveLetter(l)

    def removeLettersEverywhere(self, lettersToRemove):
        print("\t Removing Letters Everywhere {}".format(lettersToRemove))
        #for position_ in range(len(self.available)):
            #for letterToRemove in list(lettersToRemove)[:]

        #print(" removing {} | from {} ".format([lettersToRemove]*L, [list(range(L)]) )
        #self.removeLettersAtLocations([lettersToRemove]*L,          [list(range(L))] )
        for l in lettersToRemove:
            self.removeLettersAtLocations([l]*self.lineLength, list(range(self.lineLength)) )
        self._update() 

    def setOnlyLetter(self, letterToSet, position):
        #likely lettersToSet is length 1, ie when we know a certain letter at a specific location
        print("\t Setting Letter to Only {} at locations {}".format(letterToSet, position))
        self.available[position] = list( letterToSet )
        self._update()
        #print(len(b.currentWordList))

    def setOnlyLetters(self, lettersToSet, locations):
        if any( [type(lettersToSet) != type([]), type(lettersToSet) != type([]) ] ):
            lettersToSet = list( [lettersToSet] )
            locations    = list( [locations]    ) 
        for _ in range( len(lettersToSet) ):
            self.setOnlyLetter(lettersToSet[_] , locations[_])

    def _checkFits(self, testWord):
        fits = True
        #print(testWord)
        #print(self.available)
        for position in range(self.lineLength):
            
            if testWord[position] not in self.available[position]:
                fits = False
                break
        #self._update()
        return fits

    def _update(self):

        for word in self.currentWordList[:]:
            if not self._checkFits(word):
                self.currentWordList.remove(word)
        return len(self.currentWordList)

    def printDiagnostics(self, printCurrentWordList = False):
        print( "Lenght of remaining word list: {}"
              .format (len(self.currentWordList)) )
        for _ in range(self.lineLength):
            print("Letters Available at Location {}: {}"
                  .format(_, self.available[_] ))
        if len(b.currentWordList) == 1:
            print("YOU WIN! {}".format( self.currentWordList) )

        if printCurrentWordList:
            self.printCurrentWordListFancy()
        print( " -------------------------- ")

    def printCurrentWordListFancy(self):
        if len(self.currentWordList) == 0: 
            print("NO WORDS LEFT")

        elif len(self.currentWordList) == 1:
            print("ONLY WORD LEFT: {}".format(self.currentWordList[0]) )
        else:
            print ("Remaing Words: \n\t", '%s' % ', '
                   .join(map(str, self.currentWordList)))
##############################################################################

    def setAnswer(self, answer):
        self.ANSWER = answer

    def applyGuess(self, guess = None):
        """
        # three guess cases against ANSWER:

        # Letter not anywhere
            # remove letter everywhere
            # set letter status NOT

        # Letter is here
            # set onlyLetter
            # HERE

        # Letter is somewhere
            # remove at current location
            # apply mustHaveLetter somewhere

        # update Guess remaining word list length
        # update Guess remaining words ?
        """
        if guess == None:
            guess = self._getRandomWord() # from current word list

        if len(guess) != self.lineLength:
            print( "ERROR: guess not same length as answer")

        #Check letter not anywhere:
        for l in guess:
            if l not in self.ANSWER:
                self.removeLettersEverywhere(l)

        #Check letter is here
        for i in range(self.lineLength):
            if guess[i] == self.ANSWER[i]:
                self.setOnlyLetter(guess[i], i)

        #Check letter is somewhere but not here:

        for i in range( self.lineLength ):
            pass

            if guess[i] in self.ANSWER and guess[i] not in self.available[i]:
                #means letter is in the word but not here (at location i)
                self.removeLetterAtLocation(guess[i], i)
                self.mustHaveLetter(guess[i])

#%%
# ToDo: 

#   read from github list

#   get wordlist and letters in Wordle class (currenly BoardLine() )
#       allWords = nltk.corpus.words.words()
#       words = getWordsOfLength(allWords, wordLength = 5)


#%%
#
# NOT       = 0
# SOMEWHERE = 1
# HERE      = 2


# LETTER_COLOR_DICT = {
#     NOT       : TXT_COLORS.red    ,
#     SOMEWHERE : TXT_COLORS.orange ,
#     HERE      : TXT_COLORS.green
#     }

#%%






#%%
#NYT 09/06/2024
# TEMPORARY KEY:

allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
b = BoardLine(myLetters = letters, initialWordList = words, answer='marco')
b.printDiagnostics()

#%% From NYT 09/13/24:
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
b = BoardLine(myLetters = letters, initialWordList = words, answer='marco')
b.printDiagnostics()

b.removeLettersEverywhere(['l', 'i', 'v', 'e', 'w', 'o', 'k','n', 'u', 'p'])
b.setOnlyLetters(['a', 'r', 's'], [1,2,3])
#%%
# From real guesses on 09/04/2024 NYT Wordle
# TEMPORARY KEY:
#   "X" means Letter not in Word anywhere"
#   "!" means Letter in Word at location specifically"
#   "~" means Letter is in Word but not at that location
# Example for guess "AMIGO"
# then              "!~XXX"
# means "A" is first letter; 'M' is in the word but not in the second (1 for zero-based index)
# and letters 'I' 'G' 'O' are not anywhere

# Guess #1) SLATE XXXX~
b.removeLettersEverywhere(['s', 'l','a', 't'])
b.removeLettersAtLocations('e', 4)
b.printDiagnostics()

#%%
# Guess #2 WEIRD X!X~X
b.removeLettersEverywhere(['w','i', 'd'])
b.setOnlyLetters('e', 1) 
b.printDiagnostics()
# Guess #3 PERKY X!!XX
#%%
b.removeLettersEverywhere(['p','k', 'y'])
b.setOnlyLetters(['e', 'r'], [1,2]) 
b.printDiagnostics()
b.printCurrentWordListFancy() #10 left
#%%
# Guess #4 MERCH X!!XX
b.removeLettersEverywhere(['m','c','h'])
b.printDiagnostics()
b.printCurrentWordListFancy() #10 left
#%%
# Guess RERUN !!!!! WIN
#######################################
#%%
#NYT 09/04/2024
allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
b = BoardLine(myLetters = letters, initialWordList = words)
b.printDiagnostics()
#%%
# From real guesses on 09/04/2024 NYT Wordle

# Guess #1) AMIGO XXXXX
b.removeLettersEverywhere(['a', 'm', 'i', 'g', 'o'])
b.printDiagnostics()
#%%

# Guess #2) SLEPT - !X!X~
b.removeLettersEverywhere(['l', 'p'])
b.removeLettersAtLocations(['t'], [4])

b.setOnlyLetters(['s','e'], [0,2]) 
b.printDiagnostics()
#%%

# Guess #3) STUCK - !!XXX
b.removeLettersEverywhere(['u', 'c', 'k'])
b.setOnlyLetters(['s', 't'], [0,1] )
b.printDiagnostics(printCurrentWordList=True)
#%%

# GUESS #4) STERN !!!!!
b.setOnlyLetters(['s','t', 'e', 'r', 'n'], [0,1,2,3,4])
b.printDiagnostics(printCurrentWordList=True)
# Gives "Remaining Words" as ['stern', 'stern'] - doesn't realize it won already



#%%
#NYT 09/03/2024
# TEMPORARY KEY:
#   "X" means Letter not in Word anywhere"
#   "!" means Letter in Word at location specifically"
#   "~" means Letter is in Word but not at that location
# Example for guess "AMIGO"
# then              "!~XXX"
# means "A" is first letter; 'M' is in the word but not in the second (1 for zero-based index)
# and letters 'I' 'G' 'O' are not anywhere

allWords = nltk.corpus.words.words()
words = getWordsOfLength(allWords, wordLength = 5)
letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"
b = BoardLine(myLetters = letters, initialWordList = words)
b.printDiagnostics()
#%%
# From real guesses on 09/03/2024 NYT Wordle

# Guess #1) SLATE XX~~X
b.removeLettersEverywhere(['s', 'l', 'e'])
b.removeLettersAtLocations(['a', 't'], [2,3])
b.printDiagnostics()
#%%
# Guess #2) ACTOR - ~X~XX
b.removeLettersEverywhere(['c', 'o', 'r'])
b.removeLettersAtLocations([ 'a', 't'], [0,2])
b.printDiagnostics()
#%%
# Guess #3) FAINT !!!!!
# WIN!
# redundant but anyway:
b.setOnlyLetters(['f','a','i','n','t'], [0,1,2,3,4])
b.printDiagnostics()









#%%

###############################################################################
###############################################################################

#%% NYT 3/1/24

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
#%%

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

