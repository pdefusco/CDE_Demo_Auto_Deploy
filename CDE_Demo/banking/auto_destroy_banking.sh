#!/bin/sh

cdp_data_lake_storage=$1
cde_user=$2

echo "##########################################################"
echo "DELETE DOCKER CREDS AND SPARK JOBS"
echo "##########################################################"
echo "Delete CDE Credentials for User: "$cde_user
cde credential delete --name dckr-crds-$cde_user"-bnk"
echo "Delete batch_load-"$cde_user"-bnk"
cde job delete --name batch-load-$cde_user"-bnk"
echo "Delete ge_data_quality-"$cde_user"-bnk"
cde job delete --name ge-data-quality-$cde_user"-bnk"
echo "Delete data_quality_orchestration-"$cde_user"-bnk"
cde job delete --name data-quality-orch-$cde_user"-bnk"

echo "##########################################################"
echo "DELETE FILES RESOURCES"
echo "##########################################################"
echo "Delete resosurce ge-runtime-"$cde_user"-bnk"
cde resource delete --name ge-runtime-$cde_user"-bnk"
echo "Upload teardown script to resource files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Demo/banking/spark/teardown.py
echo "Create teardown job teardown-"$cde_user"-bnk"
cde job create --name teardown-$cde_user"-bnk" --arg $cdp_data_lake_storage --arg $cde_user --type spark --mount-1-resource "files-"$cde_user"-bnk" --application-file teardown.py
echo "Run teardown job teardown-"$cde_user"-bnk"
cde job run --name teardown-$cde_user"-bnk"

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

loading_icon 60 "Teardown in progress"


echo "##########################################################"
echo "DELETE TEARDOWN JOB"
echo "##########################################################"
echo "Delete teardown job teardown-"$cde_user"-bnk"
cde job delete --name teardown-$cde_user"-bnk"
echo "Delete resource files-"$cde_user"-bnk"
cde resource delete --name files-$cde_user"-bnk"
