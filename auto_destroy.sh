#!/bin/bash

cde_user=$1
cde_demo=$2
cdp_data_lake_storage=$3

cde_user=${cde_user//[-._]/}

cde_user_formatted=${cde_user//[-._]/}
d=$(date)
fmt="%-30s %s\n"

echo "##########################################################"
printf "${fmt}" "CDE ${cde_demo} demo teardown initiated."
printf "${fmt}" "demo launch time:" "${d}"
printf "${fmt}" "performed by CDP User:" "${cde_user_formatted}"
printf "${fmt}" "performed by Docker User:" "${docker_user}"
echo "##########################################################"

. CDE_Demo/$cde_demo/auto_destroy_$cde_demo.sh $cde_user $cdp_data_lake_storage

e=$(date)

echo "##########################################################"
printf "${fmt}" "CDE ${cde_demo} demo teardown completed."
printf "${fmt}" "demo launch time:" "${e}"
printf "${fmt}" "performed by CDP User:" "${cde_user_formatted}"
printf "${fmt}" "performed by Docker User:" "${docker_user}"
echo "##########################################################"
