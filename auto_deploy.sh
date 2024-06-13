#!/bin/bash

docker_user=$1
cde_user=$2
cde_demo=$3

docker_user=${docker_user//[-._]/}

echo "Provided Docker User: "$docker_user
echo "Provided CDE User: "$cde_user
echo "Provided CDE Demo: "$cde_demo

. CDE_Demo/$cde_demo/auto_deploy_$cde_demo.sh $docker_user $cde_user
