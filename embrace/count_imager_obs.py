import Webscrape as wb 
import datetime as dt 
import imager as im 
import json 
from tqdm import tqdm 
import base as b 


def get_dates(links, emission = 'O6'):
            
    return [im.fn2datetime(f) for f in links if emission in f]

def get_infos(links, emission = 'O6'):
    
    d = get_dates(links, emission)
    
    begin =  d[0]
    end = d[-1]
    delta = (end - begin).seconds / 3600 
    infos = {
        'begin': begin.strftime('%Y-%m-%d %H:%M:%S'),
        'end': end.strftime('%Y-%m-%d %H:%M:%S'), 
        'delta': str(delta), 
        'len': str(len(d))
        }
    return {emission: infos}


def join_layers(dn, site = 'cariri'):
    
    url = wb.embrace_url(
        dn, 
        site = site, 
        inst = 'imager'
        )

    links = wb.request(url)
    
    return {dn.strftime('%Y-%m-%d'): 
            {**get_infos(links, emission = 'O6'), 
             **get_infos(links, emission = 'OH')}
            }



def run_days(year, site = 'cariri'):
    
    out = {}
    
    b.make_dir(site)
    
    for day in tqdm(range(365), str(year)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1) + delta 
        try:
            out.update(join_layers(dn, site = site))
        except:
            continue
        
    save_in = f'{site}/{year}'
    
    with open(save_in, "w") as f:
        json.dump(out, f)
        
    return out


def run_years(site = 'cariri'):

    out = {}
    
    for year in range(2013, 2024):
        
        out.update(run_days(year, site = site))
        
    save_in = ''
    
    with open(site, "w") as f:
        json.dump(out, f)
        
# run_years(site = 'cariri')