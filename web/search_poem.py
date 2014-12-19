# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

import pymorphy2
import codecs
import re
index = {}
delete = re.compile(u'\W+?|\d+?', re.UNICODE)
f = codecs.open('atlas_shrugged.txt', encoding='utf-8')
morph = pymorphy2.MorphAnalyzer()
for line in f.readlines():
    line = delete.sub(' ', line)
    line = line.split()
    normal = []
    for word in line:
        forms = morph.parse(word)
        for item in forms:
            p = item.normal_form
            if p not in normal:
                normal.append(p)
    for word in normal:
        index.setdefault(word,0)
        index[word] +=1

keys = sorted(index.keys(), key=lambda x: index[x], reverse=True)
print len(keys)
for key in keys:
    print key + ' ------> ',index[key]


import pymorphy2

def get_normal(word):
    """возвращает список туплей, содержащих нормальную форму и часть речи"""
    morph = pymorphy2.MorphAnalyzer()
    forms = morph.parse(word)
    normal = []
    p_speech = []
    for item in forms:
        p = item.normal_form
        if p not in normal:
            normal.append(p)
            p_speech.append(item.tag.POS)
    return zip(normal,p_speech)

if __name__ == '__main__':
    print get_normal(u'стали')