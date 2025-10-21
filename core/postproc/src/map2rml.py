import sys
import yatter
from ruamel.yaml import YAML


class Map2RML:
    def __init__(self):
        self.yaml = YAML(typ="safe", pure=True)

    def __call__(self, yarrrml_str: str) -> str:
        if not yarrrml_str:
            raise ValueError("Input YARRRML string is empty")

        yaml_content = self.yaml.load(yarrrml_str)

        return yatter.translate(yaml_content)


def main() -> int:
    yarrrml_str = sys.stdin.read()

    map2rml = Map2RML()
    output = map2rml(yarrrml_str)
    print(output)


if __name__ == "__main__":
    sys.exit(main())
