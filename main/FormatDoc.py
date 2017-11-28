# -*- coding: utf-8 -*-
from constants import *

def getAllDocsName():
    docName = []
    for num in range(startYear, endYear + 1):
        docName.append(entype + "-" + str(num) + ".txt")


    return docName

def getAllDocsPath():
    docNames = getAllDocsName()
    return map(lambda name: ddir + name, docNames)



def readDoc(docPath):
    with open(docPath) as doc:
        linesList = doc.readlines()
        docStr = "".join(linesList)
        docStr = docStr.replace("\n", " ")

        return list(docStr)

def loadStopWord(path = "stopwords.txt"):
    with open(name=path) as stf:
        stopwords = stf.readlines()
        stopwords = map(lambda word: word.replace("\n", ""), stopwords)
        stopwords = filter(lambda words: len(stopwords) > 2, stopwords)
        return stopwords


def _formatDoc(docStr):

    index = 0
    docStrLength = len(docStr)
    while index < docStrLength:

        dch = docStr[index]
        isMainStr =  "A" <= dch <= "Z" or "a" <= dch <= "z"
        isMainStr = isMainStr or dch in ['\'']

        if not isMainStr:
            docStr[index] = " "

            # 如果前一个为空则删除当前的字符
            if index > 0 and docStr[index-1] in [' ', '']:
                docStr.pop(index)
                docStrLength -= 1
            else:
                index += 1

        else:
            index += 1

    words = "".join(docStr).split()
    words = filter(lambda word: len(word) > 2 or word == " ", words)
    words = map(lambda word: word.lower(), words)

    stopwords = set(loadStopWord())

    # print "Before length:", len(words)

    for stopword in stopwords:
        while stopword in words:
            words.remove(stopword)

    return words

def formatDoc(docPath):
    return _formatDoc(readDoc(docPath))


if __name__ == '__main__':

    # print "".join(_formatDoc(list("is __4__ in severity, acco")))

    # words = set(formatDoc("2-2010.txt"))

    # wfile = file("docjson.json", mode="w")
    # wfile.write("[\"" + "\",\"".join(words) + "\"]")
    # wfile.close()

    print " ".join(formatDoc("docs/2-2010.txt"))




















