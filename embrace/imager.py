import datetime as dt 
import os
import Webscrape as wb 
import base as b 
from tqdm import tqdm 



def make_folder(url, root = 'database\\'):
    fn = url.split('/')[-2]
    
    path_to_save = os.path.join(
        root, fn)
    b.make_dir(path_to_save)
    return path_to_save
    
    
def download_images(dn, site = 'cariri', layer = 'O6'):
    
    url = wb.embrace_url(
        dn, 
        site = site, 
        inst = 'imager'
        )
    
    path_to_save = make_folder(url)
    
    print(site, layer, dn.strftime('%Y/%m/%d'))
    
    for link in tqdm(
            wb.request(url),
            'download_images'
            ):
       
        if layer in link:
            
            if 'DARK' in link:
                pass
            else:
                
                wb.download(
                    url, 
                    link, 
                    path_to_save
                    )


dn = dt.datetime(2016, 2, 11, 20)


download_images(dn, site = 'cariri', layer = 'O6')