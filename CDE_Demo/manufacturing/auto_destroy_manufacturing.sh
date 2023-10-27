#!/bin/sh

cde_user=$1

echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name docker-creds-$cde_user"-mfct"
echo "Delete Jobs"
echo "Delete table_setup-"$cde_user"-mfct"
cde job delete --name table_setup-$cde_user"-mfct"
echo "Delete create_staging_table-"$cde_user"-mfct"
cde job delete --name create_staging_table-$cde_user"-mfct"
echo "Delete iceberg_mergeinto-"$cde_user"-mfct"
cde job delete --name iceberg_mergeinto-$cde_user"-mfct"
echo "Delete airflow_orchestration-"$cde_user"-mfct"
cde job delete --name airflow_orchestration-$cde_user"-mfct"
echo "Delete iceberg_metadata_querie-"$cde_user"-mfct"
cde job delete --name iceberg_metadata_queries-$cde_user"-mfct"
echo "Delete resosurce dex-spark-runtime-dbldatagen-"$cde_user"-mfct"
cde resource delete --name dex-spark-runtime-dbldatagen-$cde_user"-mfct"
echo "Upload cleanup script to resource cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/cleanup.py
echo "Create cleanup job cleanup-"$cde_user"-mfct"
cde job create --name cleanup-$cde_user"-mfct" --type spark --mount-1-resource cde_demo_files-$cde_user"-mfct" --application-file cleanup.py
echo "Run cleanup job cleanup-"$cde_user"-mfct"
cde job run --name cleanup-$cde_user"-mfct"
n=1
while [ $n -lt 50 ]
do
  echo "Running Cleanup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete cleanup job cleanup-"$cde_user"-mfct"
cde job delete --name cleanup-$cde_user"-mfct"
echo "Delete resource cde_demo_files-"$cde_user"-mfct"
cde resource delete --name cde_demo_files-$cde_user"-mfct"
echo "Delete resource cde_airflow_files-"$cde_user"-mfct"
cde resource delete --name cde_airflow_files-$cde_user"-mfct"
