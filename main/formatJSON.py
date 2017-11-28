# -*- coding: utf-8 -*-


def formatJSON(json):
    if type(json) == list:
        _formatList(json, 0)
    elif type(json) == dict:
        _formatDict(json)
    else:
        print json

def _formatDict(json, ind=1, predic=True):
    indStr = "\t"* ind
    cindStr = "\t" * (ind - 1)
    if predic:
        print "{"
    else:
        print cindStr,"{"
    for key, values in json.items():
        print indStr, key, ":",
        if type(values) == dict:
            _formatDict(values, ind=ind+1)
        elif type(values) == list:
            _formatList(values, ind=ind)
        else:
            print values
    print cindStr,"}", ","


def _formatList(v, ind):
    cindStr = "\t"*ind
    if len(v) <= 0:
        print "[]"
        return

    print "["
    for index in range(len(v)):
        item = v[index]
        if type(item) == dict:
            _formatDict(item, ind+2, predic=False)
        elif type(item) == list:
            _formatList(item, ind=ind)
        else:
            print "\t"*(ind + 1), index, ":", item
    print cindStr, "]", ","

if __name__ == '__main__':
    formatJSON({"asd1":123, "d":{"asd":123}, "l": [{"123": 123}, 123, 3]})







