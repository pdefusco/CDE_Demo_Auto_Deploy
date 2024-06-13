#!/bin/sh

cde_user=$1
cdp_data_lake_storage=$2

echo "##########################################################"
echo "CREATE DOCKER RUNTIME RESOURCE"
echo "##########################################################"
echo "Delete Docker Credentials"
cde credential delete --name dckr-crds-$cde_user"-telco" -v

echo "##########################################################"
echo "DELETE SPARK JOBS"
echo "##########################################################"
echo "Delete geospatial_rdd-"$cde_user"-telco"
cde job delete --name geospatial_rdd-$cde_user"-telco" -v
echo "Delete create_staging_table-"$cde_user"-telco"
cde job delete --name geospatial_joins-$cde_user"-telco" -v
echo "Delete create_staging_table-"$cde_user"-telco"
cde job delete --name geo_orch-$cde_user"-telco" -v

echo "Upload teardown script to resource cde_demo_files-"$cde_user
cde resource upload --name app_code-$cde_user"-telco" --local-path CDE_Demo/telco/spark/teardown.py -v
echo "Create teardown job teardown-"$cde_user"-telco"
cde job create --name teardown-$cde_user"-telco" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource app_code-$cde_user"-telco" --application-file teardown.py -v
echo "Run teardown job teardown-"$cde_user"-telco"
cde job run --name teardown-$cde_user"-telco" -v
echo "##########################################################"
echo "RUN TEARDOWN JOB"
echo "##########################################################"
n=1
while [ $n -lt 20 ]
do
  echo "Running teardown Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done
echo "Delete teardown job teardown-"$cde_user
cde job delete --name teardown-$cde_user"-telco" -v
echo "Delete resource job_code-"$cde_user"-telco"
cde resource delete --name app_code-$cde_user"-telco" -v
echo "Delete resource countries_data-"$cde_user"-telco"
cde resource delete --name countries_data-$cde_user"-telco" -v
echo "Delete Custom Docker Runtime sedona-runtime-$cde_user-telco"
cde resource delete --name sedona-runtime-$cde_user"-telco" -v
