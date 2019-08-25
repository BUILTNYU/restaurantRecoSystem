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

import asyncio
import aiofiles
import aiohttp


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
API_KEYS = config.api_keys


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

# Defaults
GLOBAL_OFFSET = 0 #meters
GLOBAL_LIMIT = 50
GLOBAL_SORT_BY = "best_match" # best_match, rating, review_count or distance

#Price
PRICE = {1:"1",2:"1, 2",3:"1, 2, 3",4:"1, 2, 3, 4"}


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
    print("Requesting time:",start)
    
    offsets = [i for i in range(0,600,GLOBAL_LIMIT)]
   

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(get_restaurant(restaurants, current_time, longitude, latitude, radius, price, GLOBAL_LIMIT, offset) for offset in offsets)
        )
    )

    end = time.time()

    print("Number of restaurants actually retrieved",len(restaurants))
    print("Total time it takes:",end-start)

    return restaurants



async def get_restaurant(restaurants, current_time, longitude,latitude, radius, price, limit, offset):
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

    params = {
        'term': term.replace(' ', '+'),
        'longitude': str(longitude),
        'latitude': str(latitude),
        "radius": radius,
        "open_now":str(True),
        "price": price,        
        'limit': limit,
        "offset":offset
    }

    api_key = random.choice(API_KEYS)
    # randomly choose one of the keys

    HEADERS = {
        'Authorization': 'Bearer %s' % api_key,
    }

    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    print('Requesting restaurant with offset {}'.format(offset))

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as resp:
            data = await resp.json()
            print("Responsing time:",time.time())
    try:
        restaurants.extend(data.get("businesses"))
    except:# too many request error
        print(data)


if __name__ == "__main__":
    DEFAULT_TIME = time.strftime('%H:%M')  #get current time
    DEFAULT_LONGITUDE = -73.984345
    DEFAULT_LATITUDE = 40.693899
    DEFAULT_RADIUS = 5000 #meters
    DEFAULT_PRICE = 2 #means "$$". the program reads $$ as 3754, so need to use int to represent it

    restaurants = query_api(DEFAULT_TIME, DEFAULT_LONGITUDE, DEFAULT_LATITUDE, DEFAULT_RADIUS,DEFAULT_PRICE )
