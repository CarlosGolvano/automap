"""
Compute Graph Evaluation Metrics

This script evaluates RDF graphs using the grapheval package.
Updated to use the new grapheval package structure with YAML configuration.
"""

import json
from rdflib import Graph
from grapheval import GraphEvaluator
from grapheval.utils.config import Config
from argparse import ArgumentParser


def compute_metrics(gold_graph: Graph, pred_graph: Graph, config: Config) -> dict:
    """
    Compute evaluation metrics between gold and predicted RDF graphs.

    Args:
        gold_graph (Graph): The reference RDF graph.
        pred_graph (Graph): The predicted RDF graph.
        config (Config): Configuration for the evaluation.

    Returns:
        dict: A dictionary containing evaluation metrics.
    """
    evaluator = GraphEvaluator(pred_graph, gold_graph, config)
    results = evaluator.evaluate_all()
    return results


if __name__ == '__main__':
    import sys
    import json

    parser = ArgumentParser(description="Evaluate RDF graphs using grapheval.")
    parser.add_argument('--config', type=str, help='Path to the YAML configuration file.')
    parser.add_argument('--gold_graph', type=str, help='Path to the gold standard RDF graph file.')

    args = parser.parse_args()

    pred_graph = ""
    for line in sys.stdin:
        pred_graph += line

    results = compute_metrics(
        gold_graph=Graph().parse(args.gold_graph),
        pred_graph=Graph().parse(data=pred_graph),
        config=Config(args.config)
    )

    print(json.dumps(results, ensure_ascii=False))
