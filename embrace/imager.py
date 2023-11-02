import datetime as dt 
import os
import FabryPerot as fp 
import numpy as np 
import Webscrape as wb 
import base as b 



ds = fp.get_similar()

dates = np.unique(ds.index.date)


layer = 'O6'

save_in = 'D:\\img\\'

for dn in dates:
        
    url = wb.embrace_url(
        dn, 
        site = 'cariri', 
        inst = 'imager'
        )
    

    fn = url.split('/')[-2]
    folder = dn.strftime('%Y%m%d')
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

# print(path_save) 