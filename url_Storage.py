'''
DS5010 Final Project
Converts url txt file to dataframe "storage" that holds all relevant info
from epa website
'''
import pandas as pd
import requests
import os
from url_Grabber import *
import zipfile
import shutil

# defining global static variables

URL_PREFIX = 'https://aqs.epa.gov/aqsweb/airdata/'

# https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_2023.zip

def get_storage():
    '''
    Purpose: generate the url_storage dataframe that holds info for all urls
    Parameters: none, this is the driving file, no inputs needed
    Returns: generates the storage dataframe 
    '''
    # creating empty lists to build from url_library
    url_list = []
    period_list = []
    year_list = []
    variable_list = []
    csv_file_name_list = []
    zip_file_name_list = []

    '''
    url_list: list containing urls to directly download the files
    period_list: list containing "periods" of each zip fil(e, hourly/daily etc
    year_list: year of data acquisition for each file
    variable_list: meteorlogical information held in file
    csv_file_name_list: the name of the actual csv file pandas will be working with
    '''

    # building the lists that will make up df columns
    with open(get_library_clean(), "r") as url_library_read:
        lines = url_library_read.readlines()
        for line in lines:
            line = line.strip() # removing new line
            url_list.append(URL_PREFIX + line) # building url_list 
            
            zip_file_name_list.append(line)
            line = line.replace(".zip","") # now removing .zip from working line

            csv_file_name_list.append(line + ".csv") # building csv name list

            line_split = line.split("_") #splitting on  _ delimiter 
            
            period_list.append(line_split[0]) # period is the first value on line
            line_split.pop(0) # remove period
            
            year_list.append(line_split[-1]) # year is the last value on line 
            line_split.pop(-1) # remove year
            variable_list.append(line_split[0]) # variable is remaining value on line
            
    # storage is the dataframe that holds all the relevant info for access
    accessed_list = [False] * len(url_list) # default this list to 0, urls have not been accessed
    storage = pd.DataFrame({'csv_file_name':csv_file_name_list,
                            'variable':variable_list, 
                            'period':period_list, 
                            'year':year_list, 
                            'zip_file_name':zip_file_name_list,
                            'url':url_list,
                            'accessed': accessed_list
                            })
             
    return storage

# index map:
# csv_file_name: 0
# variable: 1
# period: 2
# year: 3
# zip_file_name 4
# url: 5
# accessed: 6

def clear_csv_folder():
    '''
    Deletes csv_folder
    '''
    folder_name = "csv_folder"
    current_working_directory = os.getcwd()
    folder_path = os.path.join(current_working_directory, folder_name)
    shutil.rmtree(folder_path)
    return


def check_for_csv_folder():
    '''
    Purpose: checks if csv folder exist.
    if not, generates a folder to store all the csv files for the user
    Parameters: none
    Returns: path of csv_folder, generates csv_folder if it doesn't exist
    '''
    
    folder_name = "csv_folder"
    current_working_directory = os.getcwd()
    folder_path = os.path.join(current_working_directory, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print("'csv_folder' exists within your current directory")
    else:
        print("csv_folder' does not exist within your current directory'")
        print("Generating 'csv_folder' for you...")
        os.makedirs(folder_name)
    
    return(folder_path)

def update_accessed_list(storage, csv_file_name, updater_boolean):
    '''
    Purpose: update storage df for when a file is downloaded. Changes 'accessed'
    row for input file name from 0 to 1
    Paramaters: storage, the url/csv dataframe being edited
    csv_file_name: the row being edited 
    updater_boolean: updates if csv file is downloaded or not 
    Returns: updated storage dataframe
    '''
    row_index = storage.index[storage['csv_file_name']==csv_file_name][0]
    accessed_index = storage.columns.get_loc("accessed")
    storage.iat[row_index, accessed_index] = updater_boolean
 
    return storage

def download_and_extract_zip(url, zip_file_name, csv_folder):
    '''
    Gets the zip file from the url website based on url input, unzips, and puts
    into the csv_folder for data analysis.
    Parameters: url: the epa url that has the zip file to be downloaded
    zip_file_name: the name of the zip file
    csv_folder, the location where the csv file will be extracted to
    Returns None, but will extract zip file to csv folder
    '''
    response = requests.get(url)
    if response.status_code == 200:
        with open(zip_file_name, 'wb') as zip_file:
            zip_file.write(response.content)
        print(f"File downloaded successfully and saved as '{zip_file_name}'")

        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(csv_folder)
        print(f"Contents extracted to '{csv_folder}'")
    else:
        print("Failed to download the zip file.")
    return
        
def download_driver(storage, csv_file_name):
    '''
    Purpose: downloads csv file based on storage dataframe's row
    Parameters: csv_file_name, the name of the csv_file, also used as storage's row index
    Returns: Updated version of storage.
    This function also downloads csv file to csv folder if it has 
    not been downloaded during this session
    '''
    csv_folder_path = check_for_csv_folder()
    csv_file_path = os.path.join(csv_folder_path, csv_file_name)
    row_index = storage.index[storage['csv_file_name']==csv_file_name][0]
    accessed_index = storage.columns.get_loc("accessed")

    if os.path.exists(csv_file_path) and storage.iat[row_index, accessed_index] is True:
        print('This csv file is already downloaded')
        return
    else: 
        url = storage.iat[row_index, storage.columns.get_loc('url')]
        zip_file_name = storage.iat[row_index, storage.columns.get_loc('zip_file_name')]
        download_and_extract_zip(url, zip_file_name,csv_folder_path)
        storage = update_accessed_list(storage, csv_file_name, True)
        return storage

# def main():
#     #clear_csv_folder()
#     store = get_storage()
#     print(store.head(1))
#     # csv_file_name at index 0: annual_conc_by_monitor_2023.csv  
#     store = download_driver(store, 'annual_conc_by_monitor_2023.csv')
#     print(store.head(1))

# if __name__ == "__main__":
#     main()

