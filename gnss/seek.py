import Webscrape as wb
import GEO as g
import GNSS as gs
from base import make_dir
import os
import json


def save_last_day(
        year = 2016,
        doy = 365
        ):
    
    print('[save_last_day] processing the last day')
    
    make_dir(gs.paths(year).json)

    data = gs.save_atributes(gs.paths(year, doy))
    
    print('[save_last_day] converting into geodesic')
    
    save_in = f'database/GEO/coords/{year}.json'
    dic = gs.convert_positions_to_coords(data)
    with open(save_in, "w") as f:
        json.dump(dic, f)
     

def fetch_receivers(path):
    year_folder = path.rinex
    make_dir(year_folder)
    
    print('starting...', path.year)
    wb.download_rinex(
            path.year, 
            365, 
            root = path.root,
            stations = None
            )
    
    save_last_day(
            path.year,
            doy = 365,
            root = path.root
            )
    
    return g.stations_near_of_equator(path.year)


def get_stations(path):
    
    path_coord = f'database/GEO/coords/{path.year}.json'
    
    if os.path.exists(path_coord):
        stations = g.stations_near_of_equator(path.year)
    else:
        stations = fetch_receivers(path)
        
    return stations