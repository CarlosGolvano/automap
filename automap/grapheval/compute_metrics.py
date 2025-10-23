"""
Compute Graph Evaluation Metrics

This script evaluates RDF graphs using the grapheval package.
Updated to use the new grapheval package structure with YAML configuration.
"""
import sys
import json
from rdflib import Graph
from automap.grapheval.metrics import GraphEvaluator
from automap.utils.config import Config
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
    return evaluator.evaluate_all()


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(
        description="Evaluate RDF graphs using grapheval.",
        epilog="Example: python compute_metrics.py --config config.yaml --gold gold.nt < pred.nt"
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to the YAML configuration file'
    )
    parser.add_argument(
        '--gold_graph',
        type=str,
        required=True,
        help='Path to the gold standard RDF graph file'
    )
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()

    pred_graph_data = sys.stdin.read()

    gold_graph = Graph().parse(args.gold_graph)
    pred_graph = Graph().parse(data=pred_graph_data)
    config = Config(args.config)

    results = compute_metrics(gold_graph, pred_graph, config)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
