"""
Generate baseline metrics using the old rdfeval implementation.

This script runs the old implementation to generate baseline results
that we can compare against the new grapheval implementation.
"""

import os
import sys
import json
from rdflib import Graph

# Add parent directory to path to import rdfeval
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import old implementation
try:
    from rdfeval.rdfeval import RDFeval
except ImportError:
    print("ERROR: Cannot import rdfeval. Make sure the old implementation is available.")
    print("If you've already migrated, you can use pre-generated baselines.")
    sys.exit(1)


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


def generate_baseline(test_file, reference_file, output_file):
    """Generate baseline metrics for a test case."""
    print(f"\n{'='*60}")
    print(f"Generating baseline for:")
    print(f"  Test: {test_file}")
    print(f"  Reference: {reference_file}")
    print(f"{'='*60}")
    
    # Load graphs
    print("Loading graphs...")
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
    
    # Run old implementation
    print("Running old implementation (rdfeval)...")
    try:
        evaluator = RDFeval(test_graph, reference_graph)
        results = evaluator.createStatistics()
        
        # Serialize and save
        serialized = serialize_results(results)
        
        with open(output_file, 'w') as f:
            json.dump(serialized, f, indent=2)
        
        print(f"✅ Baseline saved to: {output_file}")
        
        # Print summary
        print("\nBaseline Summary:")
        if 'triples' in results:
            print(f"  Triple F1: {results['triples'].get('f1', 0):.4f}")
        if 'subjects' in results:
            print(f"  Subject F1: {results['subjects'].get('f1', 0):.4f}")
        if 'predicates' in results:
            print(f"  Predicate F1: {results['predicates'].get('f1', 0):.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating baseline: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Generate baseline metrics using the old rdfeval implementation."""
    print(f"{Colors.BOLD}🔧 Baseline Generator{Colors.ENDC}")
    print("=" * 60)
    print("Using OLD implementation (rdfeval) to create baselines")
    print("=" * 60)
    
    data_dir = './tests'
    output_dir = './tests/baselines'
    
    # Create baseline directory
    os.makedirs(baseline_dir, exist_ok=True)
    
    # Test cases
    test_cases = [
        {
            'name': 'gold_vs_pred',
            'test': os.path.join(data_dir, 'pred.nt'),
            'reference': os.path.join(data_dir, 'gold.nt'),
            'output': os.path.join(baseline_dir, 'baseline_gold_pred.json')
        },
        {
            'name': 'gold2_vs_pred',
            'test': os.path.join(data_dir, 'pred.nt'),
            'reference': os.path.join(data_dir, 'gold2.nt'),
            'output': os.path.join(baseline_dir, 'baseline_gold2_pred.json')
        }
    ]
    
    # Generate baselines
    success_count = 0
    for test_case in test_cases:
        print(f"\n📋 Test case: {test_case['name']}")
        
        if not os.path.exists(test_case['test']):
            print(f"⚠️  Test file not found: {test_case['test']}")
            continue
        
        if not os.path.exists(test_case['reference']):
            print(f"⚠️  Reference file not found: {test_case['reference']}")
            continue
        
        if generate_baseline(
            test_case['test'],
            test_case['reference'],
            test_case['output']
        ):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Generated {success_count}/{len(test_cases)} baselines")
    print(f"{'='*60}")
    
    if success_count == len(test_cases):
        print("\n🎉 All baselines generated successfully!")
        print("\nNext steps:")
        print("  1. Run: python tests/test_regression.py")
        print("  2. This will compare new implementation against baselines")
    else:
        print("\n⚠️  Some baselines failed to generate")


if __name__ == '__main__':
    main()
