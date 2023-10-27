#!/bin/sh

cde_user=$1

echo "TEARDOWN INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE

cde credential delete --name docker-creds-$cde_user"-telco"
echo "Delete Jobs"

echo "Delete geospatial_rdd-"$cde_user"-telco"
cde job delete --name geospatial_rdd-$cde_user"-telco"
echo "Delete create_staging_table-"$cde_user"-telco"
cde job delete --name geospatial_joins-$cde_user"-telco"

echo "Upload cleanup script to resource cde_demo_files-"$cde_user
cde resource upload --name job_code-$cde_user"-telco" --local-path CDE_Demo/telco/spark/cleanup.py
echo "Create cleanup job cleanup-"$cde_user"-telco"
cde job create --name cleanup-$cde_user"-telco" --type spark --mount-1-resource job_code-$cde_user"-telco" --application-file cleanup.py
echo "Run cleanup job cleanup-"$cde_user"-telco"
cde job run --name cleanup-$cde_user"-telco"
n=1
while [ $n -lt 20 ]
do
  echo "Running Cleanup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete cleanup job cleanup-"$cde_user
cde job delete --name cleanup-$cde_user"-telco"
echo "Delete resource job_code-"$cde_user"-telco"
cde resource delete --name job_code-$cde_user"-telco"
echo "Delete resource countries_data-"$cde_user"-telco"
cde resource delete --name countries_data-$cde_user"-telco"
echo "Delete Custom Docker Runtime dex-spark-runtime-sedona-geospatial-$cde_user-telco"
cde resource delete --name dex-spark-runtime-sedona-geospatial-$cde_user"-telco"

echo "."
echo ".."
echo "..."
echo "....TEARDOWN COMPLETED"
