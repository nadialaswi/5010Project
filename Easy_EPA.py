'''
user_interface: The front end driver for the user.
Allows the user to dictate which information they want to work with
'''
from url_storage import *
from backend_functions import * 
import re
import datetime

# storage is static gloabl variable holding csv file information
STORAGE = get_storage()

# List of variables
VARIABLE_LIST = ["aqi, temperature, wind, criteria gases"]

# List of valid US states
US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

# Regular expression pattern to match valid date in YYYY-MM-DD format
DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}$'

def is_valid_date(date):
    '''
    '''
    # First check that date is valid format string
    if not re.match(DATE_PATTERN, date):
        print('Invalid date format!')
        return False
    
    # Next check date is valid calendar date
    year, month, day = map(int, date.split('-'))
    try:
        # Attempt to create a datetime object from the input date
        newDate = datetime.datetime(year,month,day)
        return True
    except ValueError:
        print("Invalid calendar date!")
        return False

def is_valid_state(state_name):
    if state_name.strip().title() in US_STATES:
        return True
    else:
        return False

def get_variable_year_range(variable, period):
    filtered_df = STORAGE.loc[STORAGE['variable'].str.contains(variable)]
    filtered_df = filtered_df.loc[filtered_df['period'].str.contains(period)]

    year_min = filtered_df['year'].min()
    year_max = filtered_df['year'].max()
    return [year_min, year_max]

def get_multiple_variable_year_range(variable1, variable2, variable3, period):
    list = [variable1, variable2, variable3]
    min_max = []
    for each in list:
        min_max.append(get_variable_year_range(each, period))
    
    mins = [row[0] for row in min_max]
    maxes = [row[1] for row in min_max]
    
    final_min = max(mins)
    final_max = min(maxes)

    return [final_min, final_max]

def is_valid_year1(variable, period, year_input):
    [year_min, year_max] = get_variable_year_range(variable, period)

    if year_min <= year_input and year_input <= year_max:
        return True
    else:
        print('Year is not in range!')
        print(f"The range of years for this variable is {year_min} to {year_max}")
        return False
    
def is_valid_year2(year_min, year_max, year_input):
    if year_min <= year_input and year_input <= year_max:
        return True
    else:
        print('Year is not in range!')
        print(f"The range of years for this variable is {year_min} to {year_max}")
        return False

def daily_finder_variable_select():
    CHOICES = ['Temperature', 'AQI', 'Wind']
    valid_choice = False

    while valid_choice == False:
        choice = input("Pick a variable (Temperature: 1, AQI: 2, Wind: 3): ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice! Please enter 1, 2, or 3.")
        else:
            if choice == '1':
                # Code for working with Temperature
                print("You chose Temperature.")
                return 'Temperature'
            elif choice == '2':
                # Code for working with CO2
                print("You chose AQI.")
                return 'AQI'
            elif choice == '3':
                # Code for working with AQI
                print("You chose Wind.")
                return 'Wind'

def yearly_finder_variable_select():
    CHOICES = ['Temperature', 'AQI']
    valid_choice = False

    while valid_choice == False:
        choice = input("Pick a variable (Temperature: 1, AQI: 2): ")
        if choice not in ['1', '2']:
            print("Invalid choice! Please enter 1, or 2")
        else:
            if choice == '1':
                # Code for working with Temperature
                print("You chose Temperature.")
                return 'Temperature'
            elif choice == '2':
                # Code for working with CO2
                print("You chose AQI.")
                return 'AQI'

def yearly_plot_variable_select():
    CHOICES = ['Temperature', 'AQI', 'Criteria Gases']
    valid_choice = False

    while valid_choice == False:
        choice = input("Pick a variable (Temperature: 1, AQI: 2, Criteria Gases: 3): ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice! Please enter 1, 2 or 3")
        else:
            if choice == '1':
                # Code for working with Temperature
                print("You chose Temperature.")
                return 'Temperature'
            elif choice == '2':
                # Code for working with AQI
                print("You chose AQI.")
                return 'AQI'
            elif choice == '3':
                # Code for working with Criteria Gases
                print("You chose Criteria Gases (Ozone, SO2, NO2, and CO).")
                return 'Criteria Gases'

def extract_year(date_str):
    # Extract the first four integers from the date string
    match = re.match(r'^\d{4}', date_str)
    if match:
        return match.group()
    else:
        return None

def get_state():
    print("Input a state name to analyze")
    print(US_STATES)
    valid_state = False
    while valid_state is False:
        state_name = input("Enter a state name: ").title()
        valid_state = is_valid_state(state_name)
    
    return state_name

def daily_finder_selected():
    '''
    Used in menu_driver for when user selects finder option
    
    '''
    # Implementation for daily_finder removed. Replaced with daily summary

    period = 'daily'
    print("You selected daily finder")
    # get variable
    variable = daily_finder_variable_select()
    # get year range
    year_range = get_variable_year_range(variable, period)

    print(f"The range of years for this variable is {year_range[0]} to {year_range[1]}")

    # check user inputs valid year and date
    valid_date_format = False
    valid_year = False
    while valid_date_format is False or valid_year is False:
        date = input("Input a date as YYYY-MM-DD: ")
        valid_date_format = is_valid_date(date)
        year = extract_year(date)
        valid_year = is_valid_year1(variable, period, year)

    # getting state name input
    print('Valid Date selected!')
    
    state_name = get_state()

    file = download_driver(STORAGE, variable, year, period)
    current_working_directory = os.getcwd()
    folder_path = current_working_directory + "/csv_folder/" + file
    print(folder_path)
    
    if variable == 'Wind':
        wind_daily_finder(folder_path, date, state_name)

    if variable == 'Temperature':
        temp_daily_finder(folder_path, date, state_name)
    
    if variable == 'AQI':
        aqi_daily_finder(folder_path, date, state_name)


def path_builder(file):
    current_working_directory = os.getcwd()
    folder_path = current_working_directory + "/csv_folder/" + file
    return folder_path

def daily_summary_selected():
    '''
    Drives when the user selects the daily summary action
    '''
    period = 'daily'

    # Current implementation of daily summary only supports Wind, AQI, and Temp
    wind_var = 'Wind'
    aqi_var = 'AQI'
    temp_var = 'Temperature'

    print(f"You selected Daily Summary! Summarizing {wind_var}, {aqi_var}, and {temp_var}!")
          
    # get year range
    year_range = get_multiple_variable_year_range(wind_var, aqi_var, temp_var, period)

    print(f"The range of years for the Daily Summary is {year_range[0]} to {year_range[1]}")

    # check user inputs valid year and date
    valid_date_format = False
    valid_year = False
    while valid_date_format is False or valid_year is False:
        date = input("Input a date as YYYY-MM-DD: ")
        valid_date_format = is_valid_date(date)
        year = extract_year(date)
        valid_year = is_valid_year2(year_range[0], year_range[1], year)

    # getting state name input
    print('Valid Date selected!')
    
    state_name = get_state()

    file1 = download_driver(STORAGE, wind_var, year, period)
    file1_path = path_builder(file1)

    file2 = download_driver(STORAGE, aqi_var, year, period)
    file2_path = path_builder(file2)
    
    file3 = download_driver(STORAGE, temp_var, year, period)
    file3_path = path_builder(file3)

    daily_summary(file1_path, file2_path, file3_path, date, state_name)

def yearly_finder_selected():
    period = 'daily'
    print("You selected 'Yearly Finder. Find the temperature in a State for a given year.")

    # get variable
    variable = yearly_finder_variable_select()
    # get year range
    year_range = get_variable_year_range(variable, period)

    print(f"The range of years for this variable is {year_range[0]} to {year_range[1]}")

    # check user inputs valid year and date
    valid_year = False
    while valid_year is False:
        year = input("Input a date as YYYY: ")
        valid_year = is_valid_year1(variable, period, year)

    # getting state name input
    print('Valid Date selected!')
    
    state_name = get_state()

    file = download_driver(STORAGE, variable, year, period)
    current_working_directory = os.getcwd()
    folder_path = current_working_directory + "/csv_folder/" + file
    print(folder_path)
    
    if variable == 'Temperature':
        temp_yearly_finder(folder_path, year, state_name)
   
    elif variable == 'AQI':
       aqi_yearly_finder(folder_path, year, state_name)

def plot_selected(type):

    period = 'daily'
    if type == 'plot':
        print("You selected Yearly Plot.")

        # get variable
        variable =  yearly_plot_variable_select()
    
        year = input("Input a year as YYYY: ")
        
        state_name = get_state()

        if variable == 'Criteria Gases':
            file1 = download_driver(STORAGE, 'Ozone', year, period)
            file1_path = path_builder(file1)

            file2 = download_driver(STORAGE, 'CO', year, period)
            file2_path = path_builder(file2)
            
            file3 = download_driver(STORAGE, 'SO2', year, period)
            file3_path = path_builder(file3)

            file4 = download_driver(STORAGE, 'NO2', year, period)
            file4_path = path_builder(file4)

            criteria_gases_plot(file1_path, file2_path, file3_path, file4_path, year, state_name)

        else:
            file = download_driver(STORAGE, variable, year, period)
            current_working_directory = os.getcwd()
            folder_path = current_working_directory + "/csv_folder/" + file
            print(folder_path)
            
            if variable == 'Temperature':
                temp_yearly_plot(folder_path, year, state_name)
        
            elif variable == 'AQI':
                aqi_yearly_plot(folder_path, year, state_name)
    if type == 'state':
        print("You selected State comparison plot.")

        # get variable
        variable =  yearly_plot_variable_select()
    
        year = input("Input a year as YYYY: ")
        
        state_name = get_state()

        if variable == 'Criteria Gases':
            file1 = download_driver(STORAGE, 'Ozone', year, period)
            file1_path = path_builder(file1)

            file2 = download_driver(STORAGE, 'CO', year, period)
            file2_path = path_builder(file2)
            
            file3 = download_driver(STORAGE, 'SO2', year, period)
            file3_path = path_builder(file3)

            file4 = download_driver(STORAGE, 'NO2', year, period)
            file4_path = path_builder(file4)

            criteria_gases_plot(file1_path, file2_path, file3_path, file4_path, year, state_name)

        else:
            file = download_driver(STORAGE, variable, year, period)
            current_working_directory = os.getcwd()
            folder_path = current_working_directory + "/csv_folder/" + file
            print(folder_path)
            
            if variable == 'Temperature':
                temp_yearly_plot(folder_path, year, state_name)
        
            elif variable == 'AQI':
                aqi_yearly_plot(folder_path, year, state_name)



def menu_select():
    select = None 
    while select not in ['D','F','P','S','Q','R']:
        print("Welcome to the main menu. Input a letter to explore the"
              "United States Environmental Protection Agency's meteorological data. \n"
              "Input Options: \n"
              "D: Obtain the daily summary of Temperature, Wind, and Air Quality Index (AQI) for a designated date and State. \n"
              "Y: Retrieve a summary of Temperature or Air Quality Index (AQI) for a particular State for a specified year. \n"
              "P: Retrieve a Plot of Temperature, Air Quality Index (AQI), or Pollutant Gases for a particular State for a specified year. \n"
              "S: Compare States via plot for either Temperature or Air Quality Index (AQI) for a specified year. \n" 
              "Q: Quit out.\n"
              "R: Type R at anytime to return to the main menu.")

        select = input(" ").capitalize()
    return select

def menu_driver():

    option = None
    while option != 'Q':
        option = menu_select()
        if option  == 'D':
            daily_summary_selected()
        if option == 'Y':
            yearly_finder_selected()
        if option == 'P':
            plot_selected('plot')
        if option == 'S':
            plot_selected('state')

def main():
    menu_driver()

if __name__ == "__main__":
    main()
