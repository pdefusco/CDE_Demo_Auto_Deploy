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

import os
import numpy as np
import pandas as pd
from datetime import datetime
from pyspark.sql.types import LongType, IntegerType, StringType
import dbldatagen as dg
import dbldatagen.distributions as dist

class DataGen:

    '''Class to Generate Data'''

    def __init__(self, spark, username):
        self.spark = spark
        self.username = username
        ## TODO: look into adding custom db functionality

    def car_installs_gen(self, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):

        model_codes = ["A","B","D","E"]

        testDataSpec = (
            dg.DataGenerator(self.spark, name="car_installs", rows=row_count, partitions=partitions_num).withIdOutput()
            .withColumn("model", "string", values=model_codes, random=True, distribution="normal")#, distribution="normal"
            .withColumn("VIN", "string", template=r'\\N8UCGTTVDK5J', random=True)
            .withColumn("serial_no", "string", template=r'\\N42CLDR0156661577860220', random=True)
        )

        df = testDataSpec.build()

        return df

    def car_sales_gen(self, x, y, z, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):

        model_codes = ["Model A","Model B","Model D","Model E"]

        testDataSpec = (
            dg.DataGenerator(self.spark, name="car_sales", rows=row_count,partitions=partitions_num).withIdOutput()
            .withColumn("customer_id", "integer", minValue=10000, maxValue=1000000, random=True, distribution="normal")
            .withColumn("model", "string", values=model_codes, random=True, distribution=dist.Gamma(x, y))
            .withColumn("saleprice", "decimal(10,2)", minValue=5000, maxValue=100000, random=True, distribution=dist.Exponential(z))
            .withColumn("VIN", "string", template=r'\\N8UCGTTVDK5J', random=True)
            .withColumn("month", "integer", minValue=1, maxValue=12, random=True, distribution=dist.Exponential(z))
            .withColumn("year", "integer", minValue=1999, maxValue=2023, random=True, distribution="normal")
            .withColumn("day", "integer", minValue=1, maxValue=28, random=True, distribution=dist.Gamma(x, y))
        )

        df = testDataSpec.build()

        return df

    def customer_gen(self, x, y, z, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):

        model_codes = ["Model A","Model B","Model D","Model E"]
        gender_codes = ["M","F"]

        testDataSpec = (
            dg.DataGenerator(self.spark, name="customer_data", rows=row_count,partitions=partitions_num).withIdOutput()
            .withColumn("customer_id", "integer", minValue=10000, maxValue=1000000, random=True)
            .withColumn('username', 'string', template=r'\\w', random=True)
            .withColumn('name', 'string', template=r'\\w', random=True)
            .withColumn('gender', 'string', values=gender_codes, random=True)
            .withColumn("email", 'string', template=r"\\w.\\w@\\w.com", random=True)
            .withColumn("birthdate", "timestamp", begin="1950-01-01 01:00:00",
                    end="2003-12-31 23:59:00", interval="1 minute", random=True, distribution="normal")
            .withColumn("salary", "decimal(10,2)", minValue=50000, maxValue=1000000, random=True, distribution="normal")
            .withColumn("zip", "integer", minValue=10000, maxValue=99999, random=True, distribution="normal")
        )

        df = testDataSpec.build()

        return df

    def factory_gen(self, x, y, z, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):

        testDataSpec = (
            dg.DataGenerator(self.spark, name="factory_data", rows=row_count,partitions=partitions_num).withIdOutput()
            .withColumn("factory_no", "int", minValue=10000, maxValue=1000000, random=True, distribution=dist.Gamma(x, y))
            .withColumn("machine_no", "int", minValue=120, maxValue=99999, random=True, distribution=dist.Gamma(x, y))
            .withColumn("serial_no", "string", template=r'\\N42CLDR0156661577860220', random=True)
            .withColumn("part_no", "string", template=r'\\a42CLDR', random=True)
            .withColumn("timestamp", "timestamp", begin="2000-01-01 01:00:00",
                    end="2003-12-31 23:59:00", interval="1 minute", random=True, distribution="normal")
            .withColumn("status", "string", values=["beta_engine"])

        )

        df = testDataSpec.build()

        return df

    def geo_gen(self, x, y, z, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):

        state_names = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida"]

        testDataSpec = (
            dg.DataGenerator(self.spark, name="geo_data", rows=row_count, partitions=partitions_num).withIdOutput()
            .withColumn("country_code", "string", values=["US"])
            .withColumn("state", "string", values=state_names, random=True, distribution=dist.Gamma(x, y))
            .withColumn("postalcode", "integer", minValue=10000, maxValue=99999, random=True, distribution="normal")
            .withColumn("latitude", "decimal(10,2)", minValue=-90, maxValue=90, random=True, distribution=dist.Exponential(z))
            .withColumn("longitude", "decimal(10,2)", minValue=-180, maxValue=180, random=True)
        )

        df = testDataSpec.build()

        return df
