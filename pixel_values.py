# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 12:12:35 2020

@author: apamula
"""

#Import the required libraries
import pandas as pd
from osgeo import gdal, osr, ogr
from matplotlib import pyplot as plt


#Give the path to the shapefile and rasterfile
shp = r"C:\Users\abhiram\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\github\Clipping_raster\Grand_Lake_4326"
raster = r"C:\Users\abhiram\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\Landsat\landsat\Grand_Lake_GRDA\LC08_L1TP_026035_20160512_20170223_01_T1_B11.TIF"


#Open the raster in gdal and read it as an array
srcImage = gdal.Open(raster)

srcArray = srcImage.ReadAsArray()

geoTrans = srcImage.GetGeoTransform()


#Read the csv file using pandas
df = pd.read_csv(r"C:\Users\abhiram\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\GRDA\Hudson\GRDA_Hudson_05-12-2016.csv",encoding= 'unicode_escape')

#print(df.head())

lat = df['Lat'].tolist()
lon = df['Long'].tolist()

points = [(lon[i],lat[i]) for i in range(0,len(lon))]

# get the source reference
driver = ogr.GetDriverByName('ESRI Shapefile')
dataset = driver.Open(shp + '.shp')
layer = dataset.GetLayer()
inSpatialRef = layer.GetSpatialRef()
dataset = None

# get the destination reference
outSpatialRef = osr.SpatialReference()
dataset = gdal.Open(raster)
prj = dataset.GetProjection()
outSpatialRef = osr.SpatialReference(wkt=prj)
dataset = None

# create the transform
transform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

x_point = []
y_point = []
for i,j in points:
    x,y,z = transform.TransformPoint(i,j)
    x_point.append(x)
    y_point.append(y)

def world_to_pixel(geo_matrix, x, y):
    ul_x= geo_matrix[0]
    ul_y = geo_matrix[3]
    x_dist = geo_matrix[1]
    y_dist = geo_matrix[5]
    pixel = int((x - ul_x) / x_dist)
    line = -int((ul_y - y) / y_dist)
    return pixel, line

points_list = [(x_point[i],y_point[i]) for i in range(0,len(x_point))]

x_pos = []
y_pos = []
for i,j in points_list:   
    X_pos,Y_pos = world_to_pixel(geoTrans, i, j)
    x_pos.append(X_pos)
    y_pos.append(Y_pos)
    
pixel_locs = [(x_pos[i],y_pos[i]) for i in range(0,len(x_pos))] 

pixel_values = []    
for i,j in pixel_locs:
    pixel_values.append(srcArray[j][i])
    
df['Thermal Infrared (TIRS) 2 (B11)-(11.5-12.51)'] = pixel_values

df.to_csv(r"C:\Users\abhiram\OneDrive - Oklahoma A and M System\Oklahoma State University\GRA\Water quality monitoring\GRDA\Hudson\GRDA_Hudson_05-12-2016.csv", index = False, header=True)