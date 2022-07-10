# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 11:28:51 2020

@author: abhiram
"""

# example usage of landsat tool


# initiate timer

import time
import json


import os

# input file containing site names and locations (formatting needed)
filename = r"C:\Users\abhir\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\Landsat\SpatialData\grandlake.csv"

# destination directory where landsat images will be downloaded
destination = r'sentinel'

# login information for the USGS Earth Explorer Website
username = 'abhiramp1'
password = 'Jeloabar143#'
dataset = "SENTINEL_2A"
#dataset = "LANDSAT_8_C1"
user = (username, password)

# start and end date (formatting must be the same YYYY-MO-DA)
start = '2015-07-01'
end   = '2020-11-30'

#from Landsat_tool import Landsat_Tool
#os.chdir(r"C:\Users\sridh\Desktop\test")
from Sentinel_tool import Sentinel_Tool

# create the landsat extraction tool and login
l = Sentinel_Tool(user, destination = destination,dataset=dataset)
l.login()



# find all images available for the test location between test dates
# matches is a list of the available product ids
URLs_return = l.search(filename, start, end)
# print('Possible scenes include:')
print(URLs_return)

all_links=[]
for j,i in enumerate(URLs_return):
    link_fmt = l.sentinel_url_constructor(destination,i)
    links = l.url_band_constructor(link_fmt)
    all_links.append(links)
# print(all_links[2])

for url in all_links:
    print(url,"URL..............")
    for i in url:
        l.download(i)
        time.sleep(2)





