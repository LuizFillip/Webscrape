import datetime
import os
import pandas as pd
import shutil 

class date_from_filename(object):
    
    """Convert digisonde, imager and TEC files filename (EMBRACE format) to datetime"""
    
    def __init__(self, file):
        
        extension = file[-4:]
        args = file[:-4].split("_")
        
        if ((extension == ".SAO") or 
            (extension == ".RSF")):
            
            
            year = int(args[1][:4])
            doy = int(args[1][4:7])
            hour = int(args[1][7:9])
            minute = int(args[1][9:11])
            
            date = datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)
        
            day = date.day
            month = date.month
        
            self.datetime = datetime.datetime(year, month, day,
                                              hour, minute)
            
        elif ((extension == ".png") or
              (extension == ".tif")):
            
            args = file[:-4].split("_")
            
            date = args[2]
            time = args[3]
            self.datetime = datetime.datetime.strptime(date + time, 
                                                       "%Y%m%d%H%M%S")
            
        elif ((extension == ".txt") or 
             ("TECMAP" in file)):
            
            args = file[:-4].split("_")
            
            date = args[1]
            time = args[2]
            self.datetime = datetime.datetime.strptime(date + time, 
                                                       "%Y%m%d%H%M%S")

def copy_tec_files(date, 
                   infile = "G:\\My Drive\\TEC_2014\\", 
                   path_to_save = ""):
    
    delta = datetime.timedelta(days = 1)
    
    times = pd.date_range(f"{date} 21:00", 
                          f"{date + delta} 07:00", 
                          freq = "10min")
    
    _, folders, _ = next(os.walk(infile))

    str_mon = date.strftime("%m")

    def split_folder(folder):
        args = folder.split("_")
        year = args[1]
        mon = args[2]
        return year, mon

    for folder in folders:
        year, mon = split_folder(folder)
        
        if mon == str_mon:
            _, _, files = next(os.walk(infile + folder))
            
            for filename in files:
                
                ref_time = date_from_filename(filename).datetime
                
                if (ref_time >= times[0]) and (ref_time <= times[-1]):
                    path_src = os.path.join(infile, folder, filename)
                    path_dst = os.path.join(path_to_save, filename)
                    try:
                        shutil.copy2(path_src, path_dst)
                    except:
                        print("doesn cant copy the files")
                        