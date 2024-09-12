import pandas as pd
from base import make_dir
import datetime as dt
# import core as c
import Webscrape as wb 
import os 
from tqdm import tqdm 


PATH_IONO = 'database/ionogram/'
PATH_IONO = 'E:\\ionogram\\'

def iono_dt(f):        
    
    site, date = tuple(f.split('_'))
    
    date_string = date.split('.')[0]
    fmt = '%Y%j%H%M%S'

    return dt.datetime.strptime(date_string, fmt)

def periods(dn, hours = 24):
    
    end = dn + dt.timedelta(hours = hours)

    return pd.date_range(dn, end, freq = '10min')
    
    

def FOLDER_NAME(dn, site = 'saa', dirc = 0):
    
    ext = site[0].upper()
    if dirc == 1:
        FOLDER_NAME = dn.strftime('%Y%m%d' +  ext)
    else:
        FOLDER_NAME = dn.strftime('\\%Y\\%Y%m%d' + ext)
    return FOLDER_NAME


def download_ionograms(
        start, 
        site = 'sao_luis', 
        ext = ['RSF'], 
        hours = 25
        ):
    
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
                    try:
                        if (iono_dt(link) == dn):
                            # try:
                             
                            wb.download(
                                url, 
                                link,   
                                save_in
                                )
                    except:
                        pass
                    
    return None



start = dt.datetime(2016, 10, 3, 18)
start = dt.datetime(2017, 8, 30, 18)
start = dt.datetime(2013, 12, 24, 18)
start = dt.datetime(2014, 1, 2, 18)
start = dt.datetime(2022, 7, 24, 18)
start = dt.datetime(2013, 5, 15, 18)


def download_dates(date):
    
    import core as c 
    
    dates = c.undisturbed_days(date, threshold = 8) 
    sites  = ['fortaleza', 'sao_luis',
              'cachoeira', 'boa_vista']
    
    # delta = dt.timedelta(hours = 20)
    for dn in dates:
    
        for site in sites:
            download_ionograms(
                    dn, 
                    site = site, 
                    ext = ['RSF', 'SAO'], 
                    hours = 14
                    )



def download_by_dates(site, dn):

    start = dn - dt.timedelta(days = 2)
    end = dn + dt.timedelta(days = 3)
    
    
    dates = pd.date_range(start, end)
    
    for dn in dates:
        download_ionograms(
                dn, 
                site = site, 
                ext = ['RSF', 'SAO'], 
                hours = 18
                )
        

def download_sites_by_date(dn):
    
    sites  = ['sao_luis', 'cachoeira', 'boa_vista']
    
    for site in sites:
        
        download_ionograms(
                        dn, 
                        site, 
                        ext = ['SAO', 'RSF'], 
                        hours =  11
                        )
        
    return None 


dates = [
    dt.datetime(2015, 12, 2, 9), 
    dt.datetime(2015, 12, 13, 9),
    dt.datetime(2015, 12, 16, 9), 
    dt.datetime(2015, 12, 18, 9),
    dt.datetime(2015, 12, 29, 9)
    ]

for dn in dates:
    download_sites_by_date(dn)