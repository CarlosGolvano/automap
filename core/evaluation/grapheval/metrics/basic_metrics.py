"""
Basic Graph Evaluation Metrics

This module provides fundamental metrics for comparing RDF graphs:
- Subject comparison
- Triple comparison  
- Class comparison
"""

from grapheval.utils import overlapping_lists, calculate_metrics
from .base import Metrics


class BasicMetrics(Metrics):
    def evaluate_triples(self) -> dict:
        """
        Evaluate complete triples (s+p+o) with exact matching.

        Returns:
            dict: Metrics including tp, fp, fn, tn, precision, recall, f1
        """
        test_triples = set([str(s) + str(p) + str(o) for s, p, o in self.test_graph])
        reference_triples = set([str(s) + str(p) + str(o) for s, p, o in self.reference_graph])

        tp = len(test_triples.intersection(reference_triples))
        fp = len(test_triples) - tp
        fn = len(reference_triples) - tp
        tn = 0

        return calculate_metrics(tp, fp, fn, tn)

    def evaluate_subjects_unique(self) -> dict:
        """
        Evaluate unique subject IRIs with exact matching.

        Returns:
            dict: Metrics including tp, fp, fn, tn, precision, recall, f1
        """
        test_subjects = set([s for s, p, o in self.test_graph])
        reference_subjects = set([s for s, p, o in self.reference_graph])

        tp = len(test_subjects.intersection(reference_subjects))
        fp = len(test_subjects) - tp
        fn = len(reference_subjects) - tp
        tn = 0

        return calculate_metrics(tp, fp, fn, tn)

    def evaluate_subjects_fuzzy(self) -> dict:
        """
        Evaluate subjects with fuzzy matching based on ID extraction.

        Useful when subjects have different prefixes but same IDs.

        Returns:
            dict: Metrics including tp, fp, fn, tn, precision, recall, f1
        """
        test_subjects = set([s for s, p, o in self.test_graph])
        reference_subjects = set([s for s, p, o in self.reference_graph])
        reference_ids = [str(s).split("/")[-1] for s, p, o in self.reference_graph]

        tp = 0
        for s in test_subjects:
            if any(ref_id in str(s) for ref_id in reference_ids):
                tp += 1

        fp = len(test_subjects) - tp
        fn = len(reference_subjects) - tp
        tn = 0

        return calculate_metrics(tp, fp, fn, tn)

    def evaluate_classes_unique(self) -> dict:
        """
        Evaluate unique classes (rdf:type objects) used in the graphs.

        Returns:
            dict: Metrics and lists of test/reference classes
        """
        test_classes = set([o for s, p, o in self.test_graph if str(p) == self.config.rdf_type_uri])
        reference_classes = set([o for s, p, o in self.reference_graph if str(p) == self.config.rdf_type_uri])

        tp = len(test_classes.intersection(reference_classes))
        fp = len(test_classes) - tp
        fn = len(reference_classes) - tp
        tn = 0

        return {
            'test_classes': list(test_classes),
            'reference_classes': list(reference_classes),
            **calculate_metrics(tp, fp, fn, tn),
        }

    def evaluate_classes(self) -> dict:
        """
        Evaluate class usage (counting duplicates).

        Useful when multiple subjects have the same class.

        Returns:
            dict: Metrics including tp, fp, fn, tn, precision, recall, f1, and class lists
        """
        test_classes = list([o for s, p, o in self.test_graph if str(p) == self.config.rdf_type_uri])
        reference_classes = list(
            [o for s, p, o in self.reference_graph if str(p) == self.config.rdf_type_uri])

        tp = len(overlapping_lists(test_classes, reference_classes))
        fp = len(test_classes) - tp
        fn = len(reference_classes) - tp
        tn = 0

        return {
            'test_classes': test_classes,
            'reference_classes': reference_classes,
            **calculate_metrics(tp, fp, fn, tn)
        }
