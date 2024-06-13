#!/bin/bash

cde_user=$1
cde_demo=$2

docker_user=${docker_user//[-._]/}

echo "Provided CDE User: "$cde_user
echo "Provided CDE Demo: "$cde_demo

. CDE_Demo/$cde_demo/auto_destroy_$cde_demo.sh $cde_user
