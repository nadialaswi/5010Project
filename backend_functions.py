'''
DS5010 Final Project
backend_functions uses pandas and matplotlib to accomplish data analysis and plotting of EPA data
'''

import pandas as pd
import matplotlib.pyplot as plt

'''
DAILY SUMMARY
'''
def daily_summary(wind_file: str, aqi_file:str, temp_file:str, date: str, state_name: str):
    '''
    Finds temperature, AQI, and wind data for a given day and location
    Inputs: .csv files from aqs.epa.gov of the same year(str), date as YYYY-MM-DD (str), state name (str)   
    Returns: str
    '''
    df_wind = pd.read_csv(wind_file)
    df_aqi = pd.read_csv(aqi_file)
    df_temp = pd.read_csv(temp_file)
    
    # Find rows where date and state match
    chosen_date_wind = df_wind['Date Local'] == date
    chosen_state_wind = df_wind['State Name'] == state_name
    in_knots = df_wind['Units of Measure'] == 'Knots' # Multiple units offered for wind, choose one

    
    chosen_date_aqi = df_aqi['Date'] == date
    chosen_state_aqi = df_aqi['State Name'] == state_name
    
    chosen_date_temp = df_temp['Date Local'] == date
    chosen_state_temp = df_temp['State Name'] == state_name
    
    
    # If date/state not found
    if not (chosen_date_wind.any() and chosen_date_aqi.any() and chosen_date_temp.any()):
        print(f'Sorry, {date} is not recorded in this file. Note that the latest recorded data is ' 
              f'from October of 2023, and the date should be written as YYYY-MM-DD.')
    elif not (chosen_state_wind.any() and chosen_state_aqi.any() and chosen_state_temp.any()):
        print(f'Sorry, {state_name} is not recorded in this file. Note that the following have no '
              f'available data: Delaware, New York, New Jersey, Vermont.')
    
    # Update dataframe with conditions
    df_wind = df_wind[chosen_date_wind & chosen_state_wind & in_knots]
    df_aqi = df_aqi[chosen_date_aqi & chosen_state_aqi]
    df_temp = df_temp[chosen_date_temp & chosen_state_temp]

        
    # Values of interest:
#     wind_max = df['1st Max Value'].values.max() # Maximum speed recorded 
    wind_mean = df_wind['Arithmetic Mean'].values.mean() # Mean of means
    aqi_mean = df_aqi['AQI'].values.mean()
    temp_mean = df_temp['1st Max Value'].values.mean()
    
    print((f'For {date}, {state_name} had an average wind speed of {wind_mean:.1f} Knots, an average AQI '
            f'of {aqi_mean:.1f}, and an average temperature of {temp_mean:.1f} degrees Farenheit.'))    
    return 


'''
YEARLY SUMMARY FUNCTIONS
'''
def aqi_yearly_finder(file: str, year: str, state_name: str):
    '''
    Finds air quality index in an area for a given year
    Inputs: .csv file from aqs.epa.gov (str), date as YYYY (str), state name (str)   
    Returns: str
    '''
    df = pd.read_csv(file)
    
    # Find rows where date and state match
    chosen_year = df['Date'].str.slice(0,4) == year
    chosen_state = df['State Name'] == state_name
    
    # If date/state not found
    if not chosen_year.any():
        print(f'Sorry, {year} is not recorded in this file. The year should be written as YYYY.')
    elif not chosen_state.any():
        print(f'Sorry, {state_name} is not recorded in this file. Note that Delaware is not '
              f'recorded in this file. Check for any typos!')
    
    # Update dataframe with conditions
    df = df[chosen_year & chosen_state]
    
    # Values of interest:
    aqi = df['AQI'].values
    aqi_max = max(df['AQI'].values)
    aqi_mean = aqi.mean()
    
    # Determine count of categories recorded in the filtered data
    condition = df['Category'].value_counts()
    condition_count = ", ".join([f"{count} {category}" for category, count in condition.items() if count != 0])
        
    
    number_counties = len(df['county Name'].unique())
    
    recorded_days = len(df['Date'].unique())

    
    print(f'The AQI in {state_name} in {year} was recorded for {number_counties} {state_name} counties, '
          f'and a total of {recorded_days} days were recorded. '
          f'The average AQI was {aqi_mean:.1f} and the maximum recorded AQI was {aqi_max:.1f}. '
          f'(AQI\'s over 100 are considered unhealthy for sensitive groups.)')
            
        
def temp_yearly_finder(file: str, year: str, state_name: str):
    '''
    Finds temperature in an area for the given year
    Inputs: .csv file from aqs.epa.gov (str), year as YYYY (str), state name (str)   
    Returns: str
    '''
    df = pd.read_csv(file)
    
    # Find rows where date and state match
    chosen_year = df['Date Local'].str.slice(0,4) == year
    chosen_state = df['State Name'] == state_name
    
    # If date/state not found
    if not chosen_year.any():
        print(f'Sorry, {year} is not recorded in this file. The year should be written as YYYY.')
        print(f'Sorry, {state_name} is not recorded in this file. Note that the following have no '
              f'available data: Delaware, New York, New Jersey, Vermont')
    
    # Update dataframe with conditions
    df = df[chosen_year & chosen_state]
    
    # Values of interest:
    recorded_days = len(df['Date Local'].unique())
    
    temp_max = max(df['1st Max Value'].values) # High of the year
    temp_mean = df['1st Max Value'].values.mean() # Mean of the year across all counties
    # Note: We found some temperatures that are obviously wrong (at least 1 over 200F in CA)
    
    number_counties = len(df['County Name'].unique())

        
    print(f'The temperature in {state_name} was recorded across {number_counties} {state_name} counties, '
          f'and a total of {recorded_days} days were recorded in {year}. '
          f'The average temperature was {temp_mean:.1f} degrees Farenheit across {number_counties} counties. '
          f'The highest temperature recorded for {state_name} in {year} was {temp_max: .1f} degrees Farenheit.')
            
    
'''
YEARLY PLOTS
'''
def aqi_yearly_plot(file: str, year: str, state: str):
    
    '''
    Plots air quality of each day recorded in given year
    Inputs: .csv file from aqs.epa.gov (str), date as YYYY (str), state name (str)   
    Returns: plot
    '''
    df = pd.read_csv(file)
    
    # Find rows where date and state match
    chosen_year = df['Date'].str.slice(0,4) == year
    chosen_state = df['State Name'] == state
    
    # If date/state not found
    if not chosen_year.any():
        print(f'Sorry, {year} is not recorded in this file. The year should be written as YYYY.')
    elif not chosen_state.any():
        print(f'Sorry, {state} is not recorded in this file. Note that Delaware is not '
                f'recorded in this file. Check for any typos!')
    
    # Update dataframe with conditions
    df = df[chosen_year & chosen_state]
    
    # Find average across all counties that record a single day for a daily average:
    
    daily_avg = df.groupby('Date')['AQI'].mean().tolist()
    daily_max = df.groupby('Date')['AQI'].max().tolist()

    number_counties = len(df['county Name'].unique())
    
    unique_days = df['Date'].str.slice(5).unique() # For x-ticks, we don't need the year to show

    # Plotting
    plt.figure(figsize = (10,8))
    plt.rcParams['figure.dpi'] = 500
    plt.plot(unique_days, daily_avg, color='steelblue', label='Daily Average')
    plt.plot(unique_days,  daily_max, color='lightcoral', label='Daily Maximum')
    plt.axhline(y=100, color='black', linestyle='--', label='Unhealthy AQI')
    plt.axhline(y=50, color='orange', linestyle='--', label='Moderate AQI')
    plt.ylabel('Air Quality Index', fontsize=12)
    plt.xlabel('Date')
    plt.xticks(range(0, len(unique_days), 30), rotation=25, fontsize=10)
    plt.legend()
    plt.title(f'{year} Air Quality Across {number_counties} Counties in {state}')
    plt.show()
    
def temp_yearly_plot(file: str, year: str, state_name: str):
    '''
    Plots temperature of each day recorded in given year and place
    Inputs: .csv file from aqs.epa.gov (str), date as YYYY (str), state name (str)   
    Returns: plot
    '''
    df = pd.read_csv(file)
    
    # Find rows where date and state match
    chosen_year = df['Date Local'].str.slice(0,4) == year
    chosen_state = df['State Name'] == state_name
    
    # If date/state not found
    if not chosen_year.any():
        print(f'Sorry, {year} is not recorded in this file. The year should be written as YYYY.')
    elif not chosen_state.any():
        print(f'Sorry, {state_name} is not recorded in this file. Note that the following have no '
                f'available data: Delaware, New York, New Jersey, Vermont')
    
    # Update dataframe with conditions
    df = df[chosen_year & chosen_state]
    
    # Find average across all counties that record a single day for a daily average:
    
    daily_avg = df.groupby('Date Local')['1st Max Value'].mean().tolist()
    daily_max = df.groupby('Date Local')['1st Max Value'].max().tolist()

    number_counties = len(df['County Name'].unique())
    
    unique_days = df['Date Local'].str.slice(5).unique() # For x-ticks, we don't need the year to show

    # Plotting
    plt.figure(figsize = (10,8))
    plt.rcParams['figure.dpi'] = 500
    plt.plot(unique_days, daily_avg, color='steelblue', label='Daily Average')
    plt.plot(unique_days,  daily_max, color='goldenrod', label='Daily Maximum')
    plt.ylabel('Temperature (Degrees Farenheit)', fontsize=12)
    plt.xlabel('Date')
    plt.xticks(range(0, len(unique_days), 30), rotation=25, fontsize=10)
    plt.legend()
    plt.title(f'{year} Temperatures Across {number_counties} Counties in {state_name}')
    plt.show()
    
def criteria_gases_plot(ozone_file: str, co2_file:str, so2_file:str, no2_file:str, year: str, state: str):
    '''
    Plots detection of criteria gases of each day recorded in given year and place
    Inputs: 4 .csv files from aqs.epa.gov (str), date as YYYY (str), state name (str)   
    Returns: plot
    '''
    ozone = pd.read_csv(ozone_file)
    co2 = pd.read_csv(co2_file)
    so2 = pd.read_csv(so2_file)
    no2 = pd.read_csv(no2_file)
    
    
    # Find rows where date and state match
    chosen_year_ozone = ozone['Date Local'].str.slice(0,4) == year
    chosen_state_ozone = ozone['State Name'] == state
    
    chosen_year_co2 = co2['Date Local'].str.slice(0,4) == year
    chosen_state_co2 = co2['State Name'] == state
    
    chosen_year_so2 = so2['Date Local'].str.slice(0,4) == year
    chosen_state_so2 = so2['State Name'] == state
    
    chosen_year_no2 = no2['Date Local'].str.slice(0,4) == year
    chosen_state_no2 = no2['State Name'] == state
    
    
    # If date/state not found
    if not (chosen_year_ozone.any() and chosen_year_co2.any() and chosen_year_so2.any() \
            and chosen_year_no2.any()):
        print(f'Sorry, {year} is not recorded in all necessary files.')
    elif not (chosen_state_ozone.any() and chosen_state_co2.any() and chosen_state_so2.any() \
              and chosen_state_no2.any()):
        print(f'Sorry, {state} is not recorded in all necessary files. Note that the following '
              f'have no available data: Alaska, Delaware')
    
    # Update dataframes with conditions
    ozone = ozone[chosen_year_ozone & chosen_state_ozone]
    co2 = co2[chosen_year_co2 & chosen_state_co2]
    so2 = so2[chosen_year_so2 & chosen_state_so2]
    no2 = no2[chosen_year_no2 & chosen_state_no2]

    
    # Find average across all counties that record a single day for a daily average:
    
    daily_avg_ozone = ozone.groupby('Date Local')['Observation Count'].mean().tolist()
    
    daily_avg_co2 = co2.groupby('Date Local')['Observation Count'].mean().tolist()
    
    daily_avg_so2 = so2.groupby('Date Local')['Observation Count'].mean().tolist()

    daily_avg_no2 = no2.groupby('Date Local')['Observation Count'].mean().tolist()
    
    # We want to plot each day only once on our graph
    unique_days_ozone = ozone['Date Local'].str.slice(5).unique() # For x-ticks, we don't need the year to show
    unique_days_co2 = co2['Date Local'].str.slice(5).unique()
    unique_days_so2 = so2['Date Local'].str.slice(5).unique()
    unique_days_no2 = no2['Date Local'].str.slice(5).unique()
    
    # Plotting:
    
    fig, axs = plt.subplots(2, 2, figsize=(10, 8), dpi=500)

    axs[0, 0].plot(unique_days_ozone, daily_avg_ozone, color='orange')
    axs[0, 0].set_title(f'Ozone observed in {state} {year}')
    axs[0, 0].set_xticks(range(0, len(unique_days_ozone), 30))
    axs[0, 0].set_ylabel('Observation Count (parts per million)')
    axs[0, 0].set_xlabel('Date')

    
    axs[0, 1].plot(unique_days_co2, daily_avg_co2, color='forestgreen')
    axs[0, 1].set_title(f'CO observed in {state} {year}')
    axs[0, 1].set_xticks(range(0, len(unique_days_co2), 30))
    axs[0, 1].set_ylabel('Observation Count (parts per million)')
    axs[0, 1].set_xlabel('Date')
    
    axs[1, 0].plot(unique_days_so2, daily_avg_so2, color='steelblue')
    axs[1, 0].set_title(f'SO2 observed in {state} {year}')
    axs[1, 0].set_xticks(range(0, len(unique_days_so2), 30))
    axs[1, 0].set_ylabel('Observation Count (parts per million)')
    axs[1, 0].set_xlabel('Date')
    
    axs[1, 1].plot(unique_days_no2, daily_avg_no2, color='brown')
    axs[1, 1].set_title(f'NO2 observed in {state} {year}')
    axs[1, 1].set_xticks(range(0, len(unique_days_no2), 30))
    axs[1, 1].set_ylabel('Observation Count (parts per million)')
    axs[1, 1].set_xlabel('Date')
    
    plt.tight_layout()
    plt.show()
    

'''
State COMPARISON PLOTS
'''

def aqi_states_plot(file: str, year: str):
    '''
    Plots average air quality of all states in given year
    Inputs: .csv file from aqs.epa.gov (str), date as YYYY (str)
    Returns: plot
    '''
    df = pd.read_csv(file)
    
    # Find rows where date and state match
    chosen_year = df['Date'].str.slice(0,4) == year
    
    # If date/state not found
    if not chosen_year.any():
        print(f'Sorry, {year} is not recorded in this file. The year should be written as YYYY.')
    
    # Update dataframe with conditions
    df = df[chosen_year]
    
    # Find average of each state for the whole year
    yearly_avg = df.groupby('State Name')['AQI'].mean().tolist()
    
    unique_states = df['State Name'].unique() 
    number_states = len(unique_states)


    # Plotting
    plt.figure(figsize = (10,8))
    plt.rcParams['figure.dpi'] = 500
    plt.bar(unique_states, yearly_avg, color='lightblue')
    plt.axhline(y=50, color='orange', linestyle='--', label='Moderate AQI')
    plt.grid(axis='y', linestyle='--', alpha=0.7)


    # Title and axes 
    plt.ylabel('Air Quality Index', fontsize=12)
    plt.xlabel('State / Country')
    plt.xticks(unique_states, rotation=90, fontsize=10)
    plt.legend()
    plt.title(f'Average Air Quality Recorded Across {number_states} Regions in {year}')
    plt.show()
    
def temp_states_plot(file: str, year: str):
    '''
    Plots average temperature of all states in given year
    Inputs: .csv file from aqs.epa.gov (str), date as YYYY (str)
    Returns: plot
    '''
    df = pd.read_csv(file)
    
    # Find rows where date and state match
    chosen_year = df['Date Local'].str.slice(0,4) == year
    
    # If date/state not found
    if not chosen_year.any():
        print(f'Sorry, {year} is not recorded in this file.')
    
    # Update dataframe with conditions
    df = df[chosen_year]
    
    # Find average of each state for the whole year
    yearly_avg = df.groupby('State Name')['1st Max Value'].mean().tolist()
    
    unique_states = df['State Name'].unique() 
    number_states = len(unique_states)


    # Plotting
    plt.figure(figsize = (10,8))
    plt.rcParams['figure.dpi'] = 500
    plt.bar(unique_states, yearly_avg, color='steelblue', label='Average Temperature')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Title and axes 
    plt.ylabel('Temperature (Degrees Farenheit)', fontsize=12)
    plt.xlabel('State / Country')
    plt.xticks(unique_states, rotation=90, fontsize=10)
    plt.title(f'Average Temperature Recorded Across {number_states} Regions in {year}')
    plt.show()
    
    
    