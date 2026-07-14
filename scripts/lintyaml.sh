#!/bin/bash
cd src/test_new/templates
for file in *
do
argo lint "$file" --offline
SUCCESSFULLINT=$?
[ $SUCCESSFULLINT -ne 0 ] && exit 1
done
exit 0
