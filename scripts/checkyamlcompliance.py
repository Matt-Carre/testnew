#!/bin/python
import os
import re

import yaml

yamlpath = "src/test_new/templates/"
yamllist: list[str] = []
for x in os.listdir(yamlpath):
    if x.endswith(".yaml"):
        yamllist.append(x)

for file in yamllist:
    metadata = api_ver = clst_tmpt = title = repo = group = annotations = labels = False
    with open(yamlpath + file) as s:
        yamldata = yaml.load(s, Loader=yaml.FullLoader)
    if "apiVersion" in yamldata.keys():
        match yamldata["apiVersion"]:
            case "argoproj.io/v1alpha1":
                api_ver = True
            case _:
                api_ver = False
    else:
        api_ver = False
    if "kind" in yamldata.keys():
        match yamldata["kind"]:
            case "Workflow":
                clst_tmpt = True
            case _:
                clst_tmpt = False
    else:
        clst_tmpt = False
    if "metadata" in yamldata.keys():
        metadata = True
        gen_name = "generateName" in yamldata["metadata"].keys()
        normal_name = "name" in yamldata["metadata"].keys()
        if "annotations" in yamldata["metadata"].keys():
            annotations = True
            title = (
                "workflows.argoproj.io/title"
                in yamldata["metadata"]["annotations"].keys()
            )
            repo = (
                "workflows.diamond.ac.uk/repository"
                in yamldata["metadata"]["annotations"].keys()
            )
        else:
            annotations = title = repo = False
        if "labels" in yamldata["metadata"].keys():
            labels = True
            if yamldata["metadata"]["labels"]:
                group = any(
                    re.match(r"workflows.diamond.ac.uk/science-group-.+", d)
                    for d in yamldata["metadata"]["labels"].keys()
                )
            else:
                group = False
        else:
            group = labels = False
    else:
        metadata = normal_name = gen_name = False
    if all([api_ver, clst_tmpt, title, repo, group, annotations, labels]):
        if gen_name != normal_name:
            exit(0)
        else:
            print(
                "generated_name and normal_name error, must have one of these not both"
            )
            exit(1)
    else:
        print(f"""
                within file: {file}...
                metadata present?: {metadata}
                annotations present?: {annotations}
                labels present?: {labels}
                api_ver present?: {api_ver}
                cluster template present?: {clst_tmpt}
                title present?: {title}
                repository present?: {repo}
                group present?: {group}""")
        exit(1)
