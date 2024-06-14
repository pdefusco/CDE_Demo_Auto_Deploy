#****************************************************************************
# (C) Cloudera, Inc. 2020-2023
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Paul de Fusco
#***************************************************************************/

from os.path import exists
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from utils import *
from datetime import datetime
import sys, random, os, json, random
from sedona.spark import *
from shapely.geometry import Point
from shapely.geometry import Polygon

## CDE PROPERTIES
data_lake_name=sys.argv[1]
username=sys.argv[2]

print("\nRunning as Username: ", username)

CDE_DEMO = "TLCO"

dbname = "CDE_DEMO_{0}_{1}".format(username, CDE_DEMO)

print("\nUsing DB Name: ", dbname)

geoparquetoutputlocation = "CDE_GEOSPATIAL"

#---------------------------------------------------
#               CREATE SPARK SESSION WITH ICEBERG
#---------------------------------------------------

spark = SparkSession \
    .builder \
    .appName("IOT DEVICES LOAD") \
    .config("spark.kubernetes.access.hadoopFileSystems", data_lake_name)\
    .getOrCreate()

#---------------------------------------------------
#               CREATE SEDONA CONTEXT
#---------------------------------------------------

config = SedonaContext.builder().getOrCreate()

sedona = SedonaContext.create(spark)

sc = sedona.sparkContext
sc.setSystemProperty("sedona.global.charset", "utf8")

#---------------------------------------------------
#       SQL CLEANUP: DATABASES, TABLES, VIEWS
#---------------------------------------------------
print("JOB STARTED...")
sedona.sql("DROP DATABASE IF EXISTS {} CASCADE".format(dbname))

sedona.sql("CREATE DATABASE IF NOT EXISTS {}".format(dbname))

print("SHOW DATABASES LIKE '{}'".format(dbname))
sedona.sql("SHOW DATABASES LIKE '{}'".format(dbname)).show()
print("\n")

#-----------------------------------------------------------------------------------
# CREATE TABLE FROM DATA IN CDE FILES RESOURCE
#-----------------------------------------------------------------------------------

print("CREATING COUNTRIES RDD FROM FILE \n")
print("\n")

countries_rdd = ShapefileReader.readToGeometryRDD(sc, "/app/mount/countriesData")

print("SAVING COUNTRIES RDD TO GEOJSON FILE \n")
print("\n")

try:
    countries_rdd.saveAsGeoJSON(data_lake_name + geoparquetoutputlocation + "/countries.json")
except Exception as e:
    print("RDD NOT written successfully to cloud storage")
    print("\n")
    print(f'caught {type(e)}: e')
    print(e)

print("CREATING COUNTRIES DF FROM RDD \n")
print("\n")

countries_df = Adapter.toDf(countries_rdd, sedona)
#countries_df.printSchema()

print("SAVING COUNTRIES DF TO GEOPARQUET \n")
print("\n")

countries_df.write.mode("overwrite").format("geoparquet").save(data_lake_name + geoparquetoutputlocation + "/countries.parquet")

print("\tCOUNTRIES TABLE CREATION COMPLETED")

#-----------------------------------------------------------------------------------
# CREATE IOT DEVICES DATASET
#-----------------------------------------------------------------------------------

print("CREATING IOT DEVICES\n")
print("\n")

dg = DataGen(spark, username)

iot_points_df = dg.iot_points_gen(row_count = 100000, unique_vals=100000)
iot_points_df.createOrReplaceTempView("iot_geo_tmp")

iot_points_geo_df = sedona.sql("SELECT id, device_id, manufacturer, event_type, event_ts, \
                                ST_Point(CAST(iot_geo_tmp.latitude as Decimal(24,20)), \
                                CAST(iot_geo_tmp.longitude as Decimal(24,20))) as arealandmark \
                                FROM iot_geo_tmp")
iot_points_geo_df.show()

#-----------------------------------------------------------------------------------
# SAVE IOT DEVICES TO GEOPARQUET AND GEOJSON FILES IN CLOUD STORAGE
#-----------------------------------------------------------------------------------

#iot_points_geo_df.write.mode("overwrite").saveAsTable("{0}.IOT_GEO_DEVICES_{1}".format(dbname, username))
iot_points_geo_df.write.mode("overwrite").format("geoparquet").save(data_lake_name + geoparquetoutputlocation + "/iot_geo_devices.parquet")
iot_points_geo_df.printSchema()

#-----------------------------------------------------------------------------------
# USE SEDONA RDD API TO ANALYZE DATA
#-----------------------------------------------------------------------------------

print("\nAdapter allow you to convert geospatial data types introduced with sedona to other ones")
iotSpatialRDD = Adapter.toSpatialRdd(iot_points_geo_df, "arealandmark")

print("\nSave iotSpatialRDD as GeoJSON File in Cloud Storage")
try:
    iotSpatialRDD.saveAsGeoJSON(data_lake_name + geoparquetoutputlocation + "/iot_spatial.json")
except Exception as e:
    print("RDD NOT written successfully to cloud storage")
    print("\n")
    print(f'caught {type(e)}: e')
    print(e)

print("\nRun Analyze Function on iotSpatialRDD")
iotSpatialRDD.analyze()

print("\nTake One Row from iotSpatialRDD")
iotSpatialRDD.rawSpatialRDD.take(1)

print("\nApproximate Count of iotSpatialRDD")
print(iotSpatialRDD.approximateTotalCount)

print("\nCalculate number of records without duplicates")
print(iotSpatialRDD.countWithoutDuplicates())

print("\nApache Sedona spatial partitioning method can significantly speed up the join query. \
        Three spatial partitioning methods are available: KDB-Tree, Quad-Tree and R-Tree. \
        Two SpatialRDD must be partitioned by the same way when joined.")

print("\nSpatial partitioning data")
iotSpatialRDD.spatialPartitioning(GridType.KDBTREE)

print("\nSpatial Index")
print("\nApache Sedona provides two types of spatial indexes, \
        Quad-Tree and R-Tree. Once you specify an index type, \
        Apache Sedona will build a local tree index on each of the SpatialRDD partition.")

print("\nApply map functions, for example distance to Point(52 21)")
iotSpatialRDD.rawSpatialRDD.map(lambda x: x.geom.distance(Point(21, 52))).take(5)

print("\nKNN QUERY")
print("Which k number of geometries lays closest to other geometry.")

result = KNNQuery.SpatialKnnQuery(iotSpatialRDD, Point(-84.01, 34.01), 5, False)
print("\nKNN QUERY RESULTS")
print(result)

print("JOB COMPLETED.\n\n")
