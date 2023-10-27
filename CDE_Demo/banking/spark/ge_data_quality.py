#****************************************************************************
# (C) Cloudera, Inc. 2020-2022
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

import os
import sys
print("Python version:")
print(sys.version)

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.sql.functions as F
#import great_expectations as gx
from great_expectations.profile.basic_dataset_profiler import BasicDatasetProfiler
from great_expectations.dataset.sparkdf_dataset import SparkDFDataset
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
import time
import sys, random, os, json, random, configparser

# EXPECTATIONS ON ALL COLUMNS

def run_existance_expactation(gdf, MANDATORY_COLUMNS):
    for column in MANDATORY_COLUMNS:
        try:
            assert gdf.expect_column_to_exist(column).success, f"Column {column} is not found\n"
            print(f"Column {column} is found")
        except Exception as e:
            print(e)

def run_cols_not_null_expectation(gdf, MANDATORY_COLUMNS):
    for column in MANDATORY_COLUMNS:
        try:
            test_result = gdf.expect_column_values_to_not_be_null(column)
            assert test_result.success, f"Values for column {column} are null\n"
            print(f"Values for column {column} are not null")
        except Exception as e:
            print(e)

# EXPECTATIONS ON NUMERIC COLUMNS

def run_longitude_min_expectation(gdf):
    try:
        test_result = gdf.expect_column_min_to_be_between(column="longitude", min_value=-180, max_value=180).success, f"Min for column longitude is not within expected range\n"
        assert test_result.success, f"Min for column longitude is within expected range\n"
    except Exception as e:
            print(e)

def run_latitude_max_expectation(gdf):
    try:
        test_result = gdf.expect_column_max_to_be_between(column="latitude", min_value=-90, max_value=90).success, f"Max for column latitude is not within expected range\n"
        assert test_result.success, f"Max for column latitude is within expected range\n"
    except Exception as e:
            print(e)

def run_transaction_amount_mean_expectation(gdf):
    try:
        test_result = gdf.expect_column_mean_to_be_between(column="transaction_amount", min_value=0, max_value=10000).success, f"Mean for column transaction_amount is not within expected range\n"
        assert test_result.success, f"Mean for column transaction_amount is within expected range\n"
    except Exception as e:
        print(e)

def run_transaction_amount_stdev_expectation(gdf):
    try:
        test_result = gdf.expect_column_stdev_to_be_between(column="transaction_amount", min_value=1, max_value=10).success, f"STDEV for column transaction_amount is not within expected range\n"
        assert test_result.success, f"STDEV for column transaction_amount is within expected range\n"
    except Exception as e:
        print(e)

# EXPECTATIONS ON STRING COLUMNS

def run_email_match_regex_expectation(gdf):
    try:
        test_result = gdf.expect_column_values_to_match_regex(column="email", regex="^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$").success, f"Values for column Email are not within REGEX Pattern\n"
        assert test_result.success, f"Values for column Email are within REGEX Pattern\n"
    except Exception as e:
        print(e)

def run_email_not_match_regex_expectation(gdf):
    try:
        test_result = gdf.expect_column_values_to_not_match_regex(column="email", regex='@"\d{10}"').success, f"Values for column Email are withing REGEX Pattern\n"
        assert test_result.success, f"Values for column Email are not withing REGEX Pattern\n"
    except Exception as e:
        print(e)

def run_ccn_lenght_expectation(gdf):
    try:
        test_result = gdf.expect_column_value_lengths_to_be_between(column="credit_card_number", min_value=10, max_value=25).success, f"Column credit_card_number length is not within expected range\n"
        assert test_result.success, f"Column credit_card_number length is within expected range\n"
    except Exception as e:
        print(e)

# EXPECTATIONS ON CATEGORICAL COLUMNS

def run_transaction_curr_distinct_values_expectation(gdf):
    try:
        test_result = gdf.expect_column_distinct_values_to_be_in_set(column="transaction_currency", value_set=["USD", "EUR", "KWD", "BHD", "GBP", "CHF", "MEX"]).success, f"Expected values for column transaction_currency is not within provided set\n"
        assert test_result.success, f"Expected values for column transaction_currency is within provided set\n"
    except Exception as e:
        print(e)

def run_transaction_curr_values_contain_set_expectation(gdf):
    try:
        test_result = gdf.expect_column_distinct_values_to_contain_set(column="is_referral", value_set=["USD", "EUR", "KWD", "BHD", "GBP", "CHF", "MEX"]).success, f"Expected values for column transaction_currency do not contain provided set\n"
        assert test_result.success, f"Expected values for column transaction_currency contain provided set\n"
    except Exception as e:
        print(e)

def run_transaction_curr_values_match_set_expectation(gdf):
    try:
        test_result = gdf.expect_column_distinct_values_to_equal_set(column="conversion", value_set=["USD", "EUR", "KWD", "BHD", "GBP", "CHF", "MEX"]).success, f"Expected values for column transaction_currency do not equal provided set\n"
        assert test_result.success, f"Expected values for column transaction_currency equal provided set\n"
    except Exception as e:
        print(e)


def main():

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
    #spark = SparkSession.builder.appName('INGEST').config("spark.kubernetes.access.hadoopFileSystems", data_lake_name).getOrCreate()

    spark = SparkSession \
        .builder \
        .appName("BANK TRANSACTIONS DATA QUALITY") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")\
        .config("spark.sql.catalog.spark_catalog.type", "hive")\
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
        .config("spark.kubernetes.access.hadoopFileSystems", data_lake_name)\
        .getOrCreate()

    df = spark.sql("SELECT * FROM {0}.BANKING_TRANSACTIONS_{1}".format(dbname, username))

    print("\nSHOW TOP TEN ROWS")
    df.show(10)

    print("\nPRINT DF SCHEMA")
    df.printSchema()

    gdf = SparkDFDataset(df)

    gdf.spark_df.show(10)

    MANDATORY_COLUMNS = ["name","address","email","aba_routing","bank_country","account_no","int_account_no","swift11","credit_card_number","credit_card_provider","event_type","event_ts","longitude","latitude","transaction_currency","transaction_amount"]

    # RUN EXPECTATIONS
    run_existance_expactation(gdf, MANDATORY_COLUMNS)
    run_cols_not_null_expectation(gdf, MANDATORY_COLUMNS)
    run_longitude_min_expectation(gdf)
    run_latitude_max_expectation(gdf)
    run_transaction_amount_mean_expectation(gdf)
    run_transaction_amount_stdev_expectation(gdf)
    run_email_match_regex_expectation(gdf)
    run_email_not_match_regex_expectation(gdf)
    run_ccn_lenght_expectation(gdf)
    run_transaction_curr_distinct_values_expectation(gdf)
    run_transaction_curr_values_contain_set_expectation(gdf)
    run_transaction_curr_values_match_set_expectation(gdf)

if __name__ == "__main__":
    main()
