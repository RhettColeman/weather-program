# Rhett Coleman / CIS245-T302 / 10/30/2020

import requests
import time
import sys
import configparser

# Attach config.ini to program (ensure config.ini is in the same folder)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

# Confirm online connection on first loop
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

# Obtain data
def get_weather_results(user_input,api_key):
    if user_input.isnumeric():
        api_url = f'http://api.openweathermap.org/data/2.5/weather?zip={user_input}&units=imperial&appid={api_key}'
        r = requests.get(api_url)
        return r.json()
    else:
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&appid={api_key}'
        r = requests.get(api_url)
        return r.json()

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
    cloud_conditions = data['weather'][0]['description']
    temps = data['main']['temp']
    humidity = data['main']['humidity']
    feels = data['main']['feels_like']
    print(f'The current weather in {city} contains {cloud_conditions}.'
          f'\nIt is currently {temps} degrees. With {humidity}% humidity, it feels like {feels} degrees.')

#Use Again
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

        #Use Again
        again = again_input()






