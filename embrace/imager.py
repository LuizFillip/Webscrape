import datetime as dt 
import os
import Webscrape as wb 
import base as b 
from tqdm import tqdm 



def make_folder(url, root = 'imager/img/'): #'E:\\images\\'):
    fn = url.split('/')[-2]
    
    path_to_save = os.path.join(
        root, fn)
    b.make_dir(path_to_save)
    return path_to_save
    
    
def download_images(
        dn, 
        site = 'cariri', 
        layer = 'O6'
        ):
    
    url = wb.embrace_url(
        dn, 
        site = site, 
        inst = 'imager'
        )
    
    path_to_save = make_folder(url)
    date = dn.strftime('%Y/%m/%d')
    desc = f'{date}-{site}-{layer}'
        
    for link in tqdm(wb.request(url), desc):
       
        if layer in link:
            
            if 'DARK' in link:
                pass
            else:
                
                wb.download(
                    url, 
                    link, 
                    path_to_save
                    )
    return None 

dn = dt.datetime(2019, 6, 24, 21)
dn = dt.datetime(2024, 9, 24, 21)
dn = dt.datetime(2022, 7, 25, 21)

for site in [ 'lapa', 'cariri']:
    download_images(dn, site, layer = '06')