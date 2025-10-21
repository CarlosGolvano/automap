from typing import List
from map2rml import Map2RML
from pathlib import Path
from 


def _parse_argv():
    import argparse

    parser = argparse.ArgumentParser(description="Postprocess YARRRML to RDF graph.")
    parser.add_argument("path", type=str, help="Path to the experiment directory.")
    return parser.parse_args()


def postprocess():
    args = _parse_argv()

    with open(f"{args.path}/mapping.yml", 'r') as f:
        yarrrml_str = f.read()

    map2rml = Map2RML()
    rml_mapping = map2rml(yarrrml_str)

    status = 1 if not rml_mapping else 0
    add_metadata(metadata, 'mapping_status', status)

    return rml_mapping


if __name__ == "__main__":
    with open("./data/mapping.yml", 'r') as f:
        sample_yarrrml = f.read()

    metadata = {}
    postprocess(sample_yarrrml, metadata=metadata)
    print(metadata)
