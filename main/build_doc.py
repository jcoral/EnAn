# -*- coding: utf-8 -*-
from formatJSON import formatJSON
from FormatDoc import formatDoc, getAllDocsName
from constants import *
# es = Elasticsearch("http://elastic:changeme@127.0.0.1:9200")



class ENDoc:
    def __init__(self, year, content):
        self.year = year
        self.content = content


def addDoc(es, year, content):
    body = { "year" : year, "content" : content}
    return formatJSON(es.index(index=docIndex, doc_type=docType, body=body, id=year))


def initDoc(es):
    docStruct = {
        "mappings": {
            docType: {
                "properties": {
                    "year": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string",
                        "analyzer": "english"
                    }
                },
            }
        }
    }

    return formatJSON(es.indices.create(index=docIndex, body=docStruct))


def buildDocments(es):
    allDocNames = getAllDocsName()
    initDoc(es)
    for docPath in allDocNames:
        docWords = formatDoc(ddir + docPath)
        addDoc(es, docPath.replace(".txt", ""), " ".join(docWords))


if __name__ == '__main__':
    pass
    # print createDoc()
    # es.index(index=docIndex, doc_type=docType, body={
    #     "year": "2013",
    #     "content": "Defense Advanced Research Projects Agency announced plans to pay Boeing to investigate formation flight, though the program has yet to begin. There are reports that some military aircraft flew in formation when they were low on fuel during the Second World War, but Dr Lissaman says they are apocryphal. “My father was an RAF pilot and my cousin the skipper of a Lancaster lost over Berlin,” he adds. So he should know"
    # })

    # es.delete_by_query(index=docIndex, doc_type=docType, body={
    #     "query": {
    #         "match": {
    #             "content": "you"
    #         }
    #     }
    # })


    # formatJSON(es.indices.analyze(body={
    #     "query": {
    #         "match": {
    #             "content": "Defense Advanced Research Projects Agency"
    #         }
    #     }
    # }))

    # formatJSON(es.search(body={
    #     "query": {
    #         "match": {
    #             "content": "Project"
    #         }
    #     }
    # }))












