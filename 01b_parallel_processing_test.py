# -*- coding: utf-8 -*-
"""
Description:
    Using to test out parallel processing and how much it changes the time needed to read in the xml files

Created on Sun Sep 13 10:48:17 2020
@author: lauren koenig
"""
#%% set up

import glob
from timeit import default_timer as timer
from xmls_to_DataFrame import xmls_to_DataFrame_KnownStruc 
import concurrent.futures
import pandas as pd 

#First grab all the xml file paths in first folder
xmlfiles = [] #list to hold all the xml file names
for file in glob.glob("data-raw/NCT0000xxxx/NCT*.xml", recursive=True): #searching for all xml in first folder
    xmlfiles.append(file) #adds xml file to the list of file names

print(len(xmlfiles))


clin_data = pd.DataFrame() #make a dataframe to hold all the data

#%% V1: pull data from the xml files w/out parallel

start = timer()
        
for file in xmlfiles: #go through each xml file
    data = xmls_to_DataFrame_KnownStruc(file)
    data_df = pd.DataFrame([data] ) #change the dictionary into a panda dataframe
    clin_data = clin_data.append(data_df, ignore_index = True, sort='True') #append the dataframe to the larger dataframe of all data

end = timer()
print(end - start) #165 sec for 5754 records


#%% next pull data from xml files with parallel processing


start = timer()

def main():
    clin_data_small = pd.DataFrame() #make a dataframe to hold all the data
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for data in executor.map(xmls_to_DataFrame_KnownStruc, xmlfiles):
            data_df = pd.DataFrame([data] ) 
            #append the dataframe to the larger dataframe of all data
            clin_data_small = clin_data_small.append(data_df, ignore_index = True, sort='True') 
    return clin_data_small

clin_data=clin_data.append(main())

end = timer()
print(end - start) #81 sec for 5754 records

#parallel is 2x as fast so will use in Clean_all_data.py
#full data has 446 folder with 344513 trials so likely will take 60x longer