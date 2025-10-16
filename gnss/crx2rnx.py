import subprocess
import os
from tqdm import tqdm 
import GNSS as gs


year_folder = 'D:\\database\\GNSS\\rinex\\'

def run_all_ways(year_folder, executable):
    
    for year in os.listdir(year_folder):
        year_path = os.path.join(year_folder, year) 
     
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
        root = 'E:\\'
        ):
        executable = f"{root}database\\GNSS\\rinex\\CRX2RNX.exe"


        subprocess.run([executable, input_file, '-f'])
        try:
            subprocess.run([executable, input_file, '-f'])
        except:
            pass
        
        return None 


