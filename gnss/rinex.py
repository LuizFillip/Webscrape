import Webscrape as wb
import GNSS as gs
from base import make_dir
import os
from tqdm import tqdm 


def download_rinex(
        path,
        stations = None
        ):
    
    year, doy = int(path.year), int(path.doy)
    url = wb.rinex_url( year, doy)
    
    path_to_save = path.rinex     
    path_to_save = make_dir(path_to_save)
    
    if stations is not None:
        receivers_list = wb.filter_rinex(
            url, 
            sel_stations = stations
            )
    else:
        
        receivers_list = wb.request(url)
            
    for href in receivers_list:
        
        if '.zip' in href:
            print('[download_rinex]', year, doy, href)
            files = wb.download(url, href, path_to_save)
            
            wb.unzip_rinex(files, path_to_save)
            
            
    for sts in os.listdir(path_to_save):
        infile = os.path.join(
            path_to_save,
            sts
            )
        if sts.endswith('d'):
            wb.crx2rnx(infile)
            
           
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
                
            






def extract_and_convert():
    
    path = gs.paths(2021, 1)
    files = os.listdir(path.rinex)
      
    for fname in tqdm(files):
        infile = os.path.join(path.rinex, fname)
        if fname.endswith('o'):
            continue
        elif fname.endswith('d'):
           
            wb.crx2rnx(infile)
        else:
            os.remove(infile)
            

url = 'http://gps.csn.uchile.cl/data/2013/001/'