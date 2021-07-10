# -*- coding: utf-8 -*-
"""
Description:
Reads in all the XML data for the columns of interest selected previously

Created on Sat Jul  3 21:33:14 2021
@author: lauren koenig
"""

#%% Set up

#needed packages
import pandas as pd 
import glob
from timeit import default_timer as timer 
import concurrent.futures
from xmls_to_DataFrame_functions import xmls_to_DataFrame_KnownStruc 


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



#new functions
def main(xmlfiles):
    clin_data_small = pd.DataFrame() #make a dataframe to hold all the data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for data in executor.map(xmls_to_DataFrame_KnownStruc, xmlfiles):
            data_df = pd.DataFrame([data] ) 
            #append the dataframe to the larger dataframe of all data
            clin_data_small = clin_data_small.append(data_df, ignore_index = True, sort='True') 
    return clin_data_small



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

#%% next separate data into different types and save
keyword_data = clin_data[keyword_cols]
date_data = clin_data[date_cols]
num_data = clin_data[num_cols]
category_data = clin_data[category_cols]

keyword_data.to_csv('data-clean\keyword_data.csv', index=False)
date_data.to_csv('data-clean\date_data.csv', index=False)
num_data.to_csv('data-clean\num_data.csv', index=False)
category_data.to_csv('data-clean\category_data.csv', index=False)
