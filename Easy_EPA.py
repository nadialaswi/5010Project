'''
DS5010 Final Project
user_interface: The front end driver for the user.
Allows the user to dictate which information they want to work with
'''
from url_storage import *
from backend_functions import * 
from input_validation import *
import sys

# storage is static gloabl variable holding csv file information
STORAGE = get_storage()

def daily_summary_selected():
    '''
    For when the user selects daily summary
    Parameters: none
    Returns: Nothing. Prints summary for user via backend functions, then returns to menu
    '''
    period = 'daily'

    # Current implementation of daily summary only supports Wind, AQI, and Temp
    wind_var = 'Wind'
    aqi_var = 'AQI'
    temp_var = 'Temperature'
    var_list = [wind_var, aqi_var, temp_var]

    print(f"You selected (D) Daily Summary! Summarizing {var_list[0]}, {var_list[1]}, and {var_list[2]}!")
          
    # get year range
    year_range = get_year_range(var_list, period)

    # check user inputs valid year and date
    valid_date_format = False
    valid_year = False
    while valid_date_format is False or valid_year is False:
        date = input("Input a date as YYYY-MM-DD: ")
        valid_date_format = is_valid_date(date)
        year = extract_year(date)
        valid_year = is_valid_year(year_range, year)

    # getting state name input
    state_name = get_state()

    file1 = download_driver(STORAGE, wind_var, year, period)
    file1_path = path_builder(file1)

    file2 = download_driver(STORAGE, aqi_var, year, period)
    file2_path = path_builder(file2)
    
    file3 = download_driver(STORAGE, temp_var, year, period)
    file3_path = path_builder(file3)

    daily_summary(file1_path, file2_path, file3_path, date, state_name)

def yearly_finder_selected():
    '''
    For when the user selects yearly finder
    Parameters: none
    Returns: Nothing. Prints yearly summary for user via backend functions, then returns to menu
    '''
    period = 'daily'
    print("You selected (Y) Yearly Finder. Look up the Temperature or AQI in a State for a given year.")

    # get variable
    var_list = variable_select('yearly_summary')

    # get year
    year_input = get_year(var_list, period)

    # getting state name input
    state_name = get_state()

    # get folder path
    file = download_driver(STORAGE, var_list[0], year_input, period)
    current_working_directory = os.getcwd()
    folder_path = current_working_directory + "/csv_folder/" + file
    
    if var_list[0] == 'Temperature':
        temp_yearly_finder(folder_path, year_input, state_name)
   
    elif var_list[0] == 'AQI':
       aqi_yearly_finder(folder_path, year_input, state_name)

def plot_selected(type):
    '''
    For when the user selects to either plot a variable, or state comparison
    Parameters: type - dictates if the user wants a variable plot or state plot
    Returns: Nothing. Shows plot for user via backend functions, then returns to menu
    '''
    period = 'daily'
    if type == 'plot':
        print("You selected (P) Plot. Pick a variable and plot it for a given year. ")

        # get variable
        var_list =  variable_select('plot_summary')
        
        # get year
        year_input = get_year(var_list, period)
        
        # get state name
        state_name = get_state()

        if var_list[0] == 'Ozone':
            # download each relevant file
            file1 = download_driver(STORAGE, var_list[0], year_input, period)
            file1_path = path_builder(file1)

            file2 = download_driver(STORAGE, var_list[1], year_input, period)
            file2_path = path_builder(file2)
            
            file3 = download_driver(STORAGE, var_list[2], year_input, period)
            file3_path = path_builder(file3)

            file4 = download_driver(STORAGE, var_list[3], year_input, period)
            file4_path = path_builder(file4)

            criteria_gases_plot(file1_path, file2_path, file3_path, file4_path, year_input, state_name)

        else:
            file = download_driver(STORAGE, var_list[0], year_input, period)
            current_working_directory = os.getcwd()
            folder_path = current_working_directory + "/csv_folder/" + file
            
            if var_list[0] == 'Temperature':
                temp_yearly_plot(folder_path, year_input, state_name)
        
            elif var_list[0] == 'AQI':
                aqi_yearly_plot(folder_path, year_input, state_name)
    if type == 'state':
        print("You selected (C) Compare US states with easily viewable plots.")

        # get variable
        var_list =  variable_select('state_plots')

        # get year
        year_input = get_year(var_list, period)
        
        # get folder path
        file = download_driver(STORAGE, var_list[0], year_input, period)
        current_working_directory = os.getcwd()
        folder_path = current_working_directory + "/csv_folder/" + file
        
        if var_list[0] == 'Temperature':
            temp_states_plot(folder_path, year_input)
    
        elif var_list[0] == 'AQI':
            aqi_states_plot(folder_path, year_input)

def download_file_selected():
    '''
    Allows user to directly download file based on variable and year input
    Parameters: none
    Returns: none. Downloads relevant file to csv_folder
    '''
    period = "daily"
    variable_dict = {
    '1': 'Temperature',
    '2': 'AQI',
    '3': 'Wind',
    '4': 'Ozone',
    '5': 'SO2',
    '6': 'NO2',
    '7': 'CO'
    }
    print("You picked (S). Quickly SAVE a file to your csv folder")
    choice = None
    # getting input mapped to dictionary
    while choice not in variable_dict.keys():
        choice = input('Select a variable: 1: Temperature, 2: AQI, 3: Wind, 4: Ozone, 5: SO2 6: NO2, 7: CO\n')

    selected_variable = variable_dict[choice]
    print(f" You selected: {selected_variable}")
    year = get_year(selected_variable, period)
     # download file and returning to main menu
    download_driver(STORAGE, selected_variable, year, period)
    return

def menu_select():
    '''
    Drive the user selection of the menu options
    Parameters: none
    Returns: The users input menu selection, once its validated
    '''
    input_list = ['D','Y','P','S','Q', 'C','R']
    select = None 
    while select not in input_list:
        print(
              "Input Options: \n"
              "D: Obtain the DAILY summary of Temperature, Wind, and Air Quality Index (AQI) for a designated DATE and STATE. \n"
              "Y: Retrieve a SUMMARY of either Temperature or Air Quality Index (AQI) for a particular STATE for a specified YEAR. \n"
              "P: Retrieve a PLOT of Temperature, Air Quality Index (AQI), or  Criteria Pollutant Gases for a particular STATE for a specified YEAR. \n"
              "C: COMPARE STATES via PLOT for either Temperature or Air Quality Index (AQI) for a specified YEAR. \n" 
              "S: SAVE a specific csv file to your csv_folder\n"
              "Q: Quit out.\n")
              # "R: Type R at anytime to return to the main menu.") # add later

        select = input(" ").capitalize()
        if select not in input_list:
            print("!!INVALID MENU INPUT!!\n")
    return select

def menu_driver(first):
    '''
    Main driving function for Easy_EPA. Sets up the user menu that allows for
    function navigation
    Parameters: first: a flag to check if this is the first time the user has accessed
    the menu for this session. This is too print less introductory lines for better clarity
    Returns: nothing - this function drives other functions
    '''
    if first is True:
        print("\nWelcome to the main menu. Input a letter to explore the "
                "United States Environmental Protection Agency's meteorological data. \n")
    
    # implemented so results of user's search are more visible before opening menu again
    if first is False:
        quit_input = None
        while quit_input not in ['1','2']:
            quit_input = input("1: Return to main menu. 2: Quit ").strip()
        if quit_input == '2':
            print("Quitting out. Open csv_folder to view files from your session")
            sys.exit()

    option = None
    while option != 'Q': # Q quits menu 
        # getting menu select
        option = menu_select()
        # using menu select to dictate menu logic
        if option  == 'D':
            daily_summary_selected()
            menu_driver(False)
        if option == 'Y':
            yearly_finder_selected()
            menu_driver(False)
        if option == 'P':
            plot_selected('plot')
            menu_driver(False)
        if option == 'C':
            plot_selected('state')
            menu_driver(False)
        if option == 'S':
            download_file_selected()
            menu_driver(False)
        if option == 'R':
            menu_driver(False)
        if option == 'Q':
            print("Quitting out. Open csv_folder to view files form your session")
            sys.exit()

def main():
    menu_driver(True)

if __name__ == "__main__":
    main()
