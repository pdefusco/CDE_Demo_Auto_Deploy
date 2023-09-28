#!/bin/sh

cde_user=$1

echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name docker-creds-$cde_user
echo "Delete Jobs"
echo "Delete table_setup-"$cde_user
cde job delete --name table_setup-$cde_user
echo "Delete create_staging_table-"$cde_user
cde job delete --name create_staging_table-$cde_user
echo "Delete iceberg_mergeinto-"$cde_user
cde job delete --name iceberg_mergeinto-$cde_user
echo "Delete airflow_orchestration-"$cde_user
cde job delete --name airflow_orchestration-$cde_user
echo "Delete iceberg_metadata_querie-"$cde_user
cde job delete --name iceberg_metadata_queries-$cde_user
echo "Delete resosurce dex-spark-runtime-dbldatagen-"$cde_user
cde resource delete --name dex-spark-runtime-dbldatagen-$cde_user
echo "Upload cleanup script to resource cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Demo/spark/cleanup.py
echo "Create cleanup job cleanup-"$cde_user
cde job create --name cleanup-$cde_user --type spark --mount-1-resource cde_demo_files-$cde_user --application-file cleanup.py
echo "Run cleanup job cleanup-"$cde_user
cde job run --name cleanup-$cde_user
n=1
while [ $n -lt 50 ]
do
  echo "Running Cleanup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete cleanup job cleanup-"$cde_user
cde job run --name cleanup-$cde_user
echo "Delete resource cde_demo_files"
cde resource delete --name cde_demo_files-$cde_user
echo "Delete resource cde_airflow_files"
cde resource delete --name cde_airflow_files-$cde_user
