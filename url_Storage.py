import pandas as pd
text = "url_library_clean.txt"

url_list = [] # column containing urls to directly download the files
period_list = [] #column containing "periods" of each zip file, hourly/daily etc
year_list = []
variable_list = []
url_prefix = 'https://aqs.epa.gov/aqsweb/airdata/'


# building the lists that will make up df columns
with open(text, "r") as url_library_read:
    lines = url_library_read.readlines()
    for line in lines:
        line = line.strip() # removing new line
        url_list.append(url_prefix + line) # building url_list 
        line = line.replace(".zip","") # now removing .zip from working line
        
        line_split = line.split("_") #splitting on  _ delimiter 
        period_list.append(line_split[0]) # period is the first value on line
        line_split.pop(0) # remove period
        year_list.append(line_split[-1]) # year is the last value on line 
        line_split.pop(-1) # remove year
        variable_list.append(line_split[0]) # variable is remaining value on line

# storage is the dataframe that holds all the relevant info for access
storage = pd.DataFrame({'variable':variable_list, 'period':period_list, 'year':year_list, 'url':url_list})
     

        
        
    

