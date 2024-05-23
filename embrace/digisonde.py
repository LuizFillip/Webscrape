import pandas as pd
from base import make_dir
import datetime as dt
# import digisonde as dg
import Webscrape as wb 
import os 
from tqdm import tqdm 


PATH_IONO = 'database/ionogram/'
# PATH_IONO = 'D:\\drift\\'


def iono_dt(f):        
    
    site, date = tuple(f.split('_'))
    
    date_string = date.split('.')[0]
    fmt = '%Y%j%H%M%S'

    return dt.datetime.strptime(date_string, fmt)

def periods(dn, hours = 24):
    
    end = dn + dt.timedelta(hours = hours)


    return pd.date_range(
        dn, end, 
        freq = '10min'
        )
    
    

def FOLDER_NAME(dn, site = 'saa', dirc = 0):
    
    ext = site[0].upper()
    if dirc == 1:
        FOLDER_NAME = dn.strftime('%Y%m%d' +  ext)
    else:
        FOLDER_NAME = dn.strftime(F'{ext}\\%Y\\%j')
    return FOLDER_NAME


def download_ionograms(
        start, 
        site = 'sao_luis', 
        ext = ['RSF'], 
        hours = 25
        ):
    
    make_dir(PATH_IONO)
    save_in = os.path.join(
        PATH_IONO,
        FOLDER_NAME(start, site = site, dirc = 1)
        )
    
    make_dir(save_in)
    
    dn = start.strftime('%Y-%m-%d')
    info = f'{dn}-{site}'
    for dn in tqdm(periods(start, hours), info):
        
        url = wb.embrace_url(
            dn, 
            site = site, 
            inst = 'ionosonde'
            ) 
        
        for link in wb.request(url):
           
            if any(f in link for f in ext) :
                if 'XML' in link:
                    pass
                else:
                    if (iono_dt(link) == dn):
                        # try:
                         
                        wb.download(
                            url, 
                            link,   
                            save_in
                            )
                        # except:
                        #     pass
          



start = dt.datetime(2016, 10, 3, 18)
start = dt.datetime(2017, 8, 30, 18)
start = dt.datetime(2013, 12, 24, 18)
start = dt.datetime(2014, 1, 2, 18)
start = dt.datetime(2022, 7, 24, 18)
start = dt.datetime(2013, 5, 15, 18)


dates = pd.date_range(
    '2022-07-01 21:00', 
    '2022-08-01 21:00', 
    freq = '1D'
    )

for dn in dates:
    for site in ['fortaleza', 'sao_luis', 'cachoeira']:
        download_ionograms(
                dn, 
                site = site, 
                ext = ['RSF', 'SAO'], 
                hours = 14
                )

# periods(start, hours = 14)
