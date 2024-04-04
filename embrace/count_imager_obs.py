import Webscrape as wb 
import datetime as dt 
import imager as im 
import json 
from tqdm import tqdm 

def count_occurrences(links, emission = 'O6'):
            
    return [im.fn2datetime(f) for f in links if emission in f]

def get_infos(links, emission = 'O6'):
    
    d = count_occurrences(links, emission=emission)
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



def run_days(year):
    
    out = {}
    
    for day in tqdm(range(365), str(year)):
        
        delta = dt.timedelta(days = day)
        
        dn = dt.datetime(year, 1, 1) + delta 
        try:
            out.update(join_layers(dn, site = 'cariri'))
        except:
            continue
        
    return out

out = {}

for year in range(2013, 2024):
    
    out.update(run_days(year))
    
save_in = 'cariri'

with open(save_in, "w") as f:
    json.dump(out, f)