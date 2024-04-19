# Menu selection paths: 1: Pick variable, 2: Pick 
def variable_select():
    print("Welcome! Which variable would you like to work with?")
    valid_choice = False

    while valid_choice == False:
        choice = input("Enter 1, 2 or 3 (Temperature: 1, AQI: 2, Pollutant Gasses: 3): ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice! Please enter 1, 2, or 3.")
        else:
            if choice == '1':
                # Code for working with Temperature
                print("You chose Temperature.")
            elif choice == '2':
                # Code for working with CO2
                print("You chose AQI.")
            elif choice == '3':
                # Code for working with AQI
                print("You chose Pollutant Gasses.")
            valid_choice = True

    return choice



def function_select():
    CHOICES = ['temperature', 'aqi', 'wind']
    valid_choice = False

    while valid_choice == False:
        choice = input("Pick a variable (Temperature: 1, AQI: 2, Wind: 3): ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice! Please enter 1, 2, or 3.")
        else:
            if choice == '1':
                # Code for working with Temperature
                print("You chose Temperature.")
            elif choice == '2':
                # Code for working with CO2
                print("You chose AQI.")
            elif choice == '3':
                # Code for working with AQI
                print("You chose Pollutant Gasses.")
            valid_choice = True

    return choice

def input_checker(storage, input_type, input):
    '''
    Verifies user inputs are valid for menu_driver()
    Parameters: input_type: what the user's input is. ex: variable type, the year etc
    input: the actual user input being checked
    storage: checks that inputs are valid
    returns: True if input is valid, False if not
    '''
    output = False

    if input_type == 'variable' and input not in ['AQI, TEMP, ']:
        pass
    pass