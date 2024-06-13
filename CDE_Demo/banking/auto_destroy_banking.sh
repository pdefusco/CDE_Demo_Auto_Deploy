#!/bin/sh

cde_user=$1

echo "bnk DATA QUALITY DEMO TEARDOWN INITIATED...."
echo "..."
echo ".."
echo "."
echo "Provided CDE User: "$cde_user

echo "Delete CDE Credentials for User: "$cde_user
cde credential delete --name dckr-crds-$cde_user"-bnk"
echo "Delete Jobs"
echo "Delete batch_load-"$cde_user"-bnk"
cde job delete --name batch_load-$cde_user"-bnk"
echo "Delete ge_data_quality-"$cde_user"-bnk"
cde job delete --name ge_data_quality-$cde_user"-bnk"
echo "Delete data_quality_orchestration-"$cde_user"-bnk"
cde job delete --name data_quality_orch-$cde_user"-bnk"

echo "Delete resosurce ge-runtime-"$cde_user"-bnk"
cde resource delete --name ge-runtime-$cde_user"-bnk"
echo "Upload teardown script to resource files-"$cde_user"-bnk"
cde resource upload --name files-$cde_user"-bnk" --local-path CDE_Demo/bnk/spark/teardown.py
echo "Create teardown job teardown-"$cde_user"-bnk"
cde job create --name teardown-$cde_user"-bnk" --arg $data_lake --arg $cde_user --type spark --mount-1-resource files-$cde_user"-bnk" --application-file teardown.py
echo "Run teardown job teardown-"$cde_user"-bnk"
cde job run --name teardown-$cde_user"-bnk"

n=1
while [ $n -lt 50 ]
do
  echo "Running teardown Job..."
  sleep 2
  echo " "
  ((n=$n+1))
done

echo "Delete teardown job teardown-"$cde_user"-bnk"
cde job delete --name teardown-$cde_user"-bnk"
echo "Delete resource files-"$cde_user"-bnk"
cde resource delete --name files-$cde_user"-bnk"

echo "."
echo ".."
echo "..."
echo "....TEARDOWN COMPLETED"
