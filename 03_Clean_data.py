# -*- coding: utf-8 -*-
"""
Description:
    File to clean original data from Clinicaltrials.gov and make it into a     usable format
    Uses column names selected from column_selection.py
    
Created on Sat Sep 12 21:44:42 2020
@author: lauren koenig
"""


#%% Set up

#import needed packages
#pip install -U textblob
import pandas as pd 
from collections import Counter 
import datetime
from nltk import ngrams

#define custom functions for use in data cleaning
def preprocess_string(input): #makes lowercase, removes punctuation, removes stop words, lemmatization
    if input == input:
        try:
            #import packages
            import nltk
            from textblob import Word
            from nltk.corpus import stopwords
            import re
            
            #input = keyword_data['brief_title'][1] #for testing
            
            #make all letters lowercase, then remove punctuation and number
            input = re.sub( r"[^a-z0-9]" , " " , input.lower() )
    
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
            #print(input_no_stops2)
            return (input_no_stops2) 
        except:
            return (input)
        
def remov_duplicates(input, sep_val=" "): #gets rid of duplicate words in string
    if input==input:
        #import packages
        
        # split input string separated by space 
        input = input.split(sep_val) 

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
        s = sep_val.join(UniqW.keys()) #at this point there aren't any repeating words
        
        return (s) 

    
#%% clean keyword_data strings

keyword_data = pd.read_csv('data-clean\keyword_data.csv')

#remove duplicate entries (not single words, but when one value was recorded multiple times)
for i in keyword_data.columns: #applymap doesn't accept multiple arguments
    keyword_data[i] = keyword_data[i].apply(remov_duplicates,sep_val= " ; ")

#remove punctuation and stop words, lemmitize endings 
keyword_data = keyword_data.applymap(preprocess_string)

#apply the remove duplicates again but on individual words, and only for the title values
#if applied to all then 'united states; united kingdom' becomes 'united states; kingdom'
keyword_data['brief_title'] = keyword_data['brief_title'].apply(remov_duplicates)

#print some ngrams to see if it worked
for i in keyword_data.columns:
    column_data = keyword_data[i].str.cat(sep=" ")   
    ngram_counts = Counter(ngrams(column_data.split(" "), 2))
    print(i)
    print(ngram_counts.most_common(5))
    
keyword_data.to_csv('data-clean\keyword_data_clean.csv', index=False)

#%% clean date_data by converting all dates to standard format 

date_data = pd.read_csv('data-clean\date_data.csv')

for i in date_data.columns:
    date_obj = {}
    for j in date_data[i]:
        if j ==j:
            for fmt in ('%B %d, %Y', '%B %Y'):
                try:
                    full_date_obj = datetime.datetime.strptime(j, fmt)
                    date_obj[j] = full_date_obj.date()
                except ValueError:
                    pass

    date_data[i].replace(date_obj, inplace=True)

#see if start to completion times are reasonable
date_data['days_to_completion'] = (date_data['completion_date'] - date_data['start_date']).dt.days 
#there are some crazy long ones, with super late completion dates (ie 2085) but that's what's actually in the xml

#can't include dates as is, so changing to numeric with only the year included
date_data['start_year'] = pd.to_datetime(date_data['start_date']).dt.year


date_data.to_csv('data-clean\date_data_clean.csv', index=False)

#%% Clean num_data 

#Strips strings from number columns and converts all ages to years units
num_data = pd.read_csv('data-clean\num_data.csv')

print(num_data[0:10])

for i in num_data.columns:
    number_only = {}
    for j in num_data[i]:
        s = j
        
        if type(j) is str:
            if "Year" in s:
                # Remove 'years'
                s =  s.strip("Years")
                #remove remaining s
                s = s.strip('Year')  
                #remove starting and trailing whitespace
                s = s.strip() 
                #convert string to integer
                s = int(s)
 
            elif "Month" in s:
                # Remove 'months'
                s =  s.strip("Months")
                #remove remaining s
                s = s.strip('Month')  
                #remove starting and trailing whitespace
                s = s.strip() 
                #convert string to integer
                s = int(s)
                #change from months to years
                s = int(s) / 12
            
            elif "Week" in s:
                # Remove 'months'
                s =  s.strip("Weeks")
                #remove remaining s
                s = s.strip('Week')  
                #remove starting and trailing whitespace
                s = s.strip() 
                #convert string to integer
                s = int(s)
                #change from weeks to years
                s = int(s) / 52

            elif "Day" in s:
                # Remove 'months'
                s =  s.strip("Days")
                #remove remaining s
                s = s.strip('Day')  
                #remove starting and trailing whitespace
                s = s.strip() 
                #convert string to integer
                s = int(s)
                #change from days to years
                s = int(s) / 365

            
        #assign output to the list holding all the new values
        number_only[j] = s
    num_data[i].replace(number_only, inplace=True)
    num_data[i] = pd.to_numeric(num_data[i],errors='coerce')


print(num_data[0:10])
num_data.to_csv('data-clean\num_data_clean.csv', index=False)
       

#%%  Clean category_data

category_data = pd.read_csv('data-clean\category_data.csv')

#remove duplicate words 
#category_data = category_data.applymap(remov_duplicates)

for i in category_data.columns:
    print((category_data[i].value_counts())/sum((category_data[i].value_counts())))
    print('\n')
    
#Combine infrequent values into "other" categories
for i in category_data.columns:
    #set percentage want as the minimum frequency each value occurs in a column
    cut_off = 0.01
    
    #get list of values that occur less than cutoff frequency
    other_values = category_data[i].value_counts()/sum((category_data[i].value_counts())) < cut_off

    #combine uncommon values in an 'other' category
    for val in other_values[other_values].index:
        category_data[i] = category_data[i].replace(val, "Other")
    
    #if the 'other' category is still below the cut off make them all NA instead
    if len(category_data[i][category_data[i] == 'Other'])/len(category_data[i]) < cut_off:
        category_data[i] = category_data[i].replace('Other', None)
    
    
#print unique value counts to show changes that have taken effect
for i in category_data.columns:
    print((category_data[i].value_counts())/sum((category_data[i].value_counts())))
    print('\n')
    
    
category_data.to_csv('data-clean\category_data_clean.csv', index=False)
   
#%%  Combine data into one dataframe
all_data = pd.concat([date_data, num_data, category_data], axis=1)

all_data.to_csv('data-clean\all_data_clean.csv', index=False)
