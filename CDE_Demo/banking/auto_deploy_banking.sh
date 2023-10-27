#!/bin/sh

docker_user=$1
cde_user=$2

echo "CDE BANKING - DATA QUALITY DEMO DEPLOYMENT INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided Docker User: "$docker_user
echo "Provided CDE User: "$cde_user

#CREATE DOCKER RUNTIME RESOURCE
echo "Create CDE Credential docker-creds-"$cde_user"-banking"
cde credential create --name docker-creds-$cde_user"-banking" --type docker-basic --docker-server hub.docker.com --docker-username $docker_user
echo "Create CDE Docker Runtime dex-spark-runtime-ge-data-quality-"$cde_user"-banking"
cde resource create --name dex-spark-runtime-ge-data-quality-$cde_user"-banking" --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-data-quality --image-engine spark3 --type custom-runtime-image

# CREATE FILE RESOURCE
echo "Create Resource cde_demo_files-"$cde_user"-banking"
cde resource create --name cde_demo_files-$cde_user"-banking"
echo "Upload utils.py to cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Demo/banking/spark/utils.py
echo "Upload parameters.conf to cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Resources/CDE_Files/parameters.conf

# CREATE SETUP JOB
echo "Upload batch_load.py to cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Demo/banking/spark/batch_load.py
echo "Upload ge_data_quality.py to cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Demo/banking/spark/ge_data_quality.py
echo "Upload airflow.py to cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Demo/banking/airflow/airflow.py

echo "Create job batch_load-"$cde_user"-banking"
cde job create --name batch_load-$cde_user"-banking" --type spark --mount-1-prefix jobCode/ --mount-1-resource cde_demo_files-$cde_user"-banking" --application-file jobCode/batch_load.py --runtime-image-resource-name dex-spark-runtime-ge-data-quality-$cde_user"-banking"
echo "Create job ge_data_quality-"$cde_user"-banking"
cde job create --name ge_data_quality-$cde_user"-banking" --type spark --mount-1-resource cde_demo_files-$cde_user"-banking" --application-file ge_data_quality.py --runtime-image-resource-name dex-spark-runtime-ge-data-quality-$cde_user"-banking"
echo "Create job data_quality_orchestration-"$cde_user"-banking"
cde job create --name data_quality_orchestration-$cde_user"-banking" --type airflow --mount-1-resource cde_demo_files-$cde_user"-banking" --dag-file airflow.py

echo " "
echo "."
echo ".."
echo "..."
echo ".... CDE BANKING DATA QUALITY DEMO DEPLOYMENT COMPLETED"
