import Webscrape as wb

def download_gnss(year, root = "D:\\"):
    
    stations = wb.get_stations(year, root = root)
    
    wb.folders_orbits(year, root = root)
    
    doy_min = wb.minimum_doy(year, root = root)
        
    for doy in range(doy_min, 365, 1):
        print(doy, year)

        wb.download_rinex(
                year, 
                doy, 
                root = root,
                stations = stations
                )

        wb.download_orbit(
            year, 
            doy, 
            root = root
            )

    return None


download_gnss(year = 2020)