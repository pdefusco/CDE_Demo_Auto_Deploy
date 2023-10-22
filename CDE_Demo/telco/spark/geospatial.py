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
from pyspark.sql.functions import lit
import configparser
from datetime import datetime
import os
import random
from datetime import datetime
import sys
from sedona.spark import *

## CDE PROPERTIES
config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
data_lake_name=config.get("general","data_lake_name")
username=config.get("general","username")

print("\nRunning as Username: ", username)

dbname = "CDE_DEMO_{}".format(username)

print("\nUsing DB Name: ", dbname)

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

config = SedonaContext.builder().\
    config('spark.jars.packages',
           'org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.4.1,'
           'org.datasyslab:geotools-wrapper:1.4.0-28.2'). \
    getOrCreate()

sedona = SedonaContext.create(spark)

sc = sedona.sparkContext
sc.setSystemProperty("sedona.global.charset", "utf8")

# Show catalog and database
print("SHOW CURRENT NAMESPACE")
spark.sql("SHOW CURRENT NAMESPACE").show()
spark.sql("USE {}".format(dbname))

# Show catalog and database
print("SHOW NEW NAMESPACE IN USE\n")
spark.sql("SHOW CURRENT NAMESPACE").show()

_DEBUG_ = False

#---------------------------------------------------
#                READ SOURCE TABLES
#---------------------------------------------------
print("JOB STARTED...")

iot_geo_devices_df = spark.sql("SELECT * FROM {0}.IOT_GEO_DEVICES_{1}".format(dbname, username)) #could also checkpoint here but need to set checkpoint dir
countries_geo_df = spark.sql("SELECT * FROM {0}.COUNTRIES_{1}".format(dbname, username))

print("\tREAD TABLE(S) COMPLETED")

#---------------------------------------------------
#               GEOSPATIAL JOIN
#---------------------------------------------------
print("GEOSPATIAL JOIN...")

GEOSPATIAL_JOIN = """
                    SELECT c.geometry as country_geom,
                            c.NAME_EN, a.arealandmark as iot_device_location,
                            a.device_id
                    FROM {0}.COUNTRIES_{1} c, {2}.IOT_GEO_DEVICES_{3} a
                    WHERE ST_Contains(c.geometry, a.arealandmark)
                    """.format(dbname, username, dbname, username)

result = sedona.sql(GEOSPATIAL_JOIN)

result.createOrReplaceTempView("result")

#---------------------------------------------------
#               GEOSPATIAL GROUP BY
#---------------------------------------------------

groupedresult = sedona.sql("""SELECT c.NAME_EN, c.country_geom, count(*) as DeviceCount
                            FROM result c
                            GROUP BY c.NAME_EN, c.country_geom""")
groupedresult.show()

#---------------------------------------------------
#               GEOSPATIAL DISTANCE JOIN
#---------------------------------------------------

iot_geo_df_sample = spark.sql("SELECT * FROM {0}.IOT_GEO_DEVICES_{1} LIMIT 10".format(dbname, username))
iot_geo_df_sample.createOrReplaceTempView("iot_geo_df_sample")

distance_join = """
                SELECT *
                FROM iot_geo_df_sample a, {0}.IOT_GEO_DEVICES_{1} b
                WHERE ST_Distance(a.arealandmark,b.arealandmark) < 2
                """.format(dbname, username))

print("SELECTING ALL IOT DEVICES LOCATED WITHIN PROVIDED DISTANCE OF THE TEN PROVIDED IOT DEVICES")
spark.sql(distance_join).show()

print(iot_geo_df.count())
print(spark.sql(distance_join).count())


print("JOB COMPLETED!\n\n")
