"""
Visualization Module for Graph Evaluation

This module provides plotting and visualization functions for evaluation metrics.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_precision_recall_f1(scores, output_file='boxplot.png'):
    """
    Generate precision, recall, and F1-score boxplots using seaborn.
    
    Args:
        scores (list of tuples): A list where each tuple contains (precision, recall, f1_score)
        output_file (str): Path to save the plot. Default is 'boxplot.png'
    
    Returns:
        matplotlib.pyplot: The pyplot object with the plots
    
    Example:
        >>> scores = [(0.9, 0.8, 0.85), (0.92, 0.82, 0.87)]
        >>> plot_precision_recall_f1(scores, 'my_plot.png')
    """
    # Filter out empty scores
    valid_scores = [s for s in scores if s != (0, 0, 0)]
    
    if not valid_scores:
        print("Warning: No valid scores to plot")
        return plt
    
    # Unpack scores into separate lists
    precision_scores, recall_scores, f1_scores = zip(*valid_scores)
    
    # Prepare data for boxplot
    data = {
        'Precision': precision_scores,
        'Recall': recall_scores,
        'F1 Score': f1_scores
    }
    df = pd.DataFrame(data)
    
    # Create a figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    
    # Plot precision scores boxplot
    sns.boxplot(data=df, y='Precision', ax=axes[0])
    axes[0].set_title('Precision Scores')
    axes[0].set_xlabel('Sample')
    
    # Plot recall scores boxplot
    sns.boxplot(data=df, y='Recall', ax=axes[1])
    axes[1].set_title('Recall Scores')
    axes[1].set_xlabel('Sample')
    
    # Plot F1 scores boxplot
    sns.boxplot(data=df, y='F1 Score', ax=axes[2])
    axes[2].set_title('F1 Scores')
    axes[2].set_xlabel('Sample')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_file)
    
    return plt


def plot_comparison_bars(metrics_dict, output_file='comparison.png'):
    """
    Create a bar chart comparing different metrics.
    
    Args:
        metrics_dict (dict): Dictionary with metric names as keys and values as scores
        output_file (str): Path to save the plot
    
    Returns:
        matplotlib.pyplot: The pyplot object with the plot
    
    Example:
        >>> metrics = {'precision': 0.85, 'recall': 0.80, 'f1': 0.82}
        >>> plot_comparison_bars(metrics)
    """
    df = pd.DataFrame(list(metrics_dict.items()), columns=['Metric', 'Score'])
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Metric', y='Score')
    plt.title('Evaluation Metrics Comparison')
    plt.xlabel('Metric')
    plt.ylabel('Score')
    plt.ylim(0, 1.0)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.savefig(output_file)
    
    return plt
