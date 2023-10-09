import Webscrape as wb
import GNSS as gs




def download_gnss(year, rinex = True):
    
    # stations = wb.get_stations(gs.paths(year))
    
    # wb.folders_orbits(year)
            
    for doy in range(1, 366, 1):
        
        path = gs.paths(year, doy)
        
        if rinex:
            wb.download_rinex(
                    path,
                    wb.miss_stations(path)
                    )
        else:
            wb.download_orbit(
                year, 
                doy
                )

    return None


        



year = 2019
download_gnss(year)