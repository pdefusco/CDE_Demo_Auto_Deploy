#!/bin/sh

docker_user=$1
cdp_data_lake_storage=$2
cde_user=$3

echo "##########################################################"
echo "CREATE DOCKER RUNTIME RESOURCE"
echo "##########################################################"
echo "Create CDE Credential dckr-crds-"$cde_user"-telco"
cde credential create --name dckr-crds-$cde_user"-telco" --type docker-basic --docker-server hub.docker.com --docker-username $docker_user -v
echo "Create CDE Docker Runtime sedona-runtime-"$cde_user"-telco"
cde resource create --name sedona-runtime-$cde_user"-telco" --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-sedona-geospatial-003 --image-engine spark3 --type custom-runtime-image -v

echo "##########################################################"
echo "CREATE FILES RESOURCE"
echo "##########################################################"
echo "Create CDE Files Resource for Countries Data"
cde resource create --name countries-data-$cde_user"-telco" -v
echo "Upload Countries Data to CDE Files Resource"
cde resource upload-archive --name countries-data-$cde_user"-telco" --local-path CDE_Demo/telco/data/ne_50m_admin_0_countries_lakes.zip -v
echo "Create CDE Resource for Job Dependencies"
cde resource create --name app-code-$cde_user"-telco" -v
echo "Upload Job Dependencies to CDE Files Resource"
cde resource upload --name app-code-$cde_user"-telco" --local-path CDE_Demo/telco/spark/geospatial_joins.py --local-path CDE_Demo/telco/spark/geospatial_rdd.py --local-path CDE_Demo/telco/spark/utils.py --local-path CDE_Demo/telco/airflow/airflow.py -v

echo "##########################################################"
echo "CREATE SPARK AND AIRFLOW JOBS"
echo "##########################################################"
echo "Delete job geospatial-rdd-"$cde_user"-telco"
cde job delete --name geospatial-rdd-$cde_user"-telco"
echo "Delete job geospatial-joins-"$cde_user"-telco"
cde job delete --name geospatial-joins-$cde_user"-telco"
echo "Create job geospatial-rdd-"$cde_user"-telco"
cde job create --name geospatial-rdd-$cde_user"-telco" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-prefix appCode/ --mount-1-resource app-code-$cde_user"-telco" --mount-2-prefix countriesData/ --mount-2-resource countries-data-$cde_user"-telco" --runtime-image-resource-name sedona-runtime-$cde_user"-telco" --packages org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.5.0,org.datasyslab:geotools-wrapper:1.5.0-28.2 --application-file appCode/geospatial_rdd.py -v

#echo "Run GEOSPATIAL RDD SPARK JOB"
#cde job run --name geospatial_rdd-$cde_user"-telco" --executor-cores 2 --executor-memory "4g"

# CREATE CDE JOBS
echo "Create job geospatial-joins-"$cde_user"-telco"
cde job create --name geospatial-joins-$cde_user"-telco" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-prefix appCode/ --mount-1-resource app-code-$cde_user"-telco" --mount-2-prefix countriesData/ --mount-2-resource countries-data-$cde_user"-telco" --runtime-image-resource-name sedona-runtime-$cde_user"-telco" --packages org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.5.0,org.datasyslab:geotools-wrapper:1.5.0-28.2 --application-file appCode/geospatial_joins.py -v

#echo "RUN GEOSPATIAL JOINS SPARK JOB"
#cde job run --name geospatial_joins-$cde_user"-telco" --executor-cores 2 --executor-memory "4g"
echo "Delete job geo-orch-"$cde_user"-telco"
cde job delete --name geo-orch-$cde_user"-telco"

echo "Create job geo-orch-"$cde_user"-telco"
cde job create --name geo-orch-$cde_user"-telco" --type airflow --mount-1-prefix appCode/ --mount-1-resource app-code-$cde_user"-telco" --dag-file airflow.py -v
