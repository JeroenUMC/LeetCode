#!/usr/bin/env python
"""
Performance profiler for LeetCode solutions.
Profiles all Solution classes found in Jupyter notebooks.
"""

import json
import argparse
import time
import psutil
import os
from pathlib import Path
from typing import Dict, List, Any

try:
    from line_profiler import LineProfiler
except ImportError:  # Optional dependency for line-by-line profiling
    LineProfiler = None


class NotebookSolutionExtractor:
    """Extracts Solution classes from Jupyter notebooks."""

    def __init__(self, notebook_path: str):
        self.notebook_path = notebook_path
        self.solution_code = None
        self._extract_solution()

    def _extract_solution(self):
        """Extract Solution class code from notebook."""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            solutions = []
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if 'class Solution' in source:
                        solutions.append(source)
            
            if solutions:
                self.solution_code = '\n'.join(solutions)
        except Exception as e:
            print(f"Error reading notebook {self.notebook_path}: {e}")

    def get_solution_class(self):
        """Execute and return Solution class."""
        if not self.solution_code:
            return None
        
        namespace = {}
        try:
            exec(self.solution_code, namespace)
            return namespace.get('Solution')
        except Exception as e:
            print(f"Error executing Solution code: {e}")
            return None


class SolutionProfiler:
    """Profiles Solution class performance."""

    def __init__(self, solution_class, notebook_name: str):
        self.solution_class = solution_class
        self.notebook_name = notebook_name
        self.results = {}

    def _get_main_method(self) -> str:
        """Identify the main method to profile."""
        # For most LeetCode problems, look for 'trap' method specifically
        # Then fall back to first non-__init__ method
        if hasattr(self.solution_class, 'trap'):
            return 'trap'
        
        # Get methods defined in Solution class (not inherited)
        methods = [m for m in self.solution_class.__dict__.keys()
                  if not m.startswith('_') and callable(getattr(self.solution_class, m))]
        return methods[0] if methods else None

    def _invoke_method(self, method, test_input: Any):
        if isinstance(test_input, dict):
            return method(**test_input)
        return method(test_input)

    def profile_solution(self, test_input: Any, line_profile: bool = False):
        """Profile a solution with given test input."""
        instance = self.solution_class()
        main_method = self._get_main_method()
        
        if not main_method:
            print(f"  No public methods found in {self.notebook_name}")
            return None

        method = getattr(instance, main_method)
        
        # Get process for memory tracking
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Time the execution
        start_time = time.perf_counter()
        try:
            line_stats = None
            if line_profile and LineProfiler is not None:
                line_profiler = LineProfiler()
                line_profiler.add_function(method)
                line_profiler.enable_by_count()
                result = self._invoke_method(method, test_input)
                line_profiler.disable_by_count()
                line_stats = line_profiler
            else:
                result = self._invoke_method(method, test_input)
            end_time = time.perf_counter()
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            
            return {
                'method': main_method,
                'execution_time_ms': (end_time - start_time) * 1000,
                'memory_before_mb': mem_before,
                'memory_after_mb': mem_after,
                'memory_used_mb': mem_after - mem_before,
                'result': result,
                'line_stats': line_stats,
                'success': True
            }
        except Exception as e:
            return {
                'method': main_method,
                'error': str(e),
                'success': False
            }


def find_notebooks(directory: str = '.') -> List[str]:
    """Find all Jupyter notebooks in directory."""
    path = Path(directory)
    return list(path.glob('*.ipynb'))


def get_test_input_for_notebook(notebook_name: str) -> Any:
    """Get test input for specific notebook."""
    test_cases = {
        '42. Trapping Rain Water': [2, 0, 2],  # Example: 2 units trapped
        '1. Two Sum': {
            'nums': [2, 7, 11, 15],
            'target': 9
        }
    }
    
    name = Path(notebook_name).stem
    return test_cases.get(name, None)


def load_input_from_file(file_path: str) -> Any:
    """Load JSON input from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_input_arg(input_arg: str) -> Any:
    """Parse JSON input from CLI argument."""
    if input_arg is None:
        return None
    try:
        return json.loads(input_arg)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON for --input: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Profile LeetCode solution classes'
    )
    parser.add_argument(
        '--notebook',
        type=str,
        help='Specific notebook to profile'
    )
    parser.add_argument(
        '--memory',
        action='store_true',
        help='Show detailed memory statistics'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='JSON input to pass to the Solution method'
    )
    parser.add_argument(
        '--input-file',
        type=str,
        help='Path to a JSON file containing input data'
    )
    parser.add_argument(
        '--line-profile',
        action='store_true',
        help='Enable line-by-line profiling (requires line_profiler)'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='.',
        help='Directory to search for notebooks'
    )
    
    args = parser.parse_args()
    
    # Find notebooks
    if args.notebook:
        notebooks = [Path(args.notebook)]
    else:
        notebooks = find_notebooks(args.dir)
    
    if not notebooks:
        print("No notebooks found.")
        return
    
    print(f"\n{'='*70}")
    print(f"LeetCode Solution Performance Profiler")
    print(f"{'='*70}\n")
    
    total_results = []
    
    for notebook_path in notebooks:
        print(f"Processing: {notebook_path.name}")
        print(f"{'-'*70}")
        
        # Extract and load solution
        extractor = NotebookSolutionExtractor(str(notebook_path))
        solution_class = extractor.get_solution_class()
        
        if not solution_class:
            print(f"  ⚠ No Solution class found\n")
            continue
        
        # Get test input
        if args.input_file:
            test_input = load_input_from_file(args.input_file)
        else:
            test_input = parse_input_arg(args.input)
        if test_input is None:
            test_input = get_test_input_for_notebook(str(notebook_path.name))
        
        if test_input is None:
            print(f"  ⚠ No test case available for this notebook\n")
            continue
        
        # Profile the solution
        profiler = SolutionProfiler(solution_class, notebook_path.name)
        if args.line_profile and LineProfiler is None:
            print("  ⚠ line_profiler not installed; run `pip install line_profiler`")
        result = profiler.profile_solution(test_input, line_profile=args.line_profile)
        
        if result and result.get('success'):
            print(f"  Method: {result['method']}")
            print(f"  Execution Time: {result['execution_time_ms']:.4f} ms")
            print(f"  Result: {result['result']}")
            
            if args.memory:
                print(f"  Memory Before: {result['memory_before_mb']:.2f} MB")
                print(f"  Memory After: {result['memory_after_mb']:.2f} MB")
                print(f"  Memory Used: {result['memory_used_mb']:.2f} MB")

            if args.line_profile and result.get('line_stats') is not None:
                print("\n  Line-by-line profile:")
                result['line_stats'].print_stats()
            
            total_results.append(result)
        else:
            if result:
                print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print(f"  ❌ Failed to profile")
        
        print()
    
    # Summary
    if total_results:
        print(f"{'='*70}")
        print(f"Summary ({len(total_results)} solutions profiled)")
        print(f"{'='*70}")
        
        avg_time = sum(r['execution_time_ms'] for r in total_results) / len(total_results)
        print(f"Average Execution Time: {avg_time:.4f} ms")
        
        if args.memory:
            avg_memory = sum(r['memory_used_mb'] for r in total_results) / len(total_results)
            print(f"Average Memory Used: {avg_memory:.2f} MB")


if __name__ == '__main__':
    main()
