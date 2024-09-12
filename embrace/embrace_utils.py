
ends = {
        "ionosonde": ["DVL", "SKY", "DFT", "RSF", "SAO"], 
        "imager": ["PNG", "TIF"]
                                              
        }

site_codes = {
    
         "ionosonde": {
             "fortaleza": "FZA0M", 
             "sao_luis": "SAA0K", 
             "belem": "BLJ03", 
             "cachoeira": "CAJ2M", 
             "santa_maria": "SMK29", 
             "boa_vista": "BVJ03", 
             "campo_grande": "CGK21"
                        }, 
         
         "imager": {
                "cariri": "CA", 
                "lapa" : "BJL", 
                "cachoeira": "CP", 
                "ferraz": "CF", 
                "martinho": "SMS"
                    }, 
         
         'magnetometer': {
             'sao_luis': 'SLZ',
             "cachoeira": 'CXP'
             }
         }

def embrace_url(
        date, 
        site = "Cariri", 
        inst = "imager"
        ):
    
    """
    Build embrace url from date, site 
    for an intrument
    """
    url = "https://embracedata.inpe.br/"
    
    site = site.replace(' ', '_').lower()
    
    code = site_codes[inst.lower()][site]

    year = date.year
    str_doy = date.strftime("%j")
    str_mon = date.strftime("%m")
    str_day = date.strftime("%d")
    
    url += f"{inst}/{code}/{year}/"
    
    if inst == "imager":
        url += f"{code}_{year}_{str_mon}{str_day}/"
        
    elif inst == "ionosonde":
        url += f"{str_doy}/"
    
    elif inst == 'magnetometer':
        return url 
        
    return url




