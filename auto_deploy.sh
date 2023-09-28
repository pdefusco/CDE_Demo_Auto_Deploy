#!/bin/sh

docker_user=$1
cde_user=$2

echo "Provided Docker User: "$docker_user
echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE
echo "Create CDE Credential docker-creds-"$cde_user
cde credential create --name docker-creds-$cde_user --type docker-basic --docker-server hub.docker.com --docker-username $docker_user
echo "Create CDE Docker Runtime dex-spark-runtime-dbldatagen-"$cde_user
cde resource create --name dex-spark-runtime-dbldatagen-$cde_user --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-dbldatagen-002 --image-engine spark3 --type custom-runtime-image

# CREATE FILE RESOURCE
echo "Create Resource cde_demo_files-"$cde_user
cde resource create --name cde_demo_files-$cde_user
echo "Upload utils.py to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Resources/CDE_Files/utils.py
echo "Upload parameters.conf to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Resources/CDE_Files/parameters.conf

# CREATE SETUP JOB
echo "Upload table_setup.py to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Demo/spark/table_setup.py
echo "Create job table_setup-"$cde_user
cde job create --name table_setup-$cde_user --type spark --mount-1-resource cde_demo_files-$cde_user --application-file table_setup.py --runtime-image-resource-name dex-spark-runtime-dbldatagen-$cde_user
echo "Run job table_setup-"$cde_user
cde job run --name table_setup-$cde_user
n=1
while [ $n -lt 50 ]
do
  echo "Running Setup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done

# CREATE STAGING AND MERGE INTO JOBS WITH ORCH DAG AND RUN ORCH DAG
echo "Uploading staging_table.py to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Demo/spark/staging_table.py
echo "Uploading iceberg_mergeinto.py to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Demo/spark/iceberg_mergeinto.py
echo "Uploading airflow_DAG.py to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Demo/airflow/airflow_DAG.py
echo "Uploading iceberg_metadata_queries.py to cde_demo_files-"$cde_user
cde resource upload --name cde_demo_files-$cde_user --local-path CDE_Demo/spark/iceberg_metadata_queries.py
echo "Creating Spark Job staging_table-"$cde_user
cde job create --name create_staging_table-$cde_user --type spark --mount-1-resource cde_demo_files-$cde_user --application-file staging_table.py --executor-memory "4g" --executor-cores 4 --runtime-image-resource-name dex-spark-runtime-dbldatagen-$cde_user
echo "Creating Spark Job iceberg_mergeinto-"$cde_user
cde job create --name iceberg_mergeinto-$cde_user --type spark --mount-1-resource cde_demo_files-$cde_user --application-file iceberg_mergeinto.py --executor-memory "4g" --executor-cores 4
echo "Creating Spark Job iceberg_metadata_queries-"$cde_user
cde job create --name iceberg_metadata_queries-$cde_user --type spark --mount-1-resource cde_demo_files-$cde_user --application-file iceberg_metadata_queries.py

echo "Creating Airflow File Resource Dependency"
echo $cde_user >> username.conf
echo "Creating Airflow Resource cde_airflow_files-"$cde_user
cde resource create --name cde_airflow_files-$cde_user
echo "Uploading Airflow Dependency to Airflow Resourc cde_airflow_files-"$cde_user
cde resource upload --name cde_airflow_files-$cde_user --local-path username.conf
rm username.conf

echo "Creating Airflow Job airflow_orchestration-"$cde_user
cde job create --name airflow_orchestration-$cde_user --type airflow --mount-1-resource cde_demo_files-$cde_user --airflow-file-mount-1-resource cde_airflow_files  --dag-file airflow_DAG.py

# DELETE SETUP JOB
echo "Delete Spark Job table_setup-"$cde_user
cde job delete --name table_setup-$cde_user
