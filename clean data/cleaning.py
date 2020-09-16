# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:00:37 2020

@author: Ricardo 
"""
#The main idea is to clean all the data

import pandas as pd
import numpy as np

#create a data frame with the data from UCR salaries information

df = pd.read_csv('planilla-2020-08.csv', sep =';')

#%% Craeting Functions to then apply them in a pipe

def drop_this (DataFrame, list): #this function will help you drops columns you don't need
    try:
        DataFrame2 = DataFrame.drop(columns = list)
        print('Elements dropped')
        print(list)
        return DataFrame2
    except KeyError:
        print('This name is not in the DataFrame')
                
def change_columns(DataFrame, list): #this function renames ALL the columns in the data frame using a list 
    try: 
        DataFrame.columns = list
        return DataFrame
    except Exception as e:
        print(e)
        
#%%% Let's clean what we don't need


#view the date frame 

print(df.head())
#-> we see we dont need the column MES COMPLETO so we put in the next list.
column_to_drop= ['MES COMPLETO']

#view the name of each column

print(df.columns)
#-> we can see the names and how can we rename them so we put the new names in a list.
new_column_names=['position',
   'salary',
   'hours',
   'years',
   'type_job']

#apply pipe

df = (df.pipe(drop_this, column_to_drop)
 .pipe(change_columns, new_column_names)
)

df['salary_millions'] = df.salary/1000000 #salary in millions of colones

#%%% Let's fix what we need

#Hours_range

hours_bins = [0, 0.125, 0.25,0.375, 0.50, 0.625, 0.75, 0.875, 1.]
hours_label = ['1/8  of time', 
               '1/4 of  time',
               '3/8 of time', 
               'Part Time',
               '5/8 of time', 
               '3/4 of time',
               '7/8 of time',
               'Full time']

df.hours = pd.cut(df['hours'], hours_bins, labels = hours_label)

#Salary_per_hour. 
""" The main idea is create a column with the value of the hour of work for everyone so it's easier to compare how much everyone earns """

#asume that in  1 month there is 4.34524 weeks

df['Salary_per_hour'] = df.salary/4.34524
df.loc[df['hours']=='Full time', 'Salary_per_hour'] = df.Salary_per_hour/40 
df.loc[df['hours']=='7/8 of time', 'Salary_per_hour'] = df.Salary_per_hour/(40*7/8) 
df.loc[df['hours']=='3/4 of time', 'Salary_per_hour'] = df.Salary_per_hour/(40*6/8)
df.loc[df['hours']=='5/8 of time', 'Salary_per_hour'] = df.Salary_per_hour/(40*5/8) 
df.loc[df['hours']=='Part Time', 'Salary_per_hour'] = df.Salary_per_hour/(40*4/8)
df.loc[df['hours']=='3/8 of time', 'Salary_per_hour'] = df.Salary_per_hour/(40*3/8)
df.loc[df['hours']=='1/4 of  time', 'Salary_per_hour'] = df.Salary_per_hour/(40*2/8)
df.loc[df['hours']=='1/8  of time', 'Salary_per_hour'] = df.Salary_per_hour/(40*1/8)

#years_range

year_bins = [-np.inf,10, 20, 30, 40 ,50, np.inf]
df['year_cut_in_10'] = pd.cut(df['years'], year_bins)

#drop missing values

df = df.dropna()

#%%% add a date for the data fram for future comparison

df['date'] = '2020-08-01'

#%% import

df.to_csv('planilla_clean.csv', index = False)

#%% understand the new data 

#FIX the position data so we can understan better each teaching postiton

df.loc[df['position'].str.contains('VISITANTE'), 'position'] = 'PROFESOR VISITANTE'
df.loc[df['position'].str.contains('INVITADO|INV.'), 'position'] = 'PROFESOR VISITANTE'
df.loc[df['position'].str.contains('EXBECARIO | POSDOCTORADO'), 'position'] = 'PROFESOR EXBECARIO'
df.loc[df['position'].str.contains('EDUCACION SUPERIOR'), 'position'] = 'PROFESOR EDUCACION SUPERIOR'
df.loc[df['position'].str.contains('EDUCACION SUPERIOR'), 'position'] = 'PROFESOR EDUCACION SUPERIOR'
df.loc[df['position'].str.contains('CATEDRATICO'), 'position'] = 'PROFESOR CATEDRATICO'
df.loc[df['position'].str.contains('CATEDRATICO'), 'position'] = 'PROFESOR CATEDRATICO'

#%% import new data fram that only containts the teachers data

planilla_profesores = df.loc[df['position'].str.contains('PROFESOR')]
planilla_profesores = planilla_profesores.reset_index(drop = True)
planilla_profesores.to_csv('planilla_profesores .csv', index = False)

#%%% split the data frame bewtweentheacher and non-teachers

glue = df
glue.loc[~glue['type_job'].str.contains('PUESTO NO'), 'type_job'] = 'ADMINISTRATIVO'

#%% import dichotomy

glue.to_csv('dichotomy_planilla.csv', index = False)

