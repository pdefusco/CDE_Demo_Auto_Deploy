# CDE Demo Auto Deploy

## Objective

This git repository hosts the automation for a CDE Demo that includes Spark, Airflow and Iceberg. The Demo is deployed and removed in your Virtual Cluster within minutes.

## Requirements

To deploy the demo via this automation you need:

* A CDE Virtual Cluster in CDP Public Cloud AWS (Azure coming soon).
* A working installation of Docker on your local machine.
* Basic knowledge of CDE, Python, Airflow, and PySpark is recommended but not required. No code changes are required.

## Demo Content

The Demo includes an Airflow DAG orchestrating two Spark Jobs in CDE. The first Spark Job loads fresh data into a staging table. The second Spark Job executes an Iceberg Merge Into into the target table.

The Airflow Job is designed to run every 10 minutes independently. At each run new random data is generated, then added to the staging table and finally loaded into the target table.

A setup job is launched upon triggering the deployment script. However, this is not part of the demo track and is automatically removed when the setup is complete.

When the demo is deployed you will have the following in your CDE Virtual Cluster:

* Two CDE Spark Jobs: "staging_table" and "iceberg_mergeinto"
* One CDE Airflow Job: "airflow_orchestration"
* One CDE Files Resource: "cde_demo_files"
* One CDE Docker Runtime Resource: "dex-spark-runtime-dbldatagen"
* The CDE CLI is pre-installed in the Docker container.

## Deployment Instructions

The automation is provided in a Docker container. First, pull the docker container and run it:

```
docker pull pauldefusco/cde_demo_auto_deploy
docker run -it pauldefusco/cde_demo_auto_deploy
```

Then add your CDE Virtual Cluster to the CDE CLI configuration file. To do so, paste your CDE Virtual Cluster's Jobs API URL at line 2.

```
vi ~/.cde/config.yaml
```

Next open the Airflow DAG and edit the username at line 50. Put your CDP Workload User here.

#### 1. autodeploy.sh

Run the autodeploy script with:

```
./autodeploy.sh dockerusername cdpworkloaduser
```

You can follow progress in the terminal. The pipeline should deploy within 3 minutes. When the setup process is complete navigate to the CDE UI and validate that the demo has been deployed.

#### 2. autodestroy.sh

When you are done run this script to tear down the pipeline:

```
./autodestroy.sh cdpworkloaduser
```

#### Important Information

* Each generated Iceberg Table, CDE Job and Resource will be prefixed with your CDP Workload Username. Multiple users can deploy the demo in the same CDE Virtual Cluster as long as they use different credentials.
* Each user can deploy the demo at most once in the same CDE Virtual Cluster.
* All CDE Jobs and Resources are deleted from the CDE Virtual Cluster upon execution of the "autodestroy.sh" script.
* Currently Deployment is limited to AWS CDE Services but Azure and Private Cloud will be added soon.
* The entire pipeline is executed upon deployment. No jobs need to be manually triggered upon deployment.
* *Known limitation*: when the pipeline is deployed for the first time the DAG is run twice. Therefore, in the very first run you will have duplicate jobs.

## Summary

You can deploy an end to end CDE Demo with the provided automation. The demo executes a small ETL pipeline including Iceberg, Spark and Airflow.

## Next Steps

### CDE Relevant Projects

If you are exploring or using CDE today you may find the following tutorials relevant:

* [CDE 1.19 Workshop HOL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP): The HOL is typically a three to four-hour event organized by Cloudera for CDP customers and prospects, where a small technical team from Cloudera Solutions Engineering provides cloud infrastructure for all participants and guides them through the completion of the labs with the help of presentations and open discussions. Recommended for CDE Services on versions up to 1.19.

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
