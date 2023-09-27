#!/bin/sh

cde_user=$1

echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name docker-creds-$cde_user
echo "Delete Jobs"
echo "Delete table_setup"
cde job delete --name table_setup-$cde_user
echo "Delete create_staging_table"
cde job delete --name create_staging_table-$cde_user
echo "Delete iceberg_mergeinto"
cde job delete --name iceberg_mergeinto-$cde_user
echo "Delete airflow_orchestration"
cde job delete --name airflow_orchestration-$cde_user
echo "Delete iceberg_metadata_queries"
cde job delete --name iceberg_metadata_queries-$cde_user
echo "Delete resosurce dex-spark-runtime-dbldatagen-"$cde_user
cde resource delete --name dex-spark-runtime-dbldatagen-$cde_user
echo "Delete resource cde_demo_files"
cde resource delete --name cde_demo_files-$cde_user
echo "Delete resource cde_demo_files"
cde resource delete --name cde_airflow_files
