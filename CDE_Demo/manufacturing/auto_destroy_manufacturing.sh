#!/bin/sh

cde_user=$1
cdp_data_lake_storage=$2

echo "##########################################################"
echo "CREATE DOCKER RUNTIME RESOURCE"
echo "##########################################################"
cde credential delete --name dckr-crds-$cde_user"-mfct" -v
echo "Delete Jobs"
echo "Delete create_staging_table-"$cde_user"-mfct"
cde job delete --name create-staging-table-$cde_user"-mfct" -v
echo "Delete iceberg-mergeinto-"$cde_user"-mfct"
cde job delete --name iceberg-mergeinto-$cde_user"-mfct" -v
echo "Delete airflow-orchestration-"$cde_user"-mfct"
cde job delete --name airflow-orchestration-$cde_user"-mfct" -v
echo "Delete iceberg-metadata-queries-"$cde_user"-mfct"
cde job delete --name iceberg-metadata-queries-$cde_user"-mfct" -v
echo "Delete resosurce datagen-runtime-"$cde_user"-mfct"
cde resource delete --name datagen-runtime-$cde_user"-mfct" -v
echo "Upload teardown script to resource files-"$cde_user"-mfct"
cde resource upload --name files-$cde_user"-mfct" --local-path CDE_Demo/manufacturing/spark/teardown.py -v
echo "Create teardown job teardown-"$cde_user"-mfct"
cde job create --name teardown-$cde_user"-mfct" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource files-$cde_user"-mfct" --application-file teardown.py -v
echo "Run teardown job teardown-"$cde_user"-mfct"
cde job run --name teardown-$cde_user"-mfct" -v
echo "##########################################################"
echo "RUN TEARDOWN JOB"
echo "##########################################################"

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

loading_icon 100 "Teardown in progress"

echo "Delete teardown job teardown-"$cde_user"-mfct"
cde job delete --name teardown-$cde_user"-mfct" -v
echo "Delete resource files-"$cde_user"-mfct"
cde resource delete --name files-$cde_user"-mfct" -v
echo "Delete resource cde-airflow-files-"$cde_user"-mfct"
cde resource delete --name cde-airflow-files-$cde_user"-mfct" -v
