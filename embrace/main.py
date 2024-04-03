import Webscrape as wb
import datetime as dt
import pandas as pd 


# dn = dt.datetime(2019, 2, 24, 21)
# dn = dt.datetime(2016, 10, 3, 21)




dates = [
    '2016-05-27,',
    '2016-05-28,',
     '2016-05-29,',
     '2017-03-02,',
     '2017-08-30,',
     '2018-01-13,',
     '2017-09-17'
 ]


for dn in pd.to_datetime(dates):

    wb.download_images(
        dn, 
        site = 'cariri', 
        layer = 'O6'
        )
    
    wb.download_ionograms(
            dn, 
            site = 'sao_luis', 
            ext = ['RSF'], 
            hours = 16
            ) 