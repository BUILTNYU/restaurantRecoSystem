# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import time
import random

from threading import Thread
import threading

#import api key
import config

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= config.api_key


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults
GLOBAL_OFFSET = 0 #meters
GLOBAL_LIMIT = 50
GLOBAL_SORT_BY = "best_match" # best_match, rating, review_count or distance

#Price
PRICE = {1:"1",2:"1, 2",3:"1, 2, 3",4:"1, 2, 3, 4"}

# make request to yelp
def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params,timeout = 5)
    # print("net response time",requests.request('GET', url, headers=headers, params=url_params).elapsed.total_seconds())
    

    return response.json()

# format the request, especially it's parameters
def search(api_key, current_time, longitude,latitude, radius, price, offset, limit):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
        longitude (decimal): decimal	Required if location is not provided. Longitude of the location you want to search nearby.
        latitude (decimal): decimal	Required if location is not provided. Latitude of the location you want to search nearby.
    Returns:
        dict: The JSON response from the request.
    """

    #############################################
    #decide term eg: breakfast, brunch, lunch, dinner
    if current_time <= "10:30":
        term = "breakfast brunch"
    elif current_time <= "14:00":
        term = "brunch lunch"
    else:
        term = "dinner"

    #############################################
    #filter price
    price = PRICE[price]

    url_params = {
        'term': term.replace(' ', '+'),
        'longitude': longitude,
        'latitude': latitude,
        "radius": radius,
        "open_now":True,
        "price": price,        
        'limit': limit,
        "offset":offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

# main program, combine all restaurants 
# do multithreading
def query_api(current_time, longitude, latitude, radius, price):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
        longitude (decimal): decimal	Required if location is not provided. Longitude of the location you want to search nearby.
        latitude (decimal): decimal	Required if location is not provided. Latitude of the location you want to search nearby.
    """
    restaurants = []
    start = time.time()
   
    threads = []

    for num in range(0,600+1-GLOBAL_LIMIT,GLOBAL_LIMIT): #starting from the second one 
        if (num//GLOBAL_LIMIT>=5):
            time.sleep(0.12)
        print(time.time())
        thread = Thread(target=threadRestaurants, args=(restaurants,API_KEY, current_time, longitude, latitude, radius, price, num, GLOBAL_LIMIT))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

        
    end = time.time()

    print("Number of restaurants actually retrieved",len(restaurants))
    print("Total time it takes:",end-start)

    return restaurants

# multithreading
def threadRestaurants(restaurants,api_key, current_time, longitude,latitude, radius, price, offset, limit):
    start = time.time()
    response = search(api_key, current_time, longitude,latitude, radius, price, offset, limit)
    # print(response)

    if response.get("businesses") is None:
        print("Get wrong here",threading.get_ident())
        print(response)
        time.sleep(0.1)
        threadRestaurants(restaurants,api_key, current_time, longitude,latitude, radius, price, offset, limit)
        print("failure",time.time())
    else:   
        restaurants.extend(response.get("businesses"))
        end = time.time()
        print("success",end-start,end)
    

if __name__ == "__main__":
    DEFAULT_TIME = time.strftime('%H:%M')  #get current time
    DEFAULT_LONGITUDE = -73.984345
    DEFAULT_LATITUDE = 40.693899
    DEFAULT_RADIUS = 2000 #meters
    DEFAULT_PRICE = 2 #means "$$". the program reads $$ as 3754, so need to use int to represent it

    restaurants = query_api(DEFAULT_TIME, DEFAULT_LONGITUDE, DEFAULT_LATITUDE, DEFAULT_RADIUS,DEFAULT_PRICE )
