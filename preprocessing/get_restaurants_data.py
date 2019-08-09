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

# This file is used for downloading 5w restaurant information from yelp

from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import time
import random
import pickle
#import api key
import config

DEFAULT_OFFSET = 0 #meters
SEARCH_LIMIT = 50

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

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, location, offset):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
        longitude (decimal): decimal	Required if location is not provided. Longitude of the location you want to search nearby.
        latitude (decimal): decimal	Required if location is not provided. Latitude of the location you want to search nearby.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'location': location,
        'limit': SEARCH_LIMIT,
        "offset":offset,
        "price":"4",
        "sort_by":"review_count"
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)



def query_api():
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
        longitude (decimal): decimal	Required if location is not provided. Longitude of the location you want to search nearby.
        latitude (decimal): decimal	Required if location is not provided. Latitude of the location you want to search nearby.
    """
    start_time = time.time()
    restaurants = []

    # Manhattan
    response = search(API_KEY, "Manhattan", 0)
    businesses = response.get('businesses')
    restaurants.extend(businesses)
    print("Manhattan:",response.get("total"))

    for num in range(SEARCH_LIMIT,1000,SEARCH_LIMIT):
        print(num)
        response = search(API_KEY, "Manhattan", num)
        businesses = response.get("businesses")
        restaurants.extend(businesses)

    # Brooklyn
    response = search(API_KEY, "Brooklyn", 0)
    businesses = response.get('businesses')
    restaurants.extend(businesses)
    print("Brooklyn:",response.get("total"))

    for num in range(SEARCH_LIMIT,1000,SEARCH_LIMIT):
        print(num)
        response = search(API_KEY, "Brooklyn", num)
        try:
            businesses = response.get('businesses')
        except:
            print(businesses)
        restaurants.extend(businesses)

    # The Bronx
    response = search(API_KEY, "The Bronx", 0)
    businesses = response.get('businesses')
    restaurants.extend(businesses)
    print("The Bronx:",response.get("total"))

    for num in range(SEARCH_LIMIT,1000,SEARCH_LIMIT):
        print(num)
        response = search(API_KEY, "The Bronx", num)
        businesses = response.get('businesses')
        restaurants.extend(businesses)

    # Queens
    response = search(API_KEY, "Queens", 0)
    businesses = response.get('businesses')
    restaurants.extend(businesses)
    print("Queens:",response.get("total"))

    for num in range(SEARCH_LIMIT,1000,SEARCH_LIMIT):
        print(num)
        response = search(API_KEY, "Queens", num)
        businesses = response.get('businesses')
        restaurants.extend(businesses)

    # Staten Island
    response = search(API_KEY, "Staten Island", 0)
    businesses = response.get('businesses')
    restaurants.extend(businesses)
    print("Staten Island:",response.get("total"))

    for num in range(SEARCH_LIMIT,1000,SEARCH_LIMIT):
        print(num)
        response = search(API_KEY, "Staten Island", num)
        businesses = response.get('businesses')
        restaurants.extend(businesses)

    end_time = time.time()
    print("request time",end_time-start_time)
    pickle.dump(restaurants, open("restaurants_nyc_4_reviewcount.pyc","wb"))
    print("dump time",time.time()-end_time)



def main():
    try:
        query_api()
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
