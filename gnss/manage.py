import os
import Webscrape as wb 
from base import make_dir


def year_from_fname(f):
    ext = f.split('.')
    doy = ext[0][-4:-1]
    year_str = '20' + ext[-2][:2]
    return doy, year_str

infile = 'D:\\database\\peru\\'

folders = os.listdir(infile)


folder = folders[0]

files = os.listdir(os.path.join(infile, folder))

filename = files[0]

filename


path_in = os.path.join(
    infile, 
    folder, 
    filename
    )

doy, year = year_from_fname(filename)


# wb.unzip_rinex(
#         path_in, 
#         year, 
#         path_to_save
#         )

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