#!/bin/sh

cde_user=$1

echo "MANUFACTURING ICEBERG DEMO TEARDOWN INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name docker-creds-$cde_user"-mfct"
echo "Delete Jobs"
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
echo "Upload teardown script to resource cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/teardown.py
echo "Create teardown job teardown-"$cde_user"-mfct"
cde job create --name teardown-$cde_user"-mfct" --type spark --mount-1-resource cde_demo_files-$cde_user"-mfct" --application-file teardown.py
echo "Run teardown job teardown-"$cde_user"-mfct"
cde job run --name teardown-$cde_user"-mfct"
n=1
while [ $n -lt 50 ]
do
  echo "Running teardown Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete teardown job teardown-"$cde_user"-mfct"
cde job delete --name teardown-$cde_user"-mfct"
echo "Delete resource cde_demo_files-"$cde_user"-mfct"
cde resource delete --name cde_demo_files-$cde_user"-mfct"
echo "Delete resource cde_airflow_files-"$cde_user"-mfct"
cde resource delete --name cde_airflow_files-$cde_user"-mfct"

echo "."
echo ".."
echo "..."
echo "....TEARDOWN COMPLETED"
