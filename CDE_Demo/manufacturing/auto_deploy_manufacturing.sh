#!/bin/sh

docker_user=$1
cde_user=$2

echo "CDE MANUFACTURING - ICEBERG DEMO DEPLOYMENT INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided Docker User: "$docker_user
echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE
echo "Create CDE Credential docker-creds-"$cde_user"-mfct"
cde credential create --name docker-creds-$cde_user"-mfct" --type docker-basic --docker-server hub.docker.com --docker-username $docker_user
echo "Create CDE Docker Runtime dex-spark-runtime-dbldatagen-"$cde_user"-mfct"
cde resource create --name dex-spark-runtime-dbldatagen-$cde_user"-mfct" --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-dbldatagen-002 --image-engine spark3 --type custom-runtime-image

# CREATE FILE RESOURCE
echo "Create Resource cde_demo_files-"$cde_user"-mfct"
cde resource create --name cde_demo_files-$cde_user"-mfct"
echo "Upload utils.py to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Resources/CDE_Files/utils.py
echo "Upload parameters.conf to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Resources/CDE_Files/parameters.conf

# CREATE SETUP JOB
echo "Upload table_setup.py to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/table_setup.py
echo "Create job table_setup-"$cde_user"-mfct"
cde job create --name table_setup-$cde_user"-mfct" --type spark --mount-1-resource cde_demo_files-$cde_user"-mfct" --application-file table_setup.py --runtime-image-resource-name dex-spark-runtime-dbldatagen-$cde_user"-mfct"
echo "Run job table_setup-"$cde_user"-mfct"
cde job run --name table_setup-$cde_user"-mfct"
n=1
while [ $n -lt 50 ]
do
  echo "Running Setup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done

# CREATE STAGING AND MERGE INTO JOBS WITH ORCH DAG AND RUN ORCH DAG
echo "Deleting resource cde_demo_files-"$cde_user"-mfct"
cde resource delete --name cde_demo_files-$cde_user"-mfct"
echo "Deleting job staging_table-"$cde_user"-mfct"
cde job delete --name create_staging_table-$cde_user"-mfct"
echo "Deleting job iceberg_mergeinto-"$cde_user"-mfct"
cde job delete --name iceberg_mergeinto-$cde_user"-mfct"
echo "Deleting job iceberg_metadata_queries-"$cde_user"-mfct"
cde job delete --name iceberg_metadata_queries-$cde_user"-mfct"
echo "Uploading staging_table.py to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/staging_table.py
echo "Uploading iceberg_mergeinto.py to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/iceberg_mergeinto.py
echo "Uploading airflow_DAG.py to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/airflow/airflow_DAG.py
echo "Uploading iceberg_metadata_queries.py to cde_demo_files-"$cde_user"-mfct"
cde resource upload --name cde_demo_files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/iceberg_metadata_queries.py
echo "Creating Spark Job staging_table-"$cde_user"-mfct"
cde job create --name create_staging_table-$cde_user"-mfct" --type spark --mount-1-resource cde_demo_files-$cde_user"-mfct" --application-file staging_table.py --runtime-image-resource-name dex-spark-runtime-dbldatagen-$cde_user"-mfct" --executor-cores 4 --executor-memory "4g"
echo "Creating Spark Job iceberg_mergeinto-"$cde_user"-mfct"
cde job create --name iceberg_mergeinto-$cde_user"-mfct" --type spark --mount-1-resource cde_demo_files-$cde_user"-mfct" --application-file iceberg_mergeinto.py --executor-cores 4 --executor-memory "4g"
echo "Creating Spark Job iceberg_metadata_queries-"$cde_user"-mfct"
cde job create --name iceberg_metadata_queries-$cde_user"-mfct" --type spark --mount-1-resource cde_demo_files-$cde_user"-mfct" --application-file iceberg_metadata_queries.py --executor-cores 4 --executor-memory "4g"

echo "Creating Airflow File Resource Dependency"
echo $cde_user >> username.conf
echo "Creating Airflow Resource cde_airflow_files-"$cde_user"-mfct"
cde resource create --name cde_airflow_files-$cde_user"-mfct"
echo "Uploading Airflow Dependency to Airflow Resource cde_airflow_files-"$cde_user"-mfct"
cde resource upload --name cde_airflow_files-$cde_user"-mfct" --local-path username.conf
rm username.conf

echo "Deleting Airflow Job airflow_orchestration-"$cde_user"-mfct"
cde job delete --name airflow_orchestration-$cde_user"-mfct"
echo "Creating Airflow Job airflow_orchestration-"$cde_user"-mfct"
cde job create --name airflow_orchestration-$cde_user"-mfct" --type airflow --mount-1-resource cde_demo_files-$cde_user"-mfct" --airflow-file-mount-1-resource cde_airflow_files-$cde_user"-mfct"  --dag-file airflow_DAG.py

# DELETE SETUP JOB
echo "Delete Spark Job table_setup-"$cde_user"-mfct"
cde job delete --name table_setup-$cde_user"-mfct"

echo " "
echo "."
echo ".."
echo "..."
echo ".... CDE MANUFACTURING - ICEBERG DEMO DEPLOYMENT COMPLETED"
