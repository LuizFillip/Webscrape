import Webscrape as wb
import GEO as g
from GNSS import paths, save_last_day
from base import make_dir
import os

def fetch_receivers(
        year = 2017, 
        root = "D:\\"
        ):
    year_folder = paths(year, 0, root = root).rinex
    make_dir(year_folder)
    
    print('starting...', year)
    wb.download_rinex(
            year, 
            365, 
            root = root,
            stations = None
            )
    
    
    save_last_day(
            year,
            doy = 365,
            root = root
            )
    
    return g.stations_near_of_equator(year)


def get_stations(year, root = 'D://'):
    
    path = f'database/GEO/coords/{year}.json'
    
    if os.path.exists(path):
        stations = g.stations_near_of_equator(year)
    else:
        stations = fetch_receivers(
                year = year, 
                root = root
                )
        
    return stations