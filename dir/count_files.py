import os
import matplotlib.pyplot as plt




def count_in_each_day(p):
    
    return [len(os.listdir(p + f)) for f in os.listdir(p)]

out = []

for y in [2013, 2014, 2015]:

    p = f'D:\\database\\rinex\\{y}\\'
    
    out.extend( count_in_each_day(p))

# plt.plot(out)


for i, num in enumerate(out):
    if num < 40:
        print(num, i / 365)
        
        
def count_recivers_in_server():
    return 