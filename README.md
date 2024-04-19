README for EASY EPA: A meteorological file management and data retrieval system.


Easy EPA offers quick retrieval of csv files based on user input, along with easily accessible summarizations and plots via a menu selection.


webscraper.py identifies downloadable zip files by parsing the HTML files on https://aqs.epa.gov/aqsweb/airdata/download_files.html. Relevant URLs are saved to your working directory in the text file "url_library.txt."


url_storage.py retrieves and unpacks zip files into csv_folder as csv files. csv_folder is generated for the user in the current working directory. These csv_files are sent to the backend analysis function for analysis and plotting.


backend_functions.py utilizes pandas and matplotlib to offer summarization and plotting of the data based on year, state, and input variable, dictated by the user via the frontend, Easy_EPA.py.


Easy_EPA.py packages the module together via a menu selection service that allows the user to get quick summaries of data based on a meteorological variable, date, year, or state name.

test_functions.jpynb uses jupyter notebooks to demonstrate validation of functions via testing with easy readability. 