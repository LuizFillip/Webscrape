import os
import Webscrape as wb 
from base import make_dir

from tqdm import tqdm 

def year_from_fname(f):
    ext = f.split('.')
    doy = ext[0][-4:-1]
    year_str = '20' + ext[-2][:2]
    return doy, year_str


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

for folder in os.listdir(infile):


    for filename in tqdm(os.listdir(infile + folder), 
                         desc = folder):
    
    
        doy, year = year_from_fname(filename)
        path_in = os.path.join(
            infile, folder, filename)
       
        path_to_save = create_folders(
                save_in,
                year, 
                doy
                )
        
        try:
            path_out = unzip(path_in)
        
            wb.crx2rnx(path_out)
        except:
            continue
    
    #util.move(path_out.replace('d', 'o'), 
                