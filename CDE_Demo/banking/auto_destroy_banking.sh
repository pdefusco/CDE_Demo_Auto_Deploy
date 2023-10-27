#!/bin/sh

cde_user=$1

echo "TEARDOWN INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided CDE User: "$cde_user

echo "Delete CDE Credentials for User: "$cde_user
cde credential delete --name docker-creds-$cde_user"-banking"
echo "Delete Jobs"
echo "Delete batch_load-"$cde_user"-banking"
cde job delete --name batch_load-$cde_user"-banking"
echo "Delete ge_data_quality-"$cde_user"-banking"
cde job delete --name ge_data_quality-$cde_user"-banking"
echo "Delete data_quality_orchestration-"$cde_user"-banking"
cde job delete --name data_quality_orchestration-$cde_user"-banking"

echo "Delete resosurce dex-spark-runtime-great-expectations-data-quality-"$cde_user"-banking"
cde resource delete --name dex-spark-runtime-ge-data-quality-$cde_user"-banking"
echo "Upload cleanup script to resource cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Demo/banking/spark/cleanup.py
echo "Create cleanup job cleanup-"$cde_user"-banking"
cde job create --name cleanup-$cde_user"-banking" --type spark --mount-1-resource cde_demo_files-$cde_user"-banking" --application-file cleanup.py
echo "Run cleanup job cleanup-"$cde_user"-banking"
cde job run --name cleanup-$cde_user"-banking"

n=1
while [ $n -lt 50 ]
do
  echo "Running Cleanup Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done

echo "Delete cleanup job cleanup-"$cde_user"-banking"
cde job delete --name cleanup-$cde_user"-banking"
echo "Delete resource cde_demo_files-"$cde_user"-banking"
cde resource delete --name cde_demo_files-$cde_user"-banking"

echo "."
echo ".."
echo "..."
echo "....TEARDOWN COMPLETED"
