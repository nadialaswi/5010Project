'''
DS5010 Final Project
url_grabber: Pulls all urls from epa website into .txt file
'''
# importing libraries
import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_soup():
    '''
    Purpose: Employs bs4 and requests libraries to get epa website into parsed
    text file containing all information, from which links will be pulled
    Paramaters: None.
    Returns: soup, containign text html file of epa website
    '''
    # retry defensive coding in case requests fails to access epa website on 1st try
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # defining url where data is and using requests to access page
    epa_url = 'https://aqs.epa.gov/aqsweb/airdata/download_files.html'
    url_prefix = 'https://aqs.epa.gov/aqsweb/airdata/'
    req = session.get(epa_url)
    soup = BeautifulSoup(req.text, 'html.parser')

    return soup

def url_cleaner(line):
    '''
    Purpose: Uses regex to remove unncessary characters from HTML urls pulled
    from the epa website we are accessing
    Parameters: line: the line being cleaned that contains HTML-formatted urls
    Returns: A list, with True, indicating the output is a url we want to save,
    and output, which is the url we want to save. Otherwise, False, and NA,
    indicating we do not save whatever the current input was.
    '''
    regex_between_quotes = r'"([^"]*)"'
    regex_only_zip = r'.*\.zip.*'
    regex_contains_numbers = r'\d+'
    if bool(re.match(regex_only_zip, line)) and \
        bool(re.search(regex_contains_numbers, line)):
            output = re.findall(regex_between_quotes, line)[0]
            return [True, output]
    else:
        return [False, "NA"]
    
def get_library_clean():
    '''
    Purpose: Saves url_library_clean to local directory for access by other
    py files in this package. This is essentially the main func for this py file
    Parameters: none
    Returns: name of library txt file that has been generated when the func
    is called
    '''
    # setting up file_name to write urls to
    url_library_txt_unclean = "url_library_unclean.txt"
    url_library_clean_txt = "url_library_clean.txt"

    # pulling all possible links from url, using 'a' HTML tag and href = True
    with open(url_library_txt_unclean, "w") as url_library_append:
        for link in get_soup().find_all('a', href =True):
            url_library_append.write(str(link) + "\n") # writing links to .txt

    with open(url_library_txt_unclean, "r") as url_library_read:
        lines = url_library_read.readlines()
        
    # clean through url_library to leave only relevant .zip files
    with open(url_library_clean_txt, "w") as url_library_clean:
        for line in lines:
            if url_cleaner(line)[0] is True:
                cleaned_line = url_cleaner(line)[1] + "\n"
                url_library_clean.write(cleaned_line) # writing to the cleaned txt file

    return url_library_clean_txt







        
