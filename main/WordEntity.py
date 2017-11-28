# -*- coding: utf-8 -*-



class WordEntity:

    def __init__(self):
        self.score = 0
        self.gword = set()
        self.years = []
        self.chinese = None

    def addEle(self, word, score=None, years = None):
        if score is None:
            self.score += 1
        else:
            self.score = score
        self.gword.add(word)
        if years is not None:
            self.years = years
        return self

    def __str__(self):
        return "Scores: " + str(self.score) + \
               "\tWord: " + ",".join(self.gword) + \
               "\tYears: " + ",".join(self.years)

def outputWordEntity(entities):
    for k, v in zip(entities.keys(), entities.values()):
        print k, v

def outputSortedWordEntity(entities):
    for f,t in entities:
        print "BaseWord: ", f, "\t", "Words: ", t


def outputSortedSingleWordEntity(entities):
    for year, words in entities:
        print "-" * 20, year, "-"*20
        outputSortedWordEntity(words)









