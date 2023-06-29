import os
import requests 
from bs4 import BeautifulSoup 


def download(url: str, href: str, infile_save: str = "") -> str:
    
    """Function for download from link"""
    
    remote_file = requests.get(url + href)
    path_to_save = os.path.join(infile_save, href)
    print("download...", href)
    with open(path_to_save, 'wb') as f:
        for chunk in remote_file.iter_content(
                chunk_size = 1024
                ): 
            if chunk: 
                f.write(chunk) 
                
    return path_to_save


def request(url) -> list: 
    
    """Request website from url"""
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")

    parser = s.find_all('a', href = True)

    return [link['href'] for link in parser]




