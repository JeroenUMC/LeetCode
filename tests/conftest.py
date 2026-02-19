"""
Pytest configuration for LeetCode solution testing.
Provides utilities for extracting and testing Solution classes from Jupyter notebooks.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Type


class NotebookSolutionLoader:
    """Loads Solution classes from Jupyter notebooks."""
    
    @staticmethod
    def load_solution_from_notebook(notebook_path: str) -> Type:
        """
        Load Solution class from a Jupyter notebook.
        
        Args:
            notebook_path: Path to the .ipynb file
            
        Returns:
            Solution class or None if not found
        """
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            solution_code = []
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if 'class Solution' in source:
                        solution_code.append(source)
            
            if not solution_code:
                return None
            
            # Execute the combined code to get Solution class
            namespace = {}
            exec('\n'.join(solution_code), namespace)
            return namespace.get('Solution')
        
        except Exception as e:
            print(f"Error loading solution from {notebook_path}: {e}")
            return None
    
    @staticmethod
    def find_notebook(notebook_name: str) -> str:
        """Find notebook file by name in current directory."""
        # Search in current directory and parent directories
        for path in Path('.').rglob(notebook_name):
            if path.is_file() and path.suffix == '.ipynb':
                return str(path.absolute())
        
        raise FileNotFoundError(f"Notebook '{notebook_name}' not found")


# Make utilities available to tests
__all__ = ['NotebookSolutionLoader']
