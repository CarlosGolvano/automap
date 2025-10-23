# AUTOMAP

Automatic mapping generation pipeline.

## Table of Contents

- [Requirements](#requirements)
- [Preprocess](#preprocess)
- [Graph Evaluation](#graph-evaluation)
- [Postprocess](#postprocess)

## Requirements

Requirements in pyproject.toml. Use poetry.lock to install.

```bash
requires-python = "==3.12.*"
dependencies = [
    "rdflib (>=7.2.1,<8.0.0)",
    "pyyaml (>=6.0.3,<7.0.0)",
    "yatter (>=2.0.3,<3.0.0)",
]
requires = ["poetry-core>=2.0.0,<3.0.0"]
```

## 🔧 Preprocess

blablabla

## 🕸️ Graph Evaluation

A Python module for evaluating RDF graphs against reference ontologies with comprehensive metrics.

> Modified version of the evaluation code from [kg-pipeline](https://github.com/Vehnem/kg-pipeline), used in the paper ["Towards self-configuring Knowledge Graph Construction Pipelines using LLMs - A Case Study with RML"](https://ceur-ws.org/Vol-3718/paper6.pdf)

### Overview

This project provides both a command-line tool and a Python API for comparing RDF graphs. It computes precision, recall, and F1-scores across multiple dimensions including triples, subjects, predicates, objects, and classes, with support for hierarchy-aware scoring.

### Usage

#### Command Line

Use the `compute_metrics.py` script to evaluate graphs from the command line:

```bash
python compute_metrics.py --config config.yaml --gold_graph gold.nt < predicted.nt
```

The script reads the predicted graph from stdin and outputs a comprehensive JSON object with evaluation results. The output includes multiple evaluation dimensions:

- **Basic metrics**: Precision, recall, and F1-scores for triples, subjects, classes, predicates, and objects
- **Unique element metrics**: Evaluation of unique classes, predicates, and property-object pairs
- **Datatype validation**: Property-datatype combinations for literals
- **Entity coverage**: Coverage of expected entities by type
- **Hierarchy-aware scores**: Semantic similarity using ontology hierarchies for classes and properties
- **Detailed predicate analysis**: Usage statistics and correctness metrics for each configured predicate

Each metric includes true positives (tp), false positives (fp), false negatives (fn), and computed scores, providing a complete picture of how well the predicted graph matches the reference graph.

#### Python API

Import and use the `grapheval` module directly in your code:

```python
from rdflib import Graph
from grapheval import GraphEvaluator
from grapheval.config import Config

# Load graphs
test_graph = Graph().parse('predicted.nt', format='nt')
reference_graph = Graph().parse('gold.nt', format='nt')

# Evaluate with configuration
config = Config('config.yaml')
evaluator = GraphEvaluator(test_graph, reference_graph, config)

# Get all metrics
results = evaluator.evaluate_all()
print(f"F1 Score: {results['triples']['f1']:.4f}")

# Or get just a summary
summary = evaluator.get_summary()
```

### Configuration

The evaluation requires a YAML configuration file that specifies the ontology and evaluation parameters. Example structure:

```yaml
# Path to the ontology file
ontology_file: "/path/to/ontology.ttl"

# Base IRI for resources
base_iri: "http://mykg.org/resource/"

# Namespaces for predicates
namespaces:
  "dbo": "http://dbpedia.org/ontology/"

# Predicates to evaluate (using namespace prefixes)
predicates_to_evaluate:
  "dbo":
    - "starring"
    - "director"
    - "title"

# Entity IDs by type for validation
ids_by_type:
  "http://dbpedia.org/ontology/Film":
    - "tt0167423"
  "http://dbpedia.org/ontology/Person":
    - "nm0000002"
```

### Features

- **Basic Metrics**: Precision, recall, F1-score for triples, subjects, predicates, objects, and classes
- **Hierarchy-Aware Scoring**: Semantic similarity using ontology hierarchies
- **Domain-Specific Metrics**: Entity coverage, type correctness, property validation
- **Flexible Configuration**: YAML-based configuration for different ontologies
- **Dual Interface**: Use as CLI tool or Python library

## ⚙️ Postprocess

### `map2map`

`map2map` converts mapping files to the RML format. When provided with a
YARRRML file (``.yml``/``.yaml``) it relies on the
[YATTER](https://github.com/RMLio/yatter) CLI to do the conversion.  Existing
RML files are copied to the requested destination.

```
python -m src.map2map path/to/mapping.yml -o path/to/mapping.rml.ttl
```

The command prints the location of the generated file to standard output.
Set the ``YATTER_CMD`` environment variable or pass ``--yatter`` to point to a
custom executable when ``yatter`` is not on ``PATH``.

### `map2graph`

`map2graph` executes an RML mapping using the
[`RMLMapper`](https://github.com/RMLio/rmlmapper-java) CLI.  The path to the
mapper is read from the ``RMLMAPPER_JAR`` environment variable unless it is
provided via ``--rmlmapper``.  Use ``--ontology`` and ``--headers`` to provide
paths that can be consumed in the mapping via RMLMapper parameter placeholders
(``@{ontology}`` and ``@{headers}``).

```
python -m src.map2graph path/to/mapping.rml.ttl --ontology path/to/ontology.ttl \
    --headers path/to/headers.csv --rmlmapper /path/to/rmlmapper.jar
```

The generated triples are printed to standard output (one line per line in the
output file) and also written to disk. By default the file is named
``graph.ttl`` in the current working directory; supply ``--output`` to override
this behaviour. If the mapping fails or produces no triples the command exits
with a non-zero status code.


