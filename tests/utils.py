"""
Utility functions and fixtures for LeetCode solution testing.
"""

import pytest
from conftest import NotebookSolutionLoader


def create_solution_fixture(notebook_name: str):
    """
    Factory function to create a solution fixture for a specific notebook.
    
    Usage in your test file:
        solution = create_solution_fixture("42. Trapping Rain Water.ipynb")
    
    Args:
        notebook_name: Name of the notebook file
        
    Returns:
        A pytest fixture function
    """
    @pytest.fixture
    def solution():
        notebook_path = NotebookSolutionLoader.find_notebook(notebook_name)
        solution_class = NotebookSolutionLoader.load_solution_from_notebook(notebook_path)
        if solution_class is None:
            raise RuntimeError(f"Failed to load Solution from {notebook_name}")
        return solution_class()
    
    return solution


# Re-export common utilities
__all__ = ['create_solution_fixture', 'NotebookSolutionLoader']
