import os
import requests 
from bs4 import BeautifulSoup 

def download(url, href, infile_save = ""):
    
    """Use request for download the data"""
    
    remote_file = requests.get(url + href)
    path_to_save = os.path.join(infile_save, href)
    
    with open(path_to_save, 'wb') as f:
        for chunk in remote_file.iter_content(chunk_size = 1024): 
            if chunk: 
                f.write(chunk) 
                
    return path_to_save


def request(url):
    
    """Request url and filter times"""
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
 
    parser = s.find_all('a', href = True)
    

    return [link['href'] for link in parser]


