# CDE Demo Auto Deploy

## Objective

This git repository hosts the automation for a CDE Demo that includes Spark, Airflow and Iceberg. The Demo is deployed and removed in your Virtual Cluster within minutes.


## Table of Contents

* [Requirements](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#requirements)
* [Demo Content](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#demo-content)
* [Deployment Instructions](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#deployment-instructions)
  * [1. Important Information](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#1-important-information)
  * [2. autodeploy.sh](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#2-autodeploysh)
  * [3. autodestroy.sh](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#3-autodestroysh)
* [Summary](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#summary)
* [CDE Relevant Projects](https://github.com/pdefusco/CDE_Demo_Auto_Deploy#cde-relevant-projects)


## Requirements

To deploy the demo via this automation you need:

* A CDE Service with version 1.21 in CDP Public Cloud AWS.
* A CDE Virtual Cluster of type All Purpose with Spark 3.2 and Custom Docker Runtime Entitlement.
* A working installation of the CDE CLI.
* A docker account.
* Basic knowledge of CDE, Python, Airflow, Iceberg and PySpark is recommended but not required. No code changes are required.


## Demo Content

This automation contains three demos: "manufacturing", "banking", "telco".

#### Manufacturing

This demo includes a three step Spark pipeline which loads a new data batch, performs an Iceberg Merge Into and finally runs Iceberg metadata queries. An Airflow DAG orchestrates the pipeline. Car sales synthetic data is created and loaded incrementally.

#### Banking

This demo includes a two step Spark pipeline which loads synthetic credit card transaction data and performs data validation with Great Expectations. An Airflow DAG orchestrates the pipeline. This choice is recommended if you want to demo CDE Custom Runtimes.

#### Telco

This demo includes a two step Spark pipeline which loads IOT device geospatial data and performs a Spatial Join and Query with Apache Sedona. An Airflow Dag orchestrates the pipeline. This choice is recommended for geospatial use cases.  


## Setup

#### Git Repository

Clone the git repository.

#### CDE CLI Configuration

Add your CDE Virtual Cluster to the CDE CLI configuration file. To do so, paste your CDE Virtual Cluster's Jobs API URL at line 2. For example:

```
% vi ~/.cde/config.yaml

user: <cdp_workload_username>
vcluster-endpoint: https://a1b2345.cde-abcdefg.cde-xxx.xxxxx.cloudera.site/dex/api/v1
```

#### Add Username to Airflow Dag

The username variable is used to assign an Airflow DAG ID. This has to be unique to each Virtual Cluster.

Open the Airflow DAG and edit the username at line 50 by adding your CDP Workload Username. For example:

```
% vi ~/CDE_Demo/banking/airflow/airflow.py
```

<pre>
from airflow.operators.bash import BashOperator
from airflow.models.param import Param

<b>username = "cdpworkloaduser"</b> # Enter your workload username here
</pre>

## Deployment Instructions

#### 1. Important Information

* Each generated Iceberg Table, CDE Job and Resource will be prefixed with your CDP Workload Username.
* CDP Workload Users with dots, hyphens and other symbols are not currently supported. Please reach out to the Field Specialist team for a workaround.
* Multiple users can deploy the demo in the same CDE Virtual Cluster.
* Each user can deploy the same demo at most once in the same CDE Virtual Cluster. However, multiple demo options can coexist in the same cluster i.e. all three demos can run concurrently in the same cluster.  
* All Iceberg tables, CDE Jobs and Resources are deleted from the CDE Virtual Cluster upon execution of the "auto_destroy.sh" script.
* Currently Deployment is limited to AWS CDE Services.
* The entire pipeline is executed upon deployment. No jobs need to be manually triggered upon deployment.

#### 2. Run auto_deploy.sh

Run the autodeploy script with the demo parameter according to the demo you want to deploy. The demo parameter can be one of "banking", "manufacturing" and "telco".

```
./deploy.sh <dockerusername> <cdpworkloaduser> <cdp-data-lake-storage> <demo>
```

For example:

```
./deploy.sh pauldefusco pauldefusco s3a://goes-se-sandbox01/data/pdefusco/ manufacturing
```

#### 3. Run autodestroy.sh

When you are done run this script to tear down the pipeline:

```
./teardown.sh cdpworkloaduser <cdp-data-lake-storage> <demo>
```

For example:

```
./teardown.sh pauldefusco s3a://goes-se-sandbox01/data/pdefusco/ manufacturing
```


## Summary

You can deploy an end to end CDE Demo with the provided automation. The demo executes a small ETL pipeline including Iceberg, Spark and Airflow.

## CDE Relevant Projects

If you are exploring or using CDE today you may find the following tutorials relevant:

* [CDE 1.19 Workshop HOL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP): The HOL is typically a three to four-hour event organized by Cloudera for CDP customers and prospects, where a small technical team from Cloudera Solutions Engineering provides cloud infrastructure for all participants and guides them through the completion of the labs with the help of presentations and open discussions.

* [Spark 3 & Iceberg](https://github.com/pdefusco/Spark3_Iceberg_CML): A quick intro of Time Travel Capabilities with Spark 3.

* [Simple Intro to the CDE CLI](https://github.com/pdefusco/CDE_CLI_Simple): An introduction to the CDE CLI for the CDE beginner.

* [CDE CLI Demo](https://github.com/pdefusco/CDE_CLI_demo): A more advanced CDE CLI reference with additional details for the CDE user who wants to move beyond the basics.

* [CDE Resource 2 ADLS](https://github.com/pdefusco/CDEResource2ADLS): An example integration between ADLS and CDE Resource. This pattern is applicable to AWS S3 as well and can be used to pass execution scripts, dependencies, and virtually any file from CDE to 3rd party systems and viceversa.

* [Using CDE Airflow](https://github.com/pdefusco/Using_CDE_Airflow): A guide to Airflow in CDE including examples to integrate with 3rd party systems via Airflow Operators such as BashOperator, HttpOperator, PythonOperator, and more.

* [GitLab2CDE](https://github.com/pdefusco/Gitlab2CDE): a CI/CD pipeline to orchestrate Cross-Cluster Workflows for Hybrid/Multicloud Data Engineering.

* [CML2CDE](https://github.com/pdefusco/cml2cde_api_example): an API to create and orchestrate CDE Jobs from any Python based environment including CML. Relevant for ML Ops or any Python Users who want to leverage the power of Spark in CDE via Python requests.

* [Postman2CDE](https://github.com/pdefusco/Postman2CDE): An example of the Postman API to bootstrap CDE Services with the CDE API.

* [Oozie2CDEAirflow API](https://github.com/pdefusco/Oozie2CDE_Migration): An API to programmatically convert Oozie workflows and dependencies into CDE Airflow and CDE Jobs. This API is designed to easily migrate from Oozie to CDE Airflow and not just Open Source Airflow.

For more information on the Cloudera Data Platform and its form factors please visit [this site](https://docs.cloudera.com/).

For more information on migrating Spark jobs to CDE, please reference [this guide](https://docs.cloudera.com/cdp-private-cloud-upgrade/latest/cdppvc-data-migration-spark/topics/cdp-migration-spark-cdp-cde.html).
