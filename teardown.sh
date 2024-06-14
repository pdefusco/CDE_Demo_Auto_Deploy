#!/bin/bash

cde_user=$1
cdp_data_lake_storage=$2
cde_demo=$3

cde_user_formatted=${cde_user//[-._]/}
d=$(date)
fmt="%-30s %s\n"

echo "##########################################################"
printf "${fmt}" "CDE ${cde_demo} demo teardown initiated."
printf "${fmt}" "demo launch time:" "${d}"
printf "${fmt}" "performed by CDP User:" "${cde_user}"
echo "##########################################################"

. CDE_Demo/$cde_demo/auto_destroy_$cde_demo.sh $cdp_data_lake_storage $cde_user_formatted

e=$(date)

echo "##########################################################"
printf "${fmt}" "CDE ${cde_demo} demo teardown completed."
printf "${fmt}" "demo launch time:" "${e}"
printf "${fmt}" "performed by CDP User:" "${cde_user}"
echo "##########################################################"
