import classes


def get_queries() -> list: 
    '''
    Asks the user for weather queries until there are no more queries, 
    which will then return a list of all the previous inputs.
    '''
    weather_queries = []
    while True:
        query = input()
        if query == 'NO MORE QUERIES':
            break
        weather_queries.append(query)
    return weather_queries


def _print_credits(openstreet_forward: bool, openstreet_reverse: bool, nws_data: bool) -> None:
    'Prints credit for anything that was used online. Only prints credits if the tool was used.'
    if openstreet_forward:
        print("**Forward geocoding data from OpenStreetMap")
    if openstreet_reverse:
        print("**Reverse geocoding data from OpenStreetMap")
    if nws_data:
        print("**Real-time weather data from National Weather Service, United States Department of Commerce")


def run_program() -> None:
    'Runs the program from start to finish.'
    classes_dict = {'TEMPERATURE AIR C': classes.TempAir('C'), 'TEMPERATURE AIR F': classes.TempAir('F'),\
                    'TEMPERATURE FEELS C': classes.TempFeels('C'), 'TEMPERATURE FEELS F': classes.TempFeels('F'),\
                    'HUMIDITY': classes.Humidity(), 'WIND': classes.Wind(), 'PRECIPITATION': classes.Precipitation()}

    target_input = input()
    weather_input = input()
    queries_list = get_queries()
    reverse_input = input()
    openstreet_forward = False
    openstreet_reverse = False
    nws_data = False
    if target_input.startswith('TARGET NOMINATIM'):
        openstreet_forward = True
    if weather_input.startswith('WEATHER NWS'):
        nws_data = True
    if reverse_input.startswith('REVERSE NOMINATIM'):
        openstreet_reverse = True

    forecast_dict, location_name = classes.forecast_dict(target_input, weather_input, reverse_input)
    print(location_name)
    
    for query in queries_list:
        query_split = query.split()
        info = ''
        if len(query_split) == 5:
            info = query_split[0] + ' ' + query_split[1] + ' ' + query_split[2]
        else:
            info = query_split[0]

        classes_dict[info].print_info(forecast_dict, int(query_split[-2]), query_split[-1])
    
    _print_credits(openstreet_forward, openstreet_reverse, nws_data)


if __name__ == '__main__':
    run_program()