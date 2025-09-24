#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 13:37:34 2025

@author: jackkausch
"""

import pandas as pd

glosses = pd.read_csv('glosses.csv')
codebook = pd.read_csv('codebook.csv')

# Count occurrences of each unique 'Parameter_ID' in glosses
counts = glosses['Parameter_ID'].value_counts()

# Map counts to the 'ID' column in codebook, filling missing values with 0
codebook['Representation'] = codebook['ID'].map(counts).fillna(0).astype(int)

# Save to CSV
codebook.to_csv('codebook_counts.csv', index=False)


#counts = []
#for i in codebook['ID']:
#    x = 0
#    for j in glosses['Parameter_ID']:
 #       while i == j:
 #           x += 1 
 #   counts.append(x)
 #   x = 0

#print(counts)

#codebook['Representation'] = counts

#codebook.to_csv('codebook_counts.csv')

