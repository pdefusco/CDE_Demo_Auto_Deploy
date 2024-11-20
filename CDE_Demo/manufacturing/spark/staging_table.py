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

import random
import configparser
import json
import sys
import os
from os.path import exists
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.functions import lit
from utils import *
from datetime import datetime
import sys
import random

## CDE PROPERTIES
config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
environmentVar=config.get("general","externalVariable")
print(environmentVar)

## CDE PROPERTIES
data_lake_name=sys.argv[1]
username=sys.argv[2]

print("\nRunning as Username: ", username)

CDE_DEMO = "MFCT"

dbname = "CDE_DEMO_{0}_{1}".format(username, CDE_DEMO)

print("\nUsing DB Name: ", dbname)

#---------------------------------------------------
#               CREATE SPARK SESSION WITH ICEBERG
#---------------------------------------------------

spark = SparkSession \
    .builder \
    .appName("ICEBERG LOAD") \
    .getOrCreate()

#-----------------------------------------------------------------------------------
# CREATE STAGING DATASET 1 WITH SOME TARGET ID'S
#-----------------------------------------------------------------------------------

print("SAMPLING ID'S FROM TARGET TABLE\n")
print("\n")

ROW_PERCENT_car_sales_source_sample = random.randint(1,100)

print("SAMPLING {} PERCENT ROWS FROM TARGET TABLE".format(ROW_PERCENT_car_sales_source_sample))

car_sales_id_source_sample_df = spark.sql("SELECT ID FROM {0}.CAR_SALES_{1} TABLESAMPLE ({2} PERCENT)"\
        .format(dbname, username, ROW_PERCENT_car_sales_source_sample))

ROW_COUNT_car_sales_gen = car_sales_id_source_sample_df.count()

dg = DataGen(spark, username)

x_gen = random.randint(1, 3)
y_gen = random.randint(1, 4)
z_gen = random.randint(2, 5)

def check_partitions(partitions):
  if partitions > 100:
    partitions = 100
  if partitions < 5:
    partitions = 5
  else:
    return partitions
  return partitions

UNIQUE_VALS_car_sales_gen = random.randint(500, ROW_COUNT_car_sales_gen-1)
PARTITIONS_NUM_car_sales_gen = round(ROW_COUNT_car_sales_gen / UNIQUE_VALS_car_sales_gen)
PARTITIONS_NUM_car_sales_gen = check_partitions(PARTITIONS_NUM_car_sales_gen)

car_sales_staging_df = dg.car_sales_gen(x_gen, y_gen, z_gen, PARTITIONS_NUM_car_sales_gen, ROW_COUNT_car_sales_gen, UNIQUE_VALS_car_sales_gen, True)

car_sales_staging_df = car_sales_staging_df.drop("id")

df1 = car_sales_id_source_sample_df.unionByName(car_sales_staging_df, allowMissingColumns=True)

#-----------------------------------------------------------------------------------
# CREATE DATASETS WITH RANDOM DISTRIBUTIONS
#-----------------------------------------------------------------------------------

dg = DataGen(spark, username)

x_gen = random.randint(1, 3)
y_gen = random.randint(1, 4)
z_gen = random.randint(2, 5)

def check_partitions(partitions):
  if partitions > 100:
    partitions = 100
  if partitions < 5:
    partitions = 5
  else:
    return partitions
  return partitions

ROW_COUNT_car_sales_gen = random.randint(1, 499999)
UNIQUE_VALS_car_sales_gen = random.randint(500, ROW_COUNT_car_sales_gen-1)
PARTITIONS_NUM_car_sales_gen = round(ROW_COUNT_car_sales_gen / UNIQUE_VALS_car_sales_gen)
PARTITIONS_NUM_car_sales_gen = check_partitions(PARTITIONS_NUM_car_sales_gen)

print("SPARKGEN PIPELINE SPARK HYPERPARAMS")
print("\n")
print("x: {}".format(x_gen))
print("y: {}".format(y_gen))
print("z: {}".format(z_gen))
print("\n")
print("ROW_COUNT_car_sales: {}".format(ROW_COUNT_car_sales_gen))
print("UNIQUE_VALS_car_sales: {}".format(UNIQUE_VALS_car_sales_gen))
print("PARTITIONS_NUM_car_sales: {}".format(PARTITIONS_NUM_car_sales_gen))
print("\n")

df2 = dg.car_sales_gen(x_gen, y_gen, z_gen, PARTITIONS_NUM_car_sales_gen, ROW_COUNT_car_sales_gen, UNIQUE_VALS_car_sales_gen, True)

print("CREATING ICBERG TABLES FROM SPARK DATAFRAMES \n")
print("\n")

car_sales_staging_df = df1.union(df2)

car_sales_staging_df = car_sales_staging_df.dropDuplicates(['id'])

car_sales_staging_df.writeTo("{0}.CAR_SALES_STAGING_{1}".format(dbname, username))\
    .using("iceberg").tableProperty("write.format.default", "parquet").createOrReplace()

print("\tPOPULATE TABLE(S) COMPLETED")

print("JOB COMPLETED.\n\n")
