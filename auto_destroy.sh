#!/bin/sh

cde_user=$1
cde_demo=$2

echo "Provided CDE User: "$cde_user
echo "Selected CDE Demo: "$cde_demo

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name docker-creds-$cde_user"-"$cde_demo
echo "Delete Jobs"
echo "Delete table_setup-"$cde_user"-"$cde_demo
cde job delete --name table_setup-$cde_user"-"$cde_demo
echo "Delete create_staging_table-"$cde_user"-"$cde_demo
cde job delete --name create_staging_table-$cde_user"-"$cde_demo
echo "Delete iceberg_mergeinto-"$cde_user"-"$cde_demo
cde job delete --name iceberg_mergeinto-$cde_user"-"$cde_demo
echo "Delete airflow_orchestration-"$cde_user"-"$cde_demo
cde job delete --name airflow_orchestration-$cde_user"-"$cde_demo
echo "Delete iceberg_metadata_querie-"$cde_user"-"$cde_demo
cde job delete --name iceberg_metadata_queries-$cde_user"-"$cde_demo
echo "Delete resosurce dex-spark-runtime-dbldatagen-"$cde_user"-"$cde_demo
cde resource delete --name dex-spark-runtime-dbldatagen-$cde_user"-"$cde_demo
echo "Upload cleanup script to resource cde_demo_files-"$cde_user"-"$cde_demo
cde resource upload --name cde_demo_files-$cde_user"-"$cde_demo --local-path CDE_Demo/$cde_demo/spark/cleanup.py
echo "Create cleanup job cleanup-"$cde_user"-"$cde_demo
cde job create --name cleanup-$cde_user"-"$cde_demo --type spark --mount-1-resource cde_demo_files-$cde_user"-"$cde_demo --application-file cleanup.py
echo "Run cleanup job cleanup-"$cde_user"-"$cde_demo
cde job run --name cleanup-$cde_user"-"$cde_demo
n=1
while [ $n -lt 50 ]
do
  echo "Running Cleanup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete cleanup job cleanup-"$cde_user"-"$cde_demo
cde job delete --name cleanup-$cde_user"-"$cde_demo
echo "Delete resource cde_demo_files-"$cde_user"-"$cde_demo
cde resource delete --name cde_demo_files-$cde_user"-"$cde_demo
echo "Delete resource cde_airflow_files-"$cde_user"-"$cde_demo
cde resource delete --name cde_airflow_files-$cde_user"-"$cde_demo
