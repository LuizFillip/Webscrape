import pandas as pd
from base import make_dir
import datetime as dt
import digisonde as dg
import Webscrape as wb 
import os 
from tqdm import tqdm 


PATH_IONO = 'database/iono/'

def download_sao(year):
    
    save_in = os.path.join(
        PATH_IONO,
        f'{year}'
        )
    
    make_dir(save_in)
    
    dw = wb.EMBRACE(save_in = save_in)

    # miss_dates = dg.get_missing_dates(year)
    
    miss_dates = dg.missing_dates_2(year)
        
    
    delta = dt.timedelta(hours = 19)
    
    for dn in miss_dates:
        
        dn  = pd.to_datetime(dn) + delta
        
        dw.download_drift(
                dn, 
                ext = ['.SAO', '.RSF']
                )

def iono_dt(file):        
    args = file[:-4].split("_")

    year = int(args[1][:4])
    doy = int(args[1][4:7])
    hour = int(args[1][7:9])
    minute = int(args[1][9:11])
    second = int(args[1][11:])
    date = (dt.date(year, 1, 1) + 
            dt.timedelta(doy - 1))

    day = date.day
    month = date.month

    return dt.datetime(
        year, 
        month, 
        day,
        hour, 
        minute, 
        second
        )

def periods(dn, end = False):
    
    if end:
        end = dn + dt.timedelta(hours = 10)

        return pd.date_range(
            dn, end, 
            freq = '10min'
            )
    
    else:
        return pd.date_range(
            dn,
            freq = '30min', 
            periods = 12
            )




def download_from_periods(
        start, 
        site = 'sao_luis', 
        ext = ['RSF'], 
        hours = 12
        ):
    
    end = start + dt.timedelta(hours = hours)
    
    
    FOLDER_NAME = start.strftime(
        '%Y%m%d' +  site[0].upper()
        )
    
    make_dir(PATH_IONO)
    save_in = os.path.join(
        PATH_IONO,
        FOLDER_NAME
        )
    
    make_dir(save_in)
        
    
    for dn in tqdm(periods(start, end = end)):
        
        url = wb.embrace_url(
            dn, 
            site = site, 
            inst = 'ionosonde'
            ) 
        
        for link in wb.request(url):

            if (any(f in link for f in ext) and 
               (iono_dt(link) == dn)):
                try:
                 
                     wb.download(
                         url, 
                         link,   
                         save_in
                         )
                except:
                    pass
          

def run():
    dn = dt.datetime(2013, 12, 24, 20)

    
    download_from_periods(
            dn, 
            site = 'sao_luis', 
            ext = ['RSF', 'SAO']
            )
    
# run()