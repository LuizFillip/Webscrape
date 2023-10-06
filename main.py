import Webscrape as wb
import GNSS as gs
import pandas as pd
from base import make_dir
import os
import datetime as dt
import digisonde as dg



def download_gnss(year):
    
    # stations = wb.get_stations(gs.paths(year))
    
    # wb.folders_orbits(year)
            
    for doy in range(1, 366, 1):
        
        path = gs.paths(year, doy)
        
        wb.download_rinex(
                path,
                wb.miss_stations(path)
                )

        # wb.download_orbit(
        #     year, 
        #     doy
        #     )

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



# year = 2022


# download_gnss(year)