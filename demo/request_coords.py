import numpy as np
import requests
import pandas as pd

def get_coords(city, country):
    
    """
    Function for get latitude and longitude
    from name of city and country. Use 'Request' library
    for scrapy these informations
    -----
    Example
    -------
    get_coords(city = 'Campina Grande', 
               country = 'Brazil')
    >>> (-7.22, -35.88)
    """

    url_site = "https://nominatim.openstreetmap.org/?" 
    
    addressdetails = f"addressdetails=1&q={city}+{country}&format=json&limit=1"
    
    response = requests.get(url_site + addressdetails).json()
    
    lat = float(response[0]["lat"])
    lon = float(response[0]["lon"])
    return round(lat, 2), round(lon, 2) 
 
        


def main(cities, countries):
    '''
    Example
    Enter with a list of sites and their country   
    '''

    output = []

    for city, country in zip(cities, 
                             countries):
        try:
            lat_geo, lon_geo = get_coords(city, country)
            #lat_mag, lon_mag = string_to_list(0, lat_geo, lon_geo)
            
            output.append([f"{city}, {country}", 
                               lat_geo, lon_geo])
        except:
            print(f"{city}, {country} doesn't work")
            output.append([f"{city}, {country}", 
                               np.nan, np.nan])
    
    df = pd.DataFrame(output)

    
    return df

