# -*- coding: utf-8 -*-
from WordEntity import WordEntity
from HTMLTemplate import rowTemplate, tableTemplate, totalTemplate
from constants import entype

htmlPath = "../pages/content/"
spltePageWorsNum = 500

def _generateWordHTML(wordEntity):
    years = list(wordEntity.years)
    years.sort()
    return rowTemplate.substitute(td1=",".join(wordEntity.gword),
                                  td2=wordEntity.chinese,
                                  td3=",".join(years),
                                  td4=round(wordEntity.score, 2))

def generateDocWordsHTML(allDocWords):
    rows = ""
    for index, wordItem in enumerate(allDocWords):
        wordEntity = wordItem[1]
        rows += _generateWordHTML(wordEntity)

    return tableTemplate.substitute(content=rows.encode(encoding="utf-8"))


def generateAllDocWordsHTML(allDocWords, fileHeadName="total-" + entype + "-"):
    rows = ""

    def writeSectionFile(name, content):
        try:
            rows = content.encode(encoding="utf-8")
            tableHTML = tableTemplate.substitute(content=rows)
        except UnicodeDecodeError, e:
            print rows, e
            return

        sectionFile = open(name, mode="w")
        sectionFile.write(tableHTML)
        sectionFile.close()

    section = 0
    for index, wordItem in enumerate(allDocWords):
        wordEntity = wordItem[1]
        rows += _generateWordHTML(wordEntity)

        section = int((index + 1) / spltePageWorsNum)

        # 分块写入文件
        if (index + 1) % spltePageWorsNum == 0:
            fileName = htmlPath + fileHeadName
            fileName += str(section) + ".html"
            writeSectionFile(fileName, rows)
            rows = ""

    if rows != "" or rows is not None:
        fileName = htmlPath + fileHeadName
        fileName += str(section + 1) + ".html"
        writeSectionFile(fileName, rows)
    rows = ""

    return "OK"


def generateAllSingelDocWordsHTML(singleDocWords):
    for docItem in singleDocWords:
        year  = docItem[0]
        words = docItem[1]
        yearHTML = generateDocWordsHTML(words)

        htmlFile = open(htmlPath + year + ".html", mode="w")
        htmlFile.write(yearHTML)
        htmlFile.close()

    return "OK"



if __name__ == '__main__':
    pass
























