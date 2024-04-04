import Webscrape as wb
import datetime as dt
import pandas as pd 


# dn = dt.datetime(2019, 2, 24, 21)
# dn = dt.datetime(2016, 10, 3, 21)



 #fossil in são luis

dates = [
    '2016-05-27',
    '2016-05-28',
     '2016-05-29',
     '2017-03-02',
     '2017-08-30',
     '2018-01-13',
     '2017-09-17',     
     
     '2018-03-19',
     '2019-05-02',
     '2019-09-06',
     '2019-09-21',
     '2020-03-30',
     '2020-08-20', 
     '2023-07-10'
 ]

dates = [
    '2017-04-03',
    '2016-02-11',
    '2013-12-24',
    '2016-10-03',
    '2017-03-02',
    '2017-09-17',
    '2019-05-02',
    '2020-08-20',
    '2023-07-10']


def run():
    delta = dt.timedelta(hours = 21)
    for dn in pd.to_datetime(dates):
    
        # wb.download_images(
        #     dn, 
        #     site = 'cariri', 
        #     layer = 'O6'
        #     )
        for site in ['sao_luis', 'fortaleza']:
            wb.download_ionograms(
                    dn + delta, 
                    site = site, 
                    ext = ['RSF'], 
                    hours = 16
                    ) 