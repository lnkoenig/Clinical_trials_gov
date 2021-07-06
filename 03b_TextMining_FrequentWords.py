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

keyword_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data_clean.csv')
keyword_data = keyword_data[0:40]


#%% process strings


for i in keyword_data.columns:
    print((keyword_data[i].value_counts()[0:10])/sum((keyword_data[i].value_counts())))
    print('\n')
    
#check most common words and remove if appropriate
freq = pd.Series(' '.join(keyword_data).split()).value_counts()[:10]
freq
#remove words to keep
freq = freq.drop()
freq = list(freq.index)
keyword_data = keyword_data.apply(lambda x: " ".join(x for x in x.split() if x not in freq))


#check most common words in each column
for i in keyword_data.columns:
    print((keyword_data[i].value_counts()[0:10])/sum((keyword_data[i].value_counts())))
    print('\n')
    
  
 
    
from collections import Counter
from nltk import ngrams
condition = keyword_data['condition'].str.cat(sep=" ")   
ngram_counts = Counter(ngrams(condition.split(" "), 2))
ngram_counts.most_common(10)




    