import requests 
from bs4 import BeautifulSoup 


user_infos = dict(fullname = "Luiz Fillip Rodrigues Vital", 
                  affiliation = "UFCG", 
                  email = "luizfillip6@gmail.com", 
                  kinst = "5545", 
                  year = "2013", 
                  kindat = "7100", 
                  format = "ascii")

class URL(object):
    
    def __init__(self, user_infos):
        
        self.base = "http://cedar.openmadrigal.org/ftp/"
        
        user_infos["fullname"] = user_infos["fullname"].replace(" ", "+")

        user = ('/'.join('{}/{}'.format(key, value) 
                         for key, value in user_infos.items()))
        
        self.url = self.base + user 


url = URL(user_infos).url



def download_test():

    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    
    parser = s.find_all('a', href = True)
    
    for link in parser:
        href = link['href']
        name = link.text.strip()
        
        base = "http://cedar.openmadrigal.org/"
        
        if "minime" in name:
            
            remote_file = requests.get(base + href)
            print("downloading...", name)
            
            with open(name, 'wb') as f:
                for chunk in remote_file.iter_content(chunk_size = 1024): 
                    if chunk: 
                        f.write(chunk) 
                        