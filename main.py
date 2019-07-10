#!/usr/bin/env python3

import sys
import html.parser
import urllib.request
import re
import time
import json
from bs4 import BeautifulSoup
from functools import reduce

USERAGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"

def main() -> int:
    cards = dl()
    print(json.dumps([parseCard(c) for c in cards], ensure_ascii=False))
    return 0

def listRequest(offset):
    url = ('http://llsif.gamedbs.jp/card/index/{}'.format(offset) if offset
            else 'http://llsif.gamedbs.jp/card')
    hs = {'Accept-Charset': 'utf-8', 'User-Agent': USERAGENT}
    return urllib.request.Request(url, headers=hs)

def dl():
    f = lambda req: urllib.request.urlopen(req).read().decode('utf-8')
    hs = []
    for offset in (i * 50 for i in ZP()):
        hs.append(f(listRequest(offset)))
        lastInfo = parseInfo(parseLabel(parseCards(hs[-1])[-1]))
        if not lastInfo['no'] or lastInfo['no'] == 1: break
        time.sleep(1)
    return reduce(
            lambda a, b: a + b,
            (list(parseCards(h)) for h in hs),
            [])

def parseCard(c):
    res = parseInfo(parseLabel(c))
    a = c.find('div').find('a')
    ds = a.find('div').find_all('div')
    res['detail'] = a.get('href')
    res['rarity'] = ds[0].text
    res['thumb'] = 'http:' + ds[1].find('img').get('src')
    return res

def parseCards(html):
    return [inner.parent for inner in
            BeautifulSoup(html, 'html.parser').find_all(
                'div', attrs={'class', 'hvr-fade'})]

def parseLabel(c):
    return c.find('div').find('a').find('div').find_all('div')[-1].text

def parseInfo(label):
    #ts = [t for t in l.split(' ') if t != '']
    m1 = re.match('^[\s]*No.[\s]*([0-9]+)[\s]*【([^】]*)】[\s]*([^\s]+)[\s]*$', label)
    if m1:
        return {'no': int(m1.group(1)),
                'skill': m1.group(2),
                'name': m1.group(3)}
    m2 = re.match('^[\s]*No.[\s]*([0-9]+)[\s]*(.+)[\s]*$', label)
    if m2:
        return {'no': int(m2.group(1)),
                'skill': None,
                'name': m2.group(2)}
    return {'no': None, 'skill': None, 'name': None}

def ZP():
    x = 0
    while True:
        yield x
        x += 1

if __name__ == "__main__":
    exit(main())

# vim:fenc=utf-8 ff=unix ft=python ts=4 sw=4 sts=4 fdm=indent fdl=0 fdn=1:
# vim: si et cinw=if,elif,else,for,while,try,except,finally,def,class:
