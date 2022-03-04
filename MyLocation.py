import requests

def my_location():
    ipAdd = requests.get('https://api.ipify.org/').text
    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    city = geo_data['city']
    country = geo_data['country']

    return city.lower(), country.lower()


