#!/bin/bash
cd src/test_new/workflow_definitions
for file in *
do
uv run "$file"
done
mv *.yaml ../templates/
git add -u ../templates/
