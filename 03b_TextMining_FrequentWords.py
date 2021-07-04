# -*- coding: utf-8 -*-
"""
Description:
    Determine frequent words in keyword columns and make into features

Created on Sat Jul  3 23:25:53 2021
@author: lauren koenig
"""

#%% Set upZZ

#import packages
import pandas as pd 

keyword_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data_clean.csv')
keyword_data = keyword_data[0:40]

#functions for use in data cleaning
def preprocess_string(input): #makes lowercase, removes punctuation and common words, fixes spelling and lemmatization
    if input==input:
        #import packages
        import nltk
        nltk.download() #will slow things down if first time running
        from textblob import Word
        from nltk.corpus import stopwords
        import re
        
        input=keyword_data['condition'][5]
        print(input)
        #make all letters lowercase, then remove punctuation and number
        input = re.sub(r"[^a-z;]"," ",input.lower())

        #remove excess spaces introduced by previous step
        input = " ".join(input.split())
        
        #remove stop words
        stop = (stopwords.words('english'))
        input = input.split(" ") 
        for word in input:
            #word_clean = str(TextBlob(word).correct()) #enable to fix spelling - not accurate in case of medical terms
            word_clean = Word(word_clean).lemmatize() #remove endings
            word_clean = word

            if word_clean in stop:
                input.remove(word) #delete string if a stop word
            else:
                input[input.index(word)] = str(word_clean) #replace word with clean version if not a stop word
        
        #check stopwords twice
        for word in input:
              if word in stop:
                input.remove(word) #delete string if a stop word
                 
        print(input)
        input = " ".join(input) #turn back into a string
        
        return (input) 

def remov_duplicates(input): #gets rid of duplicate words in string
    if input==input:
        #import packages
        from collections import Counter 
        
        # split input string separated by space 
        input = input.split(" ") 

        # joins two adjacent elements in iterable way 
        for i in range(0, len(input)): 
            input[i] = "".join(input[i]) 

        # now create dictionary using counter method  which will have strings as key and their frequencies as value 
        # makes it so no repeating words within one record/feature
        UniqW = Counter(input) 

        replace_chars = ["   ", "  "] #characters to replace with space
        
        for key in UniqW.keys():
            if key in replace_chars:
                del UniqW[key]
                break

        # joins two adjacent elements in iterable way 
        s = " ".join(UniqW.keys()) #at this point there aren't any repeating words
        
        return (s) 

def remov_duplicates_semicolon(input): #gets rid of duplicate word chunks separated by semicolons
    if input==input:
        #import packages
        from collections import Counter 
        
        # split input string separated by space 
        input = input.split(";") 

        # joins two adjacent elements in iterable way 
        for i in range(0, len(input)): 
            input[i] = "".join(input[i]) 

        # now create dictionary using counter method  which will have strings as key and their frequencies as value 
        # makes it so no repeating words within one record/feature
        UniqW = Counter(input) 

        replace_chars = ["   ", "  "] #characters to replace with space
        
        for key in UniqW.keys():
            if key in replace_chars:
                del UniqW[key]
                break

        # joins two adjacent elements in iterable way 
        s = " ".join(UniqW.keys()) #at this point there aren't any repeating words
        
        return (s)
#%% process strings

#makes lowercase, removes punctuation and common words, fixes spelling and lemmatization
keyword_data = keyword_data.applymap(preprocess_string)

#removes duplicates words within each record and feature
keyword_data2 = keyword_data.applymap(remov_duplicates)


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
    
    
    