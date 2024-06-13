#!/bin/sh

cde_user=$1

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name dckr-crds-$cde_user"-mfct" -v
echo "Delete Jobs"
echo "Delete create_staging_table-"$cde_user"-mfct"
cde job delete --name create_staging_table-$cde_user"-mfct" -v
echo "Delete iceberg_mergeinto-"$cde_user"-mfct"
cde job delete --name iceberg_mergeinto-$cde_user"-mfct" -v
echo "Delete airflow_orchestration-"$cde_user"-mfct"
cde job delete --name airflow_orchestration-$cde_user"-mfct" -v
echo "Delete iceberg_metadata_querie-"$cde_user"-mfct"
cde job delete --name iceberg_metadata_queries-$cde_user"-mfct" -v
echo "Delete resosurce dex-spark-runtime-dbldatagen-"$cde_user"-mfct"
cde resource delete --name dex-spark-runtime-dbldatagen-$cde_user"-mfct" -v
echo "Upload teardown script to resource files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/teardown.py -v
echo "Create teardown job teardown-"$cde_user"-mfct"
cde job create --name teardown-$cde_user"-mfct" --arg $data_lake --arg $cde_user --type spark --mount-1-resource files-$cde_user"-mfct" --application-file teardown.py -v
echo "Run teardown job teardown-"$cde_user"-mfct"
cde job run --name teardown-$cde_user"-mfct" -v
n=1
while [ $n -lt 50 ]
do
  echo "Running teardown Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete teardown job teardown-"$cde_user"-mfct"
cde job delete --name teardown-$cde_user"-mfct" -v
echo "Delete resource files-"$cde_user"-mfct"
cde resource delete --name files-$cde_user"-mfct" -v
echo "Delete resource cde_airflow_files-"$cde_user"-mfct"
cde resource delete --name cde_airflow_files-$cde_user"-mfct" -v
