# -*- coding: utf-8 -*-
import hashlib
import requests
import sys
import json

# TODO
appid = "appid"
salt  = "salt"
skey  = "key"
reqURL= "http://api.fanyi.baidu.com/api/trans/vip/translate"


def _getSign(word):
    s1 = appid + word + salt + skey
    md = hashlib.md5()
    md.update(s1)
    return md.hexdigest()


def translateFromWord(word):
    params = {
        "q":    word,
        "from": "en",
        "to":   "zh",
        "appid":appid,
        "salt": salt,
        "sign": _getSign(word)
    }

    try:
        response = requests.get(url=reqURL, params=params, timeout=10)
        return  json.loads(response.content)["trans_result"][0]["dst"]
    except:
        return word


if __name__ == '__main__':
    print translateFromWord("differ")









