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
        from textblob import Word
        from nltk.corpus import stopwords
        import re
        
        #input = keyword_data['brief_title'][1] #for testing
        
        #make all letters lowercase, then remove punctuation and number
        input = re.sub(r"[^a-z;]"," ",input.lower())

        #remove excess spaces introduced by previous step
        input = " ".join(input.split())
        input = input.split(" ") #split again so can iterate over it

        #remove stop words
        stop = (stopwords.words('english'))
        input_no_stops = []
        for word in input:
            if word not in stop:
                input_no_stops.append(word) #delete string if a stop word
        
        #clean word
        try:
            for word in input_no_stops:
                word_clean = word
                #word_clean = str(TextBlob(word_clean).correct()) #enable to fix spelling - not accurate in case of medical terms
                word_clean = Word(word_clean).lemmatize() #remove endings
                input_no_stops[input_no_stops.index(word)] = str(word_clean) #replace word with clean version if not a stop word
                
        except Exception as ex:
            print(ex)
            print("It's likely you don't have nltk libraries installed, follow popup to install them")
            nltk.download() #opens downloader          

        #check for stop words again
        input_no_stops2 = []
        for word in input_no_stops:
            if word not in stop:
                input_no_stops2.append(word) #delete string if a stop word

            
        input_no_stops2 = " ".join(input_no_stops2) #turn back into a string
        print(input_no_stops2)
        
        return (input_no_stops2) 

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
        s = ";".join(UniqW.keys()) #at this point there aren't any repeating words
        
        return (s)
#%% process strings

#makes lowercase, removes punctuation and common words, lemmatization
keyword_data2 = keyword_data.applymap(preprocess_string)

#removes duplicates words within each record and feature
keyword_data3 = keyword_data2.applymap(remov_duplicates)


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
    
    
    