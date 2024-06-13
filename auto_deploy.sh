#!/bin/bash

docker_user=$1
cde_user=$2
cde_demo=$3
cdp_data_lake_storage=$4

cde_user_formatted=${cde_user//[-._]/}
d=$(date)
fmt="%-30s %s\n"


echo "##########################################################"
printf "${fmt}" "CDE ${cde_demo} demo deployment launched."
printf "${fmt}" "demo launch time:" "${d}"
printf "${fmt}" "performed by CDP User:" "${cde_user_formatted}"
printf "${fmt}" "performed by Docker User:" "${docker_user}"
echo "##########################################################"


. CDE_Demo/$cde_demo/auto_deploy_$cde_demo.sh $docker_user $cde_user $cdp_data_lake_storage

e=$(date)

printf "${fmt}" "CDE ${cde_demo} demo deployment completed."
printf "${fmt}" "completion time:" "${e}"
printf "${fmt}" "please visit CDE Job Runs UI to view in-progress demo"
echo "##########################################################"
