import Webscrape as wb
import GNSS as gs
import pandas as pd
from base import make_dir
import os
import datetime as dt
import digisonde as dg



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


        

def download_sao(year):
    
    save_in = f'D:\\iono\\saa\\{year}\\'
    
    make_dir(save_in)
    
    dw = wb.EMBRACE(save_in = save_in)

    # miss_dates = dg.get_missing_dates(year)
    
    miss_dates = dg.missing_dates_2(year)
        
    
    delta = dt.timedelta(hours = 19)
    
    for dn in miss_dates:
        
        dn  = pd.to_datetime(dn) + delta
        
        dw.download_drift(
                dn, 
                ext = ['.SAO', '.RSF']
                )



start = dt.datetime(2015, 4, 9, 20, 0)

for site in ['fortaleza', 'boa_vista', 'sao_luis']:
    wb.download_from_periods(start, site)