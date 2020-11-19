# Rhett Coleman / CIS245-T302 / 11/19/2020

import requests
import time
import sys
import configparser

# Attach config.ini to program (ensure config.ini is in the same folder)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

# Confirm online connection only on the first loop
def first_run(first_run = []):
    if first_run == []:
        confirm_connection(get_api_key())
        first_run.append('complete')

def confirm_connection(api_key):
    print("Checking connection to openweathermaps.org...")
    time.sleep(.5)
    test_url = f'http://api.openweathermap.org/data/2.5/weather?q=Orlando&appid={api_key}'
    r = requests.get(test_url)
    data =r.json()
    try:
        data['base'] == 'stations'
        print('Connected to openweathermap.org!\n')
    except:
        sys.exit('Could not connect to openweathermap.org\nPlease try again later\n')

# Obtain raw weather data
def get_weather_results(user_input,api_key):
    #If zip code input
    if user_input.isnumeric():
        api_url = f'http://api.openweathermap.org/data/2.5/weather?zip={user_input}&units=imperial&appid={api_key}'
        r = requests.get(api_url)
        return r.json()
    #If city name input
    else:
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&appid={api_key}'
        r = requests.get(api_url)
        return r.json()

#Translate raw weather data
def translate_weather(data):
    #Uses group ID to call the current weather and returns it.
    main_condition = data['weather'][0]['id']
    #main_condition = 605 #Use this to test outputs

    # translate clouds
    cloud_dict = {'with clear skys': 800,
                  'with very few clouds': 801,
                  'and partly cloudly': 802,
                  'and mostly cloudy': 803,
                  'and overcast': 804}

    def get_cloud(val):
        for key, value in cloud_dict.items():
            if val == value:
                return key

    cloud_conditon = get_cloud(main_condition)

    #Thunderstorm
    thunderstorm_ids = []
    thunderstorm_ids.extend(range(200, 299))

    #Raining
    raining_ids = []
    raining_ids.extend(range(300, 599))

    #snowing
    snowing_ids = []
    snowing_ids.extend(range(600, 699))

    #extreme
    extreme_ids = []
    extreme_ids.extend(range(700, 799))

    #Determind MAIN output
    if cloud_conditon != None:
        return f'{cloud_conditon}'

    elif main_condition in thunderstorm_ids:
        return 'and thunder storming'

    elif main_condition in raining_ids:
        return 'and raining'

    elif main_condition in snowing_ids:
        return 'and snowing'

    elif main_condition in extreme_ids:
        return 'and an extreme weather advisory as been issued'

    else:
        return 'with unreported weather'

#Translate Wind
def wind_translation(data):
    # Uses wind speed to call wind condition according to the Beaufort Scale.
    wind_speed = data['wind']['speed']
    #wind_speed = 1 #Use this to test outputs

    #Determind wind output
    if wind_speed < 1.5:
        return 'calm'

    elif 1.5 <= wind_speed < 14:
        return 'breezy'

    else:
        return 'windy'

# validate input
def validate_input(data):
    try:
        data['base'] == 'stations'
        weather_output(data)
    except:
        print("\nWe're sorry the city or zip code you have entered can not be found.")

#output
def weather_output(data):
    city = data['name']
    main = translate_weather(data)
    temps = data['main']['temp']
    winds = wind_translation(data)
    humidity = data['main']['humidity']
    feels = data['main']['feels_like']

    print(f'\nIn {city}, It is currently {winds}, at {temps}°F degrees {main}.'
          f'\nWith {humidity}% humidity, it feels like {feels} degrees.')

#Ask user to use again
def again_input():
    again = input('\nWould you like to check the weather again? (yes or no): ')
    again = again.lower()

    if again == 'n':
        print('Thank you, enjoy the weather!')
        again = False
        return again

    if again == 'no':
        print('Thank you, enjoy the weather!')
        again = False
        return again

#main function
if __name__ == '__main__':
   again = ''
   while again != False:
        print('\n### Welcome to Open Weather Map ###')

        #Confirm Connection Function
        first_run()

        #user input
        user_input = input('To know the weather, please type in the city or zip code: ')
        data = get_weather_results(user_input,get_api_key())

        #validate and output
        validate_input(data)

        #Ask user to use again
        again = again_input()






