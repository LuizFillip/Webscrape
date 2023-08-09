import Webscrape as wb
import GEO as g
from GNSS import paths, save_last_day

import os


def download_gnss(stations, year, root = "D:\\"):
    
    wb.folders_orbits(year, root = root)
    
    doy_min = wb.minimum_doy(year, root = root)
        
    for doy in range(doy_min, 365, 1):
        print(doy, year)

        wb.download_rinex(
                year, 
                doy, 
                root = root,
                stations = stations
                )

        wb.download_orbit(
            year, 
            doy, 
            root = root
            )

    return None



def get_last_day_receivers(
        year = 2017, 
        root = "D:\\"
        ):
    year_folder = paths(year, 0, root = root).rinex
    wb.make_dir(year_folder)
    
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

year = 2016

path = f'database/GEO/coords/{year}.json'

if os.path.exists(path):
    stations = g.stations_near_of_equator(year)
else:
    stations = get_last_day_receivers(
            year = year, 
            root = "D:\\"
            )
    
download_gnss(stations, year = year, root = "D:\\")