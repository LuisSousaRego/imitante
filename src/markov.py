import random

class Markov:
    countChar = "*"
    endChar = "~"

    def __init__(self):
        self.firstWords = {}
        self.words = {}

    def addFirstWord(self, word):
        if word in self.firstWords:
            self.firstWords[word] += 1
            self.firstWords[self.countChar] += 1
        else:
            self.firstWords[word] = 1
            self.firstWords[self.countChar] = 1
    
    def addWordTransition(self, before, after):
        if before not in self.words:
            self.words[before] = { after: 1, self.countChar: 1 }
        else:
            if after not in self.words[before]:
                self.words[before][after] = 1
            else:
                self.words[before][after] += 1
            self.words[before][self.countChar] += 1
        
    def getNextWord(self, previous):
        rnd = random.random()
        probSum = 0
        if previous == "":
            w = self.firstWords
        elif previous not in self.words: # end if there is no where to go
            return self.endChar
        else:
            w = self.words[previous]

        for word, p in w.items():
            if word == self.countChar: # skip counter
                continue
            probSum += p / w[self.countChar]
            if rnd <= probSum:
                return word

    def generateText(self):
        wordSet = self.getNextWord("") # get first word set
        text = " ".join(wordSet) + " "
        currentWord = ""
        while currentWord != self.endChar:
            currentWord = self.getNextWord(wordSet)
            text += currentWord + " "
            wordSet = wordSet[1:] + (currentWord, )
        return text