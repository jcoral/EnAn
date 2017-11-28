# -*- coding: utf-8 -*-
from constants import ddir
from main import getAllDocWords, getBaseWordFromText
from BaiduTranslate import translateFromWord
from threadpool import ThreadPool, NoResultsPending, WorkRequest
import json
import threading

def getAllDocPaths():
    docsName = []
    for et in [1, 2]:
        for yeaer in range(2013, 2018):
            docsName.append(ddir + str(et) + "-" + str(yeaer) + ".txt")

    return docsName

def getAllWords():
    """
    获取英语一和英语二所有的单词
    :return: [, ...]
    """

    allDocWords = getAllDocWords(getAllDocPaths())
    allDocWords = allDocWords.values()
    adwLength = len(allDocWords) - 1
    for index in xrange(adwLength):
        allDocWords[0] += allDocWords.pop(1)
    allDocWords = set(allDocWords[0])

    return allDocWords


def buildWordToBase():
    """
     找到所有单词的词根， 建立对应关系
    :return: [baseWord: word]
    """

    allWords = getAllWords()
    wordToBaseTable = {}
    for word in allWords:
        baseWord = getBaseWordFromText(word)["tokens"][0]["token"]
        wordToBaseTable[baseWord] = word

    return wordToBaseTable


def translationWord(allWords):
    def translate(baseWord, word):
        chinese = translateFromWord(word)
        allWords[baseWord] = chinese

    requests = []
    for baseWord, word in zip(allWords.keys(), allWords.values()):
        requests.append(WorkRequest(translate, args=(baseWord, word)))

    pool = ThreadPool(num_workers=8)
    [pool.putRequest(req) for req in requests]
    try:
        pool.poll(True)
    except NoResultsPending:
        pool.wait()

    # for baseWord, word in zip(allWords.keys()[0: 2], allWords.values()[0:2]):


def writeFile(allWords):
    df = open("words.json", mode="w")
    json.dump(allWords, df)


if __name__ == '__main__':
    # print getAllDocPaths()

    allWords = buildWordToBase()
    # print allWords

    # translationWord(allWords)
    # writeFile(allWords)
    # print allWords

    print "OK" * 20











