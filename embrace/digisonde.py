import pandas as pd
from base import make_dir
import datetime as dt
import Webscrape as wb 
import os 
from tqdm import tqdm 


def fn2dt(f):        
    
    site, date = tuple(f.split('_'))
    
    date_string = date.split('.')[0]
    fmt = '%Y%j%H%M%S'

    return dt.datetime.strptime(date_string, fmt)

def periods_by_range(dn, hours = 24):
    
    end = dn + dt.timedelta(hours = hours)

    return pd.date_range(dn, end, freq = '10min')

def periods_by_freq(dn, freq = '1D'):
    '''
    Range time by day
    '''
    return pd.date_range(dn, freq = freq, periods = 365)
    

def sites_codes(site):
    
    sites =  {
        "fortaleza": "FZA0M", 
        "sao_luis": "SAA0K", 
        "belem": "BLJ03", 
        "cachoeira": "CAJ2M", 
        "santa_maria": "SMK29", 
        "boa_vista": "BVJ03", 
        "campo_grande": "CGK21"
        }
    
    return sites[site]

def FOLDER_NAME(dn, site = 'saa', dirc = 0):
    
    
    
    ext = sites_codes(site)[:2].upper()
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
        site = site, 
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

PATH_IONO = 'E:\\ionogram\\'



def create_folder_by_date(
        start, 
        site
        ):
    
    make_dir(PATH_IONO)
    folder_year = os.path.join(
        PATH_IONO, 
        start.strftime('%Y')
        )
    make_dir(folder_year)
    save_in = os.path.join(
        folder_year,
        FOLDER_NAME(start, site = site, dirc = 1)
        )
    
    make_dir(save_in)
    return save_in
    
    
    
def download_ionograms(
        periods, 
        site = 'sao_luis', 
        ext = ['SAO', 'RSF']
        
        ):
    
    start = periods[0]
    
    save_in = create_folder_by_date(
            start, 
            site
            )
    
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
                try:
                    if fn2dt(file) == dn:
                        # print(file)
                        wb.download(
                            url, 
                            file, 
                            save_in
                            )
                except:
                    continue
                
    return None 
                    

def main():

    for year in range(2015, 2023):
        
        for hour in [21, 22]:
            
            dn = dt.datetime(year, 1, 1, hour)
            
            periods = periods_by_freq(dn)
            
            download_ionograms(
                    periods, 
                    site = 'fortaleza', 
                    ext = ['SAO']
                    )


def single_download(day):
    periods = periods_by_range(day, hours = 24)
    download_ionograms(
            periods, 
            site = 'belem', 
            ext = ['SAO', 'RSF']
            )

def download_in_day():
    
    # dates = pd.date_range(
    #     '2015-12-19', 
    #     '2015-12-22',
    #     )
    
    dates = [
        dt.datetime(2015, 12, 13),
        dt.datetime(2015, 12, 16), 
        dt.datetime(2015, 12, 18),
        dt.datetime(2015, 12, 29)
        ]

    for dn in dates:
        periods = periods_by_range(dn, hours = 24)
        
        download_ionograms(
                periods, 
                site = 'campo_grande', 
                ext = ['SAO', 'RSF']
                )

# download_in_day()

