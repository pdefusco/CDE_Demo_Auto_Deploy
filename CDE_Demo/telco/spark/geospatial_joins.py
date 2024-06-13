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

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import random, os, sys
from datetime import datetime
from sedona.spark import *
from keplergl import KeplerGl
from pyspark.sql.functions import col, expr, when

## CDE PROPERTIES
data_lake_name=sys.argv[1]
username=sys.argv[2]

print("\nRunning as Username: ", username)

CDE_DEMO = "TLCO"

dbname = "CDE_DEMO_{0}_{1}".format(username, CDE_DEMO)

print("\nUsing DB Name: ", dbname)

geoparquetoutputlocation = "CDE_GEOSPATIAL"

#---------------------------------------------------
#               CREATE SPARK SESSION
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

# Show catalog and database
print("SHOW CURRENT NAMESPACE")
sedona.sql("SHOW CURRENT NAMESPACE").show()
sedona.sql("USE {}".format(dbname))

# Show catalog and database
print("SHOW NEW NAMESPACE IN USE\n")
sedona.sql("SHOW CURRENT NAMESPACE").show()

_DEBUG_ = False

#---------------------------------------------------
#                READ SOURCE FILES
#---------------------------------------------------

from sedona.core.formatMapper import GeoJsonReader

geo_json_file_location = data_lake_name + geoparquetoutputlocation + "/iot_spatial.json"
saved_rdd_iot = GeoJsonReader.readToGeometryRDD(sc, geo_json_file_location)

saved_rdd_countries = ShapefileReader.readToGeometryRDD(sc, "/app/mount/countriesData")

iot_geo_devices_df = Adapter.toDf(saved_rdd_iot, sedona)
iot_geo_devices_df.printSchema()

countries_geo_df = Adapter.toDf(saved_rdd_countries, sedona)
countries_geo_df.printSchema()

print("\nSHOW IOT GEO DEVICES DF")
#iot_geo_devices_df.show()
print("\nSHOW COUNTRIES DF")
#countries_geo_df.show()

iot_geo_devices_df.createOrReplaceTempView("IOT_GEO_DEVICES_{}".format(username))
countries_geo_df.createOrReplaceTempView("COUNTRIES_{}".format(username))

#---------------------------------------------------
#               GEOSPATIAL JOIN
#---------------------------------------------------
print("GEOSPATIAL JOIN...")

GEOSPATIAL_JOIN = """
                    SELECT c.geometry as country_geom,
                            c.NAME_EN,
                            a.geometry as iot_device_location,
                            a.device_id
                    FROM COUNTRIES_{0} c, IOT_GEO_DEVICES_{0} a
                    WHERE ST_Contains(c.geometry, a.geometry)
                    """.format(username)

result = sedona.sql(GEOSPATIAL_JOIN)
result.explain()
result.show()

result.createOrReplaceTempView("result")

print("JOB COMPLETED!\n\n")
