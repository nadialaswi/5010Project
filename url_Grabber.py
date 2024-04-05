import requests
import os
from bs4 import BeautifulSoup
import re
import urllib

KEYWORDS = []

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
# req = requests.get(epa_url)
soup = BeautifulSoup(req.text, 'html.parser')

# setting up file_name to write urls to
url_library = "url_library.txt"

# pulling all possible links from url, using 'a' HTML tag and href = True
with open(url_library, "w") as url_library_append:
    for link in soup.find_all('a', href =True):
        url_library_append.write(str(link) + "\n") # writing links to .txt

with open(url_library, "r") as url_library_read:
    lines = url_library_read.readlines()

def url_cleaner(line):
    regex_between_quotes = r'"([^"]*)"'
    regex_only_zip = r'.*\.zip.*'
    regex_contains_numbers = r'\d+'
    if bool(re.match(regex_only_zip, line)) and \
        bool(re.search(regex_contains_numbers, line)):
            output = re.findall(regex_between_quotes, line)[0]
            return [True, output]
    else:
        return [False, "NA"]
    
# clean through url_library to leave only relevant .zip files
with open("url_library_clean.txt", "w") as url_library_clean:
    for line in lines:
        if url_cleaner(line)[0] is True:
            cleaned_line = url_cleaner(line)[1] + "\n"
            url_library_clean.write(cleaned_line)

    





        
