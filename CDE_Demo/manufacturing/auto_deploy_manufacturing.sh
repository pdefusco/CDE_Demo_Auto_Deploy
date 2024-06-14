#!/bin/sh

docker_user=$1
cdp_data_lake_storage=$2
cde_user=$3

echo "##########################################################"
echo "CREATE DOCKER RUNTIME"
echo "##########################################################"
echo "Create CDE Credential dckr-crds-"$cde_user"-mfct"
cde credential create --name dckr-crds-$cde_user"-mfct" --type docker-basic --docker-server hub.docker.com --docker-username $docker_user -v
echo "Create CDE Docker Runtime datagen-runtime-"$cde_user"-mfct"
cde resource create --name datagen-runtime-$cde_user"-mfct" --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-dbldatagen-002 --image-engine spark3 --type custom-runtime-image -v

echo "##########################################################"
echo "CREATE FILES RESOURCES"
echo "##########################################################"
echo "Create Resource files-"$cde_user"-mfct"
cde resource create --name files-$cde_user"-mfct" -v
echo "Upload utils.py to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Resources/CDE_Files/utils.py -v
echo "Upload parameters.conf to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Resources/CDE_Files/parameters.conf -v

echo "##########################################################"
echo "CREATE SETUP JOB"
echo "##########################################################"
echo "Upload table_setup.py to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/table_setup.py -v
echo "Create job table_setup-"$cde_user"-mfct"
cde job create --name table-setup-$cde_user"-mfct" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource files-$cde_user"-mfct" --application-file table_setup.py --runtime-image-resource-name datagen-runtime-$cde_user"-mfct" -v
echo "Run job table_setup-"$cde_user"-mfct"
cde job run --name table-setup-$cde_user"-mfct" -v

function loading_icon() {
    local load_interval="${1}"
    local loading_message="${2}"
    local elapsed=0
    local loading_animation=( '—' "\\" '|' '/' )

    echo -n "${loading_message} "

    # This part is to make the cursor not blink
    # on top of the animation while it lasts
    tput civis
    trap "tput cnorm" EXIT
    while [ "${load_interval}" -ne "${elapsed}" ]; do
        for frame in "${loading_animation[@]}" ; do
            printf "%s\b" "${frame}"
            sleep 0.10
        done
        elapsed=$(( elapsed + 1 ))
    done
    printf " \b\n"
}

loading_icon 100 "Table Setup in Progress"

echo "##########################################################"
echo "CREATE SPARK AND AIRFLOW JOBS"
echo "##########################################################"
#
echo "Deleting airflow-orchestration-"$cde_user"-mfct"
cde job delete --name airflow-orchestration-$cde_user"-mfct"
echo "Deleting resource files-"$cde_user"-mfct"
cde resource delete --name files-$cde_user"-mfct" -v
echo "Deleting job staging-table-"$cde_user"-mfct"
cde job delete --name create-staging-table-$cde_user"-mfct" -v
echo "Deleting job iceberg-mergeinto-"$cde_user"-mfct"
cde job delete --name iceberg-mergeinto-$cde_user"-mfct" -v
echo "Deleting job iceberg-metadata_queries-"$cde_user"-mfct"
cde job delete --name iceberg-metadata-queries-$cde_user"-mfct" -v
echo "Uploading staging_table.py to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/staging_table.py -v
echo "Uploading iceberg_mergeinto.py to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/iceberg_mergeinto.py -v
echo "Uploading airflow_DAG.py to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/airflow/airflow_DAG.py -v
echo "Uploading iceberg_metadata_queries.py to files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/iceberg_metadata_queries.py -v
echo "Creating Spark Job staging-table-"$cde_user"-mfct"
cde job create --name create-staging-table-$cde_user"-mfct" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource files-$cde_user"-mfct" --application-file staging_table.py --runtime-image-resource-name datagen-runtime-$cde_user"-mfct" --executor-cores 4 --executor-memory "4g" -v
echo "Creating Spark Job iceberg-mergeinto-"$cde_user"-mfct"
cde job create --name iceberg-mergeinto-$cde_user"-mfct" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource files-$cde_user"-mfct" --application-file iceberg_mergeinto.py --executor-cores 4 --executor-memory "4g" -v
echo "Creating Spark Job iceberg-metadata-queries-"$cde_user"-mfct"
cde job create --name iceberg-metadata-queries-$cde_user"-mfct" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource files-$cde_user"-mfct" --application-file iceberg_metadata_queries.py --executor-cores 4 --executor-memory "4g" -v

echo "Creating Airflow File Resource Dependency"
echo $cde_user >> username.conf
echo "Creating Airflow Resource cde-airflow-files-"$cde_user"-mfct"
cde resource create --name cde-airflow-files-$cde_user"-mfct"
echo "Uploading Airflow Dependency to Airflow Resource cde_airflow-files-"$cde_user"-mfct"
cde resource upload --name cde-airflow-files-$cde_user"-mfct" --local-path username.conf
rm username.conf

echo "Deleting Airflow Job airflow_orchestration-"$cde_user"-mfct"
cde job delete --name airflow-orchestration-$cde_user"-mfct" -v
echo "Creating Airflow Job airflow_orchestration-"$cde_user"-mfct"
cde job create --name airflow-orchestration-$cde_user"-mfct" --type airflow --mount-1-resource files-$cde_user"-mfct" --airflow-file-mount-1-resource cde-airflow-files-$cde_user"-mfct"  --dag-file airflow_DAG.py -v

# DELETE SETUP JOB
echo "Delete Spark Job table-setup-"$cde_user"-mfct"
cde job delete --name table-setup-$cde_user"-mfct" -v
