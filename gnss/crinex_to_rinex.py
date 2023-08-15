import subprocess
import os
from tqdm import tqdm 

executable_path = "database/GNSS/rinex/crx2rnx/CRX2RNX.exe"

# executable_path = r"D:\database\GNSS\rinex\CRX2RNX.exe"
input_file = "D:\\database\\GNSS\\rinex\\2022\\001\\amcr0011.22d"

                
# 

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
                    input_file = os.path.join(doy_path, filename)
                    subprocess.run([executable_path, 
                                    input_file, '-f'])
                    
                    os.remove(input_file)
                    

def test_file():
     
    doy_path = 'D:\\database\\GNSS\\rinex\\2021\\001\\'
    for filename in tqdm(os.listdir(doy_path)):
        if filename.endswith('d'):
            input_file = os.path.join(doy_path, filename)
            subprocess.run([executable_path, input_file, '-f'])
            
            os.remove(input_file)
            
            
# run_all_ways(year_folder)