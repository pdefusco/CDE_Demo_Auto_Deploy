#!/bin/sh

docker_user=$1
cde_user=$2

#CREATE DOCKER RUNTIME RESOURCE
echo "Create CDE Credential dckr-crds-"$cde_user"-bnk"
cde credential create --name dckr-crds-$cde_user"-bnk" --type docker-basic --docker-server hub.docker.com --docker-username $docker_user -v
echo "Create CDE Docker Runtime ge-runtime-"$cde_user"-bnk"
cde resource create --name ge-runtime-$cde_user"-bnk" --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-data-quality --image-engine spark3 --type custom-runtime-image -v

# CREATE FILE RESOURCE
echo "Create Resource files-"$cde_user"-bnk"
cde resource create --name files-$cde_user"-bnk" -v
echo "Upload utils.py to files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Demo/banking/spark/utils.py -v
echo "Upload parameters.conf to files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Resources/CDE_Files/parameters.conf -v

# CREATE SETUP JOB
echo "Upload batch_load.py to files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Demo/banking/spark/batch_load.py -v
echo "Upload ge_data_quality.py to files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Demo/banking/spark/ge_data_quality.py -v
echo "Upload airflow.py to files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Demo/banking/airflow/airflow.py -v

echo "Create job batch_load-"$cde_user"-bnk"
cde job create --name batch_load-$cde_user"-bnk" --arg $data_lake --arg $cde_user --type spark --mount-1-prefix jobCode/ --mount-1-resource files-$cde_user"-bnk" --application-file jobCode/batch_load.py --runtime-image-resource-name ge-runtime-$cde_user"-bnk" --executor-cores 4 --executor-memory "4g" -v
echo "Create job ge_data_quality-"$cde_user"-bnk"
cde job create --name ge_data_quality-$cde_user"-bnk" --arg $data_lake --arg $cde_user --type spark --mount-1-resource files-$cde_user"-bnk" --application-file ge_data_quality.py --runtime-image-resource-name ge-runtime-$cde_user"-bnk" --executor-cores 4 --executor-memory "4g" -v
echo "Create job data_quality_orch-"$cde_user"-bnk"
cde job create --name data_quality_orch-$cde_user"-bnk" --arg $data_lake --arg $cde_user --type airflow --mount-1-resource files-$cde_user"-bnk" --dag-file airflow.py -v
