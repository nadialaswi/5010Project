'''
DS5010 Final Project
Input validation is neccessary for validating the many user functions that drive the menu selection process for Easy_EPA
'''
from url_storage import *
import datetime
import re
# get global variable STORAGE
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

# List of US states by abbreviations
STATE_ABBREVIATIONS = [
    "AL", "AK", "AZ", "AR", "CA", "CO",
    "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD",
    "TN", "TX", "UT", "VT", "VA", "WA",
    "WV", "WI", "WY"
]

def is_valid_state(state_name):
    '''
    Checks if user input is a valid state 
    Paramaters: state_name, a written user input
    Returns: True if input is a state or state abbreviation, False otherwise
    '''
    # check if state_name is a valid state
    if state_name.strip().title() in US_STATES:
        return state_name
    elif state_name.strip().upper() in STATE_ABBREVIATIONS:
        # return state_name even if user input an abbreviation
        state_name = US_STATES[STATE_ABBREVIATIONS.index(state_name.strip().upper())]
        return state_name
    else:
        return None

def get_state():
    '''
    Requests and validates a state name from the user via input.
    Uses is_valid_state() to validate the user input. 
    paramaters: none
    returns: a valid state_name, input by the user
    '''
    print("Input a state name to analyze")
    print(US_STATES)
    valid_state = None
    # use is_valid_state to check user input
    while valid_state is None:
        state_name = input("Enter a US state name/abbreviation: ").title()
        valid_state = is_valid_state(state_name)
    
    return valid_state   

# Regular expression pattern to match valid date in YYYY-MM-DD format
DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}$'

def is_valid_date(date):
    '''
    Checks if a user input date matches the format YYYY-MM-DD using regex then 
    checks if date is a valid calendar date using datetime
    Paramaters: date: the user input string
    Returns: True if date fits format, False otherwise
    '''
    # check that date is valid format string
    if not re.match(DATE_PATTERN, date):
        print('Invalid date format!\n')
        return False
    
    # check date is valid calendar date
    year, month, day = map(int, date.split('-'))
    try:
        # attempt to create a datetime object from the input date
        newDate = datetime.datetime(year,month,day)
        return True
    except ValueError:
        print("Invalid calendar date!\n")
        return False

def extract_year(date_str):
    '''
    Gets the year from a date formated string YYYY-MM-DD
    Parameters: date_str: the user input string, as a date
    Returns: if the input is a valid date format, the first 4 characters are 
    extracted and returned
    '''
    # Extract the first four integers from the date string
    match = re.match(r'^\d{4}', date_str)
    if match:
        return match.group()
    else:
        return None

def get_year_range(variable_list, period):
    '''
    Gets the INTERSECTING minimum and maximum of for multiple meteorological variables
    Paramaters: variable_list: a list of multiple variables
    period: the period of these variables, as they must be shared
    Returns: shared_min and shared_max, the collective min and maxes of the input variables
    '''

    min_max = []
    for each in variable_list:
        # build filtered data frame for specific variable, using storage
        filtered_df = STORAGE.loc[STORAGE['variable'].str.contains(each)]
        filtered_df = filtered_df.loc[filtered_df['period'].str.contains(period)]

        # get min year and max year for that specific variable, and append to min_max list
        year_min = filtered_df['year'].min()
        year_max = filtered_df['year'].max()
        each_min_max = [year_min, year_max]
        min_max.append(each_min_max)
    
    # get lowest shared minimum, and highest shared maximum
    mins = [row[0] for row in min_max]
    maxes = [row[1] for row in min_max]
    
    shared_min = max(mins)
    shared_max = min(maxes)

    return [shared_min, shared_max]

def is_valid_year(year_range, year_input):
    '''
    Checks if a year is within year range
    Parameters: year_range, a list of two string integers, year_min and year_max
    year_input: a string of a possibly year
    Returns: True if the number is a year in range, false otherwise
    '''
    # forcing string inputs into ints for comparisons
    year_input = int(year_input)
    year_range[0] = int(year_range[0])
    year_range[1] = int(year_range[1])

    if year_range[0] <= year_input and year_input <= year_range[1]:
        return True
    else:
        print('Year is not in range!')
        print(f"The range of years for this variable is {year_range[0]} to {year_range[1]}")
        return False

def get_year(variable_list, period):
    '''
    Drives user inputs and validates if a user input is a valid year for a given list of variables
    Parameters: variable_list: the input variables, 
    period: the period of data collection, for storage indexing
    Returns: the user input year, once it is validated
    '''
    # get year range
    year_range = get_year_range(variable_list, period)

    print(f"The range of years for this variable is {year_range[0]} to {year_range[1]}")

    # check user inputs valid year and date
    valid_year = False
    while valid_year is False:
        year = input("Input a year as YYYY: ")
        valid_year = is_valid_year(year_range, year)
    
    return year


def variable_select(menu_select):
    '''
    Determines which variable the user wants to work with. Logic begin with
    menu_select, the user's input of their selected function
    Parameters: menu_select
    '''

    CHOICES = ['Temperature', 'AQI', 'Criteria Gases',]
    choice = None
    if menu_select == 'yearly_summary' or menu_select == 'state_plots':
        while choice not in ['1','2']:
            choice = input("Pick a variable. Temperature: 1, AQI: 2: ")
            if choice not in ['1','2']:
                print("Invalid choice! Please enter 1, or 2:\n")
    else:
        while choice not in ['1','2','3']:
            choice = input("Pick a variable. Temperature: 1, AQI: 2, Criteria Gases (Ozone, SO2, NO2, and CO): 3: ")
            if choice not in ['1','2','3']:
                print("Invalid choice! Please enter 1, 2 or 3:\n")

    if choice == '1':
        # Code for working with Temperature
        print("You chose Temperature.")
        return ['Temperature']
    elif choice == '2':
        # Code for working with AQI
        print("You chose AQI.")
        return ['AQI']
    elif choice == '3':
        # Code for working with Criteria Gases
        print("You chose Criteria Gases (Ozone, SO2, NO2, and CO).")
        return ['Ozone', 'SO2', 'NO2', 'CO']