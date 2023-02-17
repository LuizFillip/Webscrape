import os
import requests 
from bs4 import BeautifulSoup 


def download(url: str, href: str, infile_save: str = ""):
    
    """Function for download from link"""
    
    remote_file = requests.get(url + href)
    path_to_save = os.path.join(infile_save, href)
    print("download...", href)
    with open(path_to_save, 'wb') as f:
        for chunk in remote_file.iter_content(chunk_size = 1024): 
            if chunk: 
                f.write(chunk) 
                
    return path_to_save


def request(url): ## condition for string in hiperlink
    """Request website from url (RINEX or sp3)"""
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")

    parser = s.find_all('a', href = True)

    return [link['href'] for link in parser]



def make_dir(date, root = ""):
    """Create a new directory by path must be there year and doy"""
    doy_str = date.strftime("%j")
    
    path_to_create = os.path.join(root, doy_str)
    
    
    try:
        os.mkdir(path_to_create)
        
        for subfolder in ["imager", "ionosonde", "tec"]:   
            os.makedirs(os.path.join(path_to_create, subfolder)) 
        
            print(f"Creation of the directory {subfolder} successfully")
        
    except OSError:
        print(f"Creation of the directory {path_to_create} failed")
      
   
    return path_to_create

