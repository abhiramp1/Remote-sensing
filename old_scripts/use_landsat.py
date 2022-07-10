# example usage of landsat tool
# Abhiram Pamula

# initiate timer

import time
import json


# input file containing site names and locations (formatting needed)
filename = r"C:\Users\abhir\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\Landsat\SpatialData\grandlake.csv"

# destination directory where landsat images will be downloaded
destination = r'grandlake'

# login information for the USGS Earth Explorer Website
username = 'abhiramp1'
password = 'Jeloabar143#'
user = (username, password)

# start and end date (formatting must be the same YYYY-MO-DA)
start = '2014-06-01'
end   = '2014-07-30'

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


