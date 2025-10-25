import os
import GNSS as gs
import pandas as pd
import shutil



def find_missing_values(a, b):
    return list(set(a) ^ set(b))


def mgex2gnss_week(fname):
    
    args = fname.split('_')[1]
    
    year = int(args[:4])
    doy =  int(args[4:7])
    
    week, number = gs.gpsweek_from_doy_and_year(year, doy)
    
    return week, number

def date_list_from_orbits(
        orbit_list:list[str]):
    
    out = []
    
    for fname in orbit_list:
        
        try:
            week = int(fname[3:7])
            number = int(fname[7])
        except:
            week, number = mgex2gnss_week(fname)
        
        out.append(gs.date_from_gpsweek(
                    week, 
                    number
                    )
            )
        
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

def missing_roti(year):
    doys = list(range(1, 366, 1))
    
    path = gs.paths(year).roti
    
    files = [int(f[:-4]) for f in os.listdir(path)]
    
    return find_missing_values(files, doys)

def missing_tec(year):
    path = gs.paths(year).tec

    out = []
    
    for ln in os.listdir(path):
        
        if len(os.listdir(path + ln)) <= 11:
            out.append(int(ln))
                  
    return out 




def dn2mgex(dn):
    year, doy = dn.year, dn.timetuple().tm_yday
    
    return f'IGS0OPSFIN_{year}{doy}0000_01D_15M_ORB.SP3'

def dn2cod(dn):
    week, number = gs.gpsweek_from_date(dn)
    return  f'cod{week}{number}.eph'

def dn2sp3(dn, const = 'igv'):
    week, number = gs.gpsweek_from_date(dn)
    return  f'{const}{week}{number}.sp3'

def dn2com(dn):
    week, number = gs.gpsweek_from_date(dn)
    return f'com{week}{number}.eph'


def copy2com(src_folder, dst_folder, year = 2022):
    
    path = gs.paths(year)

    src_cod = path.orbit(const = src_folder)
    cod = date_list_from_orbits(os.listdir(src_cod))


    src_com = path.orbit(const = dst_folder)
    com = date_list_from_orbits(os.listdir(src_com))
    
    times_m = find_missing_values(cod, com)
    
    for dn in times_m:
        if dn not in com:
            
            # try:    
            #     src = os.path.join(
            #         src_cod, 
            #         dn2sp3(dn, const = src_folder)
            #         )
            # except:
            
            src = os.path.join(src_cod, dn2cod(dn))
                
                
            dst = os.path.join(src_com, dn2com(dn))
            
            print('[copy_files]', dn)
            shutil.copy(src, dst)



