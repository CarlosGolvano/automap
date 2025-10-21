"""
Helper Utilities for Graph Evaluation

This module provides general utility functions used across the package.
"""


def overlapping_lists(list1: list, list2: list) -> list:
    """
    Find overlapping elements between two lists using a two-pointer approach.

    This function sorts both lists and finds common elements efficiently.
    Time complexity: O(n log n + m log m + n + m)

    Args:
        list1: First list
        list2: Second list

    Returns:
        list: List of overlapping elements
    """
    sorted1 = sorted(list1)
    sorted2 = sorted(list2)

    overlap = []
    i = 0
    j = 0

    while i < len(sorted1) and j < len(sorted2):
        if sorted1[i] < sorted2[j]:
            i += 1
        elif sorted1[i] > sorted2[j]:
            j += 1
        else:
            overlap.append(sorted1[i])
            i += 1
            j += 1

    return overlap


def average(scores: list) -> float:
    return sum(scores) / len(scores) if len(scores) > 0 else 0.0
