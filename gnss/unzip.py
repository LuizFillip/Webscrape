import gzip
import shutil
import os

def unzip_gz(infile):
    
    with gzip.open(infile, 'rb') as f_in:
        with open(infile.replace('.gz', ''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    os.remove(infile)
    
    
