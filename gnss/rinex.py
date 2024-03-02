import Webscrape as wb
import GNSS as gs
from base import make_dir
import os
from tqdm import tqdm 

PATH_CHILE = 'D:\\database\\GNSS\\rinex\\chile\\'


def filter_by_stations(href, stations):
    if any([z in href for z in stations]):
        ends = ['d.zip', 'd.Z', 'crx.gz']
        if any([href.endswith(e) for e in ends]):
           return True
        else:
           return False
    else:
        return False
    

def download_rinex(
        path,
        stations = None,
        network = 'chile'
        ):
    
    year, doy = int(path.year), int(path.doy)
    
    url = wb.rinex_url(year, doy, network)

    path_to_save = path.rinex
    make_dir(path_to_save)
    
    for href in wb.request(url):
        
        if filter_by_stations(href, stations):
            print('[download_rinex]', year, doy, href)
            wb.download(
                url, 
                href, 
                path_to_save
                )
        
    uncompress_convert(path.rinex)

    return None

def extract_and_convert(path):
    
    files = os.listdir(path.rinex)
      
    for fname in tqdm(files):
        infile = os.path.join(path.rinex, fname)
        if fname.endswith('o'):
            continue
        elif fname.endswith('d'):
           
            wb.crx2rnx(infile)
        else:
            os.remove(infile)
            
    return None
            

def uncompress_convert(path_root):
    
    for sts in os.listdir(path_root):
        path_in = os.path.join(path_root, sts)
        
        if sts.endswith('Z'):
            print('unziping...', sts)
            wb.unzip_Z(path_in)
            
        elif sts.endswith('zip'):
            print('unziping...', sts)
            wb.unzip_zip(path_in)
        
        elif sts.endswith('gz'):
            print('unziping...', sts)
            wb.unzip_gz(path_in)
            
    for sts in os.listdir(path_root):
        path_in = os.path.join(path_root, sts)
        if sts.endswith('d') or sts.endswith('crx'):
            print('converting...', sts)
            wb.crx2rnx(path_in)
            
    return None
            

        
def test_one_day_download():
    
    year, doy = 2019, 1
    
    
    
    path = gs.paths(year, doy, root = 'D:\\')
        
    # download_rinex(
    #             path,
    #             stations,
    #             network = 'igs'
    #             )

year = 2018
doy = 1

def test_filter_stations():

    url = wb.rinex_url(year, doy, network = 'garner')
    
    stations = ['areg', 'riop',  'antf', 'iqqe', 'qui3']
    
    for href in wb.request(url):
        if filter_by_stations(href, stations):
            print(href)