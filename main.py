import pandas as pd
import datetime as dt
import os
import Webscrape as wb

# download_embrace()

def download_gnss(year = 2014, root = "D:\\"):
    
    year_folder = g.paths(year, 0, root = root).rinex

    os.mkdir(year_folder)
    for doy in range(365, 366, 1):
        print(year, doy)
        wb.download_rinex(
                year, 
                doy, 
                root = "D:\\",
                filter_stations = False
                )

    return 


import GEO as g


year = 2016
doy = 1
root = "D:\\"


stations = g.stations_near_of_equator()

# wb.download_rinex(
#         year, 
#         doy, 
#         root = root,
#         stations = stations
#         )

wb.folders_orbits(year, root = 'D:\\')

wb.download_orbit(
    year, 
    doy, 
    root = root
    )

