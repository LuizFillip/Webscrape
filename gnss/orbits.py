import Webscrape as wb
import GNSS as gs
from base import make_dir
import os
from tqdm import tqdm 


def download_orbit(
        year: int, 
        doy: int, 
        const = "com", 
        net = 'igs'
        ):
    
    wb.folders_orbits(year)
    
    fname, url = wb.orbit_url(
        year, doy, 
        network = net, 
        const = const
        )

    path_to_save = gs.paths(
        year, doy).orbit(const = const)
    
    for href in wb.request(url):
        if fname in href:
            print('[download_orbit]', year, doy, href)
            files = wb.download(
                url, href, path_to_save)
            wb.unzip_orbit(files)
            
    return path_to_save
                


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
          


def download_missing_mgex(
        year = 2022, 
        const = 'com'
        ):
    
    wb.folders_orbits(year)

    for dn in wb.missing_times(year, 'com'):
    
        url, fname = wb.mgex_fname(dn)
        
        doy = dn.timetuple().tm_yday
        
        path_to_save = gs.paths(
            year, doy
            ).orbit(const = 'cod')
        
        for href in wb.request(url):
            
            if fname in href:
               
                print('[download_orbit]', dn, href)
                
                files = wb.download(
                    url, href, path_to_save)
                                
                wb.unzip_gz(files)

    return None


def download_missing_other_const(
        in_const = 'com',
        out_const = 'cod',
        year = 2020
        ):
    
    
    for dn in wb.missing_times(year, in_const):
        doy = dn.timetuple().tm_yday
        wb.download_orbit(
                year, 
                doy, 
                const = out_const, 
                net = 'igs'
                )

    wb.copy2com(
        out_const, 
        in_const, 
        year = 2020)
