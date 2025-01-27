import pandas as pd
from base import make_dir
import datetime as dt
import Webscrape as wb 
import os 
from tqdm import tqdm 


PATH_IONO = 'database/ionogram/'
PATH_IONO = 'E:\\ionogram\\'

def fn2dt(f):        
    
    site, date = tuple(f.split('_'))
    
    date_string = date.split('.')[0]
    fmt = '%Y%j%H%M%S'

    return dt.datetime.strptime(date_string, fmt)

def periods_by_range(dn, hours = 24):
    
    end = dn + dt.timedelta(hours = hours)

    return pd.date_range(dn, end, freq = '10min')

def periods_by_freq(dn, freq = '1D'):
    return pd.date_range(dn, freq = freq, periods = 365)
    

def FOLDER_NAME(dn, site = 'saa', dirc = 0):
    
    ext = site[:2].upper()
    if dirc == 1:
        FOLDER_NAME = dn.strftime('%Y%m%d' +  ext)
    else:
        FOLDER_NAME = dn.strftime('\\%Y\\%Y%m%d' + ext)
    return FOLDER_NAME

def filter_extensions(
        dn, 
        site = 'sao_luis', 
        ext =  ['SAO', 'RSF']
        ):
    
    url = wb.embrace_url(
        dn, 
        site = 'sao_luis', 
        inst = 'ionosonde'
        ) 
    
    files_filtered = []
    
    for link in wb.request(url):
        if any(f in link for f in ext):
            if 'XML' in link:
                pass
            else:
                files_filtered.append(link)
            
    return url, files_filtered

def download_ionograms(
        periods, 
        site = 'sao_luis', 
        ext = ['SAO', 'RSF']
        ):
    
    start = periods[0]
    make_dir(PATH_IONO)
    folder_year = os.path.join(PATH_IONO, start.strftime('%Y'))
    make_dir(folder_year
        
        )
    save_in = os.path.join(
        folder_year,
        FOLDER_NAME(start, site = site, dirc = 1)
        )
    
    make_dir(save_in)
    
    dn = start.strftime('%Y-%m-%d')
    info = f'{dn}-{site}'
    
    ready_downloaded = os.listdir(save_in)
    
    for dn in tqdm(periods, info):
        
        url, files = filter_extensions(
                dn, 
                site = site, 
                ext =  ext
                )
        for file in files:
            if file in ready_downloaded:
                pass
            else:
                if fn2dt(file) == dn:
                  
                    wb.download(
                        url, 
                        file, 
                        save_in
                        )
                
    return None 
                    



dn = dt.datetime(2018, 1, 1, 22)

periods = periods_by_freq(dn)

download_ionograms(
        periods, 
        site = 'sao_luis', 
        ext = ['SAO', 'RSF']
        )

