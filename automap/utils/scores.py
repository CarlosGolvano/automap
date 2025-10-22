"""
Scoring Functions for Graph Evaluation

This module provides pure mathematical functions for calculating 
evaluation metrics such as precision, recall, and F1-score.
"""


def precision_score(tp: int, fp: int) -> float:
    return tp / (tp + fp) if tp + fp > 0 else 0.0


def recall_score(tp: int, fn: int) -> float:
    return tp / (tp + fn) if tp + fn > 0 else 0.0


def f1_score(tp: int, fp: int, fn: int) -> float:
    precision = precision_score(tp, fp)
    recall = recall_score(tp, fn)
    return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0


def calculate_metrics(tp: int, fp: int, fn: int, tn: int = 0) -> dict:
    return {
        'tp': tp,
        'fp': fp,
        'fn': fn,
        'tn': tn,
        'precision': precision_score(tp, fp),
        'recall': recall_score(tp, fn),
        'f1': f1_score(tp, fp, fn)
    }
