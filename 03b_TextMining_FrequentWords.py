# -*- coding: utf-8 -*-
"""
Description:
    Determine frequent words in keyword columns and make into features

Created on Sat Jul  3 23:25:53 2021
@author: lauren koenig
"""

#%% Set up

#import packages
import pandas as pd 
import numpy as np
from collections import Counter
from nltk import ngrams

keyword_data = pd.read_csv('data-clean\keyword_data_clean.csv')
#keyword_data = keyword_data[0:40]


#%% take a look at the most common n-grams

for n_size in range(1,6):
    print("n size is ", n_size)
    for i in keyword_data.columns:
        ngram_counts = Counter()   # or nltk.FreqDist()
        for sent in keyword_data[i]:     
            if sent is not np.nan:
                ngram_counts.update(ngrams(sent.split(" "), n_size))
        print(i)
        print([" ".join(item) for item in list(next(zip(*ngram_counts.most_common(5))))])
        
    
#%% see how many ngrams occur semi frequently 

#how many ngrams occur in over 1% of cases?
#looked at higher frequencies but get too few matches
#1% also good to use because it matches the criteria used when cleaning the category_data
 
frequency = 0.01
#print out numbers
for n_size in range(1,4):
    print("n size is ", n_size)
    for i in keyword_data.columns:
        ngram_counts = Counter()   # or nltk.FreqDist()
        for sent in keyword_data[i]:     
            if sent is not np.nan:
                ngram_counts.update(ngrams(sent.split(" "), n_size))
        print(i)
        print(len({x: count for x, count in ngram_counts.items() if count >= frequency*len(keyword_data[i])})) 

#print out actual n-grams
for n_size in range(1,4):
    print("n size is ", n_size)
    for i in keyword_data.columns:
        ngram_counts = Counter()   # or nltk.FreqDist()
        for sent in keyword_data[i]:     
            if sent is not np.nan:
                ngram_counts.update(ngrams(sent.split(" "), n_size))
        print(i)
        print({x: count for x, count in ngram_counts.items() if count >= frequency*len(keyword_data[i])})
        


#%%  create columns representing if the n-gram is found in a record 





    