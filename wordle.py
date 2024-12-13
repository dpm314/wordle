# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 20:41:12 2023
"""
# @author: DrDave

import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

import nltk
import copy
import random
import time


class TXT_COLORS:
    # could do: class TXT_COLORS(Enum) #with apppropriate import Enum
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    orange = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    lightgrey = "\033[37m"
    darkgrey = "\033[90m"
    lightred = "\033[91m"
    lightgreen = "\033[92m"
    yellow = "\033[93m"
    lightblue = "\033[94m"
    pink = "\033[95m"
    lightcyan = "\033[96m"
    BOLD = "\033[1m"
    DEFAULT = "\033[0m"


# print(TXT_COLORS.BOLD, TXT_COLORS.green , "G", end = "")
# print(TXT_COLORS.BOLD, TXT_COLORS.red , "R")
# print(TXT_COLORS.BOLD, TXT_COLORS.cyan , "C")
# print(TXT_COLORS.BOLD, TXT_COLORS.purple , "P")
# print(TXT_COLORS.BOLD, TXT_COLORS.orange , "O")
# Best probably green, red, orange

# from colorama import Fore, Back
# print( Fore.RED + "R" + Fore.LIGHTYELLOW_EX + "Y" + Fore.GREEN + "G" ) # works, not in black Spyder colorscheme
# print( "{}R{}Y{}G".format( Fore.RED, Fore.LIGHTYELLOW_EX. Fore.GREEN) ) #Doesnt work ?!?!
# print( "{}R{}Y{}G".format( TXT_COLORS.red, TXT_COLORS.yellow. TXT_COLORS.green ) ) #Doesnt work either ?!?!

# ToDo: make these class/static variables of Guess class
_NOT = 0
_SOMEWHERE = 1
_HERE = 2
_WON = 2


LETTER_COLOR_DICT = {
    _NOT: TXT_COLORS.red + TXT_COLORS.BOLD,
    _SOMEWHERE: TXT_COLORS.orange + TXT_COLORS.BOLD,
    _HERE: TXT_COLORS.green + TXT_COLORS.BOLD,
}


def readWordleWordSet(fileName="wordleWordList.txt"):
    #print("Reading words from {}".format(fileName))
    with open(fileName) as f:
        lines = f.read().splitlines()
        lines = set(lines)
        return lines


def getWordsOfLength(wordList, wordLength):
    return [str.lower(w) for w in wordList if len(w) == wordLength]

def newStandardBoard(printNothing=False, printTheDiagnostics=False, answer=None, maxIterations = 6):

    # words = readWordleWordSet()
    # letters =  list(map(chr, range(97,123))) #26 lower-case ASCII "a-z"

    board = WordleBoard(
        printNothing=printNothing,
        printTheDiagnostics=printTheDiagnostics,
        answer=answer,
        maxIterations=maxIterations
    )
    return board

class Guess:
    def __init__(self, guessText=""):
        self.text = guessText
        self.printText        = ""
        self.letterStatus = [""]*len(self.text)
        self.printText = ""
        self.letterStatus = []
        self.setText(guessText)

    def setText(self, text):
        self.text = text

    def setLetterStatus(self, letterStatusList):
        self.letterStatus = letterStatusList

    def _genPrintText(self):
        # if len(self.text) == 0:
        #    return ""

        pstr = TXT_COLORS.BOLD + ""
        for i in range(len(self.text)):

            # ERROR HERE
            # ERROR HERE
            # ERROR HERE
            pstr += LETTER_COLOR_DICT[ self.letterStatus[i] ] + " "
            + self.text[i].upper()

            pstr += LETTER_COLOR_DICT[self.letterStatus[i]] + " "
            + self.text[i].upper()
        return pstr


class WordleBoard:

    # _words = readWordleWordSet()
    # _letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"

    def __init__(
        self, lineLength=5,
        answer=None, 
        printNothing=False,
        printTheDiagnostics=False,
        maxIterations = 6
    ):

        # Used to be class level variables, getting screwed up with multiprocessing ? 
        self._words = readWordleWordSet()
        self._letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"

        self.maxIterations = maxIterations

        self.printNothing = printNothing
        self.printTheDiagnostics = printTheDiagnostics
        self.lineLength = lineLength
        self.available = []
        self.guessList = []
        self.boardIterations = 0
        self.WON = False

        self.currentWordList = copy.copy(self._words)

        if answer == None:
            self.ANSWER = self._getRandomWord()
        else:
            self.ANSWER = answer.lower()
        # WHY THIS DON'T WORK???:
        #    self.available = [copy.copy(myLetters)] * self.lineLength
        for _ in range(self.lineLength):
            self.available.append(copy.copy(self._letters))
        # if not self.printNothing:
        #     print("The ANSWER is: \t {} ".format(self.ANSWER))

    def _getRandomWord(self):
        return random.choice(list(self.currentWordList))

    def removeLetterAtLocation(self, letterToRemove, position):
        if letterToRemove in self.available[position]:
            #self.available[position].remove(letterToRemove)
            self.available[position] = [l.replace(letterToRemove, '-') 
                                        for l in self.available[position] ]
        self._update()

    def removeLettersAtLocations(self, lettersToRemove, positions):
        if any([type(lettersToRemove) != type([]), type(positions) != type([])]):
            lettersToRemove = list([lettersToRemove])
            positions = list([positions])
        if not self.printNothing:
            print(
                "\t\t Removing Letters {} at locations {}".format(
                    lettersToRemove, positions
                )
            )
        for pos in positions:
            for l in lettersToRemove:
                self.removeLetterAtLocation(l, pos)

    def mustHaveLetter(self, mustHaveLetter):
        # print("\t Requiring letter {} somewhere". format( mustHaveLetter ) )
        toRemove = set()
        for w in self.currentWordList:
            if mustHaveLetter not in w:
                # self.currentWordList.remove( mustHaveLetter )
                toRemove.add(w)
        self.currentWordList = self.currentWordList - toRemove

    def mustHaveLettersSomewhere(self, lettersMustHave):
        for l in list(lettersMustHave):
            self.mustHaveLetter(l)

    def removeLettersEverywhere(self, lettersToRemove):
        if not self.printNothing:
            print("\t Removing Letters Everywhere {}".format(lettersToRemove))

        for l in lettersToRemove:
            self.removeLettersAtLocations(
                [l] * self.lineLength, list(range(self.lineLength))
            )
        self._update()

    def setOnlyLetter(self, letterToSet, position):
        # likely lettersToSet is length 1, ie when we know a certain letter at a specific location
        if not self.printNothing:
            print(
                "\t Setting Letter to Only {} at locations {}".format(
                    letterToSet, position
                )
            )
        self.available[position] = ['-' if l !=  letterToSet else l for l in self.available[position] ]
        self._update()
        # print(len(b.currentWordList))

    def setOnlyLetters(self, lettersToSet, locations):
        if any([type(lettersToSet) != type([]), type(lettersToSet) != type([])]):
            lettersToSet = list([lettersToSet])
            locations = list([locations])
        for _ in range(len(lettersToSet)):
            self.setOnlyLetter(lettersToSet[_], locations[_])

    def _checkFits(self, testWord):
        fits = True
        # print(testWord)
        # print(self.available)
        for position in range(self.lineLength):

            if testWord[position] not in self.available[position]:
                fits = False
                break
        # self._update()
        return fits

    def _update(self):

        toRemoveSet = set()
        for word in self.currentWordList:
            if not self._checkFits(word):
                toRemoveSet.add(word)
        self.currentWordList = self.currentWordList - toRemoveSet
        # if len(self.currentWordList) == 1:
        #    self.WON == True
        return len(self.currentWordList)

    def printDiagnostics(self, printCurrentWordList=True):
        if not self.printNothing:
            print("Number of Iterations on Board {}".format(self.boardIterations))
            print("Lenght of remaining word list: {}".format(len(self.currentWordList)))
        for _ in range(self.lineLength):
            if not self.printNothing:
                print(
                    "Available at Location {}:\t".format(_) + "".join(self.available[_])
                )
        if printCurrentWordList:
            self.printCurrentWordListFancy()
            if not self.printNothing:
                print(" -------------------------- ")

    def printCurrentWordListFancy(self):
        if not self.printNothing:
            if len(self.currentWordList) == 1:
                print("ONLY WORD LEFT: {}".format(self.currentWordList))
                self.WON == True  # Don't thing needed, but not hurting anything
            else:
                 print("Remaing Words: \n\t")
                 for w in self.currentWordList:
                     print(w, end = " ")

    def setAnswer(self, answer):
        self.ANSWER = answer

    def applyGuess(self, guessWord=None):
        """
        # THREE guess CASES against self.ANSWER:

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
        # update Guess.setLetterStatus() per:
            _NOT       = 0
            _SOMEWHERE = 1
            _HERE      = 2
        """

        if guessWord == None:
            guessWord = self._getRandomWord()  # from current word list
        guessWord = guessWord.lower()  # incase user enters with any capital letters

        if not self.printNothing:
            print("*Applying guess word: \t {}".format(guessWord))
        # Check letter not anywhere:
        for l in guessWord:
            if l not in self.ANSWER:
                self.removeLettersEverywhere(l)
        # Check letter is here
        for i in range(self.lineLength):
            if guessWord[i] == self.ANSWER[i]:
                self.setOnlyLetter(guessWord[i], i)
        # Check letter is somewhere but not here:
        for i in range(self.lineLength):
            if guessWord[i] in self.ANSWER:
                if guessWord[i] is not self.ANSWER[i]:
                    # guessWord letter is in the word but not here (at location i)
                    self.removeLetterAtLocation(guessWord[i], i)
                    self.mustHaveLetter(guessWord[i])
        # Store for future diagnostics etc:

        self.boardIterations += 1
        self.guessList.append(Guess(guessWord))

        self._checkWon()

        if self.printTheDiagnostics:
            self.printDiagnostics()

        if self.WON == True:
            self._printYouWon()

    def _checkWon(self):

        self.WON = False  # Probably unnecessary but for clarity
        if len(self.currentWordList) == 1:
            if next(iter(self.currentWordList)) == self.ANSWER:
                self.WON = True

    def _printYouWon(self):
        if self.printNothing == False:
            print(
                TXT_COLORS.BOLD
                + "\n YOU WIN!: {} \n".format(next(iter(self.currentWordList)).upper())
            )

    def playAutoGen(self, maxIterations=6):
        iterCount = 0
        while (self.WON == False) and (self.boardIterations < maxIterations):
            iterCount += 1
            if not self.printNothing:
                print("\n Iteration {}/{}".format(iterCount, maxIterations))
            self.applyGuess()

##########
### TODO: make letters and words (
###       from reading file or nlp etc)
###       either globals or class variables ?
###       -> YES Want class variables, they are
###       not recomputed/loaded each instance
##########
# #
# #
# # FOR TESTING ONLY (?)
# #
# #
# # ACTUALLY can only use .available here not .ANSWER ?
# def __tryAllWords(self):
#     #returns heap queue with key as the word and value as length of remaingin wordlist if we chose the key word
#     #https://www.google.com/search?q=python+create+priority+queue+fromo+keys+in+dictionary+pythony+%3F&oq=python+create+priority+queue+fromo+keys+in+dictionary+pythony+%3F&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTE3OTIzajBqN6gCCLACAQ&client=ubuntu-chr&sourceid=chrome&ie=UTF-8

#     #for now just return a dictionary
#     tryAllDict = {}

#################################
#%%
# def targetFunc(x):
#     return x+1

# import multiprocessing
# pool = multiprocessing.Pool(processes = 4)
# #pool.map(targetFunc, listOfThingsToProcess)
# results = pool.map(targetFunc, [1,2,3,4,5,6,7,8])
# # also look at pool.imap()  !!!!!!!!!!!!!!!!!!!!!!!!
# # and imap_unordered()
# print(results)
#%%



#%%
b = newStandardBoard(printTheDiagnostics = True, answer = 'slate')
b.playAutoGen(maxIterations=3)

#%%
a = newStandardBoard(printNothing=False, 
                     printTheDiagnostics=True,
                     answer="slate")
a.applyGuess()
a.applyGuess()

# Ideas: makye make a fake .applyGuess() which
#   tries applying a guess to a copy.copy list of
#   .currentWordList and a.available then
#   counts len(.currentWordList) for each and
#   returns the guess which shortens .currentWordList
#   the most ?

# maybe work by histograms per letter in .available ? That's closer
#%%

def chomper(boardSlice):
    #[b.playAutoGen() for b in boardSlice]
    for b in boardSlice:
        b.playAutoGen(maxIterations=maxIterations)
    return boardSlice

itersReq = []
maxIterations = 6
numGames = 256
numPools = 8
numBoardsPerPool = int( numGames / numPools )

pool = mp.Pool()

allBoards = [ newStandardBoard(printNothing=True,
                    printTheDiagnostics=True,
                    maxIterations = maxIterations,
                    answer= None)
                    for _ in range(0,numGames) ]
allBoards = [ allBoards[i:(i+numBoardsPerPool)] for i in range(0,numGames,numBoardsPerPool) ]

startTime = time.time()

allBoards = pool.map(chomper, allBoards)

numWins  = sum( list( sum( [ allBoards[si][i].WON for i in range(0,len(allBoards[si] )) ]) for si in range(len(allBoards))  ))
fracWins = float(numWins) / float(numGames)

for i in range(0,len(allBoards)):
    print('Thread {}: ---'.format(i))
    for j in range(len( allBoards[i]) ):
        print( "{} \t {} \t {} \t WIN: {}".format(allBoards[i][j].ANSWER, len(allBoards[i][j].guessList), len(allBoards[i][j].currentWordList), allBoards[i][j].WON) )

print("Total Time: {}\tPer Iteration\t{}".format( (time.time() - startTime), (time.time() - startTime) / float(numGames)) )
print(" Win {}/{} \t {} %".format(numWins,numGames, fracWins) )

#%%
startTime = time.time()


itersReq = []
maxIterations = 6
numGames = 64

for i in range(numGames):
    print("Game #{} / {}".format(i, numGames))
    b = newStandardBoard(
                  answer = None,
                  printTheDiagnostics=True,
                  printNothing = True)
    b.playAutoGen()
    itersReq.append( b.boardIterations )


print("Total Time: {}\tPer Iteration{}".format( (time.time() - startTime), (time.time() - startTime) / float(numGames)) )
print(" Win {}/{} \t {}\%".format(numWins,numGames), fracWins)
#%%
iterHist = np.histogram( itersReq, bins = [0,1,2,3,4,5,6,7], density = True ) #density normalizes correctly if each histogram bin same width
print(iterHist)

plt.figure()
plt.plot( range(0, len(iterHist[0]) ) , iterHist[0] , marker = 'o', markersize = 30)
plt.plot( range(0, len(iterHist[0]) ) , iterHist[0] , linewidth = 10)
plt.xlabel("Number of Iterations", fontsize = 26)
plt.xticks(range(0, numGames), fontsize = 26)
plt.ylabel("Normalized Frequency to Win", fontsize = 26)
plt.xticks(fontsize = 26)
plt.yticks(fontsize = 26)
plt.plot([maxIterations, maxIterations], [0,1 ], 'r')
plt.grid()
plt.tight_layout()

#%%










#%%
# =============================================================================


# ###############################################################################
# ###############################################################################

# #%% NYT 3/1/24

# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words)
# print(len(b.currentWordList))  # now words left 10422
# #%%Guess "SLATE"
# # got expelled S L A T^1 E
# b.removeLettersEverywhere(["s", "l", "t", "e"])
# print("Remaining possible words {}".format(b.currentWordList))
# print("    len: " + str((len(b.currentWordList))))
# #%% Guess "ORDER"b.cur
# b.mustHaveLetters(["n", "a", "r"])  # 145
# #%%
# b.removeLettersEverywhere(["i", "h", "e", "o"])
# #%%########################################################################################################
# Guess = "GRAIN"
# b.removeLettersEverywhere(["g"])
# b.setOnlyLetter("r", position=1)
# b.setOnlyLetter("n", position=4)
# # Need a "cant be here" indication too
# # guess URBAN -> won

# #%% NYT 3/3
# b.removeLettersEverywhere(["l"])
# #%%
# b.setOnlyLetter("s", 0)
# b.setOnlyLetter("a", 2)
# b.setOnlyLetter("t", 3)
# b.setOnlyLetter("e", 4)
# #%%
# b.removeLettersEverywhere("k")
# #%%
# # guess "state" -> won

# #%% NYT 3/15/2024
# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words)
# print(len(b.currentWordList))  # now words left 10422
# #%%
# # Guess SLATE
# b.removeLettersEverywhere(["s", "l", "a"])
# #%%
# b.mustHaveLetters(["t", "e"])
# #%%
# # Guess TREAT
# b.setOnlyLetter("r", 1)
# b.setOnlyLetter("t", 4)  ## only 44 words remaining
# # Guess ERUPT -> won
# #%%

# # NYT 1/28
# # First Guess "slate"
# b.removeLettersEverywhere(["s", "l", "a", "t"])  # now 2025 words left
# print(len(b.currentWordList))  # 10422
# #%%
# b.mustHaveLetters("e")
# print(len(b.currentWordList))  # now 1478 words left
# #%% ###########################################################################
# # Second Guess "coped"
# b.removeLettersEverywhere(["c", "o", "p", "d"])

# print(len(b.currentWordList))  # now 425 words left
# #%%
# b.setOnlyLetter("e", position=3)
# print(len(b.currentWordList))  # now 249 words left
# #%%

# ###### Jump ahead, last guess:
# b.removeLettersEverywhere(
#     ["s", "l", "a", "t", "c", "o", "p", "d", "i", "k", "w", "f", "u", "n", "y"]
# )
# print(len(b.currentWordList))  # 31 words remaining.
# # know that its ??BER
# #%%
# b.setOnlyLetter("b", 2)
# print(len(b.currentWordList))  # 16 words remaining.
# b._update()
# print(len(b.currentWordList))  # 8 words remaining.
# b._update()
# print(len(b.currentWordList))  # 4 words remaining.
# b._update()
# print(
#     len(b.currentWordList)
# )  # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
# #%%
# b.setOnlyLetter("e", 3)
# print(
#     len(b.currentWordList)
# )  # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
# #%%
# b.setOnlyLetter("r", 4)
# print(
#     len(b.currentWordList)
# )  # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
# print(b.currentWordList)
# #%%
# # NYT 2/29
# ###############3 Turn #1 Guess "SLATE"
# b.setOnlyLetter("a", 2)
# #%%
# b.setOnlyLetter("e", 4)
# #%%
# b.removeLettersEverywhere(["s", "l", "t"])
# #%%############## Turn 2 Guess "RIDGE"
# b.setOnlyLetter("g", 3)
# #%%
# b.mustHaveLetters("i")
# #%%
# b.removeLettersEverywhere(["i", "m", "a", "g", " "])
# #%%
# ################ AFTER update to fix behavior removing elements from list being iterated on simultaneously ...
# # NYT 3/1/24
# #########################################################################
# # -*- coding: utf-8 -*-
# """
# Created on Fri Dec 15 20:41:12 2023
# """
# # @author: DrDave

# import matplotlib.pyplot as plt
# import numpy as np

# # import re as re

# import nltk
# import copy
# import random
# import time


# class TXT_COLORS:
#     # could do: class TXT_COLORS(Enum) #with apppropriate import Enum
#     black = "\033[30m"
#     red = "\033[31m"
#     green = "\033[32m"
#     orange = "\033[33m"
#     blue = "\033[34m"
#     purple = "\033[35m"
#     cyan = "\033[36m"
#     lightgrey = "\033[37m"
#     darkgrey = "\033[90m"
#     lightred = "\033[91m"
#     lightgreen = "\033[92m"
#     yellow = "\033[93m"
#     lightblue = "\033[94m"
#     pink = "\033[95m"
#     lightcyan = "\033[96m"
#     BOLD = "\033[1m"
#     DEFAULT = "\033[0m"


# # print(TXT_COLORS.BOLD, TXT_COLORS.green , "G", end = "")
# # print(TXT_COLORS.BOLD, TXT_COLORS.red , "R")
# # print(TXT_COLORS.BOLD, TXT_COLORS.cyan , "C")
# # print(TXT_COLORS.BOLD, TXT_COLORS.purple , "P")
# # print(TXT_COLORS.BOLD, TXT_COLORS.orange , "O")
# # Best probably green, red, orange

# # from colorama import Fore, Back
# # print( Fore.RED + "R" + Fore.LIGHTYELLOW_EX + "Y" + Fore.GREEN + "G" ) # works, not in black Spyder colorscheme
# # print( "{}R{}Y{}G".format( Fore.RED, Fore.LIGHTYELLOW_EX. Fore.GREEN) ) #Doesnt work ?!?!
# # print( "{}R{}Y{}G".format( TXT_COLORS.red, TXT_COLORS.yellow. TXT_COLORS.green ) ) #Doesnt work either ?!?!

# # ToDo: make these class/static variables of Guess class
# _NOT = 0
# _SOMEWHERE = 1
# _HERE = 2
# _WON = 2


# LETTER_COLOR_DICT = {
#     _NOT: TXT_COLORS.red + TXT_COLORS.BOLD,
#     _SOMEWHERE: TXT_COLORS.orange + TXT_COLORS.BOLD,
#     _HERE: TXT_COLORS.green + TXT_COLORS.BOLD,
# }

# def readWordleWordSet(fileName="wordleWordList.txt"):
#     print("Reading words from {}".format(fileName))
#     with open(fileName) as f:
#         lines = f.read().splitlines()
#         lines = set(lines)
#         return lines


# def getWordsOfLength(wordList, wordLength):
#     return [str.lower(w) for w in wordList if len(w) == wordLength]

# def newStandardBoard(printNothing=False, 
#                      printTheDiagnostics=False, 
#                      answer=None):

#     board = WordleBoard(
#         printNothing=printNothing,
#         printTheDiagnostics=printTheDiagnostics,
#         answer=answer,
#     )
#     return board


# class Guess:
#     def __init__(self, guessText=""):
#         self.text = guessText
#         self.printText = ""
#         self.letterStatus = []
#         self.setText(guessText)

#     def setText(self, text):
#         self.text = text

#     def setLetterStatus(self, letterStatusList):
#         self.letterStatus = letterStatusList

#     def _genPrintText(self):
#         # if len(self.text) == 0:
#         #    return ""

#         pstr = TXT_COLORS.BOLD + ""
#         for i in range(len(self.text)):
#             pstr += LETTER_COLOR_DICT[self.letterStatus[i]] + " "
#             +self.text[i].upper()
#         return pstr


# class WordleBoard:

#     _words = readWordleWordSet()
#     _letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"

#     def __init__(
#         self, lineLength=5, answer=None, printNothing=False, printTheDiagnostics=False
#     ):

#         self.printNothing = printNothing
#         self.printTheDiagnostics = printTheDiagnostics
#         self.lineLength = lineLength
#         self.available = []
#         self.guessList = []
#         self.boardIterations = 0
#         self.WON = False

#         self.currentWordList = copy.copy(self._words)

#         if answer == None:
#             self.ANSWER = self._getRandomWord()
#         else:
#             self.ANSWER = answer.lower()
#         # WHY THIS DON'T WORK???:
#         #    self.available = [copy.copy(myLetters)] * self.lineLength
#         for _ in range(self.lineLength):
#             self.available.append(copy.copy(self._letters))
#         if not self.printNothing:
#             print("The ANSWER is: \t {} ".format(self.ANSWER))

#     #

#     def _getRandomWord(self):
#         return random.choice(list(self.currentWordList))

#     def removeLetterAtLocation(self, letterToRemove, position):
#         if letterToRemove in self.available[position]:
#             #self.available[position].remove(letterToRemove)
#             self.available[position] = [l.replace(letterToRemove, '-')
#                                         for l in self.available[position]]
#         self._update()

#     def removeLettersAtLocations(self, lettersToRemove, positions):
#         if any([type(lettersToRemove) != type([]), type(positions) != type([])]):
#             lettersToRemove = list([lettersToRemove])
#             positions = list([positions])
#         if not self.printNothing:
#             print(
#                 "\t\t Removing Letters {} at locations {}".format(
#                     lettersToRemove, positions
#                 )
#             )
#         for pos in positions:
#             for l in lettersToRemove:
#                 self.removeLetterAtLocation(l, pos)

#     # NOTE: len(lettersToRemove) MUST EQUAL len(positions)
#     # IF in the strange case want to remove the same letter at multiple
#     #   positions (or viice versa)
#     #   need redundant indices or latters
#     #       ex: .removeLettersAtLocations( ['a','a','z'], [0,1,4])
#     # for pos in positions:
#     #    self.available[pos].remove(lettersToRemove[pos])
#     #    self._update()

#     def mustHaveLetter(self, mustHaveLetter):
#         # print("\t Requiring letter {} somewhere". format( mustHaveLetter ) )
#         toRemove = set()
#         for w in self.currentWordList:
#             if mustHaveLetter not in w:
#                 # self.currentWordList.remove( mustHaveLetter )
#                 toRemove.add(w)
#         self.currentWordList = self.currentWordList - toRemove

#     def mustHaveLettersSomewhere(self, lettersMustHave):
#         for l in list(lettersMustHave):
#             self.mustHaveLetter(l)

#     def removeLettersEverywhere(self, lettersToRemove):
#         if not self.printNothing:
#             print("\t Removing Letters Everywhere {}".format(lettersToRemove))
#         # for position_ in range(len(self.available)):
#         # for letterToRemove in list(lettersToRemove)[:]

#         # print(" removing {} | from {} ".format([lettersToRemove]*L, [list(range(L)]) )
#         # self.removeLettersAtLocations([lettersToRemove]*L,          [list(range(L))] )
#         for l in lettersToRemove:
#             self.removeLettersAtLocations(
#                 [l] * self.lineLength,
#                 list(range(self.lineLength))
#             )
#         self._update()

#     def setOnlyLetter(self, letterToSet, position):
#         # likely lettersToSet is length 1, ie when we know a certain letter at a specific location
#         if not self.printNothing:
#             print(
#                 "\t Setting Letter to Only {} at locations {}".format(
#                     letterToSet, position
#                 )
#             )
#         self.available[position] = list(letterToSet)
#         self._update()
#         # print(len(b.currentWordList))

#     def setOnlyLetters(self, lettersToSet, locations):
#         if any([type(lettersToSet) != type([]), type(lettersToSet) != type([])]):
#             lettersToSet = list([lettersToSet])
#             locations = list([locations])
#         for _ in range(len(lettersToSet)):
#             self.setOnlyLetter(lettersToSet[_], locations[_])

#     def _checkFits(self, testWord):
#         fits = True
#         # print(testWord)
#         # print(self.available)
#         for position in range(self.lineLength):

#             if testWord[position] not in self.available[position]:
#                 fits = False
#                 break
#         # self._update()
#         return fits

#     def _update(self):

#         toRemoveSet = set()
#         for word in self.currentWordList:
#             if not self._checkFits(word):
#                 toRemoveSet.add(word)
#         self.currentWordList = self.currentWordList - toRemoveSet
#         # if len(self.currentWordList) == 1:
#         #    self.WON == True
#         return len(self.currentWordList)

#     def printDiagnostics(self, printCurrentWordList=False):
#         if not self.printNothing:
#             print("Number of Iterations on Board {}".format(self.boardIterations))
#             print("Lenght of remaining word list: {}".format(len(self.currentWordList)))
#         for _ in range(self.lineLength):
#             if not self.printNothing:
#                 print(
#                     "Available at {}: {}".format(_, self.available[_])
#                 )
#         if printCurrentWordList:
#             self.printCurrentWordListFancy()
#             if not self.printNothing:
#                 print(" -------------------------- ")

#     def printCurrentWordListFancy(self):
#         if not self.printNothing:
#             if len(self.currentWordList) == 1:
#                 print("ONLY WORD LEFT: {}".format(self.currentWordList))
#                 self.WON == True  # Don't thing needed, but not hurting anything
#             else:
#                 print(
#                     "Remaing Words: \n\t",
#                     "%s" % ", ".join(map(str, self.currentWordList)),
#                 )

#     def setAnswer(self, answer):
#         self.ANSWER = answer

#     def applyGuess(self, guessWord=None):()
#         """
#         # THREE guess CASES against self.ANSWER:

#         # Letter not anywhere
#             # remove letter everywhere
#             # set letter status NOT

#         # Letter is here
#             # set onlyLetter
#             # HERE

#         # Letter is somewhere
#             # remove at current location
#             # apply mustHaveLetter somewhere

#         # update Guess remaining word list length
#         # update Guess remaining words ?
#         # update Guess.setLetterStatus() per:
#             _NOT       = 0
#             _SOMEWHERE = 1
#             _HERE      = 2
#         """

#         if guessWord == None:
#             guessWord = self._getRandomWord()  # from current word list
#         guessWord = guessWord.lower()  # incase user enters with any capital letters

#         # =============================================================================
#         # TODO move to get word function in a interactive play implementation;
#         #      not needed for auto guessing
#         # =============================================
#         #         if len(guessWord) != self.lineLength:
#         #             if not self.printNothing:
#         #                 print( "ERROR: guess not same length as answer")
#         #             return
#         # =============================================================================

#         if not self.printNothing:
#             print("\n --------------")
#             print("*Applying guess word: \t {}".format(guessWord))
#             print(" --------------\n")
#         # Check letter not anywhere:
#         for l in guessWord:
#             if l not in self.ANSWER:
#                 self.removeLettersEverywhere(l)
#         # Check letter is here
#         for i in range(self.lineLength):
#             if guessWord[i] == self.ANSWER[i]:
#                 self.setOnlyLetter(guessWord[i], i)
#         # Check letter is somewhere but not here:
#         for i in range(self.lineLength):
#             if guessWord[i] in self.ANSWER:
#                 if guessWord[i] is not self.ANSWER[i]:
#                     # print("i = ", i, ' if guessWord[i] in self.ANSWER and guessWord[i] is not self.ANSWER[i]')
#                     # guessWord letter is in the word but not here (at location i)
#                     self.removeLetterAtLocation(guessWord[i], i)
#                     self.mustHaveLetter(guessWord[i])
#         # Store for future diagnostics etc:

#         self.boardIterations += 1
#         self.guessList.append(Guess(guessWord))


#         if self.printTheDiagnostics:
#             self.printDiagnostics(printCurrentWordList=True)
#         self._checkWon()

#         if self.WON == True:
#             self._printYouWon()

#     def _checkWon(self):

#         if len(self.currentWordList) == 1:
#             self.WON = True
#         else:
#             self.WON = False  # Probably unnecessary but for clarity

#     def _printYouWon(self):
#         if self.printNothing == False:
#             print(
#                 TXT_COLORS.BOLD
#                 + "\n YOU WIN!: {} \n".format(next(iter(self.currentWordList)).upper())
#             )

#     def playAutoGen(self, maxIterations=6):
#         iterCount = 0
#         while (self.WON == False) and (iterCount < maxIterations):
#             iterCount += 1
#             if not self.printNothing:
#                 print("\n Iteration {}/{}".format(iterCount, maxIterations))
#             self.applyGuess()

# ##########
# ### TODO: make letters and words (
# ###       from reading file or nlp etc)
# ###       either globals or class variables ?
# ###       -> YES Want class variables, they are
# ###       not recomputed/loaded each instance
# ##########
# # #
# # #
# # # FOR TESTING ONLY (?)
# # #
# # #
# # # ACTUALLY can only use .available here not .ANSWER ?
# # def __tryAllWords(self):
# #     #returns heap queue with key as the word and value as length of remaingin wordlist if we chose the key word
# #     #https://www.google.com/search?q=python+create+priority+queue+fromo+keys+in+dictionary+pythony+%3F&oq=python+create+priority+queue+fromo+keys+in+dictionary+pythony+%3F&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTE3OTIzajBqN6gCCLACAQ&client=ubuntu-chr&sourceid=chrome&ie=UTF-8

# #     #for now just return a dictionary
# #     tryAllDict = {}


# #%%
# a = newStandardBoard(printNothing=False, 
#                      printTheDiagnostics=True, 
#                      answer="slate")
# a.printDiagnostics()  # len currentWordList 12947

# a.applyGuess()
# a.printDiagnostics()  # len currentWordList 99
# a.applyGuess()
# a.printDiagnostics()  # len currentWordList 99
# a.applyGuess()
# a.printDiagnostics()  # len currentWordList 99

# print(a.currentWordList)
# # Ideas: makye make a fake .applyGuess() which
# #   tries applying a guess to a copy.copy list of
# #   .currentWordList and a.available then
# #   counts len(.currentWordList) for each and
# #   returns the guess which shortens .currentWordList
# #   the most ? NOPE that will always work on the first try



# # testAnswer = "plage"
# # w = copy.copy(a.currentWordList)
# # while w:
# #     trialWord = w.pop()
# #     print(trialWord)
# #%%
# b = newStandardBoard(printTheDiagnostics = 1)
# #%%
# b.playAutoGen(maxIterations=6)
# #%%
# # Guess: AMIGO
# b.removeLetterAtLocation("a", 0)
# b.printDiagnostics()
# #%%
# # guess SLATE
# b.removeLettersAtLocations(["l", "a"], [1, 2])
# b.printDiagnostics()

# #%%
# # NYT 11/4/2024
# words = readWordleWordSet()
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = WordleBoard(myLetters=letters, words=words, answer="Vinyl")
# b.printDiagnostics()
# #%% Apply NYT guess )In real time)move
# # Guess: SLATE: X~XXX
# b.removeLettersEverywhere(["s", "a", "t", "e"])
# b.removeLetterAtLocation("l", 1)
# #%% Guess: GROIL: XXX~!
# b.removeLettersEverywhere(["d", "r", "o"])
# b.removeLetterAtLocation("i", 3)
# b.setOnlyLetter("l", 4)
# #%% Guess: CHILL XX~X!
# b.removeLettersEverywhere(["c", "h"])
# b.removeLetterAtLocation("i", 2)
# # Guess VINYL: win!
# b.applyGuess(guessWord="vinyl")


# #%%
# words = readWordleWordSet()
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = WordleBoard(myLetters=letters, words=words, answer="rerun")
# b.printDiagnostics()

# #%%
# b.playAutoGen(maxIterations=6)
# #%%

# #%%
# startTime = time.time()

# itersReq = boards = []
# maxIterations = 6
# numGames = 256
# for i in range(numGames):

#     b = WordleBoard(
#         answer=None,  # Choose randome guess word if None
#         printTheDiagnostics=False,
#         printNothing=True,
#     )

#     b.playAutoGen(maxIterations=maxIterations)
#     boards.append(b)

#     if b.WON:
#         print(LETTER_COLOR_DICT[2] + "{}\t".format(b.ANSWER.upper()), end="")
#     else:
#         print(LETTER_COLOR_DICT[0] + "{}\t".format(b.ANSWER.upper()), end="")
# endTime = time.time()
# print("\n" + TXT_COLORS.DEFAULT)

# gamesWon = sum([1 for b in boards if b.WON])

# print(
#     "\nWon: {}/{} {:.2f}% \t Elapsed Sec {:.3f} \t Effective Sec Per Iteration: {:.3f}".format(
#         gamesWon,
#         numGames,
#         100.0 * float(gamesWon) / float(numGames),
#         endTime - startTime,
#         float(endTime - startTime) / float(numGames),
#     )
# )

# print("Using random guess word. single threaded")
# #%%
# # =============================================================================
# # iterHist = np.histogram( itersReq, range(1, maxIterations+1), density = True) #density normalizes correctly if each histogram bin same width
# # print(iterHist)
# #
# # plt.plot( iterHist[1][:-1], iterHist[0],marker = 'x', markersize = 20)
# # plt.xlabel("Number of Iterations", fontsize = 20)
# # plt.ylabel("Normalized Frequency to Win", fontsize = 20)
# #
# # TOdo: make lists of the histograms (maybe put in a class ?)
# # Label with answer or "Random" if b.randomAnswer == True"

# # =============================================================================


# #%%
# # for removal of a string from a set of strings, need ie b.currentWordList - set(['slate'])


# #%%
# # NYT 09/06/2024
# # TEMPORARY KEY:

# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words, answer="marco")
# b.printDiagnostics()

# #%% From NYT 09/13/24:
# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words, answer="marco")
# b.printDiagnostics()

# b.removeLettersEverywhere(["l", "i", "v", "e", "w", "o", "k", "n", "u", "p"])
# b.setOnlyLetters(["a", "r", "s"], [1, 2, 3])
# #%%
# # From real guesses on 09/04/2024 NYT Wordle
# # TEMPORARY KEY:
# #   "X" means Letter not in Word anywhere"
# #   "!" means Letter in Word at location specifically"
# #   "~" means Letter is in Word but not at that location
# # Example for guess "AMIGO"
# # then              "!~XXX"
# # means "A" is first letter; 'M' is in the word but not in the second (1 for zero-based index)
# # and letters 'I' 'G' 'O' are not anywhere

# # Guess #1) SLATE XXXX~
# b.removeLettersEverywhere(["s", "l", "a", "t"])
# b.removeLettersAtLocations("e", 4)
# b.printDiagnostics()

# #%%
# # Guess #2 WEIRD X!X~X
# b.removeLettersEverywhere(["w", "i", "d"])
# b.setOnlyLetters("e", 1)
# b.printDiagnostics()
# # Guess #3 PERKY X!!XX
# #%%
# b.removeLettersEverywhere(["p", "k", "y"])
# b.setOnlyLetters(["e", "r"], [1, 2])
# b.printDiagnostics()
# b.printCurrentWordListFancy()  # 10 left
# #%%
# # Guess #4 MERCH X!!XX
# b.removeLettersEverywhere(["m", "c", "h"])
# b.printDiagnostics()
# b.printCurrentWordListFancy()  # 10 left
# #%%
# # Guess RERUN !!!!! WIN
# #######################################
# #%%
# # NYT 09/04/2024
# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words)
# b.printDiagnostics()
# #%%
# # From real guesses on 09/04/2024 NYT Wordle

# # Guess #1) AMIGO XXXXX
# b.removeLettersEverywhere(["a", "m", "i", "g", "o"])
# b.printDiagnostics()
# #%%

# # Guess #2) SLEPT - !X!X~
# b.removeLettersEverywhere(["l", "p"])
# b.removeLettersAtLocations(["t"], [4])

# b.setOnlyLetters(["s", "e"], [0, 2])
# b.printDiagnostics()
# #%%

# # Guess #3) STUCK - !!XXX
# b.removeLettersEverywhere(["u", "c", "k"])
# b.setOnlyLetters(["s", "t"], [0, 1])
# b.printDiagnostics(printCurrentWordList=True)
# #%%

# # GUESS #4) STERN !!!!!
# b.setOnlyLetters(["s", "t", "e", "r", "n"], [0, 1, 2, 3, 4])
# b.printDiagnostics(printCurrentWordList=True)
# # Gives "Remaining Words" as ['stern', 'stern'] - doesn't realize it won already


# #%%
# # NYT 09/03/2024
# # TEMPORARY KEY:
# #   "X" means Letter not in Word anywhere"
# #   "!" means Letter in Word at location specifically"
# #   "~" means Letter is in Word but not at that location
# # Example for guess "AMIGO"
# # then              "!~XXX"
# # means "A" is first letter; 'M' is in the word but not in the second (1 for zero-based index)
# # and letters 'I' 'G' 'O' are not anywhere

# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = WordleBoard(myLetters=letters, initialWordList=words)
# b.printDiagnostics()
# #%%
# # From real guesses on 09/03/2024 NYT Wordle

# # Guess #1) SLATE XX~~X
# b.removeLettersEverywhere(["s", "l", "e"])
# b.removeLettersAtLocations(["a", "t"], [2, 3])
# b.printDiagnostics()
# #%%
# # Guess #2) ACTOR - ~X~XX
# b.removeLettersEverywhere(["c", "o", "r"])
# b.removeLettersAtLocations(["a", "t"], [0, 2])
# b.printDiagnostics()
# #%%
# # Guess #3) FAINT !!!!!
# # WIN!
# # redundant but anyway:
# b.setOnlyLetters(["f", "a", "i", "n", "t"], [0, 1, 2, 3, 4])
# b.printDiagnostics()


# #%%

# ###############################################################################
# ###############################################################################

# #%% NYT 3/1/24

# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words)
# print(len(b.currentWordList))  # now words left 10422
# #%%Guess "SLATE"
# # got expelled S L A T^1 E
# b.removeLettersEverywhere(["s", "l", "t", "e"])
# print("Remaining possible words {}".format(b.currentWordList))
# print("    len: " + str((len(b.currentWordList))))
# #%% Guess "ORDER"b.cur
# b.mustHaveLetters(["n", "a", "r"])  # 145
# #%%
# b.removeLettersEverywhere(["i", "h", "e", "o"])
# #%%########################################################################################################
# Guess = "GRAIN"
# b.removeLettersEverywhere(["g"])
# b.setOnlyLetter("r", position=1)
# b.setOnlyLetter("n", position=4)
# # Need a "cant be here" indication too
# # guess URBAN -> won

# #%% NYT 3/3
# b.removeLettersEverywhere(["l"])
# #%%
# b.setOnlyLetter("s", 0)
# b.setOnlyLetter("a", 2)
# b.setOnlyLetter("t", 3)
# b.setOnlyLetter("e", 4)
# #%%
# b.removeLettersEverywhere("k")
# #%%
# # guess "state" -> won

# #%% NYT 3/15/2024
# allWords = nltk.corpus.words.words()
# words = getWordsOfLength(allWords, wordLength=5)
# letters = list(map(chr, range(97, 123)))  # 26 lower-case ASCII "a-z"
# b = BoardLine(myLetters=letters, initialWordList=words)
# print(len(b.currentWordList))  # now words left 10422
# #%%
# # Guess SLATE
# b.removeLettersEverywhere(["s", "l", "a"])
# #%%
# b.mustHaveLetters(["t", "e"])
# #%%
# # Guess TREAT
# b.setOnlyLetter("r", 1)
# b.setOnlyLetter("t", 4)  ## only 44 words remaining
# # Guess ERUPT -> won
# #%%

# # NYT 1/28
# # First Guess "slate"
# b.removeLettersEverywhere(["s", "l", "a", "t"])  # now 2025 words left
# print(len(b.currentWordList))  # 10422
# #%%
# b.mustHaveLetters("e")
# print(len(b.currentWordList))  # now 1478 words left
# #%% ###########################################################################
# # Second Guess "coped"
# b.removeLettersEverywhere(["c", "o", "p", "d"])

# print(len(b.currentWordList))  # now 425 words left
# #%%
# b.setOnlyLetter("e", position=3)
# print(len(b.currentWordList))  # now 249 words left
# #%%

# ###### Jump ahead, last guess:
# b.removeLettersEverywhere(
#     ["s", "l", "a", "t", "c", "o", "p", "d", "i", "k", "w", "f", "u", "n", "y"]
# )
# print(len(b.currentWordList))  # 31 words remaining.
# # know that its ??BER
# #%%
# b.setOnlyLetter("b", 2)
# print(len(b.currentWordList))  # 16 words remaining.
# b._update()
# print(len(b.currentWordList))  # 8 words remaining.
# b._update()
# print(len(b.currentWordList))  # 4 words remaining.
# b._update()
# print(
#     len(b.currentWordList)
# )  # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
# #%%
# b.setOnlyLetter("e", 3)
# print(
#     len(b.currentWordList)
# )  # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
# #%%
# b.setOnlyLetter("r", 4)
# print(
#     len(b.currentWordList)
# )  # 2 words remaining. #wtf ? ('ember' and 'rebeg') so we know its 'ember')
# print(b.currentWordList)
# #%%
# # NYT 2/29
# ###############3 Turn #1 Guess "SLATE"
# b.setOnlyLetter("a", 2)
# #%%
# b.setOnlyLetter("e", 4)
# #%%
# b.removeLettersEverywhere(["s", "l", "t"])
# #%%############## Turn 2 Guess "RIDGE"
# b.setOnlyLetter("g", 3)
# #%%
# b.mustHaveLetters("i")
# #%%
# b.removeLettersEverywhere(["i", "m", "a", "g", " "])
# #%%
# ################ AFTER update to fix behavior removing elements from list being iterated on simultaneously ...
# # NYT 3/1/24
# #########################################################################
