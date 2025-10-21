"""
Graph Evaluation Configuration

This module contains the Config class for loading configuration from YAML files
and backward-compatible global constants.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Union


class Config:
    def __init__(self, config_path: Union[str, Path]):
        """
        Initialize configuration from a YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is not valid YAML
            KeyError: If required config keys are missing
        """
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        if not config_data:
            raise ValueError(f"Config file is empty: {config_path}")

        self.ontology_file: str = config_data.get('ontology_file', '')
        self.rdf_type_uri: str = config_data.get('rdf_type_uri', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        self.base_iri: str = config_data.get('base_iri', '')

        self.ids_by_type: Dict[str, List[str]] = config_data.get('ids_by_type', {})
        self.property_suffixes: List[str] = config_data.get('property_suffixes', [])
        self.predicates_to_evaluate = self.build_predicates_list(config_data=config_data)

        queries = config_data.get('sparql_queries', {})
        self.subclass_query: str = queries.get('subclass', self._default_subclass_query())
        self.subproperty_query: str = queries.get('subproperty', self._default_subproperty_query())
        self.subject_class_query: str = queries.get('subject_class', self._default_subject_class_query())
        self.subject_property_query: str = queries.get(
            'subject_property', self._default_subject_property_query())
        self.subject_property_value_query: str = queries.get('subject_property_value',
                                                             self._default_subject_property_value_query())

    def build_predicates_list(self, config_data) -> List[str]:
        predicates = []
        namespaces = config_data.get('namespaces', {})
        predicates_to_evaluate_suffixes = config_data.get('predicates_to_evaluate', {})
        for prefix, suffixes in predicates_to_evaluate_suffixes.items():
            namespace = namespaces.get(prefix, '')
            for suffix in suffixes:
                if namespace:
                    predicates.append(namespace + suffix)
        return predicates

    @staticmethod
    def _default_subclass_query() -> str:
        return """
SELECT ?superClass ?subClass
WHERE {
    ?subClass rdfs:subClassOf ?superClass .
}
"""

    @staticmethod
    def _default_subproperty_query() -> str:
        return """
SELECT ?superProperty ?subProperty
WHERE {
    ?subProperty rdfs:subPropertyOf ?superProperty .
}
"""

    @staticmethod
    def _default_subject_class_query() -> str:
        return """
SELECT ?class
WHERE {
    ?s a ?class .
}
"""

    @staticmethod
    def _default_subject_property_query() -> str:
        return """
SELECT ?property
WHERE {
    ?s ?property ?o .
}
"""

    @staticmethod
    def _default_subject_property_value_query() -> str:
        return """
SELECT ?property ?value
WHERE {
    ?s ?property ?value .
}
"""

    def __repr__(self) -> str:
        return f"Config(config_path='{self.config_path}')"
