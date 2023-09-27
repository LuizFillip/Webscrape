import os
from base import make_dir
import shutil
from tqdm import tqdm 
import Webscrape as wb  


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
            
            try:
                
                crinex_file = wb.unzip(third_path)
        
                wb.crx2rnx(crinex_file, delete = True)
         
            except:
                continue
        
unzip_convert()