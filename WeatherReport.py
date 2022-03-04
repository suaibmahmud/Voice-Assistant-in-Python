import requests
import time

api_key = "15ea2e2f1b8f9b365dd84a65cccb14a8"

def weather_reports(city):
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key
    json_data = requests.get(api).json()
    
    if json_data['cod'] == '404':
        return "error"
    
    else:
        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
        sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))

        return humidity, temp, condition, wind
