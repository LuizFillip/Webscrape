import os
import base as b
import shutil
from tqdm import tqdm 
import Webscrape as wb  
import GNSS as gs

PATH_IN = 'D:\\database\\GNSS\\rinex\\'
FOLDER_IN = 'peru/rqs/'


def year_from_fname(f):
    
    if '_' in f:
        ext = f.split('_')
        ext = ext[1].split('.')
        year_str = '20' + ext[1][:2]
    else:
        ext = f.split('.')
        year_str = '20' + ext[1][:2]
        
        
    doy = ext[0][-4:-1]
    
    return doy, year_str


    


def unzip_convert():
    
    first_path = os.path.join(
        PATH_IN, 
        FOLDER_IN
        )
    
    
    for folder in os.listdir(first_path):
     
        second_path = os.path.join(
            first_path, 
            folder
            )
        
        for file in tqdm(os.listdir(second_path), 
                         folder):
            
            doy, year = year_from_fname(file)
            
            third_path = os.path.join(
                second_path, 
                file
                )
            
            path = gs.paths(year, doy)
            
            # b.make_dir(path.rinex)
            
            if file.endswith('d'):
                # print(third_path)    
                wb.crx2rnx(third_path)
             
# unzip_convert()