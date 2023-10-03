import datetime as dt
import Webscrape as wb
import base as b 
import os 
import pandas as pd

from base import make_dir

PATH_IONO = 'database/iono/'


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

    return dt.datetime(year, 
                       month, 
                       day,
                       hour, 
                       minute, 
                       second)

    
class EMBRACE(object):
    
    def __init__(
            self, 
            site = 'sao_luis', 
            save_in = 'D:\\drift\\SAA\\'
            ):
        
        self.save_in = save_in 
        self.site = site
        
    def download_drift(
            self, 
            dn, 
            ext = ['DVL']
            ):

        url = wb.embrace_url(
            dn, 
            site = self.site, 
            inst = 'ionosonde'
            )    
        
        for link in wb.request(url):
            
            if any(f in link for f in ext):
                
                delta = dt.timedelta(hours = 4)
                
                if (iono_dt(link) >= dn and 
                    (iono_dt(link) <= dn + delta)):
                   
                    print('[download_iono]', link)
                    wb.download(
                        url, 
                        link, 
                        self.save_in
                        )
                
    def download_imager(
            self, 
            site, 
            dn,
            layer = 'O6'
            ):
        
        url = wb.embrace_url(
            dn, 
            site = site, 
            inst = 'imager'
            )
        
        save_in = 'D:\\imager\\'
        
        fn = url.split('/')[-2]
        path_save = os.path.join(save_in, fn)
        b.make_dir(path_save)
        
        for link in wb.request(url):
           
            if layer in link:
                print('[download_images]', link)
                wb.download(
                    url, 
                    link, 
                    path_save
                    )



def periods(dn, end = False):
    
    if end:
        end = dn + dt.timedelta(hours = 11)

        return pd.date_range(
            dn, end, 
            freq = '10min')
    
    else:
        return pd.date_range(
            dn,
            freq = '30min', 
            periods = 12
            )




def download_from_periods(
        start, 
        site = 'sao_luis', 
        ext = ['RSF', 'SAO'], 
        end = True
        ):
    
    end = site[0].upper()
    FOLDER_NAME = start.strftime(
        '%Y%m%d' + end
        )
    
    save_in = os.path.join(
        PATH_IONO,
        FOLDER_NAME
        )
    
    make_dir(save_in)
        
    
    for dn in periods(start, end = end):
        
        url = wb.embrace_url(
            dn, 
            site = site, 
            inst = 'ionosonde'
            ) 
        
        for link in wb.request(url):
        
            if (any(f in link for f in ext) and 
               (iono_dt(link) == dn)):
                                             
             print('[download_iono]', link)
             wb.download(
                 url, 
                 link, 
                 save_in
                 )
        