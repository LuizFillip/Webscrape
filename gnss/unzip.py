import gzip
import shutil
import os
import zipfile
from unlzw3 import unlzw

def unzip_Z(path_in):
    fh = open(path_in, 'rb').read()
    
    uncompressed_data = unlzw(fh)

    decoded = eval(str(uncompressed_data)).decode('utf8')
    
    path_out = path_in.replace(".Z", "")
    
    if 'igv' in path_in:
        path_in = path_in.replace('_00', '')
        
    file = open(path_out, 'w')
    file.write(decoded)
    file.close()
    os.remove(path_in)
    return path_out


def unzip_orbit(files, path_to_save): 
    fh = open(files, 'rb')
    
    compressed_data = fh.read()
    
    uncompressed_data = unlzw(compressed_data)
    
    str_mybytes = str(uncompressed_data)
    
    decoded = eval(str_mybytes).decode('utf8')
    
    file = open(files.replace(".Z", ""), 'w')
    file.write(decoded, path_to_save)
    file.extract(file, path_to_save)
    file.close()
    fh.close()
   
    
    return None 
    
    
def unzip_zip(zip_path) -> None:
    
    zip_ref = zipfile.ZipFile(zip_path, "r") 
    
    for name in zip_ref.namelist():
        
        if any(name.endswith(ext) for ext in ['o', 'd']):
            
            pat_out = os.path.split(zip_path)[0]
            zip_ref.extract(name, pat_out)
            path_out = zip_path.replace("zip", name[-3:])
            
    zip_ref.close()
    
    
    return path_out

def unzip_gz(infile):
    
    with gzip.open(infile, 'rb') as f_in:
        with open(
                infile.replace('.gz', ''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
 
    
    
