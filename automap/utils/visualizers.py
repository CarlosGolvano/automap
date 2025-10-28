from printers import print_header, print_metrics
from automap.utils import get_in_domain, get_common


def print_eval_tabular(eval_json: dict, only_common=False, only_in_domain=False):
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


def eval2wandb(eval_json: dict) -> dict:
    """Convert evaluation results to a format suitable for Weights & Biases logging.

    Args:
        eval_json (dict): The evaluation results in JSON format.

    Returns:
        dict: A dictionary formatted for Weights & Biases logging.
    """

    common_metrics = get_common(eval_json)
    return common_metrics

    # TODO: versión final a implementar
    # summary = get_evaluation_summary(eval_json)
    # wandb_metrics = {}
    # for key, value in summary.items():
    #     if isinstance(value, (int, float)):
    #         wandb_metrics[key] = value
    #     elif isinstance(value, dict):
    #         for sub_key, sub_value in value.items():
    #             wandb_metrics[f"{key}/{sub_key}"] = sub_value
    # return wandb_metrics


if __name__ == "__main__":
    import json
    import sys

    json_data = json.loads(sys.stdin.read())

    print_eval_tabular(json_data)
