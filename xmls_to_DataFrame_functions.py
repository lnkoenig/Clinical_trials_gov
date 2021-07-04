# -*- coding: utf-8 -*-
"""
Description:
    Defines functions to add the clinical trial xml files to a pandas dataframe
    goes 10 layers deep looking for data within the xml structure
    One function for known structure
    The other is for unknown and was used to choose the variables in KnownStruc 
    
    xmlfiles is a list of paths

Created on Sat Sep 12 22:58:59 2020
@author: lauren koenig
"""
def xmls_to_DataFrame_KnownStruc(file):
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
    
    col_list = (keyword_cols + date_cols + num_cols + category_cols)

    import xml.etree.ElementTree as ET 
    tree = ET.parse(file) #open the file
    root = tree.getroot() #set the root
    data = {} #dictionary to hold all the data from one xml file

    for col in col_list:
        node_data = []
        for j in root.findall("./" + col):
            node_data = (j.text)
            if col not in data.keys(): #if not a repeated name
                data[col] = node_data #add to dictionary the colname and data
            else: #if there's already an entry in the dictionary
                data[col] = data[col]  + " ; " + node_data #concat the current entry and the new entry into one
    return data


def xmls_to_DataFrame_UnknownStruc( xmlfiles ):
    import pandas as pd 
    import xml.etree.ElementTree as ET 
      
    dataframe = pd.DataFrame() #make a dataframe to hold all the data
    
    for file in xmlfiles: #go through each xml file
    
        tree = ET.parse(file) #open the file
        root = tree.getroot() #set the root
    
        data = {} #dictionary to hold all the data from one xml file
    
        for child in root: #go through each child node from the root directory
    
            if (child.text is None) or  "\n" in child.text:
                for child2 in child:
                    if  (child2.text is None) or "\n" in child2.text:
                        for child3 in child2:
                            if  (child3.text is None) or "\n" in child3.text:
                                for child4 in child3:
                                    if  (child4.text is None) or "\n" in child4.text:
                                        for child5 in child4:
                                            if  (child5.text is None) or "\n" in child5.text:
                                                for child6 in child5:
                                                    if (child6.text is None) or "\n" in child6.text:
                                                        for child7 in child6:
                                                            if (child7.text is None) or "\n" in child7.text:
                                                                for child8 in child7:
                                                                    if (child8.text is None) or "\n" in child8.text:
                                                                        for child9 in child8:
                                                                            if  (child9.text is None) or "\n" in child9.text:
                                                                                for child10 in child9:
                                                                                    if  (child10.text is not None) and "\n" not in child10.text:
                                                                                        colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag + "/" + child5.tag + "/" + child6.tag + "/" + child7.tag + "/" + child8.tag  + "/" + child9.tag  + "/" + child10.tag
                                                                                        node_data = child10.text
                                                                                        if colname not in data.keys(): #if not a repeated name
                                                                                            data[colname] = node_data #add to dictionary the colname and data
                                                                                        else: #if there's already an entry in the dictionary
                                                                                            data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one  
                                                                            else:
                                                                                colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag + "/" + child5.tag + "/" + child6.tag + "/" + child7.tag + "/" + child8.tag  + "/" + child9.tag
                                                                                node_data = child9.text
                                                                                if colname not in data.keys(): #if not a repeated name
                                                                                    data[colname] = node_data #add to dictionary the colname and data
                                                                                else: #if there's already an entry in the dictionary
                                                                                    data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one  
                                                                    else:
                                                                        colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag + "/" + child5.tag + "/" + child6.tag + "/" + child7.tag + "/" + child8.tag
                                                                        node_data = child8.text
                                                                        if colname not in data.keys(): #if not a repeated name
                                                                            data[colname] = node_data #add to dictionary the colname and data
                                                                        else: #if there's already an entry in the dictionary
                                                                            data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one  
                                                            else:
                                                                colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag + "/" + child5.tag + "/" + child6.tag + "/" + child7.tag
                                                                node_data = child7.text
                                                                if colname not in data.keys(): #if not a repeated name
                                                                    data[colname] = node_data #add to dictionary the colname and data
                                                                else: #if there's already an entry in the dictionary
                                                                    data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one  
                                                    else:
                                                        colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag + "/" + child5.tag + "/" + child6.tag
                                                        node_data = child6.text
                                                        if colname not in data.keys(): #if not a repeated name
                                                            data[colname] = node_data #add to dictionary the colname and data
                                                        else: #if there's already an entry in the dictionary
                                                            data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one  
                                            else:
                                                colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag + "/" + child5.tag
                                                node_data = child5.text
                                                if colname not in data.keys(): #if not a repeated name
                                                    data[colname] = node_data #add to dictionary the colname and data
                                                else: #if there's already an entry in the dictionary
                                                    data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one  
                                    else:     
                                        colname = child.tag + "/" + child2.tag + "/" + child3.tag + "/" + child4.tag
                                        node_data = child4.text
                                        if colname not in data.keys(): #if not a repeated name
                                            data[colname] = node_data #add to dictionary the colname and data
                                        else: #if there's already an entry in the dictionary
                                            data[colname] = data[colname]  + " ; " + node_data #concat the current entry and the new entry into one
                            else:
                                colname = child.tag + "/" + child2.tag + "/" + child3.tag
                                node_data = child3.text
                                if colname not in data.keys(): #if not a repeated name
                                    data[colname] = node_data #add to dictionary the colname and data
                                else: #if there's already an entry in the dictionary
                                    data[colname] = data[colname]  + " ; " + node_data #concat the current entry and the new entry into one
                    else:
                        colname = child.tag + "/" + child2.tag
                        node_data = child2.text
                        if colname not in data.keys(): #if not a repeated name
                            data[colname] = node_data #add to dictionary the colname and data
                        else: #if there's already an entry in the dictionary
                            data[colname] = data[colname]  + " ; " + node_data #concat the current entry and the new entry into one                    
            else:
                colname = (child.tag) #grab the child node name
                node_data = tree.find(child.tag).text
                if colname not in data.keys(): #if not a repeated name
                    data[colname] = node_data #add to dictionary the colname and data
                else: #if there's already an entry in the dictionary
                    data[colname] = data[colname] + " ; " + node_data #concat the current entry and the new entry into one
        data_df = pd.DataFrame([data] ) #change the dictionary into a panda dataframe
        dataframe = dataframe.append(data_df, ignore_index = True, sort='True') #append the dataframe to the larger dataframe of all data

    return dataframe
