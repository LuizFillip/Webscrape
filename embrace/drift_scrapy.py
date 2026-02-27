import requests 
from bs4 import BeautifulSoup 
import pandas as pd 
from tqdm import tqdm 
import Webscrape as wb 

def raw_page(url):
    r = requests.get(url, verify = True)
    s = BeautifulSoup(r.text, "html.parser")
    
    return str(s) 

def read_one_day(dn):
    io = dn.strftime('%Y/%j/')
    url = 'https://embracedata.inpe.br/ionosonde/SAA0K/'
    url += io 
    save_in = 'F:\\database\\drift\\'
    for ln in tqdm(wb.request(url), io):
        if 'DVL' in ln:
            
            wb.download(
                url, 
                ln, 
                save_in
                )
 
def run_all():

    dates = pd.date_range(
           f'2023-01-01',  f'2025-12-31'
            )
    for dn in dates:
        
        read_one_day(dn)
       
      
df = run_all()