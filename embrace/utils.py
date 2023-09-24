import datetime as dt




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
    
        return dt.datetime(
            year, 
            month, 
            day,
            hour, 
            minute, 
            second
            )
    
    @staticmethod
    def img(file):
        args = file[:-4].split("_")
        date = args[2]
        time = args[3]
        return dt.datetime.strptime(
            date + time, 
            "%Y%m%d%H%M%S"
            )
    
    @staticmethod
    def tec(file):
        args = file[:-4].split("_")
        
        date = args[1]
        time = args[2]
        return dt.datetime.strptime(
            date + time, 
            "%Y%m%d%H%M%S"
            )
    
