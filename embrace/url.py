
ends = {
        "ionosonde": ["DVL", "SKY", "DFT", "RSF", "SAO"], 
        "imager": ["PNG", "TIF"]
                                              
        }

site_codes = {
    
         "ionosonde": {
             "Fortaleza": "FZA0M", 
             "Sao luis": "SAA0K", 
             "Belem": "BLJ03", 
             "Cachoeira": "CAJ2M", 
             "Santa Maria": "SMK29", 
             "Boa Vista": "BVJ03", 
             "Campo Grande": "CGK21"
             }, 
         
         "imager": {
                 "cariri": "CA", 
                "Bom Jesus da Lapa" : "BJL", 
                "Cachoeira Paulista": "CP", 
                "Comandante Ferraz": "CF", 
                "Sao Martinho da Serra": "SMS"
            }, 
         
         'magnetometer': {
             'sao luis': 'SLZ'
             }
         }

def URL(date, 
        site = "Cariri", 
        inst = "imager"):
    
    """
    Build embrace url from date, site 
    for an intrument
    """
    url = "https://embracedata.inpe.br/"
    
    code = site_codes[inst.lower()][site.lower()]
    # site_codes['magnetometer']['sao luis']
    year = date.year
    str_doy = date.strftime("%j")
    str_mon = date.strftime("%m")
    str_day = date.strftime("%d")
    
    url += f"{inst}/{code}/{year}/"
    
    if inst == "imager":
        url += f"{code}_{year}_{str_mon}{str_day}/"
        
    elif inst == "ionosonde":
        url += f"{str_doy}/"
        
    # elif inst == "magnetometer":
    #     url +=  f"{code}/" 
    
    return url


    



