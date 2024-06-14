#!/bin/sh

cdp_data_lake_storage=$1
cde_user=$2

echo "##########################################################"
echo "CREATE DOCKER RUNTIME RESOURCE"
echo "##########################################################"
echo "Delete Docker Credentials"
cde credential delete --name dckr-crds-$cde_user"-telco" -v

echo "##########################################################"
echo "DELETE SPARK JOBS"
echo "##########################################################"
echo "Delete geospatial-rdd-"$cde_user"-telco"
cde job delete --name geospatial-rdd-$cde_user"-telco" -v
echo "Delete create-staging-table-"$cde_user"-telco"
cde job delete --name geospatial-joins-$cde_user"-telco" -v
echo "Delete create-staging-table-"$cde_user"-telco"
cde job delete --name geo-orch-$cde_user"-telco" -v

echo "Upload teardown script to resource app-code-"$cde_user"-telco"
cde resource upload --name app-code-$cde_user"-telco" --local-path CDE_Demo/telco/spark/teardown.py -v
echo "Create teardown job teardown-"$cde_user"-telco"
cde job create --name teardown-$cde_user"-telco" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource app-code-$cde_user"-telco" --application-file teardown.py -v
echo "Run teardown job teardown-"$cde_user"-telco"
cde job run --name teardown-$cde_user"-telco" -v
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

echo "Delete teardown job teardown-"$cde_user
cde job delete --name teardown-$cde_user"-telco" -v
echo "Delete resource app-code-"$cde_user"-telco"
cde resource delete --name app-code-$cde_user"-telco" -v
echo "Delete resource countries-data-"$cde_user"-telco"
cde resource delete --name countries-data-$cde_user"-telco" -v
echo "Delete Custom Docker Runtime sedona-runtime-$cde_user-telco"
cde resource delete --name sedona-runtime-$cde_user"-telco" -v
