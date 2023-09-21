import os
from base import make_dir
import shutil
from tqdm import tqdm 

PATH_IN = 'D:\\database\\GNSS\\rinex\\'
FOLDER_IN = 'peru'


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


    
def create_folders(
        f, 
        FOLDER_OUT = 'peru_2'
        ):
    
    doy, year = year_from_fname(f)
    
    year_path = os.path.join(
        PATH_IN, 
        FOLDER_OUT, 
        year)
    
    make_dir(year_path)
    
    save_in = os.path.join(year_path, doy)
    
    make_dir(save_in)
    
    return save_in 


def copy_rinex_away():
    
    first_path = os.path.join(
        PATH_IN, 
        FOLDER_IN
        )
    
    
    for folder in os.listdir(first_path):
     
        second_path = os.path.join(
            first_path, 
            folder
            )
        
        for file in tqdm(
                os.listdir(second_path), 
                desc = folder
                ):
            
            doy, year = year_from_fname(file)
            
            third_path = os.path.join(
                second_path, 
                file
                )
            
            if file.endswith('o'):
                save_in = create_folders(file)
                
                shutil.copy(
                    third_path, 
                    save_in
                    )
        
        
copy_rinex_away()