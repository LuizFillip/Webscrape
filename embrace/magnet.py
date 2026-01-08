import datetime as dt
import Webscrape as wb
import base as b 
                
                
dn = dt.datetime(2015, 12, 19)

def dn2fn(dn, code = 'slz'):

    return dn.strftime(f'{code}%d%b.%ym').lower()

def fn2dn(file, code = 'vss'):
    fmt = f'{code}%d%b.%ym'
    return dt.datetime.strptime(file, fmt)

codes = {
    'sao_luis': 'slz',
    'cachoeira': 'cxp',
    'vassouras': 'vss',
    'eusebio': 'eus'
    }

def download_magnetometer(ref, days, site  = "sao_luis"):

    url = wb.embrace_url(
            ref, 
            site = site, 
            inst = "magnetometer"
            )

    
    save_in = f'magnet/data/{ref.year}'
    
    b.make_dir(save_in)
    
    code = codes[site]
    
    for link in wb.request(url):    
        
        if code in link:
            dn = fn2dn(link, code = code)
            
            if dn.day in days:
             if dn.month == ref.month:
                 print('Downloading', link)
                 wb.download(
                     url, 
                     link, 
                     save_in
                     )
        # except:
        #     continue 
            
    return None 



def main():
    ref = dt.datetime(2015, 12, 13)
    
    days = [13, 16, 18, 29, 19, 20, 21, 22]
    days = [3, 4, 30, 28]
    for site in ['sao_luis', 'eusebio']:
        download_magnetometer(ref, days, site)
    
# main()