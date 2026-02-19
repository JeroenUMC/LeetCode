"""
Unit tests for 42. Trapping Rain Water (LeetCode)

Tests the Solution class extracted from the Jupyter notebook.
"""

import pytest
from .conftest import NotebookSolutionLoader


class TestTrappingRainWater:
    """Test suite for trapping rain water solution."""
    
    @pytest.fixture(scope="class")
    def solution_class(self):
        """Load Solution class from notebook."""
        notebook_path = NotebookSolutionLoader.find_notebook("42. Trapping Rain Water.ipynb")
        solution = NotebookSolutionLoader.load_solution_from_notebook(notebook_path)
        assert solution is not None, "Failed to load Solution class from notebook"
        return solution
    
    @pytest.fixture
    def solution(self, solution_class):
        """Instantiate a new Solution for each test."""
        return solution_class()
    
    # Test cases from LeetCode problem 42
    def test_basic_example_1(self, solution):
        """Test case 1: [0,1,0,2,1,0,1,3,2,1,2,1]"""
        height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
        assert solution.trap(height) == 6
    
    def test_basic_example_2(self, solution):
        """Test case 2: [4,2,0,3,2,5]"""
        height = [4, 2, 0, 3, 2, 5]
        assert solution.trap(height) == 9
    
    def test_single_element(self, solution):
        """Test with single element - no water can be trapped."""
        assert solution.trap([0]) == 0
        assert solution.trap([5]) == 0
    
    def test_two_elements(self, solution):
        """Test with two elements - no water can be trapped."""
        assert solution.trap([0, 0]) == 0
        assert solution.trap([1, 2]) == 0
        assert solution.trap([2, 1]) == 0
    
    def test_ascending_order(self, solution):
        """Test with ascending heights - no water can be trapped."""
        assert solution.trap([0, 1, 2, 3, 4]) == 0
    
    def test_descending_order(self, solution):
        """Test with descending heights - no water can be trapped."""
        assert solution.trap([4, 3, 2, 1, 0]) == 0
    
    def test_valley_pattern(self, solution):
        """Test simple valley pattern."""
        # Pattern: [1, 0, 1] traps 1 unit
        assert solution.trap([1, 0, 1]) == 1
    
    def test_double_valley(self, solution):
        """Test pattern with two valleys."""
        # Pattern: [2, 0, 2, 0, 2] traps 2 + 2 = 4 units
        assert solution.trap([2, 0, 2, 0, 2]) == 4
    
    def test_large_valley(self, solution):
        """Test valley with multiple bars inside."""
        # Pattern: [3, 0, 0, 0, 3] traps 9 units
        assert solution.trap([3, 0, 0, 0, 3]) == 9
    
    def test_uneven_walls(self, solution):
        """Test valley with uneven walls (water level based on shorter wall)."""
        # Pattern: [2, 0, 3] traps 2 units (limited by left wall height of 2)
        assert solution.trap([2, 0, 3]) == 2
        # Pattern: [3, 0, 2] traps 2 units (limited by right wall height of 2)
        assert solution.trap([3, 0, 2]) == 2
    
    def test_empty_input(self, solution):
        """Test with empty input."""
        assert solution.trap([]) == 0
    
    def test_all_zeros(self, solution):
        """Test with all zero heights."""
        assert solution.trap([0, 0, 0, 0]) == 0
    
    def test_complex_pattern(self, solution):
        """Test complex pattern with multiple valleys and peaks."""
        # [2, 1, 3, 0, 2, 1, 3]
        # Traps: 1 unit at index 1 (between 2 and 3)
        #        3 units at index 3 (between 3s, zero height)
        #        1 unit at index 4 (between 3s)
        #        2 units at index 5 (between 3s)
        # Total: 7 units
        assert solution.trap([2, 1, 3, 0, 2, 1, 3]) == 7
    
    def test_consistent_height_sequence(self, solution):
        """Test with consistent height sequence."""
        # All same height - no water trapped
        assert solution.trap([2, 2, 2, 2]) == 0


# Additional test for ensuring Solution class has expected methods
class TestSolutionStructure:
    """Test the structure and interface of Solution class."""
    
    @pytest.fixture(scope="class")
    def solution_class(self):
        """Load Solution class from notebook."""
        notebook_path = NotebookSolutionLoader.find_notebook("42. Trapping Rain Water.ipynb")
        solution = NotebookSolutionLoader.load_solution_from_notebook(notebook_path)
        assert solution is not None, "Failed to load Solution class from notebook"
        return solution
    
    def test_solution_has_trap_method(self, solution_class):
        """Verify Solution class has trap method."""
        assert hasattr(solution_class, 'trap'), "Solution class must have 'trap' method"
    
    def test_trap_method_callable(self, solution_class):
        """Verify trap method is callable."""
        solution = solution_class()
        assert callable(getattr(solution, 'trap')), "'trap' method must be callable"
    
    def test_trap_accepts_list(self, solution_class):
        """Verify trap method accepts a list parameter."""
        solution = solution_class()
        # Should not raise an exception
        result = solution.trap([])
        assert isinstance(result, int), "trap() should return an integer"
