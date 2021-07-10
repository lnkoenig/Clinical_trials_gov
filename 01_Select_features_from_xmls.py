# -*- coding: utf-8 -*-
"""
Description:
File to go through a subset of data from Clinicaltrials.gov and find which columns I want to pull for all data. Once variables of interest are examined, can go to xml_to_DataFrame to get all data

Created on Sat ‎July ‎25, ‎2020   

@author: lauren koenig

"""

#%% set up


import glob
from xmls_to_DataFrame_functions import xmls_to_DataFrame_UnknownStruc 


#first make a list of some of the files I want to pull data from that I'll use to take a look at which data I want to pull from the whole dataset
xmlfiles = [] #list to hold all the xml file names

#searching for all xml in first folder
for file in glob.glob("data-raw/NCT0000xxxx/NCT*.xml", recursive=True): 
    xmlfiles.append(file) #adds xml file to the list of file names

#searching for all xml files in last folder (in case columns in use change over time I wanted to use both the oldest and newest folder
for file in glob.glob("data-raw/NCT0446xxxx/NCT*.xml", recursive=True): 
    xmlfiles.append(file) #adds xml file to the list of file names
len(xmlfiles)



#%% next pull data from all the files and combine into a DataFrame

clin_data_all = xmls_to_DataFrame_UnknownStruc( xmlfiles )
list(clin_data_all.columns)


#%% remove columns with little data, or which is mostly missing data

#remove ongoing studies
clin_data = clin_data_all[clin_data_all['overall_status'].isin(['Completed', 'Terminated','Withdrawn', 'Suspended'])]


print(len(clin_data.columns)) #how many columns we're starting with

drop_cols = [] #empty list to which I'll add columns I want to drop

for i in range(0,len(clin_data.columns)):
    if (clin_data[clin_data.columns[i]].value_counts().sum()) < (len(clin_data)*0.65): #columns only used in <45% of trials
        drop_cols.append((clin_data.columns[i])) #add it to drop list
    
#new dataframe to hold only the common columns
clin_data = clin_data.drop(columns=drop_cols) 
#print((clin_data.columns)    )
print(len(clin_data.columns)) #column number after dropping low frequency columns

drop_cols = [] #starting over with empty list
for i in range(0,len(clin_data.columns)):
    if len((clin_data[clin_data.columns[i]]).unique()) < 3: # for all columns with only 1 value
        drop_cols.append((clin_data.columns[i]))
clin_data = clin_data.drop(columns=drop_cols) 

print(len(clin_data.columns)) #column number after dropping columns with no variance


print(clin_data.columns) # all the remaining columns


#%% look at remaining columns one by one and categorize
#categories = keywords (text based), date_cols, num_cols, category_cols

#column number to look at - adjust to examine columns one at a time
a=2   

#each unique value in the chosen column + count of that value's frequency
print((clin_data[clin_data.columns[a]]).value_counts()) 


#%%  Sort columns and remove those I don't want to keep

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


#removes columns I don't want from clin_data
clin_data = clin_data.filter(items = keyword_cols + date_cols + num_cols + category_cols) 


#%% Check on lower freq columns to make sure I don't want to remove any
for i in range(0,len(clin_data.columns)):
    if clin_data[clin_data.columns[i]].value_counts().sum() /( len(clin_data) )*100 < 98: #if more than 2% of the data is NA
        print(clin_data.columns[i])
        print(clin_data[clin_data.columns[i]].value_counts().sum() /(len(clin_data) )*100)


#No need to save data, just the 4 column lists will be copied into next script (Clean_all_data.py)
