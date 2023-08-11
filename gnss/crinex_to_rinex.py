import subprocess

executable_path = "database/GNSS/rinex/crx2rnx/CRX2RNX.exe"

# executable_path = r"D:\database\GNSS\rinex\CRX2RNX.exe"
input_file = "D:\\database\\GNSS\\rinex\\2022\\001\\amcr0011.22d"

                
subprocess.run([executable_path, input_file, '-f'])