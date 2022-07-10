#Landsat_Tool for downloading landsat scenes
import csv
#from selenium import webdriver
import json
import glob
from usgs import api
import requests
import os
import shapefile
# import rasterio
import tarfile
#import wget
import numpy
#import matplotlib.pyplot as plt
# from rasterio.mask import mask
from urllib.request import urlopen
import xml.etree.ElementTree as ET
# import gsutil
#import subprocess

class Sentinel_Tool(object):
    '''
    tool to download Sentinel scenes from google cloud services
    :params:

    user, type tuple, (username, password)
    destination: type str, directory to download landsat images into

    :optional params:
    dataset: type str, which satellite dataset to query defaults to LANDSAT_8_C1
    which is the code for LANDSAT_8 collection 1 data
    other dataset codes found at http://kapadia.github.io/usgs/_sources/reference/catalog/ee.txt

    '''

    def __init__(self,user,destination=None,dataset='SENTINEL_2A'):
        self.user = tuple(user)
        self.username = user[0]
        self.password = user[1]
        self.dataset = dataset
        self.node = 'EE'
        self.destination = destination
        if self.destination is None: #if no destination given in init method set destination to the directory of this python script
            self.destination = os.path.dirname(os.path.abspath(__file__))
        if self.destination is not None: #if destination does not exist, make it
            if not os.path.isdir(self.destination):
                os.mkdir(self.destination)
        self.metadatafolder = os.path.join(self.destination,'metadata')
        if not os.path.isdir(self.metadatafolder):
            os.mkdir(self.metadatafolder)
        self.urltemplate = 'https://storage.googleapis.com/gcp-public-data-landsat/{}/01/{}/{}/{}/{}_B{}.TIF'
        self.metadata = 'https://storage.googleapis.com/gcp-public-data-landsat/{}/01/{}/{}/{}/{}_MTL.txt'
        self.host = 'https://espa.cr.usgs.gov/api/v1/'

    def login(self):
        api.login(self.username,self.password)

    def _get_coordinates(self,csvfile):
        '''
        private method to read the .csv file with list of coordinates
        file must be of the format.

        siteid,lat,long
        bear,32.45345,-94.11423
        cat,32.34234,-94.12321
        '''
        coordinates = []
        with open(csvfile) as csvfile:
            reader = csv.reader(csvfile)
            for i,row in enumerate(reader):
                if i != 0:
                    coordinates.append((row[1],row[2]))

        return coordinates

    def search(self,csvfile,start,end,dataset=None,):
        '''
        method for finding scene ids given a list of coordinates

        params:
        csvfile: type str, path to csv file with format specified in _get_coordinates
        start: type str, start date of query format 'yyyy-mm-dd' ex. '2015-07-13'
        end: type str, end date of query format 'yyyy-mm-dd'
        optional params:
        dataset: type str, which satellite dataset to query defaults to LANDSAT_8_C1
        which is the code for LANDSAT_8 collection 1 data
        other dataset codes found at http://kapadia.github.io/usgs/_sources/reference/catalog/ee.txt

        '''
        coordinates = self._get_coordinates(csvfile)
        if dataset is None:
            dataset = self.dataset

        for loc in coordinates:
            response = api.search(dataset,self.node,lat=float(loc[0]),lng=float(loc[1]),start_date=start,end_date=end,extended =True)
            data = response['data']
            results = data['results']
            final_candidates = []
            for r in results:
                cloud_cover = r.get("cloudCover")
                data_access_url = r.get("metadataUrl")
                disp_id = r.get("displayId")
                # print(r)
                tile = r.get("summary").split(',')[3].split(':')[1]
                if float(cloud_cover) < 10.0:
                    final_candidates.append((data_access_url,tile,disp_id))
            print(final_candidates)
            return final_candidates
        
    def productid(self,url):
        var_url = urlopen(url)
        tree = ET.parse(var_url)
        root = tree.getroot()
        metadata_root = list(root)[0]
        for child in metadata_root:
            attribs = child.attrib
            if 'name' in attribs.keys():
                if child.attrib['name'] == 'Vendor Product ID':
                    return(list(child)[0].text)
                
    def tileid(self,url):
        var_url = urlopen(url)
        tree = ET.parse(var_url)
        root = tree.getroot()
        metadata_root = list(root)[0]
        for child in metadata_root.iter():
            attribs = child.attrib
            if 'name' in attribs.keys():
                if child.attrib['name'] == 'Vendor Tile ID':
                    return(list(child)[0].text)
                
    def sentinel_url_constructor(self,destination,url):
        self.title = url[1]
        # self.download(url[0])
        self.display_id = url[2]
        self.product_id = self.productid(url[0])
        if self.display_id.startswith("L1C"):
            #print("********IN LIC*****************")
            #https://console.cloud.google.com/storage/browser/gcp-public-data-sentinel-2/tiles/15/S/UA/S2A_MSIL1C_20161221T171722_N0204_R112_T15SUA_20161221T172206.SAFE
            tile1 =self.title[2:4]
            tile2 = self.title[4]
            tile3 = self.title[-2:]
            datef = self.product_id.split('_')[2].lstrip()
            #print(tile1,tile2,tile3,self.product_id,self.display_id)
            # self.sentinel_url = 'https://console.cloud.google.com/storage/browser/_details/gcp-public-data-sentinel-2/tiles/{}/{}/{}/{}.SAFE/GRANULE/{}/IMG_DATA/{}_{}_B0{}.jp2'
            self.sentinel_url = 'https://storage.googleapis.com/gcp-public-data-sentinel-2/tiles/{}/{}/{}/{}.SAFE/GRANULE/{}/IMG_DATA/{}_{}'
            x =self.sentinel_url.format(tile1,tile2,tile3,self.product_id,self.display_id,self.title.lstrip(),datef)
            # print(x)
        else:
            tile1 =self.title[2:4]
            tile2 = self.title[4]
            tile3 = self.title[-2:]
            product_id = self.productid(url[0])
            tile_id = self.tileid(url[0])
            #storing vendor product item elemts by splitting _
            # base_url = 'https://console.cloud.google.com/storage/browser/gcp-public-data-sentinel-2/tiles/'
            # base_url ='https://console.cloud.google.com/gcp-public-data-sentinel-2/tiles/'
            base_url ='https://storage.googleapis.com/gcp-public-data-sentinel-2/tiles/'
                   
            ven_idsp = product_id.split('_')
            tile_idsp = tile_id.split('_')
            
            pro_id = "S2A_MSIL1C_"+ven_idsp[-1] + '_' + tile_idsp[-1].replace(".","") + '_' + ven_idsp[6] + '_' + tile_idsp[-2] + '_' + ven_idsp[5] 
            # print(pro_id,"Prod ID")
            til_id = tile_id.replace("_"+tile_idsp[-1],"") 
            # self.sentinel_url = base_url + '{}/{}/{}/{}.SAFE/GRANULE/{}/IMG_DATA/{}_B0{}.jp2'
            self.sentinel_url = base_url + '{}/{}/{}/{}.SAFE/GRANULE/{}/IMG_DATA/{}'
            x =self.sentinel_url.format(tile1,tile2,tile3,pro_id,tile_id,til_id)
            # print(x)
        return x
    def url_band_constructor(self,x):
        bands=[]
        if not x == '':
            for i in range(1,13):
                if i<= 9:
                    fmt = '_B0{}.jp2'
                    self.sentinel_url = x +fmt.format(i)
                    bands.append(self.sentinel_url)
                else:
                    fmt = '_B{}.jp2'
                    self.sentinel_url =  x +fmt.format(i)
                    bands.append(self.sentinel_url)
        return bands
            
                    
            

    def check_cloud_cover(self,percent_cloud_cover=10):
        '''
        percent_cloud_cover: percentage of cloud cover which is acceptable
        '''
        print('desired cloud cover percentage is less than or equal to {}%'.format(percent_cloud_cover))
        candidates = []
        files = glob.glob(os.path.join(self.metadatafolder,'*.txt'))
        text = 'CLOUD_COVER'
        for file in files:
            with open(file,'r') as f:
                for line in f:
                    if text in line:
                        matchedline = line
                        z = matchedline.partition("=")
                        cloudcover,sep,value = z
                        value = float(value.strip(' ').strip('\n'))

                        if value <= percent_cloud_cover:
                            print(file, 'has {}% cloud cover, adding to candidates'.format(value))
                            y = file.rsplit('_',1)[0].rsplit(os.sep,1)[1]
                            candidates.append(y)
                        else:
                            print(file, 'has {}% cloud cover, removed from candidates'.format(value))
                        break
        print('scenes which meet the desired cloud cover percentage of less than or equal to {}% are:\n'.format(percent_cloud_cover), candidates)
        return candidates


    def download(self,url):
        local_filename = url.split('/')[-1]
        if local_filename.endswith('.txt'):
            destination = os.path.join(self.metadatafolder,local_filename)
            if not os.path.isfile(destination):
                print('starting download of {}'.format(local_filename))
                r = requests.get(url, stream=True)
                with open(destination, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print('finished download of {}'.format(local_filename))
            else:
                print('{} already exists moving on'.format(destination))
        else:
            destination = os.path.join(self.destination,local_filename)
            if not os.path.isfile(destination):
                print('starting download of {}'.format(local_filename))
                r = requests.get(url, stream=True)
                with open(destination, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print('finished download of {}'.format(local_filename))
            else:
                print('{} already exists moving on'.format(destination))
        return local_filename
    
    def espa_api(self, endpoint, verb='get', body=None,verbose=False):
        """
        method to interact with the ESPA json API
        params:
        endpoint, type str, URI to be accessed
        verb, type str, HTTP method to be used
        body, type dict, inputs to be sent to the api
        verbose, type str, print HTTP status_code if True

        """
        response = getattr(requests, verb)(self.host + endpoint, auth=self.user, json=body)

        data = response.json()

        if verbose is True:
            print('{} {}'.format(response.status_code, response.reason))

            if isinstance(data, dict):
                messages = data.pop("messages", None)
                if messages:
                    print(json.dumps(messages, indent=4))
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
            return None
        else:
            return data

    def espa_download(self,orders):
        '''
        orders, type list, completed orders to be downloaded
        '''
        for o in orders:
            orderstatus = self.espa_api('item-status/{}'.format(o))
            download_url = orderstatus[o][0]['product_dload_url']
            self.download(download_url)

    def list_orders(self):
        resp = self.espa_api('user')
        email = resp['email']
        all_orders = self.espa_api('list-orders/{0}'.format(email or ''))
        print('the following orders associated with {}'.format(email))
        return all_orders

    def check_status(self):
        orders = self.list_orders()
        for o in orders:
            orderstatus = self.espa_api('order-status/{}'.format(o))
            print(orderstatus)
    def retrieve_completed_orders(self):
        resp = self.espa_api('user')
        email = resp['email']
        filters = {'status': 'complete'}
        all_orders = self.espa_api('list-orders/{0}'.format(email or ''),
                                      body=filters)
        print('the following orders associated with {} are completed:\n'.format(email),all_orders)
        return all_orders

    def extract_tar(self,filename):
        '''
        extract all the tar.gz files in specified folder
        '''

        tar = tarfile.open(filename)
        tar.extractall()
        tar.close()


    def mask_raster(self, raster, shape, destination):

        sh = shapefile.Reader(shape)
        #first feature of the shapefile
        features = []
        for shape_rec in sh.shapeRecords():
            print(shape_rec.record)
        feature = sh.shapeRecords()[0]
        first = feature.shape.__geo_interface__
        features.append(first)

        with rasterio.open(raster) as src:
            print(src.meta)
            out_image, out_transform = mask(src, features,crop=True)
            out_meta = src.meta.copy()

        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        with rasterio.open(destination, "w", **out_meta) as dest:
            dest.write(out_image)

    def calculate_index(self, raster1, raster2,destination):
        with rasterio.open(raster1) as src1:
            b1 = src1.read()
        with rasterio.open(raster2) as src2:
            b2 = src2.read()
        # Allow division by zero
        numpy.seterr(divide='ignore', invalid='ignore')
        index = (b1.astype(float)-b2.astype(float)) / (b1+b2)
        print(index.shape)
        out_meta = src2.meta.copy()

        out_meta.update({"driver": "GTiff",
                        "height": index.shape[1],
                        "width": index.shape[2],
                        "dtype": 'float64'
                        })
        print(out_meta)
        with rasterio.open(destination,'w',**out_meta) as dest:
            dest.write(index)
