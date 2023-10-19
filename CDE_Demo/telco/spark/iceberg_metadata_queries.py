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
from datetime import datetime
import sys
import random

## CDE PROPERTIES
config = configparser.ConfigParser()
config.read('/app/mount/parameters.conf')
data_lake_name=config.get("general","data_lake_name")
username=config.get("general","username")

print("\nRunning as Username: ", username)

dbname = "CDE_DEMO_{}".format(username)

print("\nUsing DB Name: ", dbname)

#---------------------------------------------------
#               CREATE SPARK SESSION WITH ICEBERG
#---------------------------------------------------

spark = SparkSession \
    .builder \
    .appName("ICEBERG METADATA") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")\
    .config("spark.sql.catalog.spark_catalog.type", "hive")\
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
    .config("spark.kubernetes.access.hadoopFileSystems", data_lake_name)\
    .getOrCreate()

#---------------------------------------------------
#               ICEBERG METADATA QUERIES
#---------------------------------------------------

try:
    spark.sql("SELECT * FROM {0}.CAR_SALES_{1}.history".format(dbname, username)).show()
except Exception as e:
    print(f'caught {type(e)}: e')
    print("Query did not run Successfully")

print("""Finding the latest snapshot with a previous schema: Maybe you made a change to the schema, and
now want to go back to the previous schema. You’ll want to find the latest snapshot using that schema which can be determined with a
query that will rank the snapshots for each schema_id then return only the top ranked snapshot for each schema_id:""")

QUERY = "WITH Ranked_Entries AS (\
    SELECT \
        latest_snapshot_id, \
        latest_schema_id, \
        timestamp, \
        ROW_NUMBER() OVER(PARTITION BY latest_schema_id ORDER BY timestamp DESC) as row_num\
    FROM \
        {0}.CAR_SALES_{1}.metadata_log_entries\
    WHERE \
        latest_schema_id IS NOT NULL\
)\
SELECT \
    latest_snapshot_id,\
    latest_schema_id,\
    timestamp AS latest_timestamp\
FROM \
    Ranked_Entries\
WHERE \
    row_num = 1\
ORDER BY \
    latest_schema_id DESC;".format(dbname, username)

print(QUERY)

try:
    spark.sql(QUERY).show()
except Exception as e:
    print(f'caught {type(e)}: e')
    print("Query did not run Successfully")

print("ALL METADATA LOG ENTRIES")
QUERY = "SELECT * FROM {0}.CAR_SALES_{1}.metadata_log_entries;".format(dbname, username)
print(QUERY)

try:
    spark.sql(QUERY).show()
except Exception as e:
    print(f'caught {type(e)}: e')
    print("Query did not run Successfully")

print("""Understanding Data Addition Patterns: Another use case is to understand the pattern of data additions to the table.
This could be useful in capacity planning or understanding data growth over time.
 Here is an SQL query that shows the total records added at each snapshot:""")

QUERY = "SELECT \
            committed_at,\
            snapshot_id,\
            summary['added-records'] AS added_records\
        FROM \
            {0}.CAR_SALES_{1}.snapshots;".format(dbname, username)

try:
    spark.sql(QUERY).show()
except Exception as e:
    print(f'caught {type(e)}: e')
    print("Query did not run Successfully")

print("""Monitoring Operations Over Time: Another use case for the snapshots metadata table is
to monitor the types and frequency of operations performed on the table over time.
This could be useful in understanding the workload and usage patterns of the table.
Here is an SQL query that shows the count of each operation type over time:""")

QUERY = "SELECT \
            operation,\
            COUNT(*) AS operation_count,\
            DATE(committed_at) AS date\
        FROM \
            {0}.CAR_SALES_{1}.snapshots\
        GROUP BY \
            operation, \
            DATE(committed_at)\
        ORDER BY \
            date;".format(dbname, username)

try:
    spark.sql(QUERY).show()
except Exception as e:
    print(f'caught {type(e)}: e')
    print("Query did not run Successfully")

print("QUERY ALL SNAPSHOTS")
QUERY = "SELECT * FROM {0}.CAR_SALES_{1}.snapshots;".format(dbname, username)

try:
    spark.sql(QUERY).show()
except Exception as e:
    print(f'caught {type(e)}: e')
    print("Query did not run Successfully")
