import datetime as dt



site_codes = {
    
         "ionosonde": {"Fortaleza": "FZA0M", 
                       "Sao luis": "SAA0K", 
                       "Belem": "BLJ03", 
                       "Cachoeira": "CAJ2M", 
                       "Santa Maria": "SMK29", 
                       "Boa Vista": "BVJ03", 
                       "Campo Grande": "CGK21"}, 
         
         "imager": {"Cariri": "CA", 
                    "Bom Jesus da Lapa" : "BJL", 
                    "Cachoeira Paulista": "CP", 
                    "Comandante Ferraz": "CF", 
                    "Sao Martinho da Serra": "SMS"} 
         }


class href_attrs(object):
    
       
    """Convert digisonde, imager and TEC files 
    filename (EMBRACE format) to datetime"""
    
        
    @staticmethod
    def iono(file):
        
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
    
    @staticmethod
    def img(file):
        args = file[:-4].split("_")
        date = args[2]
        time = args[3]
        return dt.datetime.strptime(date + time, 
                                    "%Y%m%d%H%M%S")
    
    @staticmethod
    def tec(file):
        args = file[:-4].split("_")
        
        date = args[1]
        time = args[2]
        return dt.datetime.strptime(date + time, 
                                     "%Y%m%d%H%M%S")
    
def main():
    f = 'FZA0M_2015144235555.SKY'
    c = href_attrs()
    print(c.iono(f))
#main()