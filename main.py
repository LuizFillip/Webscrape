import Webscrape as wb
import GNSS as gs
import pandas as pd
from base import make_dir
import os

def download_gnss(year):
    
    stations = wb.get_stations(gs.paths(year))
    
    wb.folders_orbits(year)
    
    doy_max = wb.minimum_doy(year)
        
    for doy in range(35, 40, 1):
        print(doy_max, year)

        wb.download_rinex(
                year, 
                doy,
                stations = stations
                )

        wb.download_orbit(
            year, 
            doy
            )

    return None


def download_single(year = 2018, doy = 260):
    stations = wb.get_stations(gs.paths(year))
    wb.download_rinex(
            year, 
            doy,
            stations = stations
            )
    
def download_orbits(
        year = 2022, 
        const = 'com'
        ):
    
    for doy in wb.missing_times(year, const):
        
        wb.download_orbit(
                year, 
                doy, 
                const = 'com', 
                net = 'igs'
                )
        
        


import datetime as dt

def download_sao():
    
    save_in = 'D:\\iono\\saa\\'
    dw = wb.EMBRACE(save_in = save_in)
    
    dates = pd.date_range(
        dt.datetime(2013, 1, 1, 20), 
        dt.datetime(2013, 6, 1, 20), 
        freq = '1D'
        )
    
    for dn in dates:
        dw.download_drift(
                dn, 
                ext = ['.SAO']
                )
        
download_sao()