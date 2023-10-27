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

    def loan_gen(self, x, y, z, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):
        """
        Method to create Loan DF
        Data modeled after Loan Kaggle Dataset: https://www.kaggle.com/datasets/burak3ergun/loan-data-set/
        Attributes:
            Loan_ID,
            Gender,
            Married,
            Dependents,
            Education,
            Self_Employed,
            ApplicantIncome,
            CoapplicantIncome,
            LoanAmount,
            Loan_Amount_Term,
            Credit_History,
            Property_Area,
            Loan_Status
        """
        from pyspark.sql.types import StructType, StructField, IntegerType, StringType

        schema = StructType([
            StructField("Loan_ID_base", IntegerType(), True),
            StructField("Loan_ID", StringType(), True),
            StructField("Gender", StringType(), True),
            StructField("Married", StringType(), True),
            StructField("Dependents", IntegerType(), True),
            StructField("Education", StringType(), True),
            StructField("Self_Employed", StringType(), True),
            StructField("ApplicantIncome", IntegerType(), True),
            StructField("CoapplicantIncome", IntegerType(), True),
            StructField("LoanAmount", IntegerType(), True),
            StructField("Loan_Amount_Term", IntegerType(), True),
            StructField("Credit_History", IntegerType(), True),
            StructField("Property_Area", StringType(), True),
            StructField("Loan_Status", StringType(), True),
        ])

        testDataSpec = (
            dg.DataGenerator(spark, name="loan_data", rows=row_count, partitions=partitions_num).withIdOutput()
            .withColumn("Loan_ID_base", minValue=1, maxValue=row_count, step=1)
            .withColumn("Loan_ID", prefix='LP00', baseColumn="Loan_ID_base")
            .withColumn("Gender", values=["Male", "Female"],random=True)
            .withColumn("Married", values=["Yes", "No"], random=True,distribution="normal")
            .withColumn("Dependents", minValue=0, maxValue=3,random=True)
            .withColumn("Education", values=["Graduate", "Not Graduate"], random=True)
            .withColumn("Self_Employed", values=["Yes", "No"], random=True)
            .withColumn("ApplicantIncome", minValue=1000, maxValue=100000, random=True)
            .withColumn("CoapplicantIncome", minValue=1000, maxValue=100000,random=True, distribution="normal")
            .withColumn("LoanAmount", minValue=10000, maxValue=1000000, random=True, distribution="normal")
            .withColumn("Loan_Amount_Term", minValue=180, maxValue=520, step=180)
            .withColumn("Credit_History", minValue=0, maxValue=1, random=True, distribution="normal")
            .withColumn("Property_Area", values=["Urban", "Semiurban", "Rural"], random=True)
            .withColumn("Loan_Status", values=["Y", "N"], random=True, distribution="normal")
        )

        df = testDataSpec.build()

        df = df.drop("Loan_ID_base")

        return df

    def telco_gen(self, x, y, z, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):
        """
        Method to create Telco DF
        Data modeled after Telco Kaggle Dataset: https://www.kaggle.com/datasets/spscientist/telecom-data
        Attributes:
            state,
            account_length,
            area_code,
            international_plan,
            voice_mail_plan,
            number_vmail_messages,
            total_day_minutes,
            total_day_calls,
            total_day_charge,
            total_eve_minutes,
            total_eve_calls,
            total_eve_charge,
            total_night_minutes,
            total_night_calls,
            total_night_charge,
            total_intl_minutes,
            total_intl_calls,
            total_intl_charge,
            customer_service_calls,
            churn
        """
        from pyspark.sql.types import StructType, StructField, IntegerType, StringType

        schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("state", StringType(), True),
            StructField("account_length", IntegerType(), True),
            StructField("area_code", StringType(), True),
            StructField("international_plan", StringType(), True),
            StructField("voice_mail_plan", StringType(), True),
            StructField("number_vmail_messages", IntegerType(), True),
            StructField("total_day_minutes", IntegerType(), True),
            StructField("total_day_calls", IntegerType(), True),
            StructField("total_day_charge", IntegerType(), True),
            StructField("total_eve_minutes", IntegerType(), True),
            StructField("total_eve_calls", IntegerType(), True),
            StructField("total_eve_charge", IntegerType(), True),
            StructField("total_night_minutes", IntegerType(), True),
            StructField("total_night_calls", IntegerType(), True),
            StructField("total_night_charge", IntegerType(), True),
            StructField("total_intl_minutes", IntegerType(), True),
            StructField("total_intl_calls", IntegerType(), True),
            StructField("total_intl_charge", IntegerType(), True),
            StructField("customer_service_calls", IntegerType(), True),
            StructField("churn", StringType(), True),
        ])

        states = ["MA"]
        area_codes = ["339", "351", "508", "617", "774", "781", "857", "978"]

        testDataSpec = (
            dg.DataGenerator(spark, name="telco_data", rows=row_count, partitions=partitions_num).withIdOutput()
            .withColumn("customer_id", minValue=1, maxValue=row_count, step=1)
            .withColumn("state", values=states, random=True)
            .withColumn("account_length", minValue=0, maxValue=3,random=True)
            .withColumn("area_code", values=area_codes,random=True)
            .withColumn("international_plan", values=["yes", "no"], random=True,distribution="normal")
            .withColumn("voice_mail_plan", values=["yes", "no"], random=True,distribution="normal")
            .withColumn("number_vmail_messages", minValue=0, maxValue=3,random=True)
            .withColumn("total_day_minutes", minValue=0, maxValue=1440,random=True)
            .withColumn("total_day_calls", minValue=0, maxValue=100,random=True)
            .withColumn("total_day_charge", minValue=0, maxValue=1000,random=True)
            .withColumn("total_eve_minutes", minValue=0, maxValue=360,random=True)
            .withColumn("total_eve_calls", minValue=0, maxValue=50,random=True)
            .withColumn("total_eve_charge", minValue=0, maxValue=500,random=True)
            .withColumn("total_night_minutes", minValue=0, maxValue=360,random=True)
            .withColumn("total_night_calls", minValue=0, maxValue=200,random=True)
            .withColumn("total_night_charge", minValue=0, maxValue=36,random=True)
            .withColumn("total_intl_minutes", minValue=0, maxValue=36,random=True)
            .withColumn("total_intl_calls", minValue=0, maxValue=360,random=True)
            .withColumn("total_intl_charge", minValue=0, maxValue=100,random=True)
            .withColumn("customer_service_calls", minValue=0, maxValue=200,random=True)
            .withColumn("churn", values=["Y", "N"], random=True, distribution="normal")
        )

        df = testDataSpec.build()

        return df

    def iot_points_gen(self, partitions_num=10, row_count = 100000, unique_vals=100000, display_option=True):
        """
        Method to create dataframe with IoT readings and randomly located latitude and longitude
        -90 to 90 for latitude and -180 to 180 for longitude
        """
        testDataSpec = (
            dg.DataGenerator(spark, name="iot", rows=data_rows,partitions=partitions_requested).withIdOutput()
            .withColumn("internal_device_id", "long", minValue=0x1000000000000,uniqueValues=device_population, omit=True, baseColumnType="hash",)
            .withColumn("device_id", "string", format="0x%013x", baseColumn="internal_device_id")
            .withColumn("manufacturer", "string", values=manufacturers, baseColumn="internal_device_id")
            .withColumn("model_ser", "integer", minValue=1, maxValue=11, baseColumn="device_id", baseColumnType="hash", omit=True, )
            .withColumn("model_line", "string", expr="concat(line, '#', model_ser)", baseColumn=["line", "model_ser"] )
            .withColumn("event_type", "string", values=["activation", "deactivation", "plan change", "telecoms activity","internet activity", "device error"],random=True)
            .withColumn("event_ts", "timestamp", begin="2020-01-01 01:00:00",end="2020-12-31 23:59:00",interval="1 minute", random=True )
            .withColumn("longitude", "float", minValue=-180, maxValue=180, random=True)
            .withColumn("latitude", "float", minValue=-90, maxValue=90, random=True)
        )

        df = testDataSpec.build()

        return df
