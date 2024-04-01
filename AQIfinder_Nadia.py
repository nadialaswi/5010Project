#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[101]:


df = pd.read_csv('daily_aqi_by_cbsa_2023.csv')

new = (df['CBSA Code'] == '2023-01-02')
df['CBSA Code'].drop_duplicates()

# Only 488 zip codes in this file. 41,000 across USA


# In[92]:



def aqi_finder(file: str, date, zip_code):
    '''
    Finds air quality index in an area on a given day
    Inputs: .csv file from aqs.epa.gov (str), date as YYYY-MM-DD (str), 5-digit zip code (int)   
    Returns: str
    '''
    df = pd.read_csv(file)
    # Find rows where date and zip code match
    chosen_date = df['Date'] == date
    chosen_zip = df['CBSA Code'] == zip_code
    
    # If date/zip not found
    if not chosen_date.any():
        return f'Sorry, {date} is not recorded in this file.'
    elif not chosen_zip.any():
        return f'Sorry, {zip_code} is not recorded in this file.'
    
    # Update dataframe with conditions
    df = df[chosen_date & chosen_zip]
    # Values of interest:
    aqi = df['AQI'].values
    condition = df['Category'].values
    
    return f'The AQI in {zip_code} on {date} was {aqi}, meaning the air quality was {condition}.'
        


# In[97]:


file1 = 'daily_aqi_by_cbsa_2023.csv'
date1 = '2023-01-19'
zip_code1 = 10100


# In[98]:


aqi_finder(file1, date1, zip_code1)


# In[ ]:




