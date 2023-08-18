import subprocess
import os
from tqdm import tqdm 

executable_path = "database/GNSS/rinex/crx2rnx/CRX2RNX.exe"


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
                        subprocess.run([executable_path, 
                                        input_file, '-f'])
                        
                        os.remove(input_file)
                    except:
                        continue
                        

def test_file():
     
    doy_path = 'D:\\database\\GNSS\\rinex\\2021\\001\\'
    for filename in tqdm(os.listdir(doy_path)):
        if filename.endswith('d'):
            input_file = os.path.join(doy_path, filename)
            subprocess.run([executable_path, input_file, '-f'])
            
            os.remove(input_file)
            
# base = 'D:\\database\\GNSS\\rinex\\'

run_all_ways(year_folder)

