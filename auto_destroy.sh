#!/bin/bash

cde_user=$1
cde_demo=$2

echo "Provided CDE User: "$cde_user
echo "Provided CDE Demo: "$cde_demo

. CDE_Demo/$cde_demo/auto_destroy_$cde_demo.sh $cde_user
