import os
import GNSS as gs
import pandas as pd

def find_missing_values(a, b):
    return list(set(a) ^ set(b))

def date_list_from_orbits(
        orbit_list
        ):
    
    out = []
    
    for fname in orbit_list:
    
        gnss_week = int(fname[3:7])
        gnss_number = int(fname[7])
        
        out.append(
            pd.to_datetime(
                gs.date_from_gpsweek(
                    gnss_week, 
                    gnss_number
            )))
        
    return sorted(out)


def orbit_year_list(
        year, 
        const = 'igl'
        ):

    dates = pd.date_range(
        f'{year}-01-01', 
        f'{year}-12-31',
        freq = '1D')
    
    dates = [date.date() for date in dates]
    
    out = []
    
    if const == 'com':
        ext = 'eph'
    else:
        ext = 'sp3'
        
        
    for date in dates:
    
        week, number = gs.gpsweek_from_date(date)
        
        out.append(f'{const}{week}{number}.{ext}')
        
    return sorted(out)


def missing_times(year, const):

    dummy = orbit_year_list(year, const = const)
    orbits = os.listdir(gs.paths(year).orbit(const))
    
    orbit_list = find_missing_values(dummy, orbits)
        
    return date_list_from_orbits(orbit_list)



def find_doy_missing(year):
    path = gs.paths(year).rinex

    out = []
    
    for ln in os.listdir(path):
        
        if len(os.listdir(path + ln)) == 0:
            out.append(int(ln))
                  
    return out 

# import Webscrape as wb 


year = 2022
const = 'com'
# dn = missing_times(year, const)