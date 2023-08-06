#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__credits__ = ["Robin Weiland", ]
__copyright__ = "Copyright 2019, Robin Weiland"

__date__ = "2019-05-04"
__version__ = "0.1.0"
__license__ = "MIT"

__status__ = "In Development"
__maintainer__ = "Robin Weiland"

__all__ = ['wiiss']

"""This module provides a function to return the rough current location of the International Space Station
by using the open-notify and the nominatim osm apis"""

from requests import get
from requests.exceptions import ConnectionError

OPEN_NOTIFY_API = 'http://api.open-notify.org/iss-now.json'  # gets current iss coordinates, nothing to specify
OSM_API = 'https://nominatim.openstreetmap.org/reverse?' \
          'accept-language=en&' \
          'format=geocodejson&' \
          'lat={latitude}&' \
          'lon={longitude}&' \
          'zoom=18&' \
          'addressdetails=1'  # retrieves location info from coords (or at least tries to -> GeoLocationIndeterminable)


class ResponseFailed(Exception):
    """Any attempt (not api specific) to connect to an url failed, probably no connection"""
    pass


class BadStatusCode(Exception):
    """API request responded with an unexpected response code, anything but 200 in this case"""
    pass


class GeoLocationIndeterminable(Exception):
    """The Nominatim reverse api seems to struggle to resolve some coords to readable information, this API seems to
    be the best solution so far but this exception might occur from time to time. Try it later"""
    pass


def handleApiRequest(url):
    """
    retrieves json data from the apis
    :param url: str: the api url
    :return: dict: json responses (if successful)
    """
    try: response = get(url)
    except (ConnectionError,): raise ResponseFailed('Reaching {} failed'.format(url))
    if response.status_code == 200: return response.json()
    else: raise BadStatusCode('{} returned a {} code'.format(url, response.status_code))


def getCoords():
    """
    specifically return current coords of the iss
    :return: tuple: latitude and longitude
    """
    request = handleApiRequest(OPEN_NOTIFY_API)
    return request['iss_position']['latitude'], request['iss_position']['longitude'],


def getRawLocation(latitude, longitude):
    """
    requests the location data based on the coords from the nominatim api
    :param latitude: float: latitude coordinate
    :param longitude: float: longitude coordinate
    :return: dict: raw location information
    """
    request = handleApiRequest(OSM_API.format(latitude=latitude, longitude=longitude))
    return request


def getISSLocationData():
    """
    combines the coords request and the location info request
    :return: dict: usable location data
    """
    coords = getCoords()
    raw = getRawLocation(*coords)
    if 'error' in raw:
        raise GeoLocationIndeterminable('The nominatim-api could not determine the exact '
                                        'location description for {} : {}'.format(*coords))
    data = raw['features'][0]['properties']['geocoding']
    return data


def wiiss():
    """prints the rough location of the International Space Station"""
    locationData = getISSLocationData()
    print(f"The ISS is now roughly over {locationData['label']}")
    input('press enter to continue...')


if __name__ == '__main__': wiiss()
