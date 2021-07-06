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
import numpy as np
import pandas as pd 
from collections import Counter 
import datetime


#define custom functions for use in data cleaning
def preprocess_string(input): #makes lowercase, removes punctuation and common words, fixes spelling and lemmatization
    if input==input:
        #import packages
        import nltk
        from textblob import Word
        from nltk.corpus import stopwords
        import re
        
        #input = keyword_data['brief_title'][1] #for testing
        
        #make all letters lowercase, then remove punctuation and number
        input = re.sub(r"[^a-z]"," ",input.lower())

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
    
def remov_duplicates(input): #gets rid of duplicate words in string
    if input==input:
        #import packages
        
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
    
#%% clean keyword_data strings

keyword_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data.csv')

keyword_data = keyword_data.applymap(preprocess_string)

for i in keyword_data.columns:
    print((keyword_data[i].value_counts()[0:10])/sum((keyword_data[i].value_counts())))
    print('\n')
    
keyword_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data_clean.csv', index=False)

#%% clean date_data by converting all dates to standard format 

date_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\date_data.csv')

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


date_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\date_data_clean.csv', index=False)

#%% Clean num_data 

#Strips strings from number columns and converts all ages to years units
num_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\num_data.csv')

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
num_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\num_data_clean.csv', index=False)
       

#%%  Clean category_data

category_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\category_data.csv')

#clean strings
category_data = category_data.applymap(preprocess_string)

#remove duplicate words 
category_data = category_data.applymap(remov_duplicates)

    
#combine some category values as appropriate
        
category_data['phase'] = category_data['phase'].replace('Phase 1 2', "Phase 1")
category_data['phase'] = category_data['phase'].replace('Phase 2 3', "Phase 2")
category_data['phase'] = category_data['phase'].replace('Early Phase 1', "Phase 1")

category_data['study_type'] = category_data['study_type'].replace('Observational Patient Registry', "Observational")
category_data['study_type'] = category_data['study_type'].replace('Expanded Access', "N A")

category_data['phase'] = category_data['phase'].replace('N A', np.nan)

#get list of study_design_info values that occur less than 2% of the time
other_values = (category_data['study_design_info/primary_purpose'].value_counts()/sum((category_data['study_design_info/primary_purpose'].value_counts())) < 0.02)

#combine uncommon study_design_info values in an 'other' category
for i in other_values[other_values].index:
    category_data['study_design_info/primary_purpose'] = category_data['study_design_info/primary_purpose'].replace(i, "Other")

#get list of sponsors.lead_sponsor.agency_class values that occur less than 5% of the time
other_values = (category_data['sponsors/lead_sponsor/agency_class'].value_counts()/sum((category_data['sponsors/lead_sponsor/agency_class'].value_counts())) < 0.02)

#combine uncommon sponsors.lead_sponsor.agency_class values in an 'other' category
for i in other_values[other_values].index:
    category_data['sponsors/lead_sponsor/agency_class'] = category_data['sponsors/lead_sponsor/agency_class'].replace(i, "Other")

#get list of study_type values that occur less than 5% of the time
other_values = (category_data['study_type'].value_counts()/sum((category_data['study_type'].value_counts())) < 0.02)

#delete uncommon values 
for i in other_values[other_values].index:
    category_data['study_type'] = category_data['study_type'].replace(i, None)
    
    
    
#print unique value counts to show changes that have taken effect
for i in category_data.columns:
    print((category_data[i].value_counts()[0:10])/sum((category_data[i].value_counts())))
    print('\n')
    
    
category_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\category_data_clean.csv', index=False)
   
#%%  Combine data into one dataframe
all_data = pd.concat([date_data, num_data, category_data], axis=1)

all_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\all_data_clean.csv', index=False)
