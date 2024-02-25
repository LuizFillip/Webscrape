import requests 
from bs4 import BeautifulSoup 
import os
import datetime as dt 

BASE = "http://cedar.openmadrigal.org/"

# dates = ['2021_10_07', '2022_03_03', '2022_03_08',
#          '2022_03_09', '2022_03_10', '2022_09_25', 
#          '2022_09_26', '2022_09_27', '2022_09_28', '2022_09_29']

    
                        
def download(href, path_to_save):
    
    remote_file = requests.get(BASE + href)
    
    with open(path_to_save, 'wb') as f:
        for chunk in remote_file.iter_content(chunk_size = 1024): 
            if chunk: 
                f.write(chunk) 

class filenames(object):
    
    def __init__(self, filename):
        
        self.filename = filename
        
    @staticmethod 
    def to_date(date, fmt):
        return dt.datetime.strptime(date, fmt)
    
    @property
    def minime(self):

        try:
        
            s = self.filename.split('_')
            obs_list = s[-1].split('.')
            
        except:
            p = os.path.split(self.filename)[-1]
            s = p.split('_')
            obs_list = s[-1].split('.')
            
        return self.to_date(obs_list[0], "%Y%m%d")
    
    @property
    def bfp(self):
        
        s = self.filename.split('.')[0][3:-1]
       
        return self.to_date(s, '%y%m%d')
    
def build_url(
        year = 2013, 
        kindat = 7100, 
        kinst = 5545, 
        fmt = "ascii"
        ):
        
    user_infos = dict(
        fullname = "Luiz Fillip Rodrigues Vital", 
        email = "luizfillip6@gmail.com",
        affiliation = "UFCG", 
        kinst = str(kinst), 
        year = str(year), 
        kindat = str(kindat), 
        format = fmt
        )

    
    user_infos["fullname"] = user_infos["fullname"].replace(" ", "+")

    join_infos = ('/'.join('{}/{}'.format(key, value) 
            for key, value in user_infos.items()))
    
    return f'{BASE}ftp/{join_infos}/'

def filter_by_month(name, month):
    try:
        date = filenames(name).bfp 
        
        if date.month == month:
            return True
        else:
            return False
        
    except:
        pass



def MadrigalDownload(url, save_in):
    
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    
    parser = s.find_all('a', href = True)
    
    for link in parser:
        href = link['href']
        name = link.text.strip()
        
        for month in [3, 9]:
            
            if filter_by_month(name, month):
                path_to_save = os.path.join(
                    save_in, 
                    str(month), 
                    name
                    )
                print('downloding...', name)
                download(href, path_to_save)
            
    
def main():
    save_in = "FabryPerot/data/FPI/"
    url = build_url(kinst = 5362, year = 2022)
    
    MadrigalDownload(url, save_in)