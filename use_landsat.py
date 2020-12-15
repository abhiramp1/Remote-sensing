# example usage of landsat tool
# Abhiram Pamula

# initiate timer

import time
import json


# input file containing site names and locations (formatting needed)
filename = r"E:\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\Landsat\SpatialData\grandlake.csv"

# destination directory where landsat images will be downloaded
destination = r'sentinel'

# login information for the USGS Earth Explorer Website
username = 'abhiramp1'
password = 'Demokboys2020'
user = (username, password)

# start and end date (formatting must be the same YYYY-MO-DA)
start = '2011-06-01'
end   = '2011-07-30'

from Landsat_Tool import Landsat_Tool

# create the landsat extraction tool and login
l = Landsat_Tool(user, destination = destination)
l.login()

# find all images available for the test location between test dates
# matches is a list of the available product ids
matches = l.search(filename, start, end)
print('Possible scenes include:')
print(matches)

# get urls for metadata files
metadata_urls = [l.metadata_url_constructor(m) for m in matches]

# download metadata files
for url in metadata_urls:
    l.download(url)

#find products with acceptable cloud cover percentage using metadata files,
#function defaults to 10%
#the function finds all metadata txt files in the metadata folder located within
#the defined destination
candidates = l.check_cloud_cover()

# # candidates is now all scenes which cover the area of interest and have acceptable
# # cloud cover levels
# # construct urls to download all the bands for candidates
urls = [l.url_constructor(c) for c in candidates]
#
#
# Here are two different use cases for this script:
#
# #downloading collection 1 data
#download bands 1 - 11 for each product
for product in urls:
    for url in product:
        l.download(url)
        time.sleep(2)

#ordering surface reflectance prodcuts from the USGS
# order = l.espa_api('available-products', body=dict(inputs=candidates))
# print(json.dumps(order, indent=4))

#order is dictionary with all the available products for
#the scenes queried

#replace all the available products with just what we want in this case the surface
#reflectance
# for sensor in order.keys():
    # if isinstance(order[sensor], dict) and order[sensor].get('inputs'):
        # if set(candidates) & set(order[sensor]['inputs']):
            # order[sensor]['products'] = ['sr']
        # if set(candidates) & set(order[sensor]['inputs']):
            # order[sensor]['products'] = ['sr']

# order['format'] = 'gtiff'

# print(json.dumps(order, indent=4))
# resp = l.espa_api('order', verb='post',body=order)
# print('order submitted')
# print('orderid is: {}'.format(resp['orderid']))

#check the status of all orders assosciated with email
# l.check_status()

# view all completed orders
# this should be automated with windows task manager using the script Order_Status.py
# Windows Task Manager: Start a Program: the path to your python installation exe and path to the Order_Status.py file
# completed_orders = l.retrieve_completed_orders()
# l.espa_download(completed_orders)
# l.extract_tar(r"C:\Users\Abu\Desktop\landsat\LC080270332017081001T1-SC20180530152911.tar.gz")
#l.mask_raster(r"C:\Users\Abu\Desktop\LC08_L1TP_027033_20170810_20170824_01_T1_sr_band3.tif",r"C:\Users\Abu\Downloads\MyShapefiles-20180531T164858Z-001\MyShapefiles\John Redmond Reservoir.shp",r"C:\Users\Abu\Desktop\landsat\croppped_John_Redmond_b3.tif")
#l.mask_raster(r"C:\Users\Abu\Desktop\LC08_L1TP_027033_20170810_20170824_01_T1_sr_band4.tif",r"C:\Users\Abu\Downloads\MyShapefiles-20180531T164858Z-001\MyShapefiles\John Redmond Reservoir.shp",r"C:\Users\Abu\Desktop\landsat\croppped_John_Redmond_b4.tif")
#l.calculate_index(r"C:\Users\Abu\Desktop\landsat\croppped_John_Redmond_b3.tif",r"C:\Users\Abu\Desktop\landsat\croppped_John_Redmond_b4.tif",r"C:\Users\Abu\Desktop\landsat\aglae_index_john_redmond_example.tif")
