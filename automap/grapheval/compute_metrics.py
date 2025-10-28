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


def compute_metrics(
        gold_graph: Graph,
        pred_graph: Graph,
        config: Config,
        pred_mapping: str,
        only_common: bool = False,
        only_in_domain: bool = False,
) -> dict:
    """
    TODO: update docstring
    Compute evaluation metrics between gold and predicted RDF graphs.

    Args:
        gold_graph (Graph): The reference RDF graph.
        pred_graph (Graph): The predicted RDF graph.
        config (Config): Configuration for the evaluation.

    Returns:
        dict: A dictionary containing evaluation metrics.
    """

    is_triples = len(pred_graph) > 0
    map_is_correct = pred_mapping
    results = {}

    if is_triples and map_is_correct:
        evaluator = GraphEvaluator(pred_graph, gold_graph, config)
        if only_common:
            results = evaluator.evaluate_common()
        elif only_in_domain:
            results = evaluator.evaluate_in_domain()
        else:
            results = evaluator.evaluate_all()

    results["errors"] = {"NoTriples": not is_triples,
                         "NoCorrectMapping": not map_is_correct}

    return results


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
    parser.add_argument(
        '--pred_mapping',
        type=str,
        required=True,
        help='Path to the predicted mapping file (not used in current implementation)',
    )
    parser.add_argument(
        '--pred_graph',
        type=str,
        required=False,
        help='Path to the predicted RDF graph file (if not provided, read from stdin)'
    )
    parser.add_argument(
        "--only_common",
        action="store_true",
        help='Evaluate only common metrics.'
    )
    parser.add_argument(
        "--only_in_domain",
        type=bool,
        default=False,
        help='Evaluate only in domain metrics.'
    )

    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()

    if args.only_common and args.only_in_domain:
        raise ArgumentParser.error("Args --common and --in_domian are exclusive.")

    if not args.pred_graph:
        pred_graph_data = sys.stdin.read()
    else:
        with open(args.pred_graph, 'r') as f:
            pred_graph_data = f.read()

    with open(args.pred_mapping, 'r') as f:
        pred_mapping = f.read()

    gold_graph = Graph().parse(args.gold_graph)
    pred_graph = Graph().parse(data=pred_graph_data)
    config = Config(args.config)

    results = compute_metrics(
        gold_graph,
        pred_graph,
        config,
        pred_mapping,
        args.only_common,
        args.only_in_domain,
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
