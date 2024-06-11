#!/bin/sh

cde_user=$1

echo "TELCO GEOSPATIAL DEMO TEARDOWN INITIATED...."
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
echo "Delete create_staging_table-"$cde_user"-telco"
cde job delete --name geo_orch-$cde_user"-telco"

echo "Upload teardown script to resource cde_demo_files-"$cde_user
cde resource upload --name job_code-$cde_user"-telco" --local-path CDE_Demo/telco/spark/teardown.py
echo "Create teardown job teardown-"$cde_user"-telco"
cde job create --name teardown-$cde_user"-telco" --type spark --mount-1-resource job_code-$cde_user"-telco" --application-file teardown.py
echo "Run teardown job teardown-"$cde_user"-telco"
cde job run --name teardown-$cde_user"-telco"
n=1
while [ $n -lt 20 ]
do
  echo "Running teardown Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete teardown job teardown-"$cde_user
cde job delete --name teardown-$cde_user"-telco"
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
