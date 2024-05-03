import pandas as pd
from base import make_dir
import datetime as dt
# import digisonde as dg
import Webscrape as wb 
import os 
from tqdm import tqdm 


PATH_IONO = 'database/ionogram/'
# PATH_IONO = 'D:\\drift\\'



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

def periods(dn, hours = 24):
    
    end = dn + dt.timedelta(hours = hours)

    
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
        hours = 14
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

            if (any(f in link for f in ext) and 
                (iono_dt(link) == dn)):
               
                # try:
                 
                wb.download(
                    url, 
                    link,   
                    save_in
                    )
                # except:
                #     pass
          


def download_whole_day(site = 'sao_luis', ext = ['.SAO']):
    
    for day in tqdm(range(182, 366)):
        delta = dt.timedelta(days = day)
        dn = dt.datetime(2023, 1, 1, 0) + delta
        
        url = wb.embrace_url(
            dn, 
            site = site, 
            inst = 'ionosonde'
            ) 
        
        # 
        # save_in = os.path.join(
        #       PATH_IONO,
        #       FOLDER_NAME(dn, site = 'saa', dirc = 0)
        #       )
        save_in = 'D:\\drift\\dece\\'
        for link in wb.request(url):
            if 'XML' in link:
                pass
            else:
                if any(f in link for f in ext): 
                    print(link)
                    wb.download(
                        url, 
                        link,   
                        save_in
                        )
    
    return 

# delta= dt.timedelta(hours = 21)
# start = dt.datetime(2014, 1, 28, 21)
# download_ionograms(
#         start, 
#         site = 'fortaleza', 
#         ext = ['RSF'], 
#         hours = 12
#         )

