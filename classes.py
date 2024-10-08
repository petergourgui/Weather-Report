import datetime
import math
import api
import json

class TempAir:
    def __init__(self, scale: str):
        self._scale = scale

    def print_info(self, forecast_dict: dict, length: int, limit: str) -> None:
        '''
        Prints the maximum or minimum air temperature based on the given length, limit, and forecast dictionary.
        Converts the temperature to whatever the scale is.
        '''
        hourly_forecast = forecast_dict['properties']['periods']
        max_min = hourly_forecast[0]['temperature']
        time = hourly_forecast[0]['startTime']

        if length > len(hourly_forecast):
            length = len(hourly_forecast)
        for i in range(length):
            current = hourly_forecast[i]['temperature']
            current_time = hourly_forecast[i]['startTime']
            if limit == 'MAX' and current > max_min:
                max_min = current
                time = current_time
            if limit == 'MIN' and current < max_min:
                max_min = current
                time = current_time

        if self._scale == 'C' and hourly_forecast[0]['temperatureUnit'] == 'F':
            max_min = (max_min - 32) * (5/9)
        if self._scale == 'F' and hourly_forecast[0]['temperatureUnit'] == 'C':
            max_min = max_min * (9/5) + 32

        max_min = "{:.4f}".format(max_min)
        utc_time = _utc_format(time)
        print(utc_time, max_min)


class Humidity:
    def print_info(self, forecast: dict, length: int, limit: str) -> None:
        'Prints the maximum or minimum humidity as a percentage based on the given length, limit, and forecast dictionary.'
        hourly_forecast = forecast['properties']['periods']
        time = hourly_forecast[0]['startTime']
        max_min = hourly_forecast[0]['relativeHumidity']['value']

        if length > len(hourly_forecast):
            length = len(hourly_forecast)
        for i in range(length):
            current = hourly_forecast[i]['relativeHumidity']['value']
            current_time = hourly_forecast[i]['startTime']
            if limit == 'MAX' and current > max_min:
                max_min = current
                time = current_time
            if limit == 'MIN' and current < max_min:
                max_min = current
                time = current_time
        
        max_min = "{:.4f}".format(max_min) + '%'
        utc_time = _utc_format(time)
        print(utc_time, max_min)


class Wind:
    def print_info(self, forecast: dict, length: int, limit: str) -> None:
        'Prints the maximum or minimum wind speed based on the given length, limit, and forecast dictionary.'
        hourly_forecast = forecast['properties']['periods']
        time = hourly_forecast[0]['startTime']
        max_min = hourly_forecast[0]['windSpeed']
        wind_speed_index = max_min.find(' ')
        max_min = int(max_min[:wind_speed_index])  

        if length > len(hourly_forecast):
            length = len(hourly_forecast)
        for i in range(length):
            current = hourly_forecast[i]['windSpeed']
            wind_speed_index = current.find(' ')
            current = int(current[:wind_speed_index])    
            current_time = hourly_forecast[i]['startTime']
            if limit == 'MAX' and current > max_min:
                max_min = current
                time = current_time
            if limit == 'MIN' and current < max_min:
                max_min = current
                time = current_time
        
        max_min = "{:.4f}".format(max_min)
        utc_time = _utc_format(time)
        print(utc_time, max_min)


class TempFeels:
    def __init__(self, scale: str):
        self._scale = scale

    def print_info(self, forecast: dict, length: int, limit: str) -> None:
        '''
        Prints the maximum or minimum feels like temperature based on the given length, limit, and forecast dictionary.
        Converts the temperature to whatever the scale is.
        '''
        hourly_forecast = forecast['properties']['periods']
        time = hourly_forecast[0]['startTime']
        temp = hourly_forecast[0]['temperature']
        humidity = hourly_forecast[1]['relativeHumidity']['value']
        wind = hourly_forecast[0]['windSpeed']
        wind_speed_index = wind.find(' ')
        wind = int(wind[:wind_speed_index])
        max_min = _calc_feels_like(temp, humidity, wind)

        if length > len(hourly_forecast):
            length = len(hourly_forecast)
        for i in range(length):
            current_temp = hourly_forecast[i]['temperature']
            current_humidity = hourly_forecast[i]['relativeHumidity']['value']
            current_wind = hourly_forecast[i]['windSpeed']
            wind_speed_index = current_wind.find(' ')
            current_wind = int(current_wind[:wind_speed_index])
            current = _calc_feels_like(current_temp, current_humidity, current_wind)
            current_time = hourly_forecast[i]['startTime']
            if limit == 'MAX' and current > max_min:
                max_min = current
                time = current_time
            if limit == 'MIN' and current < max_min:
                max_min = current
                time = current_time

        if self._scale == 'C' and hourly_forecast[0]['temperatureUnit'] == 'F':
            max_min = (max_min - 32) * (5/9)
        if self._scale == 'F' and hourly_forecast[0]['temperatureUnit'] == 'C':
            max_min = max_min * (9/5) + 32

        max_min = "{:.4f}".format(max_min)
        utc_time = _utc_format(time)
        print(utc_time, max_min)


class Precipitation:
    def print_info(self, forecast: dict, length: int, limit: str) -> None:
        '''
        Prints the maximum or minimum precipitation as a percentage based on the given length, 
        limit, and forecast dictionary.
        '''
        hourly_forecast = forecast['properties']['periods']
        time = hourly_forecast[0]['startTime']
        max_min = hourly_forecast[0]['probabilityOfPrecipitation']['value']
        
        if length > len(hourly_forecast):
            length = len(hourly_forecast)
        for i in range(length):
            current = hourly_forecast[i]['probabilityOfPrecipitation']['value']
            current_time = hourly_forecast[i]['startTime']
            if limit == 'MAX' and current > max_min:
                max_min = current
                time = current_time
            if limit == 'MIN' and current < max_min:
                max_min = current
                time = current_time
        
        max_min = "{:.4f}".format(max_min) + '%'
        utc_time = _utc_format(time)
        print(utc_time, max_min)


def _utc_format(time: str) -> str:
    'Converts the local time to UTC and puts it in ISO 8601 format.'
    time = time[:-6]
    date_and_time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    utc_time = date_and_time.astimezone(datetime.timezone.utc)
    utc_time = str(utc_time)
    utc_time = utc_time.replace('+00:00', 'Z')
    utc_time = utc_time.replace(' ', 'T')
    
    return utc_time

def _calc_feels_like(temp: float, humidity: float, wind: float) -> float:
    'Calculates the feels like temperature based on the given temperature, humidity, and wind speed.'
    feels_like = None
    if temp >= 68:
        feels_like = -42.379 + (2.04901523 * temp) + (10.14333127 * humidity) + (-0.22475541 * temp * humidity)\
            + (-0.00683783 * temp * temp) + (-0.05481717 * humidity * humidity) + (0.00122874 * temp * temp * humidity)\
                + (0.00085282 * temp * humidity * humidity) + (-0.00000199 * temp * temp * humidity * humidity)
    elif temp <= 50 and wind > 3:
        feels_like = 35.74 + (0.6215 * temp) + (-35.75 * math.pow(wind, 0.16)) + (0.4275 * temp * math.pow(wind, 0.16))
    else:
        feels_like = temp

    return feels_like


def _get_result_file(file_path: str) -> dict:
    'Opens the file, and returns a dictionary containing information of the file. Returns None if fails.'
    try:
        user_file = open(file_path, 'r')
    except:
        print("FAILED")
        print(file_path)
        print("MISSING")
        return None
    try:
        result = json.load(user_file)
        if type(result) == list:
            result = result[0]
        return result
    except:
        print("FAILED")
        print(file_path)
        print('FORMAT')
        return None



def forecast_dict(target_input: str, weather_input: str, reverse_input: str) -> (dict, str):
    '''
    Determines whether each input is a file or will use online searching. Prints the necessary
    information according to each input. Returns a dictionary containing the forecast of a ceratin location.
    Also returns the name of the location found.
    '''
    target_split = target_input.split()
    target_path = ' '.join(target_split[2:])
    if not target_input.startswith('TARGET NOMINATIM'):
        target_input = _get_result_file(target_path)
        if target_input == None:
            exit()
    
    if not weather_input.startswith('WEATHER NWS'):
        weather_split = weather_input.split()
        weather_input = _get_result_file(' '.join(weather_split[2:]))
        if weather_input == None:
            exit()

    if not reverse_input.startswith('REVERSE NOMINATIM'):
        reverse_split = reverse_input.split()
        reverse_input = _get_result_file(' '.join(reverse_split[2:]))
        if reverse_input == None:
            exit()

    if type(target_input) == dict:
        lat, lon = api.get_lat_and_lon(target_input, None)
    else:
        lat, lon = api.get_search_coordinates(target_path)
    print("Target ", end='')
    if (lat < 0):
        print(lat * -1, "/S ", sep='', end='')
    else:
        print(lat, "/N ", sep='', end='')
    
    if (lon < 0):
        print(lon * -1, "/W ", sep='')
    else:
        print(lon, "/E ", sep='')
        

    if type(reverse_input) == dict:
        location_name = reverse_input['display_name']
    else:
        location_name = api.get_forecast_location(lat, lon)

    if type(weather_input) == dict:
        forecast_dict = weather_input
    else:
        forecast_dict = api.get_forecast(lat, lon)

    return forecast_dict, location_name