#!/bin/sh

docker_user=$1
cde_user=$2

echo "CDE TELCO - GEOSPATIAL DEMO DEPLOYMENT INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided Docker User: "$docker_user
echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE
echo "Create CDE Credential docker-creds-"$cde_user"-telco"
cde credential create --name docker-creds-$cde_user"-telco" --type docker-basic --docker-server hub.docker.com --docker-username $docker_user
echo "Create CDE Docker Runtime dex-spark-runtime-dbldatagen-"$cde_user"-telco"
cde resource create --name dex-spark-runtime-sedona-geospatial-$cde_user"-telco" --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-sedona-geospatial-003 --image-engine spark3 --type custom-runtime-image

# CREATE FILE RESOURCE
echo "Create CDE Files Resource for Countries Data"
cde resource create --name countries_data-$cde_user"-telco"
echo "Upload Countries Data to CDE Files Resource"
cde resource upload-archive --name countries_data-$cde_user"-telco" --local-path CDE_Demo/telco/data/ne_50m_admin_0_countries_lakes.zip
echo "Create CDE Resource for Job Dependencies"
cde resource create --name job_code-$cde_user"-telco"
echo "Upload Job Dependencies to CDE Files Resource"
cde resource upload --name job_code-$cde_user"-telco" --local-path CDE_Demo/telco/spark/geospatial_joins.py --local-path CDE_Demo/telco/spark/geospatial_rdd.py --local-path CDE_Demo/telco/spark/parameters.conf --local-path CDE_Demo/telco/spark/utils.py

#current_date_time=$(date +"%Y-%m-%d %T" )

# CREATE CDE JOBS
echo "Create GEOSPATIAL RDD SPARK JOB"
cde job create --name geospatial_rdd-$cde_user"-telco" --type spark --mount-1-prefix jobCode/ --mount-1-resource job_code-$cde_user"-telco" --mount-2-prefix countriesData/ --mount-2-resource countries_data-$cde_user"-telco" --runtime-image-resource-name dex-spark-runtime-sedona-geospatial-$cde_user"-telco" --packages org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.5.0,org.datasyslab:geotools-wrapper:1.5.0-28.2 --application-file jobCode/geospatial_rdd.py

echo "Run GEOSPATIAL RDD SPARK JOB"
cde job run --name geospatial_rdd-$cde_user"-telco" --executor-cores 2 --executor-memory "4g"

n=1
while [ $n -lt 10 ]
do
  echo "Running GEOSPATIAL RDD Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done

# RUN CDE JOBS
echo "Run GEOSPATIAL RDD SPARK JOB"
cde job run --name geospatial_rdd-$cde_user"-telco" --executor-cores 2 --executor-memory "4g"

echo "RUN GEOSPATIAL JOINS SPARK JOB"
cde job run --name geospatial_joins-$cde_user"-telco" --executor-cores 2 --executor-memory "4g"
echo " "
echo "."
echo ".."
echo "..."
echo ".... CDE TELCO DEMO DEPLOYMENT COMPLETED"
