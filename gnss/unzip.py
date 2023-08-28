import gzip
import shutil
import os
import zipfile
from unlzw3 import unlzw

def unzip_orbit(files, path_to_save): 
    fh = open(files, 'rb')
    
    
    compressed_data = fh.read()
    
    uncompressed_data = unlzw(compressed_data)
    
    str_mybytes = str(uncompressed_data)
    
    decoded = eval(str_mybytes).decode('utf8')
    
    file = open(files.replace(".Z", ""), 'w')
    file.write(decoded, path_to_save)
    # file.extract(file, path_to_save)
    file.close()
    fh.close()
    # os.remove(files)
    
    
def unzip_rinex(
        files:str,   
        path_to_save:str
        ) -> None:
    
    zip_path = os.path.join(path_to_save, files)
    zip_file = zipfile.ZipFile(zip_path, 'r') 
    # ext_year = str(year)[-2:] 
    
    # extensions = [f"{ext_year}o", f"{ext_year}d"]
    extensions = ['o', 'd']
    zip_file = zipfile.ZipFile(zip_path, 'r') 
    
    for file in zip_file.namelist():
        
        if any(file.endswith(ext) for ext in extensions):
            
            zip_file.extract(file, path_to_save)
            
    zip_file.close()
    os.remove(zip_path)

def unzip_gz(infile):
    
    with gzip.open(infile, 'rb') as f_in:
        with open(infile.replace('.gz', ''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    os.remove(infile)
    
    
