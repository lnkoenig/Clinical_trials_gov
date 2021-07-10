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
#keyword_data = keyword_data[0:40] #for testing


#%% take a look at the 5 most common n-grams to make sure it's working

for n_size in range(1,6):
    for col in keyword_data.columns:
        ngram_counts = Counter()   
        for record in keyword_data[col]:     
            if record is not np.nan:
                ngram_counts.update(ngrams(record.split(" "), n_size))
        print(col, "ngrams of size", n_size, ":")
        print([" ".join(gram) for gram in list(next(zip(*ngram_counts.most_common(5))))])
        
    
#%% see how many ngrams occur semi frequently 

#how many ngrams occur in over 1% of cases?
#looked at higher frequencies but get too few matches
#1% also good to use because it matches the criteria used when cleaning the category_data
 
#prints how how many high frequency n-grams occur for each column with a range of n

frequency = 0.01

for n_size in range(1,4):
    for col in keyword_data.columns:
        ngram_counts = Counter()
        for record in keyword_data[col]:     
            if record is not np.nan:
                ngram_counts.update(ngrams(record.split(" "), n_size))
        print(col, "ngrams of size", n_size, ":")
        print(len({x: count for x, count in ngram_counts.items() if count >= frequency*len(keyword_data[col])})) 

   


#%%  create list of most common n-grams 

common_ngram_list = [[] for _ in range(len(keyword_data.columns))]


#print out actual n-grams
for n_size in range(1,4):
    for col in keyword_data.columns:
        ngram_counts = Counter()
        for record in keyword_data[col]:     
            if record is not np.nan:
                ngram_counts.update(ngrams(record.split(" "), n_size))
        print(col, "ngrams of size", n_size, ":")
        ngram_counts = Counter({k: ngram_counts for k, ngram_counts in ngram_counts.items() if ngram_counts >= frequency*len(keyword_data[col])})
        for gram in list(ngram_counts):
            gram = " ".join(gram)
            print(gram)
            common_ngram_list[keyword_data.columns.get_loc(col)].append(gram)


 #%%  create variable for each common ngram detecting if it exists in a record
ngram_frequency = pd.DataFrame()

for col in keyword_data.columns:
    for gram in common_ngram_list[keyword_data.columns.get_loc(col)]:
        gram_match = []
        for record in keyword_data[col]:
            if(record is not np.nan):
                gram_match.append(gram in record)
            else:
                gram_match.append(None) #could use False or None
        ngram_frequency[str(col + ': ' + gram)] = gram_match
        
 
ngram_frequency.to_csv('data-clean\keyword_data_clean_ngrams.csv', index=False)
    
   
   
   