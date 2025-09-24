#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 12:05:24 2024

@author: jackkausch
"""

import pandas as pd
import math
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('enwiki_20180420_100d.txt',error_bad_lines=False, delimiter=',')

sequence =[]
for i in df['entities']:
    sequence.append(i)



mydf = df.drop(['entities'], axis='columns')
index = pd.DataFrame()
index['entities'] = sequence

test = pd.read_csv('test.csv')

for i in test['class']:
    i.replace(" ","_")
    index[str(i)] = math.acos(cosine_similarity(mydf,mydf.iloc[[sequence.index(i)]]))
    

for i in index['entities']:
    while i.startswith('ENTITY'):
        pass
    else:
        index.drop(index[index['entities'] == i].index[0])

#index = index.head(200)
#print(index)
index.to_csv('RealCharacterLanguage.csv')


