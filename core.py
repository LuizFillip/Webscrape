import os
import requests 
from bs4 import BeautifulSoup 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download(
        url: str, 
        href: str, 
        save_in: str = "", 
        verify = False
        ) -> str:
    
    """Function for download from link"""
    
    remote_file = requests.get(
        url + href, 
        verify = verify
        )
    
    path_to_save = os.path.join(save_in, href)
    
    print("download...", href)
    
    with open(path_to_save, 'wb') as f:
        for chunk in remote_file.iter_content(
                chunk_size = 1024
                ): 
            if chunk: 
                f.write(chunk) 
                
    return path_to_save


def request(url, verify = False) -> list: 
    
    """Request website code source from url"""
    
    r = requests.get(url, verify = verify)
    s = BeautifulSoup(r.text, "html.parser")

    parser = s.find_all('a', href = True)

    return [link['href'] for link in parser]




# url = 'http://ftp.cptec.inpe.br/'

# request(url)