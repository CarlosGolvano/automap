from automap.utils import get_common


def eval2wb(eval_json: dict) -> dict:
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

    eval2wb(json.loads(sys.stdin.read()))
