"""
Unit tests for Q1. Kth Largest Element in a Stream.

Tests the KthLargest class extracted from the Jupyter notebook.
"""

import pytest

from .conftest import NotebookSolutionLoader


class TestKthLargestElementInAStream:
    """Test suite for the KthLargest stream implementation."""

    @pytest.fixture(scope="class")
    def kth_largest_class(self):
        """Load KthLargest class from notebook."""
        notebook_path = NotebookSolutionLoader.find_notebook(
            "Q1. Kth Largest Element in a Stream.ipynb"
        )
        kth_largest = NotebookSolutionLoader.load_class_from_notebook(
            notebook_path, "KthLargest"
        )
        assert kth_largest is not None, "Failed to load KthLargest class from notebook"
        return kth_largest

    def test_leetcode_example_with_empty_initial_stream(self, kth_largest_class):
        """Validate the required example sequence from the prompt."""
        kth_largest = kth_largest_class(1, [])

        results = [
            kth_largest.add(-3),
            kth_largest.add(-2),
            kth_largest.add(-4),
            kth_largest.add(0),
            kth_largest.add(4),
        ]

        assert results == [-3, -2, -2, 0, 4]

    def test_standard_leetcode_example(self, kth_largest_class):
        """Validate the common LeetCode sample for KthLargest."""
        kth_largest = kth_largest_class(3, [4, 5, 8, 2])

        assert kth_largest.add(3) == 4
        assert kth_largest.add(5) == 5
        assert kth_largest.add(10) == 5
        assert kth_largest.add(9) == 8
        assert kth_largest.add(4) == 8

    def test_values_below_cutoff_do_not_change_result(self, kth_largest_class):
        """Values smaller than the kth largest should leave the result unchanged."""
        kth_largest = kth_largest_class(2, [5, 10])

        assert kth_largest.add(1) == 5
        assert kth_largest.add(4) == 5

    def test_reaches_k_elements_then_updates_cutoff(self, kth_largest_class):
        """Crossing the k-element threshold should establish and then update the cutoff."""
        kth_largest = kth_largest_class(3, [7, 6])

        assert kth_largest.add(5) == 5
        assert kth_largest.add(8) == 6


class TestKthLargestStructure:
    """Basic interface checks for the KthLargest implementation."""

    @pytest.fixture(scope="class")
    def kth_largest_class(self):
        """Load KthLargest class from notebook."""
        notebook_path = NotebookSolutionLoader.find_notebook(
            "Q1. Kth Largest Element in a Stream.ipynb"
        )
        kth_largest = NotebookSolutionLoader.load_class_from_notebook(
            notebook_path, "KthLargest"
        )
        assert kth_largest is not None, "Failed to load KthLargest class from notebook"
        return kth_largest

    def test_class_has_add_method(self, kth_largest_class):
        """Verify the class exposes the required add method."""
        assert hasattr(kth_largest_class, "add")

    def test_add_returns_integer(self, kth_largest_class):
        """Verify add returns the kth-largest value as an integer."""
        kth_largest = kth_largest_class(1, [])
        assert isinstance(kth_largest.add(10), int)