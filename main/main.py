# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from build_doc import buildDocments
from FormatDoc import formatDoc, getAllDocsPath
from formatJSON import formatJSON
from constants import docIndex, docType, ddir, hostName, entype
from math import ceil, floor
from WordEntity import *
import json
from GenerateHTML import generateAllSingelDocWordsHTML, generateAllDocWordsHTML
from time import sleep
from GenerateHTMLPage import HTMLTemplater

es = Elasticsearch(hostName)

def searchWord(word):
    return es.search(index=docIndex, doc_type=docType, body={
        "query": {
            "match": {
                "content": word
            }
        }
    })


def getBaseWordFromText(text):
    return es.indices.analyze(index=docIndex, body={
        "analyzer": "english",
        "text": text
    })


def getAllDocWords(docPaths=None):
    if docPaths is None:
        docPaths = getAllDocsPath()
    allDocWords = {}
    for docPath in docPaths:
        name = docPath.replace(".txt", "").replace(ddir, "")
        allDocWords[name] = formatDoc(docPath)

    # print len(allDocWords)
    return allDocWords


# 获取在文章中单词出现的次数
def getSingleDocFre(chineseDictionary):
    allDocWords = getAllDocWords()
    singleDocFreTables = {}
    for year, docWords in zip(allDocWords.keys(), allDocWords.values()):
        # 获取所有的词根
        docBaseWords = getBaseWordFromText(" ".join(docWords))["tokens"]

        # 统计频率
        docFreWordTable = {}
        for index, baseWordDic in enumerate(docBaseWords):
            baseWord = baseWordDic["token"]
            wordEntity = docFreWordTable.get(baseWord, WordEntity())
            wordEntity.years   = [year]
            if baseWord in chineseDictionary:
                wordEntity.chinese = chineseDictionary[baseWord]
            docFreWordTable[baseWord] = wordEntity.addEle(docWords[index])

        singleDocFreTables[year] = docFreWordTable

    return singleDocFreTables


# 获取在所有文章的次数
def getFinalFrequent(chineseDictionary):
    allDocWords = getAllDocWords()
    allWordKeys = [] # 所有单词的词根
    for doc in allDocWords.values():
        allWordKeys += doc

    finalFreTable = {}
    allWordKeys = set(allWordKeys)

    # 搜索在所有文章中出现的次数
    for word in allWordKeys:
        baseWord = getBaseWordFromText(word)["tokens"][0]["token"]
        results = searchWord(word)["hits"]["hits"]
        containYear = []
        sumScore = 0.0

        for doc in results:
            containYear.append(doc["_id"])
            sumScore += doc["_score"]

        sumScore *= len(results)
        wordEntity = finalFreTable.get(baseWord, WordEntity())
        if baseWord in chineseDictionary:
            wordEntity.chinese = chineseDictionary[baseWord]
        if sumScore > wordEntity.score:
            finalFreTable[baseWord] = wordEntity.addEle(word, sumScore, containYear)
        else:
            wordEntity.gword.add(word)

    return finalFreTable

# 根据得分进行排序
def cmp(x, y):
    dif = y[1].score - x[1].score
    if dif < 0:
        dif = floor(dif)
    else:
        dif = ceil(dif)
    return int(dif)

# 对近五年所有的单词进行排序
def sortWordFre(finalWordFreTable, reverse=False):
    finalWordFreTable = sorted(finalWordFreTable.items(), cmp=cmp, reverse=reverse)
    for index in range(len(finalWordFreTable)):
        finalWordFreTable[index] = list(finalWordFreTable[index])

    return finalWordFreTable

# 对单年的单词进行排序
def sortSingleDocWordsFre(wordTable, reverse=False):
    # 根据年份进行排序
    def strCMP(x, y):
        if x == y:  return 0
        elif x > y: return 1
        else:       return -1
    wordTable = sorted(wordTable.items(), cmp=lambda x, y: strCMP(x[0], y[0]))
    sortedScordFreTable = []
    for docItem in wordTable:
        year = docItem[0]
        docWords = docItem[1]

        sortedWordFre = sorted(docWords.items(), cmp=cmp, reverse=reverse)
        sortedScordFreTable.append([year, sortedWordFre])

    return sortedScordFreTable

# 获取中文字典
def getChinese():
    df = open("words.json")
    words = json.load(df, encoding="utf-8")
    return words

# 最终处理流程
def finalProcess():

    chineseDictionary = getChinese()
    # 统计在单年中出现的次数
    singleDocFreTable = getSingleDocFre(chineseDictionary)
    sortedSingleDocFreTable = sortSingleDocWordsFre(singleDocFreTable)

    # 生成HTML文件
    print generateAllSingelDocWordsHTML(sortedSingleDocFreTable)

    # 统计在所有文章的次数
    finalWordFreTable = getFinalFrequent(chineseDictionary)
    # 排序
    finalWordFreTable = sortWordFre(finalWordFreTable)

    # 生成HTML文件
    print generateAllDocWordsHTML(finalWordFreTable)

    ### 生成得分大于0.5的单词
    # dstDir  = "../pages/" + "top-n-en" + str(entype) + ".html"
    # print HTMLTemplater.makeTotalTopHelfPage(finalWordFreTable, dstDir)


# # 更换词根
# finalWordFreTable = {}
# for baseWord, freItem in zip(allWordFreTable.keys(), allWordFreTable.values()):
#
#     # 找到词根变换出来的一个词
#     for singleDocFreWord in singleDocFreTable.values():
#         if baseWord in singleDocFreWord:
#             subWord = list(singleDocFreWord[baseWord].gword)[0]
#             finalWordFreTable[subWord] = freItem
#             break

if __name__ == '__main__':
    pass
    # 所有所有的文件
    # formatJSON(buildDocments(es))
    # #
    # sleep(2)

    # # 开始处理
    finalProcess()
    print "Translate finished!"

    # 生成HTML文件
    print "Start make HTML pages"
    HTMLTemplater.makeAllPages()
    print "Make HTML pages finished"






























