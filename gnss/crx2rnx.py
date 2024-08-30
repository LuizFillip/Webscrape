import subprocess
import os
from tqdm import tqdm 
import GNSS as gs

executable = "D:\\database\\GNSS\\CRX2RNX.exe"


year_folder = 'D:\\database\\GNSS\\rinex\\'

def run_all_ways(year_folder):
    
    for year in os.listdir(year_folder):
        year_path = os.path.join(year_folder, year) 
        print(year)
        for doy in os.listdir(year_path):
            doy_path = os.path.join(year_path, doy)
            for filename in tqdm(os.listdir(doy_path), 
                                 desc = doy):
                if filename.endswith('d'):
                    
                    input_file = os.path.join(
                        doy_path, filename)
                    try:
                        subprocess.run([executable, 
                                        input_file, '-f'])
                        
                        os.remove(input_file)
                    except:
                        continue
      
                    
def run_local(
        year = 2022,
        doy = 260
        ):
    
    doy_path = gs.paths(year, doy).rinex
    
    for filename in tqdm(os.listdir(doy_path)):
        if filename.endswith('d'):
            input_file = os.path.join(doy_path, filename)
            crx2rnx(input_file)
            
            
            
def crx2rnx(
        input_file, 
        executable = executable
        ):
        
        # subprocess.run([executable, input_file, '-f'])
        try:
            subprocess.run([executable, input_file, '-f'])
        except:
            pass
        
        os.remove(input_file)
            



# 


