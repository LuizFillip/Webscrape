import Webscrape as wb 
import datetime as dt 
import base as b 
from tqdm import tqdm

def built_url(dn):
    base = 'https://stdb2.isee.nagoya-u.ac.jp/GPS/shinbori/RGRID2/nc/'
    
    year = dn.strftime('%Y')
    doy = dn.strftime('%j')
    
    return f'{base}/{year}/{doy}'


def download_shinbori(dn):
    
    url = built_url(dn)
    
    save_in = 'E:\\database\\GNSS\\roti\\shibori\\'
    
    path_to_save = f'{save_in}\\{dn.year}\\'
    
    b.make_dir(path_to_save)
    
    for href in tqdm(wb.request(url), f'{dn.day}'):
    
        wb.download(
            url, 
            href, 
            path_to_save
            )


for i in range(1, 365):
    
    delta =  dt.timedelta(days = i)
    dn = dt.datetime(2013, 1, 1) + delta
    
    download_shinbori(dn)