#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:15:19 2025

@author: jackkausch
"""

from requests_oauthlib import OAuth1
import requests
import json
import pandas as pd

codebook = pd.read_csv('codebook.csv')
auth = OAuth1("fa7b0e6e3aa44590b3a44229744b8f76", "f5ce3a9b1aec486db75106d6a4794d06")
headers = {'Accept': 'application/json'}
method = "GET"
url = 'https://api.thenounproject.com/v2/icon?query=DUST'

response = requests.get(url, headers=headers, auth=auth)

print(response.json()['total'])

total = []

for i in codebook['Name']:
    url = 'https://api.thenounproject.com/v2/icon?query=' + str(i)
    response = requests.get(url, headers=headers, auth=auth)
    number = response.json()['total']
    total.append(number)
    print(i,number)
       
codebook['Noun Project Count'] = total

codebook.to_csv('codebook_noun.csv')