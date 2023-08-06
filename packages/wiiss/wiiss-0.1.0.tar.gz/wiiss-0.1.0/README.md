# wiiss
 -- short for 'where is iss' - provides the current location of the ISS based on data from the open-notify and nominatim osm apis

Just call `wiis.wiis()` to print the location information

There isn't much behind it, the docstrings might help to understand the details
    
    
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
        :return: dict: json respneses (if successfull)
        """
    
    
    def getCoords():
        """
        specifically return current coords of the iss
        :return: tuple: latitude and longitude
        """
    
    
    def getRawLocation(latitude, longitude):
        """
        requests the location data based on the coords from the nominatim api
        :param latitude: float: latitude coordinate
        :param longitude: float: longitude coordinate
        :return: dict: raw location information
        """


    def getISSLocationData():
        """
        combines the coords request and the location info request
        :return: dict: usable location data
        """
    
    
    def wiiss():
        """prints the rough location of the International Space Station"""
