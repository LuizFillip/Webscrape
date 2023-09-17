import os
import Webscrape as wb 
from base import make_dir

from tqdm import tqdm 

def year_from_fname(f):
    
    if '_' in f:
        ext = f.split('_')
        ext = ext[1].split('.')
        year_str = '20' + ext[1][:2]
    else:
        ext = f.split('.')
        year_str = '20' + ext[-2][:2]
        
        
    doy = ext[0][-4:-1]
    
    return doy, year_str

def unzip_convert(path_in, path_out):
    try:
        path_out = unzip(path_in)
    
        wb.crx2rnx(path_out)
    except:
        pass
    
# def run():
def create_folders(
        infile, 
        year, 
        doy
        ):
    
    year_path = os.path.join(
        infile,
        year
        )
    
    make_dir(year_path)
    
    doy_path = os.path.join(
        year_path, 
        doy 
        )
    make_dir(doy_path)
    
    return doy_path
    

from unlzw3 import unlzw


def unzip(path_in):
    fh = open(path_in, 'rb').read()
    
    uncompressed_data = unlzw(fh)

    decoded = eval(str(uncompressed_data)).decode('utf8')
    
    path_out = path_in.replace(".Z", "")
    
    file = open(path_out, 'w')
    file.write(decoded)
    file.close()
    
    return path_out

save_in = 'D:\\database\\GNSS\\rinex\\peru_2\\'

infile = 'D:\\database\\GNSS\\rinex\peru\\'

def run_all():
    
    
    # for folder in os.listdir(infile):
    folder = os.listdir(infile)[0]
    files = os.listdir(infile + folder)
    # for filename in tqdm(files, desc = folder):
    filename = files[0]
    
    
    
    doy, year = year_from_fname(filename)
    
    path_in = os.path.join(
        infile, 
        folder, 
        filename
        )
       
    # path_to_save = create_folders(
    #         save_in,
    #         year, 
    #         doy
    #             )
        
        
    
