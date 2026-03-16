"""
Pytest configuration for LeetCode solution testing.
Provides utilities for extracting and testing Solution classes from Jupyter notebooks.
"""

import json
from pathlib import Path
from typing import Type


class NotebookSolutionLoader:
    """Loads Solution classes from Jupyter notebooks."""
    
    @staticmethod
    def load_class_from_notebook(notebook_path: str, class_name: str) -> Type:
        """
        Load a class from a Jupyter notebook.
        
        Args:
            notebook_path: Path to the .ipynb file
            class_name: Name of the class to load
            
        Returns:
            Requested class or None if not found
        """
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            class_code = []
            found_class = False
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    class_code.append(source)
                    if f'class {class_name}' in source:
                        found_class = True
                        break
            
            if not found_class:
                return None
            
            # Execute the combined code to get the requested class.
            namespace = {}
            exec('\n'.join(class_code), namespace)
            return namespace.get(class_name)
        
        except Exception as e:
            print(f"Error loading {class_name} from {notebook_path}: {e}")
            return None

    @staticmethod
    def load_solution_from_notebook(notebook_path: str) -> Type:
        """Load Solution class from a Jupyter notebook."""
        return NotebookSolutionLoader.load_class_from_notebook(notebook_path, 'Solution')
    
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
