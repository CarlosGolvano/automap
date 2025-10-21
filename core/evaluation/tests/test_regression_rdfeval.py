"""
Regression Test Suite - OLD Implementation

This script verifies that the old rdfeval implementation produces
the same results as the baselines (which were generated from it).
This serves as a sanity check.
"""

import os
import sys
import json
from rdflib import Graph

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rdfeval.rdfeval import RDFeval


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def read_or_pass(data_or_file):
    """Read file content if path exists, otherwise return the string as-is."""
    if os.path.exists(data_or_file):
        with open(data_or_file, 'r') as f:
            return f.read()
    else:
        return data_or_file


def serialize_results(results):
    """Convert results to JSON-serializable format."""
    def convert_value(v):
        if isinstance(v, (int, float, bool, type(None))):
            return v
        elif isinstance(v, dict):
            return {str(k): convert_value(val) for k, val in v.items()}
        elif isinstance(v, list):
            return [convert_value(item) for item in v]
        else:
            return str(v)
    
    return convert_value(results)


def compare_metric(baseline_value, new_value, tolerance=1e-6):
    """
    Compare two metric values.
    
    Returns:
        tuple: (matches, difference)
    """
    if isinstance(baseline_value, (int, float)) and isinstance(new_value, (int, float)):
        diff = abs(baseline_value - new_value)
        matches = diff <= tolerance
        return matches, diff
    elif baseline_value == new_value:
        return True, 0
    else:
        return False, None


def compare_results(baseline, old_results, test_name):
    """
    Compare baseline results with old implementation results.
    
    Returns:
        dict: Comparison statistics
    """
    print(f"\n{Colors.BOLD}Comparing: {test_name}{Colors.ENDC}")
    print("=" * 60)
    
    stats = {
        'total_metrics': 0,
        'matching_metrics': 0,
        'mismatches': [],
        'missing_in_old': [],
        'extra_in_old': []
    }
    
    # Compare all metrics in baseline
    for metric_name in baseline.keys():
        if metric_name not in old_results:
            stats['missing_in_old'].append(metric_name)
            print(f"{Colors.YELLOW}⚠️  Missing in old: {metric_name}{Colors.ENDC}")
            continue
        
        baseline_metric = baseline[metric_name]
        old_metric = old_results[metric_name]
        
        # Compare key values (tp, fp, fn, precision, recall, f1)
        for key in ['tp', 'fp', 'fn', 'tn', 'precision', 'recall', 'f1']:
            if key in baseline_metric:
                stats['total_metrics'] += 1
                
                baseline_val = baseline_metric[key]
                old_val = old_metric.get(key)
                
                if old_val is None:
                    stats['mismatches'].append({
                        'metric': f"{metric_name}.{key}",
                        'baseline': baseline_val,
                        'old': None,
                        'reason': 'Missing in old'
                    })
                    print(f"{Colors.RED}❌ {metric_name}.{key}: Missing in old results{Colors.ENDC}")
                else:
                    matches, diff = compare_metric(baseline_val, old_val)
                    
                    if matches:
                        stats['matching_metrics'] += 1
                        print(f"{Colors.GREEN}✅ {metric_name}.{key}: {old_val}{Colors.ENDC}")
                    else:
                        stats['mismatches'].append({
                            'metric': f"{metric_name}.{key}",
                            'baseline': baseline_val,
                            'old': old_val,
                            'diff': diff
                        })
                        print(f"{Colors.RED}❌ {metric_name}.{key}: baseline={baseline_val}, old={old_val}, diff={diff}{Colors.ENDC}")
    
    return stats


def run_old_implementation(test_file, reference_file):
    """Run the old rdfeval implementation."""
    print(f"\nRunning old implementation (rdfeval)...")
    
    # Load graphs
    with open(reference_file, 'r') as f:
        reference_data = f.read()
    reference_graph = Graph()
    reference_graph.parse(data=read_or_pass(reference_data), format='turtle')
    print(f"  Reference: {len(reference_graph)} triples")
    
    with open(test_file, 'r') as f:
        test_data = f.read()
    test_graph = Graph()
    test_graph.parse(data=read_or_pass(test_data), format='turtle')
    print(f"  Test: {len(test_graph)} triples")
    
    # Run evaluation
    evaluator = RDFeval(test_graph, reference_graph)
    results = evaluator.createStatistics()
    
    return serialize_results(results)


def run_test_case(test_case):
    """Run a single test case."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"Test Case: {test_case['name']}")
    print(f"{'='*60}{Colors.ENDC}")
    
    # Check if baseline exists
    if not os.path.exists(test_case['baseline']):
        print(f"{Colors.RED}❌ Baseline not found: {test_case['baseline']}{Colors.ENDC}")
        print(f"{Colors.YELLOW}   Run: python tests/generate_baseline.py{Colors.ENDC}")
        return None
    
    # Load baseline
    with open(test_case['baseline'], 'r') as f:
        baseline = json.load(f)
    print(f"✅ Baseline loaded: {len(baseline)} top-level metrics")
    
    # Run old implementation
    try:
        old_results = run_old_implementation(
            test_case['test'],
            test_case['reference']
        )
        print(f"✅ Old implementation completed: {len(old_results)} top-level metrics")
    except Exception as e:
        print(f"{Colors.RED}❌ Error running old implementation: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        return None
    
    # Compare results
    stats = compare_results(baseline, old_results, test_case['name'])
    
    return stats


def main():
    """Run all regression tests."""
    print(f"{Colors.BOLD}🧪 Regression Test Suite - OLD Implementation{Colors.ENDC}")
    print("=" * 60)
    print("Verifying rdfeval (old) matches its own baselines")
    print("=" * 60)
    
    data_dir = './tests'
    baseline_dir = './tests/baselines'
    
    # Test cases
    test_cases = [
        {
            'name': 'gold_vs_pred',
            'test': os.path.join(data_dir, 'pred.nt'),
            'reference': os.path.join(data_dir, 'gold.nt'),
            'baseline': os.path.join(baseline_dir, 'baseline_gold_pred.json')
        },
        {
            'name': 'gold2_vs_pred',
            'test': os.path.join(data_dir, 'pred.nt'),
            'reference': os.path.join(data_dir, 'gold2.nt'),
            'baseline': os.path.join(baseline_dir, 'baseline_gold2_pred.json')
        }
    ]
    
    # Run tests
    all_stats = []
    for test_case in test_cases:
        stats = run_test_case(test_case)
        if stats:
            all_stats.append((test_case['name'], stats))
    
    # Print summary
    print(f"\n{Colors.BOLD}{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}{Colors.ENDC}")
    
    total_metrics = 0
    total_matching = 0
    total_mismatches = 0
    
    for test_name, stats in all_stats:
        total_metrics += stats['total_metrics']
        total_matching += stats['matching_metrics']
        total_mismatches += len(stats['mismatches'])
        
        match_rate = (stats['matching_metrics'] / stats['total_metrics'] * 100) if stats['total_metrics'] > 0 else 0
        
        print(f"\n{Colors.BOLD}{test_name}:{Colors.ENDC}")
        print(f"  Total metrics: {stats['total_metrics']}")
        print(f"  {Colors.GREEN}Matching: {stats['matching_metrics']} ({match_rate:.1f}%){Colors.ENDC}")
        
        if stats['mismatches']:
            print(f"  {Colors.RED}Mismatches: {len(stats['mismatches'])}{Colors.ENDC}")
            for mismatch in stats['mismatches'][:5]:  # Show first 5
                print(f"    - {mismatch['metric']}: {mismatch['baseline']} → {mismatch['old']}")
        
        if stats['missing_in_old']:
            print(f"  {Colors.YELLOW}Missing: {len(stats['missing_in_old'])}{Colors.ENDC}")
    
    # Overall summary
    print(f"\n{Colors.BOLD}Overall:{Colors.ENDC}")
    print(f"  Total metrics compared: {total_metrics}")
    
    if total_mismatches == 0:
        print(f"  {Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED! ({total_matching}/{total_metrics}){Colors.ENDC}")
        return 0
    else:
        match_rate = (total_matching / total_metrics * 100) if total_metrics > 0 else 0
        print(f"  {Colors.GREEN}✅ Matching: {total_matching} ({match_rate:.1f}%){Colors.ENDC}")
        print(f"  {Colors.RED}❌ Mismatches: {total_mismatches}{Colors.ENDC}")
        return 1


if __name__ == '__main__':
    exit(main())
