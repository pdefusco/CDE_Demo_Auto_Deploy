#!/bin/sh

cde_user=$1

echo "BANKING DATA QUALITY DEMO TEARDOWN INITIATED...."
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
echo "Upload teardown script to resource cde_demo_files-"$cde_user"-banking"
cde resource upload --name cde_demo_files-$cde_user"-banking" --local-path CDE_Demo/banking/spark/teardown.py
echo "Create teardown job teardown-"$cde_user"-banking"
cde job create --name teardown-$cde_user"-banking" --type spark --mount-1-resource cde_demo_files-$cde_user"-banking" --application-file teardown.py
echo "Run teardown job teardown-"$cde_user"-banking"
cde job run --name teardown-$cde_user"-banking"

n=1
while [ $n -lt 50 ]
do
  echo "Running teardown Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done

echo "Delete teardown job teardown-"$cde_user"-banking"
cde job delete --name teardown-$cde_user"-banking"
echo "Delete resource cde_demo_files-"$cde_user"-banking"
cde resource delete --name cde_demo_files-$cde_user"-banking"

echo "."
echo ".."
echo "..."
echo "....TEARDOWN COMPLETED"
