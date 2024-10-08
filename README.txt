Weather Report

The project is a Python application that allows users to retrieve and display weather information based on user-defined queries.
It integrates data from OpenStreetMap for geocoding and the National Weather Service for real-time weather data.

Features: 

Retrieve maximum or minimum temperature, humidity, wind speed, feels-like temperature, and precipitation probability.
Supports both Celsius and Fahrenheit temperature scales.
Provides real-time weather data from the National Weather Service.
Allows users to input multiple queries in a single session, including up to how many hours.
Outputs weather information in a user-friendly format.

How to Run:
1. Run the program by executing main.py
2. Enter the target input for location geocoding in the format:
    TARGET NOMINATIM <city, state>
3. Enter the weather data input in the format:
    WEATHER NWS
4. Input your weather queries. Supported queries include:
    TEMPERATURE AIR C <hours>
    TEMPERATURE AIR F <hours>
    TEMPERATURE FEELS C <hours>
    TEMPERATURE FEELS F <hours>
    HUMIDITY <hours>
    WIND <hours>
    PRECIPITATION <hours>
    *Each query should end with the desired the limit type (e.g., MAX or MIN)*
5. To finish entering queries, type:
    NO MORE QUERIES
6. Enter the reverse geocoding input in the format:
    REVERSE NOMINATIM