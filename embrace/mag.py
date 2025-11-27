import datetime as dt
import Webscrape as wb
import base as b 
                
                
dn = dt.datetime(2015, 12, 19)

def dn2fn(dn, code = 'slz'):

    month = dn.strftime('%b').lower()
    fmt = f'{code}%d{month}.%ym'
    return dn.strftime(fmt)

def download_magnetometer(dn, site = "sao_luis"):

    url = wb.embrace_url(
            dn, 
            site = site, 
            inst = "magnetometer"
            )
    
    if site == 'sao_luis':
        code = 'slz'
    elif site == 'cachoeira':
        code = 'cxp'
    
    save_in = f'magnetometers/data/{dn.year}'
    
    b.make_dir(save_in)
    
    for link in wb.request(url):    
        
        print(f'{dn.month}/{dn.day}', site)
        if link ==  dn2fn(dn, code):
            
            wb.download(
                url, 
                link, 
                save_in
                )
            
    return None 

def download_days():
    for i in range(4):
        delta = dt.timedelta(days = i)
        download_magnetometer(dn + delta)