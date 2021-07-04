# -*- coding: utf-8 -*-
"""
Description:
    Trying to predict how long it took for a clinical trial to be completed
    Not using keyword data yet as text processing takes a lot more effort

Created on Fri Jul  2 18:51:27 2021
@author: lauren koenig
"""

#%% Set up
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn import tree
from sklearn import neural_network
from sklearn import ensemble


all_data = pd.read_csv('data-clean/all_data_clean.csv', parse_dates=['completion_date', 'start_date'])

#%% Prep for regression - select features, scale, impute, split into train and test

#remove rows with prediction variable values that aren't of interest
all_data = all_data[all_data.overall_status=='Completed']; #remove incomplete/ongoing trials - doesn't make sense for what we're trying to predict 

#remove extreme days to completion
y_outliers = all_data['days_to_completion'].mean() + 3*all_data['days_to_completion'].std()
all_data = all_data[all_data['days_to_completion']<y_outliers]

#print remaining values to make sure only includes the ones we want
print (all_data.overall_status.value_counts(normalize=True))
print (all_data.days_to_completion.describe())

#separate independent and dependent variables
x = all_data.loc[:, all_data.columns != 'days_to_completion']
y = all_data["days_to_completion"] #what I'm trying to predict (days to completion)

#remove columns not using
x = x.drop(['completion_date', 'start_date', 'overall_status'], axis=1)

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
x_noImpution = x
x = SimpleImputer(missing_values=np.nan, strategy='mean').fit_transform(x)

# split data into train and test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

#remove extra variables to save memory
del [all_data, x, y]

### Now we're ready to try some different algorithms

#%% LASSO Regression

#Train
lasso_fit = Lasso(alpha=0.001, max_iter=50000).fit(x_train, y_train)

#Test
lasso_rmse = np.round(np.sqrt(mean_squared_error(y_test, lasso_fit.predict(x_test))))
print(lasso_rmse)  #643
print (np.round(lasso_fit.score(x_test, y_test), decimals = 2 )*100) #26%

del [lasso_fit]

#%% Support Vector Machine 

#commented out as it currently causes computer to freeze
##Train
#svr_fit = SVR(C=8, epsilon=0.2, gamma=0.5).fit(x_train, y_train)
#
##Test
#svr_rmse = np.round(np.sqrt(mean_squared_error(y_test, svr_fit.predict(x_test))))
#print(svr_rmse)
#print (np.round(svr_fit.score(x_test, y_test), decimals = 2 )*100)
#
#del [svr_fit]

#%% KNN Regression

#Train
knn_fit = KNeighborsRegressor().fit(x_train, y_train)

#Test
knn_rmse = np.round(np.sqrt(mean_squared_error(y_test, knn_fit.predict(x_test))))
print(knn_rmse)  #651
print (np.round(knn_fit.score(x_test, y_test), decimals = 2 )*100) #24%

del [knn_fit]

#%% Tree Regression

#Train
tree_fit = tree.DecisionTreeRegressor().fit(x_train, y_train)

#Test
tree_rmse = np.round(np.sqrt(mean_squared_error(y_test, tree_fit.predict(x_test))))
print(tree_rmse)  #835
print (np.round(tree_fit.score(x_test, y_test), decimals = 2 )*100) #-27% - negative means it's worse than a horizontal line

del [tree_fit]



#%% MLP Regression

#Train
mlp_fit = neural_network.MLPRegressor(max_iter = 1000).fit(x_train, y_train)

#Test
mlp_rmse = np.round(np.sqrt(mean_squared_error(y_test, mlp_fit.predict(x_test))))
print(mlp_rmse) #618
print (np.round(mlp_fit.score(x_test, y_test), decimals = 2 )*100) #31%

del [mlp_fit] 

#%% Random Forest Regression

#Train
forest_fit = ensemble.RandomForestRegressor().fit(x_train, y_train)

#Test
forest_rmse = np.round(np.sqrt(mean_squared_error(y_test, forest_fit.predict(x_test))))
print(forest_rmse) #657
print (np.round(forest_fit.score(x_test, y_test), decimals = 2 )*100) #22%

del [forest_fit]

#%% Gradient Boosting Regression

#Train
GB_fit = ensemble.GradientBoostingRegressor().fit(x_train, y_train)

#Test
GB_rmse = np.round(np.sqrt(mean_squared_error(y_test, GB_fit.predict(x_test))))
print(GB_rmse) #611
print (np.round(GB_fit.score(x_test, y_test), decimals = 2 )*100) #33%

GB_features =  pd.Series(GB_fit.feature_importances_, index=features)
GB_features.sort_values(ascending=False)[0:5]





