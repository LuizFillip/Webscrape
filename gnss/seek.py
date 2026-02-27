import Webscrape as wb
import GEO as g
import GNSS as gs
from base import make_dir
import os
import json

def date_from_fname(fname):
    week = int(fname[3:7])
    number = int(fname[7:8])

    return gs.doy_from_gpsweek(week, number)




class minimum_doy(object):
    
    def __init__(self, path):
        
        self.path = path
        
    def orbit(self, const = 'com'):
        
        path = self.path.orbit(const)
        
        return max([date_from_fname(f)[1] for f 
             in os.listdir(path)])

    @property
    def rinex(self):
        return self.cond_max(
            self.list_doy(self.path.rinex)
            )
    
    @property   
    def tec(self):
        return self.cond_max(
            self.list_doy(self.path.tec)
            )
    
    @property   
    def roti(self):
        list_doy = [
            int(f.replace('.txt', '')) 
            for f in os.listdir(self.path.roti)
            ]
        return self.cond_max(list_doy)
    
    @staticmethod
    def list_doy(path):
        return [int(f) for f in 
                os.listdir(path) if f != '365']
    
    @staticmethod
    def cond_max(list_doy):
        if len(list_doy) == 0:
            return 1
        else:
            return max(list_doy)
        


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
     

def fetch_receivers(path, doy = 365):
    
    print(f'[fetch_receivers] downloading 365 in {path.year}')
    
    year_folder = path.rinex
    make_dir(year_folder)
    
    print('starting...', path.year)
    
    year = int(path.year)
    wb.download_rinex(
            year, 
            doy, 
            stations = None
            )
    
    save_last_day(
            year,
            doy = doy,
            )
    
    return g.stations_near_of_equator(path.year)


def get_stations(path):
    
    print('[get_stations] loading nearby receivers')
    
    path_coord = f'database/GEO/coords/{path.year}.json'
    
    if os.path.exists(path_coord):
        stations = g.stations_near_of_equator(path.year)
    else:
        stations = fetch_receivers(path)
        
    return stations


def delete_far_of_equator(path):
    
    print('[delete_files_in_last] deleting far away receivers')

    
    stations = get_stations(path)
    
    out_folder = [f[:4] for f in os.listdir(path.rinex)]
    
    
    for i, sts in enumerate(out_folder):
        if sts not in stations:
            try:
                os.remove(path.fn_rinex(sts))
            except:
                os.remove(path.fn_rinex(sts, zip_f = True))
    return None 
