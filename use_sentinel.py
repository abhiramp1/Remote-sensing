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
filename = r"E:\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\Landsat\SpatialData\grandlake.csv"

# destination directory where landsat images will be downloaded
destination = r'E:\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\Sentinel\Grand_lake_sentinel'

# login information for the USGS Earth Explorer Website
username = 'abhiramp1'
password = 'Demokboys2020'
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
# l.download('https://console.cloud.google.com/storage/browser/_details/gcp-public-data-sentinel-2/tiles/15/S/UA/S2A_MSIL1C_20150806T171225_N0202_R069_T15SUA_20160517T083719.SAFE/GRANULE/S2A_OPER_MSI_L1C_TL_EPA__20160516T202538_A000638_T15SUA_N02.02/IMG_DATA/S2A_OPER_MSI_L1C_TL_EPA__20160516T202538_A000638_T15SUA_B01.jp2')
        
    
# for product in all_links:
#     for url in product:
#         l.download(url)
#         time.sleep(2)
    
# # download metadata files
# # # for url in URLs_return:
# #     if dataset =="SENTINEL_2A":
# #         fail_list = l.download_sentinel(username,password,destination,url)
# #     elif dataset == "LANDSAT_8_C1":
# #         l.download_Landsat(username,password,destination,url)
# #     #break
   
# if fail_list:
#     for l in fail_list:
#         fail_list = l.download_sentinel(username,password,destination,url)
# #find products with acceptable cloud cover percentage using metadata files,
# #function defaults to 10%
# #the function finds all metadata txt files in the metadata folder located within
# #the defined destination
# if dataset == "LANDSAT_8_C1":
#     candidates = l.check_cloud_cover()
#     print(candidates)
# else:
#     print("No Lancet data to process for cloud cover")




