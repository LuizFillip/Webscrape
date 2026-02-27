import GNSS as gs 
import scrap as sp
import base as b 
year = 2015

# sp.download_rinex_daily(
#     year, 
#     start_doy = 1, 
#     stations = None, 
#     root = "D:\\", 
#     resume = True
#     )

# sp.download_orbits_daily(
#     year,
#     root = "D:\\", 
#     const = 'esa', 
#     network = "garner",
#     resume = False,
#     verbose = True
#     )


def one_day():
    year = 2010
    path = gs.paths(year, root= 'D:\\')
    doy = 1
    b.make_dir(path.rinex_base)
    path_to_save = f"{path.rinex}{doy:03d}"
    
    # stations = sp.miss_receivers(year, doy)
    stations = ['rnmo', 'pbcg',  'pepe', 'recf', 'rnna', 'pbjp', 'alar']
    sp.download_routine(year, doy, path_to_save, stations)
    
    
# one_day()