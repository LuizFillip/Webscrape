
ends = {
        "ionosonde": ["DVL", "SKY", "DFT", "RSF", "SAO"], 
        "imager": ["PNG", "TIF"]
                                              
        }

site_codes = {
    
         "ionosonde": {
             "Fortaleza": "FZA0M", 
             "sao_luis": "SAA0K", 
             "belem": "BLJ03", 
             "cachoeira": "CAJ2M", 
             "santa_maria": "SMK29", 
             "boa_vista": "BVJ03", 
             "campo_grande": "CGK21"
                        }, 
         
         "imager": {
                 "cariri": "CA", 
                "Bom Jesus da Lapa" : "BJL", 
                "cachoeira": "CP", 
                "Comandante Ferraz": "CF", 
                "Sao Martinho da Serra": "SMS"
                    }, 
         
         'magnetometer': {
             'sao luis': 'SLZ'
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
        
    
    return url


import datetime as dt

def iono_dt(file):        
    args = file[:-4].split("_")

    year = int(args[1][:4])
    doy = int(args[1][4:7])
    hour = int(args[1][7:9])
    minute = int(args[1][9:11])
    second = int(args[1][11:])
    date = (dt.date(year, 1, 1) + 
            dt.timedelta(doy - 1))

    day = date.day
    month = date.month

    return dt.datetime(year, 
                       month, 
                       day,
                       hour, 
                       minute, 
                       second)

