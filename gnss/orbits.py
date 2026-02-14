import Webscrape as wb
import GNSS as gs
import base as b
import shutil
import pandas as pd 
import os 
import datetime as dt 

infos = {
    "igs": 'https://igs.bkg.bund.de/root_ftp/IGS/products/', 
    "igs2": 'https://files.igs.org/pub/', 
    'garner': 'http://garner.ucsd.edu/pub/products/',
    
    }

consts = ["igl", "igr"]# 'igv', 'cod', 'igs', 'mgex', 'com']

def folders_orbits(year):
    
    b.make_dir(gs.paths(year).orbit_base)
    
    for const in consts:
        
        path_to_save = gs.paths(year).orbit(const = const)
        
        b.make_dir(path_to_save)
        
    return None 

def orbit_url(
        dn, 
        network:str = "igs", 
        const:str = "igr"
        ):
    
    """
    Build urls and filenames from year, doy and GNSS        
    system
    """
    
    week, number = gs.dn2gpsweek(dn)

    strd = dn.strftime('%j')
    url = infos[network]

    if network == "igs":

        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        elif const == "igl":
            url += f"glo_orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
        elif const == 'com':
            url += f"mgex/{week}/"
            filename = f'{const}{week}{number}.eph.Z'
            
        elif const == 'cod':
            
            url += f"orbits/{week}/"
            filename = f'cod{week}{number}.eph.Z'
            
        elif const == 'igv':
            url += f"orbits/{week}/"
            filename = f'igv{week}{number}_00.sp3.Z'
            
        elif const == 'igs':
            url += f"orbits/{week}/"
            filename = f'igs{week}{number}.sp3.Z'
            
        elif const == 'mgex':
            year = dn.year
            filename = f'IGS0OPSULT_{year}{strd}1800_02D_15M_ORB.SP3.gz'
            url += f"{week}/"
    
    elif network == 'garner':
        
        if const == "igv":
            filename = f'igv{week}{number}_00.sp3.Z'
            url += f"{week}/"
            
        elif const == 'esa':
            filename = f'esa{week}{number}.sp3.Z'
            url += f"{week}/"
         
    elif network == "igs2":
        
        if const == "igr":
            url += f"orbits/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"

        
        elif const == "igl":
            url += f"glonass/products/{week}/"
            filename = f"{const}{week}{number}.sp3.Z"
            
        elif const == 'igv':
            url += f"glonass/products/{week}/"
            filename = 'com{week}{number}.eph.Z'
        

    return filename, url


def download_single(year = 2018, doy = 260):
    stations = wb.get_stations(gs.paths(year))
    wb.download_rinex(
            year, 
            doy,
            stations = stations
            )
    
    return None 


def fn2dn(fn):
    gpsweek, dayofweek = int(fn[3:7]), int(fn[7:8])  
    return gs.gpsweek2dn(gpsweek, dayofweek)

def copy_rewrite(src):
    
    dst = src.replace('igv', 'cod').replace('_00', '')
    shutil.copy(src, dst)
    
    return None 

def download_orbit(
        dn, 
        const = "igv", 
        network = 'garner', 
        root = 'C:\\'
        ):

    fname, url = orbit_url(
        dn, 
        network = network, 
        const = const
        )
            
   
      
   
            
        
    
    return None 
    

def last_download(year, const, root = 'E:\\'):
        
    path = gs.paths(year, doy = 0, root = root)
    
    pin = path.orbit(const = const) 
    
    b.make_dir(path.orbit_base)
    
    path_to_save = path.orbit(const = const)
    
    b.make_dir(path_to_save)
    
    files = [fn2dn(fn) for fn in os.listdir(pin)]
    
    if len(files) == 0:
        return dt.datetime(year, 1, 1)
    else:
        return max(files) 
    
def igv_sp3_name(fn):
    return fn.replace('_00', '').replace('.Z', '')

def rename_igv(year, root = 'E:\\'):
    
    path_in = gs.paths(year, root = root).orbit(const = 'igv')
    
    for fn in os.listdir(path_in):
        src = os.path.join(path_in, fn)
        dst = os.path.join(path_in, fn.replace('_00', ''))
        os.rename(src, dst)
        
    return None
        
def download_orbits_dialy(
        year = 2022, 
        root = 'E:\\', 
        const = 'esa',
        network = 'garner'
        ):
    
    sts, end = f'{year}-01-01', f'{year}-12-31'
      
    # sts = last_download(year, const, root = root)
    
    # print(sts)
    # print('Starting downloading', year)
    for dn in pd.date_range(sts, end):
        
        path = gs.paths(dn, root = root)
        
        fn, url = orbit_url(
            dn, 
            network = network, 
            const = const
            )
        
        path_in = os.path.join(
            path.orbit(const = const), 
            igv_sp3_name(fn)
            )
        
        b.make_dir(path.orbit_base)
        
        path_to_save = path.orbit(const = const)
        
        b.make_dir(path_to_save)
        
        if os.path.exists(path_in):
            continue
        else:
            
                 
            for href in wb.request(url):
                if fn in href:        
                    print('[download_orbit]', dn.date(), href)
                     
                    path_in = wb.download(
                        url, 
                        href, 
                        path_to_save
                        )
                    wb.unzip_Z(path_in)
    #     try:
    #         download_orbit(
    #             dn, 
    #             const = const, 
    #             network = network, 
    #             root = root
    #             )
    #     except:
    #         continue 
        
    # if const == 'igv':
    #     rename_igv(year, root = root)
        
    return None 

year = 2010
download_orbits_dialy(
        year = year, 
        root = 'F:\\',
        const = 'igv', 
        )


# rename_igv(year, root = 'F:\\')

