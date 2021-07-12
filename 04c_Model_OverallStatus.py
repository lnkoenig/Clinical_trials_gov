# -*- coding: utf-8 -*-
"""
Description:
    Trying to classify which of the completed clinical trials were completed successfully vs. those that were terminated/cancelled
    Now including keyword data

Created on Fri Jul  2 18:51:27 2021
@author: lauren koenig
"""

#%% Set up
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import ensemble

date_data = pd.read_csv('data-clean\date_data_clean.csv')
num_data = pd.read_csv(r'data-clean\num_data_clean.csv')
category_data = pd.read_csv('data-clean\category_data_clean.csv')
keyword_data = pd.read_csv('data-clean\keyword_data_clean_ngrams.csv')


all_data = pd.concat([date_data, num_data, category_data, keyword_data], axis=1)

del [date_data, num_data, category_data, keyword_data]

#%% Prep for classification - select features, scale, impute, split into train and test

#remove rows with prediction variable values that aren't of interest
all_data = all_data[~all_data.overall_status.isin(['Recruiting', 'Unknown status', 'Active, not recruiting', 'Not yet recruiting','Other'])]; #remove ongoing trials -only want complete and ended trials (terminated, withdrawn, suspended, witheld, no longer available )

#print remaining values to make sure only includes the ones we want
print (all_data.overall_status.value_counts(normalize=True))
min_accuracy = round(all_data.overall_status.value_counts(normalize=True)[0]*100)

#separate independent and dependent variables
x = all_data.loc[:, all_data.columns != 'overall_status']
y = all_data['overall_status']=='Completed' #what I'm trying to predict (trials that completed vs didn't)

#remove columns not using
x = x.drop(['completion_date', 'start_date', 'days_to_completion'], axis=1) #these would definitely be cheating to use

#convert category data to dummy coded variables
category_cols = ['eligibility/gender', 'eligibility/healthy_volunteers', 'phase', 'study_design_info/primary_purpose', 'study_type', 'sponsors/lead_sponsor/agency_class']

for cat in category_cols:
    for elem in all_data[cat].unique():
        x[(str(cat) + '-' + str(elem))] = x[cat] == elem
    x = x.drop(cat, axis=1)


#save feature list
features = x.columns.to_list()

# scale features if numeric
num_cols = ['start_year','eligibility/maximum_age', 'eligibility/minimum_age', 'enrollment']
scaler = StandardScaler()
x[num_cols] = scaler.fit_transform(x[num_cols])

#drop incompletes - commented out, instead we're going to impute the missing values
#all_data.dropna(axis = 0, how = 'any', inplace = True)

#impute missing data (instead of deleting incomplete cases)
x = SimpleImputer(missing_values=np.nan, strategy='mean').fit_transform(x)

# split data into train and test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

#remove extra variables to save memory
del [all_data, x, y, cat, category_cols, elem, num_cols]

### Now we're ready to try some different algorithms

#%% Train and Test K-Nearest Neighbors (KNN)

#Train
knn_fit = KNeighborsClassifier(n_neighbors = 5).fit(x_train, y_train)

# Test
knn_accuracy =  np.round(knn_fit.score(x_test, y_test)*100)
print(knn_accuracy) #86%

if knn_accuracy <= min_accuracy: #save space by deleting non useful models
    del [knn_fit]


#%% Train and Test Logistic regression with cross validation 

#Train
log_cv_fit = LogisticRegressionCV(max_iter=5000).fit(x_train, y_train)

#Test
log_cv_accuracy = np.round(log_cv_fit.score(x_test, y_test)*100)
print(log_cv_accuracy) #87%

if log_cv_accuracy <= min_accuracy: #save space by deleting non useful models
    del [log_cv_fit]

#%% Train and Test Support Vector Machine (SVM)

#commented out as it stalls out - try again with ugdates RAM

#Train
#svm_fit = svm.SVC().fit(x_train, y_train)
#
##Test
#svm_accuracy = np.round(svm_fit.score(x_test, y_test)*100)
#print(svm_accuracy)
#
#if svm_accuracy <= min_accuracy: #save space by deleting non useful models
#    del [svm_fit]

#%% Train and Test Classification and Regression Tree (CART)

#Train
tree_fit = DecisionTreeClassifier().fit(x_train, y_train)

#Test
tree_accuracy = np.round(tree_fit.score(x_test, y_test)*100)
print(tree_accuracy) #86%

if tree_accuracy <= min_accuracy: #save space by deleting non useful models
    del [tree_fit]

#%% Train and Test Random Forest

#Train
forest_fit = ensemble.RandomForestClassifier().fit(x_train, y_train)

#Test
forest_accuracy = np.round(forest_fit.score(x_test, y_test)*100)
print(forest_accuracy) #91%

if forest_accuracy <= min_accuracy: #save space by deleting non useful models
    del [forest_fit]
    
#%% Train and Test multi-layer perceptron (MLP) 

#Train
mlp_fit = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1).fit(x_train, y_train)

#Test
mlp_accuracy =np.round(mlp_fit.score(x_test, y_test)*100)
print(mlp_accuracy) #86%

if mlp_accuracy <= min_accuracy: #save space by deleting non useful models
    del [mlp_fit]
    
#%% Train and Test Gradient Boosted Decision Tree

#Train
GB_fit = ensemble.GradientBoostingClassifier().fit(x_train, y_train)

#Test
GB_accuracy = np.round(GB_fit.score(x_test, y_test)*100)
print(GB_accuracy) #92% - highest so keeping it

if GB_accuracy <= min_accuracy: #save space by deleting non useful models
    del [GB_fit]

#%% Examine features in best model

GB_features =  pd.Series(GB_fit.feature_importances_, index=features)
GB_features.sort_values(ascending=False)[0:5]
#primarily driven by enrollment, which is updated as the study goes 
#so enrollment not really a fair predictor, wouldn't apply to new trials


#%% Train and Test Gradient Boosted Decision Tree without Enrollment feature

#remove enrollment feature
x_train2 = np.delete(x_train, features.index('enrollment'), axis=1)
x_test2 = np.delete(x_test, features.index('enrollment'), axis=1)
features2 =  [x for x in features if x != 'enrollment']

#Train
GB_fit2 = ensemble.GradientBoostingClassifier().fit(x_train2, y_train)

#Test
GB_accuracy2 = np.round(GB_fit2.score(x_test2, y_test)*100)
print (GB_accuracy2) #87% - model no longer works without enrollment


GB_features2 =  pd.Series(GB_fit2.feature_importances_, index=features2)
GB_features2.sort_values(ascending=False)[0:5]



