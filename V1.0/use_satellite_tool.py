# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 11:28:51 2020

@author: abhiram
"""

#usage of sentinel ectractor


# initiate timer

import time
import json
import os
#from gcloud import storage
import subprocess
import re

# input file containing site names and locations (provide the path to csv file)
filename = r"\.....\grandlake.csv"

# destination directory where sentinel images will be downloaded
destination = r"\.....\sentinel directory"

# login information for the USGS Earth Explorer Website
username = 'Provide user name here'
password = 'Provide your password here'
dataset = "SENTINEL_2A"
#dataset = "LANDSAT_8_C1"
user = (username, password)

# start and end date (formatting must be the same YYYY-MO-DA)
start = '2022-01-01'
end   = '2022-02-31'

try:
    os.remove(r"C:/Users/abhir/.usgs")
except OSError:
    pass

#from Landsat_tool import Landsat_Tool
#os.chdir(r"C:\Users\sridh\Desktop\test")
from Sentinel_tool import Sentinel_Tool

# create the landsat extraction tool and login
l = Sentinel_Tool(user, destination = destination,dataset=dataset)
l.login()

#Important information obtained from the API response
# id_return = l.search(filename, start,end)
# print("The possible scene IDs include:")
# print(id_return)

# find all images available for the test location between test dates
# matches is a list of the available product ids
URLs_return = l.search(filename, start, end)
#print('Possible scenes include:')
#print(URLs_return)

all_links=[]
for j,i in enumerate(URLs_return):
    link_fmt = l.sentinel_url_constructor(destination,i)
    links = l.url_band_constructor(link_fmt)
    all_links.append(links)
#print(all_links)

gsutil_command = 'gsutil -m cp -r "gs://{gc_path}/" "C:/"'
regex = "https:\/\/storage.googleapis.com\/(.*)\/GRANULE"


for url in all_links:
    l = re.findall(regex, url[0])
    #print(l[0])
    file_name = l[0].split('/')[-1]
    command = gsutil_command.format(gc_path=l[0])
    print(command)
    if not os.path.isdir(r"F:/SAFE/" + file_name):
        myBat = open(r'F:/gcp.bat','w+')
        myBat.write(command)
        myBat.write("\n")
        myBat.close()
        r = subprocess.run([r'F:/gcp.bat'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(r.stderr)
        #print("yes")
    else:
        print("Already downloaded")
