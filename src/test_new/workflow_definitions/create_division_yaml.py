import json
import os

from hera.shared import global_config
from hera.workflows import (
    Artifact,
    EmptyDirVolume,
    Steps,
    Workflow,
    script,  # pyright: ignore[reportUnknownVariableType]
)
from hera.workflows import models as m

global_config.host = os.environ.get("HOST")
global_config.image = str(os.environ.get("IMAGE"))
global_config.token = os.environ.get("TOKEN")


@script(
    volume_mounts=[m.VolumeMount(name="output-dir", mount_path="/output-dir/")],
    outputs=Artifact(name="json-output", path="/output-dir/output.json"),
)
def do_division(a: int, b: int):
    div = a / b
    intdiv = a // b
    remain = a % b
    dictionary_of_results = {
        "divide": div,
        "quotient": intdiv,
        "remainder": remain,
    }
    with open("/output-dir/output.json", "w") as otpt:
        json.dump(dictionary_of_results, otpt)


with Workflow(
    generate_name="hera-division-",  # when running on graphql this should be name
    entrypoint="divide",
    namespace=os.environ.get("NAMESPACE"),
    api_version="argoproj.io/v1alpha1",
    kind="Workflow",  # ClusterWorkflowTemplate", when on graphql
    labels={"workflows.diamond.ac.uk/science-group-examples": "true"},
    annotations={
        "workflows.argoproj.io/title": "Division via hera test",
        "workflows.argoproj.io/description": """Takes a numerical input and returns the
         remainder, output float, and output string to a json file""",
        "workflows.diamond.ac.uk/repository": "https://github.com/DiamondLightSource/{{repo_name}}",
    },
    volumes=EmptyDirVolume(name="output-dir", mount_path="/output-dir"),
) as w:
    with Steps(name="divide"):
        do_division(name="first", arguments={"a": 2, "b": 5})


with open("divisionyaml.yaml", "w") as div:
    div.write(w.to_yaml())  # pyright: ignore[reportUnknownMemberType]


# w.create()
