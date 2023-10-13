import Webscrape as wb
import GNSS as gs
from base import make_dir
import os
from tqdm import tqdm 


def download_rinex(
        path,
        stations = None,
        network = 'chile'
        ):
    
    year, doy = int(path.year), int(path.doy)
    
    url = wb.rinex_url(year, doy, network)
    

    if network == 'chile':
        path_to_save = 'D:\\database\\GNSS\\rinex\\chile\\'
        make_dir(path_to_save)
    else:
        path_to_save = path.rinex
        make_dir(path_to_save)
        
    
    if stations is not None:
        receivers_list = wb.filter_rinex(
            url, 
            sel_stations = stations
            )
    else:
        
        receivers_list = wb.request(url)
    
    zipped = ['.zip', '.Z']
    
    for href in receivers_list:
        
        if any([z in href for z in zipped]):
            print('[download_rinex]', year, doy, href)
            wb.download(
                url, 
                href, 
                path_to_save
                )
        
            
            
   
           



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
            

def uncompress_convert(infile):
    
    for sts in os.listdir(infile):
        
        infile = os.path.join(
            infile,
            sts
            )
        
        if sts.endswith('Z'):
            wb.unzip_Z(infile)
        
        
        if sts.endswith('d'):
            wb.crx2rnx(infile)
            