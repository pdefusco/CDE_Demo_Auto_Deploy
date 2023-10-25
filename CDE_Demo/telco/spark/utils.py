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

    def iot_points_gen(self, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):
        """
        Method to create dataframe with IoT readings and randomly located latitude and longitude
        -90 to 90 for latitude and -180 to 180 for longitude
        """
        manufacturers = ["IOT corp", "GEOSPATIAL Inc.", "United Geo Enterprises Ltd", "IOT_Century Corp", "Satellite Devices"]

        testDataSpec = (
            dg.DataGenerator(self.spark, name="iot", rows=row_count,partitions=partitions_num).withIdOutput()
            .withColumn("internal_device_id", "long", minValue=0x1000000000000,uniqueValues=unique_vals, omit=True, baseColumnType="hash",)
            .withColumn("device_id", "string", format="0x%013x", baseColumn="internal_device_id")
            .withColumn("manufacturer", "string", values=manufacturers, baseColumn="internal_device_id")
            .withColumn("model_ser", "integer", minValue=1, maxValue=11, baseColumn="device_id", baseColumnType="hash", omit=True, )
            .withColumn("event_type", "string", values=["activation", "deactivation", "plan change", "telecoms activity","internet activity", "device error"],random=True)
            .withColumn("event_ts", "timestamp", begin="2020-01-01 01:00:00",end="2020-12-31 23:59:00",interval="1 minute", random=True )
            .withColumn("longitude", "float", minValue=-180, maxValue=180, random=True)
            .withColumn("latitude", "float", minValue=-90, maxValue=90, random=True)
        )

        df = testDataSpec.build()

        return df
