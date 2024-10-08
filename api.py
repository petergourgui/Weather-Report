import json
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError


base_nominatim_search_url = 'https://nominatim.openstreetmap.org/search?'
base_nominatim_reverse_url = 'https://nominatim.openstreetmap.org/reverse?'
base_nws_search_url = 'https://api.weather.gov/points/'

def get_search_url(target: str) -> str:
    'Builds and returns the URL that will be used to search for the location.'
    queries = [('q', target), ('format', 'json')]
    url = base_nominatim_search_url + urllib.parse.urlencode(queries, encoding='utf-8')
    return url 


def get_result_url(url: str) -> dict:
    'Opens the URL, and returns a dictionary containing information of the URL.'
    response = None
    request = None
    try:
        request = urllib.request.Request(url)
        if 'weather' in url:
            request.add_header("User-Agent", "(https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/, pgourgui@uci.edu)")
            response = urllib.request.urlopen(request)
        else:
            request.add_header("Referer", "https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/pgourgui")
            response = urllib.request.urlopen(request)
            time.sleep(1)
    except HTTPError as error:
        print('FAILED')
        print(error.code, url)
        print('NOT 200')
        if response != None:
            response.close()
        exit()
    except:
        print('FAILED')
        print(url)
        print('NETWORK')
        if response != None:
            response.close()
        exit()

    try:
        text = response.read().decode(encoding='utf-8')
        result_dict = json.loads(text)
        if response != None:
            response.close()
        return result_dict
    except:
        print('FAILED')
        print(200, url)
        print("FORMAT")
        if response != None:
            response.close()
        exit()


def get_lat_and_lon(result: dict | list, url: str) -> (float, float):
    'Gets the latitude and longitude from the resulting dictionary or list.'
    if type(result) == list:
        result_dict = result[0]
        latitude = float(result_dict['lat'])
        longitude = float(result_dict['lon'])
        return latitude, longitude
    elif type(result) == dict:
        latitude = float(result['lat'])
        longitude = float(result['lon'])
        return latitude, longitude


def get_forecast_url(lat: float, lon: float) -> str:
    'Builds and returns the URL for the hourly forecast using coordinates'
    url = base_nws_search_url + f"{lat},{lon}"
    return url


def get_forecast_coordinates(location: str) -> (float, float):
    'Returns the average coordinates that the weather forecast report is from'
    lat, lon = get_search_coordinates(location)
    forecast_dict = get_forecast(lat, lon)
    coordinates = forecast_dict['geometry']['coordinates'][0]

    coordinates_dict = dict()    
    for coordinate in coordinates:
        coordinates_dict[coordinate[0]] = coordinate[1]

    long_total = 0
    for key in coordinates_dict.keys():
        long_total += key

    lat_total = 0
    for value in coordinates_dict.values():
        lat_total += value

    long_avg = long_total / len(coordinates_dict.keys())
    lat_avg = lat_total / len(coordinates_dict.values())

    return lat_avg, long_avg


def get_reverse_url(lat, long) -> str:
    'Builds and returns the URL that will be used to search for the location.'
    queries = [('lat', lat), ('lon', long), ('format', 'json')]
    url = base_nominatim_reverse_url + urllib.parse.urlencode(queries, encoding='utf-8')
    return url


def get_forecast_location(lat: float, long: float) -> str:
    'Returns the location of the nearest weather forecast to the initial location.'
    reverse_url = get_reverse_url(lat, long)
    reverse_dict = get_result_url(reverse_url)
    forecast_location = reverse_dict['display_name']

    return forecast_location


def get_search_coordinates(location: str) -> (float, float):
    'Returns the nearest coordinates of the location that was searched for'
    search_url = get_search_url(location)
    search_dict = get_result_url(search_url)
    lat, lon = get_lat_and_lon(search_dict, search_url)
    return lat, lon

def get_forecast(lat: float, lon: float) -> dict:
    'Returns a dictionary containing the forecast of the given coordinates'
    weather_url = get_forecast_url(lat, lon)
    weather_dict = get_result_url(weather_url)
    forecast_url = weather_dict['properties']['forecastHourly']
    forecast_dict = get_result_url(forecast_url)
    return forecast_dict