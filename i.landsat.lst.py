#!/usr/bin/env python2

# Install i.landsat8.swlst via the installer

# Import Libraries
import glob
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules import Module
from grass.script import setup as gsetup
from grass.pygrass.gis import Mapset
import grass.script as grass 

# Define path to Landsat images
path = "/media/sf_GEO450/scenes/test_marc/landsat-8/"

#Define Path to AOI
path_aoi = "/media/sf_GEO450/AOI/jena-roda-testsite.shp"

#Define path to landcover
path_landcover = "/media/sf_GEO450/FROM-GLC/landcover_merged"

#Define path to the output
path_output = path

# Set mapset parameter
mapset = Mapset()
#print mapset

# Look up B10 and B11 TIF-files in dir + subdirs and write path/filename to "files"
files = glob.glob(path + '/**/*B[1][0-1].TIF')

# Look up BQA TIF-files in dir + subdirs and write path/filename to "files_temp"
files_bqa = glob.glob(path + '/**/*BQA.TIF')

# Create list with B10 only (for lst creation)
#files_b10 = glob.glob(path + '/**/*B[1][0].TIF')

# Add "files_temp" to "files"
files.extend(files_bqa)

# Import AOI from file
Module("v.import",
    overwrite = True,
    input= "/media/sf_GEO450/AOI/jena-roda-testsite.shp", 
    output="aoi")

# Set AOI as Region
Module("g.region",
    overwrite = True, 
    vector="aoi@PERMANENT")

# Import each file "LC08xxxxxxxxxxxx"
for i in files:
    Module("r.import",
       overwrite = True, 
       memory = 2000,
       input = i,
       output = i[-28:-4],
	extent = "region")

# Import landcover map
Module("r.import",
       overwrite = True, 
       memory = 2000,
       input = path_landcover,
       output = "landcover", extent = "region")

# Apply LST-Skript and export TIFs
for i in files_bqa:
	Module("i.landsat8.swlst", 
	overwrite = True, 
	mtl= i[0:len(i)-7]+"MTL.txt",
	b10=i[-28:-7]+ "B10@" + str(mapset),
	b11=i[-28:-7]+"B11@" + str(mapset),
	qab=i[-28:-4]+ "@" + str(mapset),
	landcover="landcover@"+str(mapset),
	lst=i[-28:-7]+"_LST")
    	Module("r.out.gdal",
    	flags = "f",
    	overwrite = True,
    	input= i[-28:-7]+"_LST@" + str(mapset),
   	output= path_output + i[-28:-7]+"_LST.TIF",
    	format="GTiff",
    	type="UInt16",
    	nodata=9999)

# Remove everything (does not delete files, only maps)
# g.remove type=raster,vector pattern=* -f

