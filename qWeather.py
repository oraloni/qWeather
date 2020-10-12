# Weather data and icons from https://openweathermap.org/

import requests, json, sys, time
import datetime as dt
from urllib.request import urlopen 
from PIL import Image, ImageTk
from io import BytesIO


class Weather():
    def __init__(self):
        self.apiKey = 'e0cffd4ce08b4814e5c526b56d2261ab'

    def getApi(self, location, lang = 'en', units = 'metric'):
        # Download the JSON data from openWeatherMap.org's API
        self.location = location
        url = 'http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=%s&lang=%s' % (self.location,
                                                                              self.apiKey, units, lang)
        self.api_response = requests.get(url)
        self.api_response.raise_for_status() 
        # Load JSON data into python variable
        self.weatherData = json.loads(self.api_response.text)
        return self.weatherData
    
    def update_time(self):
        # TODO: Check if location changes
        location = 'Kfar Saba'
        self.data = Weather.getApi(self, location)
        time_update_data =  time.localtime(self.data['dt'])
        self.last_update = time.strftime('%d/%m/%y %H:%M:%S')
        return self.last_update
        
    def today_weather_data(self, location):
        self.data = Weather.getApi(self, location)
        #self.gen_weather_description = (data['weather'][0]['main'], data['weather'][0]['description'])
        self.conditions = {
                        'description': self.data['weather'][0]['description'],
                        'tempatures': self.data['main']['temp'],
                        'feels_like': self.data['main']['feels_like'],
                        'humidity': self.data['main']['humidity'],
                        'windspeed': self.data['wind']['speed'],
                        'wind_direction': self.data['wind']['deg'], 
                        'clouds': self.data['clouds']['all'],
                        'icon': self.data['weather'][0]['icon']
                        }
        return self.conditions

    def get_icon(self):
        self.icon_code = self.conditions['icon']
        self.icon_url = f'http://openweathermap.org/img/wn/{self.icon_code}@2x.png' 
        url = urlopen(self.icon_url)  
        rawData = url.read()
        url.close()
        self.image = Image.open(BytesIO(rawData))
        self.icon_img = ImageTk.PhotoImage(self.image)
        return self.icon_img
    

class Forcast:
    def __init__(self, location, lang='en', units='metric'):
        self.units = units
        self.lang = lang
        self.location = location
        self.apiKey = 'e0cffd4ce08b4814e5c526b56d2261ab'

    def forcast_data(self):
        # Download the JSON data from openWeatherMap.org's API
        #self.apiKey = 'e0cffd4ce08b4814e5c526b56d2261ab'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={self.location}&appid={self.apiKey}&units={self.units}&lang={self.lang}'
        self.api_response = requests.get(url)
        self.api_response.raise_for_status() 
        # Load JSON data into python variable
        self.forcastData = json.loads(self.api_response.text)
        return self.forcastData
    
    def lon_and_lat(self):
        data = Weather()
        data = data.getApi(self.location)
        self.lon = data['coord']['lon']
        self.lat = data['coord']['lat']
        return (self.lon, self.lat)
    
    def daily_forcast(self, num_of_days=3):
        data = self.lon_and_lat()
        lon = data[0]
        lat = data[1]
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={self.apiKey}&units={self.units}&lang={self.lang}'
        self.api_response = requests.get(url)
        self.api_response.raise_for_status() 
        # Load JSON data into python variable
        self.forcastData = json.loads(self.api_response.text)
        daily = self.forcastData['daily']
        # Setting a dictonary containing the date, name of day, min/max temp and icon
        #print(daily)
        self.tommorow = {'date': dt.date.fromtimestamp(daily[1]['dt'])  ,'min': daily[1]['temp']['min'], 'max':daily[1]['temp']['max'], 'icon': daily[1]['weather'][0]['icon'], 'description': daily[1]['weather'][0]['description'] }
        self.day_after_tommorw = {'date': dt.date.fromtimestamp(daily[2]['dt'])  ,'min': daily[2]['temp']['min'], 'max':daily[2]['temp']['max'], 'icon': daily[2]['weather'][0]['icon'], 'description': daily[2]['weather'][0]['description'] }
        self.in_three_days = {'date': dt.date.fromtimestamp(daily[3]['dt']) ,'min': daily[3]['temp']['min'], 'max':daily[3]['temp']['max'], 'icon': daily[3]['weather'][0]['icon'], 'description': daily[3]['weather'][0]['description'] }
        return [self.tommorow, self.day_after_tommorw, self.in_three_days]

    def forcast_icon(self, icon_code):
        self.icon_code = icon_code
        self.icon_url = f'http://openweathermap.org/img/wn/{self.icon_code}@2x.png' 
        url = urlopen(self.icon_url)  
        rawData = url.read()
        url.close()
        self.image = Image.open(BytesIO(rawData))
        self.icon_img = ImageTk.PhotoImage(self.image)
        return self.icon_img

##### Under Construction #####
# Pass to the other side of the road please!  
class Query():
    def __init__(self, location, lang='en', units = 'metric'):
        self.location = location
        self.lang = lang
        self.units = units
        api = Weather()
        api_data = api.api_response(self.location, self.units, self.lang)
        data = api_data



def main():
    f = Forcast('kfar Saba')
    print(f.lon_and_lat())
    print(f.daily_forcast())
    # t = Weather()
    # d = t.getApi('kfar Saba')
    # print(d)
    # print(t.update_time())

if __name__ == "__main__":
    main()






