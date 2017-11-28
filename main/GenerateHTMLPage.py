# -*- coding: utf-8 -*-
from string import Template
from HTMLTemplate import rowTemplate, totalTemplate
from constants import startYear, endYear
import json

itemsNum = 6
htmlContentDir = "../pages/content/"
targetPageDir  = "../pages/"
totalMaxPageNum = 6
totalTemplatePath = targetPageDir + "totaltemplate.html"

splitePage = """
<div class="page-width bottom">
    <div class="ui buttons">
        <a href="${pre}" class="ui left labeled icon button"><i class="left arrow icon"></i> 上一页 </a>
        ${items}
        <a href="${next}" class="ui right labeled icon button"><i class="right arrow icon"></i> 下一页 </a>
    </div>
</div>
"""
splitePageTemplate = Template(splitePage)


def readFileText(path):
    temp = open(path)
    lines = temp.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    return "".join(lines)

class HTMLTemplater:
    templateHTML = None

    @staticmethod
    def makeSplitPageHTML(pageNum, hrefTemplate=None, startNum=0, curPage=0):
        rows = ""
        selected = ""
        for i in range(1, pageNum+1):
            if hrefTemplate is not None and hrefTemplate != "":
                href = hrefTemplate.substitute(content=str(startNum+i))
            else:
                href = ""
            if i == curPage:
                selected = "active"
            else:
                selected = ""
            rows += """<a href="{href}" class="ui button {selected}">{page}</button>""".\
                format(href = href, page=str(i), selected=selected)

        pre = curPage
        nextPage = curPage
        if curPage != 0:
            pre -= 1

        if curPage != pageNum:
            nextPage += 1

        return splitePageTemplate.substitute(items = rows,
                                             pre   = hrefTemplate.substitute(content=str(pre)),
                                             next  = hrefTemplate.substitute(content=str(nextPage)))

    @staticmethod
    def _fillContent(params):
        if HTMLTemplater.templateHTML is None:
            template = readFileText("../pages/template.html")
            HTMLTemplater.templateHTML = Template(template)

        return HTMLTemplater.templateHTML.substitute(**params)

    @staticmethod
    def makeHTMLPage(path,
                     content,
                     entype,
                     hrefTemplate=None,
                     itemActive=0,
                     pageNum=None,
                     startNum = 0,
                     curPage=0):

        params = {}
        params["content"] = content

        for item in range(itemsNum):
            if item == itemActive:
                params["itemactive" + str(item)] = "active"
            else:
                params["itemactive" + str(item)] = ""

        for navItem in range(itemsNum):
            href = ""
            if navItem == 0:
                href = "total-{}-1.html".format(entype)
            else:
                href = "{}-{}.html".format(entype, startYear + navItem - 1)

            params["navhref" + str(navItem)] = href

        if str(entype) == "1":
            params["entype1"] = "active"
            params["entype2"] = ""
        else:
            params["entype1"] = ""
            params["entype2"] = "active"

        if pageNum is not None and hrefTemplate is not None:
            splitePages = HTMLTemplater.\
                makeSplitPageHTML(pageNum=pageNum,
                                  hrefTemplate=hrefTemplate,
                                  startNum=0,
                                  curPage=curPage)
            params["splitpages"] = splitePages
        else:
            params["splitpages"] = ""

        htmlContent = HTMLTemplater._fillContent(params)
        hf = open(path, mode="w")
        hf.write(htmlContent)
        hf.close()
        # TODO 写入文件
        return True

    @staticmethod
    def makeAllPages():
        # 每年的
        for entype in ["1", "2"]:
            for year in range(startYear, endYear + 1):
                name = "{}-{}.html".format(entype, year)
                path = htmlContentDir + name
                dstDir = targetPageDir + name
                content = readFileText(path)
                HTMLTemplater.makeHTMLPage(dstDir, entype=entype, content=content, itemActive=year-startYear+1)

        # 总的
        for entype in ["1", "2"]:
            for pageNum in range(1, totalMaxPageNum + 1):
                name = "total-{}-{}.html".format(entype, pageNum)
                path = htmlContentDir + name
                dstDir = targetPageDir + name
                content = readFileText(path)
                HTMLTemplater.makeHTMLPage(path=dstDir,
                                           content=content,
                                           hrefTemplate=Template("total-" + entype +"-${content}.html"),
                                           pageNum=totalMaxPageNum,
                                           entype=entype,
                                           curPage=pageNum)

    @staticmethod
    def removeEW(allDocWords, dstPath):
        pageTemplate = Template(readFileText(totalTemplatePath))
        # 生成得分在0.5以上的
        rows = ""
        def makeRow(we1, we2):
            return rowTemplate.substitute(td1=",".join(we1.gword),
                                          td2=we1.chinese,
                                          td3=",".join(we2.gword),
                                          td4=we2.chinese)

        index = [0]
        wordsSize = len(allDocWords)

        # TODO 去除简单词
        # print allDocWords
        easyWord = []
        with open("easyword.txt") as ewf:
            easyWord = ewf.readlines()
            easyWord = map(lambda word: word.replace("\n", ""), easyWord)

        def findNextNotEW(index):
            if index[0] >= wordsSize or allDocWords[index[0]][1].score < 0.5: return None
            if allDocWords[index[0]][0] in easyWord:
                index[0] += 1
                return findNextNotEW(index)
            else:
                return allDocWords[index[0]][1]

        while (index[0] + 1) < wordsSize:

            frontWE = findNextNotEW(index)
            index[0] += 1
            tailWE  = findNextNotEW(index)
            if frontWE is None or tailWE is None: break

            rows += makeRow(frontWE, tailWE)

            index[0] += 2

        print index, len(allDocWords)
        tableHTML = totalTemplate.substitute(content=rows.encode(encoding="utf-8"))

        df = open(dstPath, mode="w")
        df.write(pageTemplate.substitute(content=tableHTML))
        df.close()
        return True

    @staticmethod
    def makeTotalTopHelfPage(allDocWords, dstPath):
        return HTMLTemplater.removeEW(allDocWords, dstPath)

        pageTemplate = Template(readFileText(totalTemplatePath))
        # 生成得分在0.5以上的
        rows = ""
        def makeRow(we1, we2):
            return rowTemplate.substitute(td1=",".join(we1.gword),
                                          td2=we1.chinese,
                                          td3=",".join(we2.gword),
                                          td4=we2.chinese)

        index = 0
        wordsSize = len(allDocWords)
        while (index + 1) < wordsSize:
            rows += makeRow(allDocWords[index][1], allDocWords[index][1])

            if allDocWords[index+1] <= 0.5: break

            index += 2

        print index, len(allDocWords)
        tableHTML = totalTemplate.substitute(content=rows.encode(encoding="utf-8"))

        df = open(dstPath, mode="w")
        df.write(pageTemplate.substitute(content=tableHTML))
        df.close()
        return True

if __name__ == '__main__':
    # print HTMLTemplater.makeSplitPageHTML(4, hrefTemplate=Template("h${content}H"), curPage=4)
    # print HTMLTemplater.makeHTMLPage("text.html", 123, hrefTemplate=Template("h${content}H"), pageNum=4)
    HTMLTemplater.makeAllPages()










