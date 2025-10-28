from printers import print_header, print_metrics
from automap.utils import get_in_domain, get_common


def eval2Tabular(eval_json: dict, only_common=False, only_in_domain=False):
    if only_common:
        print_header("COMMON")
        print_metrics(get_common(eval_json))
    elif only_in_domain:
        print_header("IN DOMAIN")
        print_metrics(get_in_domain(eval_json))
    else:
        print_header("COMMON")
        print_metrics(get_common(eval_json))
        print_header("IN DOMAIN")
        print_metrics(get_in_domain(eval_json))


if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--only_common",
        action="store_true",
        help="Evaluate only common metrics.",
    )
    group.add_argument(
        "--only_in_domain",
        action="store_true",
        help="Evaluate only in domain metrics.",
    )
    args = parser.parse_args()

    eval2Tabular(json.loads(sys.stdin.read()), only_common=args.only_common, only_in_domain=args.only_in_domain)
