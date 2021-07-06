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
from collections import Counter
from nltk import ngrams

keyword_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data_clean.csv')
keyword_data = keyword_data[0:40]


#%% take a look at the most common n-grams

for n_size in range(1,6):
    print("n size is ", n_size)
    for i in keyword_data.columns:
        column_data = keyword_data[i].str.cat(sep=" ")   
        ngram_counts = Counter(ngrams(column_data.split(" "), n_size))
        print(i)
        print(ngram_counts.most_common(5))
    
#%% see how many ngrams occur semi frequently 

for n_size in range(1,6):
    print("n size is ", n_size)
    for i in keyword_data.columns:
        column_data = keyword_data[i].str.cat(sep=" ")   
        ngram_counts = Counter(ngrams(column_data.split(" "), n_size))
        print(i)
        print(len({x: count for x, count in ngram_counts.items() if count >= 0.01*len(keyword_data[i])})) #how many ngrams occur in over 1% of cases? - higher frequencies seem to be too few, and the 1% matches the criteria used in the category_data
    
  
#%% see how many ngrams occur too frequently 

for n_size in range(1,6):
    print("n size is ", n_size)
    for i in keyword_data.columns:
        column_data = keyword_data[i].str.cat(sep=" ")   
        ngram_counts = Counter(ngrams(column_data.split(" "), n_size))
        print(i)
        print(len({x: count for x, count in ngram_counts.items() if count >= 0.10*len(keyword_data[i])})) #how many ngrams occur in over 1% of cases? - higher frequencies seem to be too few, and the 1% matches the criteria used in the category_data

#since few n-grams occur more than 10% of the time, I'm not going to worry about removing those that occur too frequently from the list
        


#%% make columns representing if the n-gram is found in a record 

for n_size in range(1,6):
    for i in keyword_data.columns:
        column_data = keyword_data[i].str.cat(sep=" ")   
        ngram_counts = Counter(ngrams(column_data.split(" "), n_size))
        print(i)
        print({x: count for x, count in ngram_counts.items() if count >= 0.10*len(keyword_data[i])})
        




    