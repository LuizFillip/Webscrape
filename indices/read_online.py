import os
import urllib.request

DIR_FILE = os.path.dirname(__file__)

pyglow_dir = os.path.join(DIR_FILE, "kpap/")

src = "https://kp.gfz-potsdam.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt"
dest = pyglow_dir + "/Kp_ap_Ap_SN_F107_since_1932.txt"

urllib.request.urlretrieve(src, dest)
