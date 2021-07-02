# -*- coding: utf-8 -*-
"""
Description:
    File to clean original data from Clinicaltrials.gov and make it into a     usable format
    Uses column names selected from column_selection.py
    
Created on Sat Sep 12 21:44:42 2020
@author: lauren koenig
"""

#%% Set up


#columns I want to keep, as selected earlier in column_selection.py
# these lists are also built into xmls_to_DataFrame_KnownStruc
keyword_cols = ['brief_title',
                'condition',
                'intervention/intervention_type',
                'location_countries/country']

date_cols = ['completion_date', 
             'start_date']

num_cols = ['eligibility/maximum_age', 
            'eligibility/minimum_age', 
            'enrollment']

category_cols = ['eligibility/gender', 
                 'eligibility/healthy_volunteers', 
                 'overall_status', 
                 'phase', 
                 'study_design_info/primary_purpose',
                 'study_type',
                 'sponsors/lead_sponsor/agency_class']

#needed packages
import glob
import pandas as pd 
from timeit import default_timer as timer 
from xmls_to_DataFrame import xmls_to_DataFrame_KnownStruc 
import concurrent.futures
from collections import Counter 
import datetime
import numpy as np


#new functions
def main(xmlfiles):
    clin_data_small = pd.DataFrame() #make a dataframe to hold all the data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for data in executor.map(xmls_to_DataFrame_KnownStruc, xmlfiles):
            data_df = pd.DataFrame([data] ) 
            #append the dataframe to the larger dataframe of all data
            clin_data_small = clin_data_small.append(data_df, ignore_index = True, sort='True') 
    return clin_data_small


def remov_duplicates(input): #gets rid of duplicate words in string and deletes common words
    if input==input:
       #clean up string
        replace_chars = ["'s", ",", "(", ")", "[", "]", ":", "&", "/", ":", "\"", "\'", "#", "$", "+", "-", "  "] #characters to delete
        for character in replace_chars:
            input = input.replace(character, " ")


        # split input string separated by space 
        input = input.split(" ") 

        # joins two adjacent elements in iterable way 
        for i in range(0, len(input)): 
            input[i] = "".join(input[i]) 

        # now create dictionary using counter method 
        # which will have strings as key and their  
        # frequencies as value 
        UniqW = Counter(input) 

        replace_chars = ["a", "A", "in", "In", "the", "The", "with", "With", "and", "And", "or", "Or", "by", "By", "to", "To", "of", "Of", "from", "From", "for", "For", "  ", "   "] #characters to replace with space
        
        for key in UniqW.keys():
            if key in replace_chars:
                del UniqW[key]
                break

        # joins two adjacent elements in iterable way 
        s = " ".join(UniqW.keys()) #at this point there aren't any repeating words
        
        
        return (s) 
    
    

#%% now ready to grab all the xml file paths

xmlfiles = [] #list to hold all the xml file names
for file in glob.glob("data-raw/*/NCT*.xml", recursive=True): #searching for all xml files
    xmlfiles.append(file) #adds xml file to the list of file names

print(len(xmlfiles))

clin_data = pd.DataFrame() #make a dataframe to hold all the data

#%% next pull data from all the xml files and combine into a DataFrame using parallel processing
#for some reason stalled out when trying to do all at once, but fine if split into 3 parts

start = timer() #will take a while so I'm timing it

clin_data=clin_data.append(main(xmlfiles[:100000]))

end = timer()
print(end - start) #part 1 done

start = timer()

clin_data=clin_data.append(main(xmlfiles[100000:200000]))

end = timer()
print(end - start) #part 2 done

start = timer()

clin_data=clin_data.append(main(xmlfiles[200000:]))

end = timer()
print(end - start) #part 3 done

#%% next separate data into different types
keyword_data = clin_data[keyword_cols]
date_data = clin_data[date_cols]
num_data = clin_data[num_cols]
category_data = clin_data[category_cols]

keyword_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data.csv', index=False)
date_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\date_data.csv', index=False)
num_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\num_data.csv', index=False)
category_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\category_data.csv', index=False)

del [clin_data, keyword_data, date_data, num_data, category_data, xmlfiles, file, start, end]

#%% removes repeated words for keyword_cols

keyword_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data.csv')


keyword_data = keyword_data.applymap(remov_duplicates)

for i in keyword_cols:
    print((keyword_data[i].value_counts()[0:10])/sum((keyword_data[i].value_counts())))
    print('\n')
    
keyword_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\keyword_data_clean.csv', index=False)
del [keyword_data]

#%% convert all dates to standard format 

date_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\date_data.csv')

for i in date_cols:
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



date_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\date_data_clean.csv', index=False)
del [date_data, date_obj, fmt, full_date_obj, i, j]

#%% Clean up number columns

#Strips strings from number columns and converts all ages to years units
num_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\num_data.csv')

print(num_data[0:10])

for i in num_cols:
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
del [num_data, number_only, s, i, j]
       

#%%  Clean up category columns

category_data = pd.read_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\category_data.csv')

#remove duplicate words 
category_data = category_data.applymap(remov_duplicates)

    
#combine some categories as appropriate
        
category_data['phase'] = category_data['phase'].replace('Phase 1 2', "Phase 1")
category_data['phase'] = category_data['phase'].replace('Phase 2 3', "Phase 2")
category_data['phase'] = category_data['phase'].replace('Early Phase 1', "Phase 1")

category_data['study_type'] = category_data['study_type'].replace('Observational Patient Registry', "Observational")
category_data['study_type'] = category_data['study_type'].replace('Expanded Access', "N A")

category_data['phase'] = category_data['phase'].replace('N A', np.nan)

#get list of study_design_info values that occur less than 5% of the time
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
for i in category_cols:
    print((category_data[i].value_counts()[0:10])/sum((category_data[i].value_counts())))
    print('\n')
    
category_data.to_csv(r'C:\Users\lkoen\BOX\Clinical_trials_gov\data-clean\category_data_clean.csv', index=False)
del [category_data, other_values, i]
   
    