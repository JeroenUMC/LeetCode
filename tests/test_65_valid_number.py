"""
Unit tests for 65. Valid Number (LeetCode)

Tests the Solution class extracted from the Jupyter notebook.
Validates numbers using a state machine (DFA) approach.
"""

import pytest
from .conftest import NotebookSolutionLoader


class TestValidNumber:
    """Test suite for valid number validation solution."""
    
    @pytest.fixture(scope="class")
    def solution_class(self):
        """Load Solution class from notebook."""
        notebook_path = NotebookSolutionLoader.find_notebook("65. Vald Number.ipynb")
        solution = NotebookSolutionLoader.load_solution_from_notebook(notebook_path)
        assert solution is not None, "Failed to load Solution class from notebook"
        return solution
    
    @pytest.fixture
    def solution(self, solution_class):
        """Instantiate a new Solution for each test."""
        return solution_class()
    
    # ===== BASIC VALID NUMBERS =====
    def test_single_digit(self, solution):
        """Test single digit numbers."""
        assert solution.isNumber("0") is True
        assert solution.isNumber("5") is True
        assert solution.isNumber("9") is True
    
    def test_multiple_digits(self, solution):
        """Test multi-digit integers."""
        assert solution.isNumber("123") is True
        assert solution.isNumber("0123") is True
        assert solution.isNumber("999") is True
    
    def test_signed_integers(self, solution):
        """Test integers with optional sign."""
        assert solution.isNumber("+123") is True
        assert solution.isNumber("-456") is True
        assert solution.isNumber("+0") is True
        assert solution.isNumber("-9") is True
    
    def test_decimal_numbers(self, solution):
        """Test decimal point numbers."""
        assert solution.isNumber("3.14") is True
        assert solution.isNumber(".5") is True
        assert solution.isNumber("5.") is True
        assert solution.isNumber(".0") is True
    
    def test_signed_decimals(self, solution):
        """Test decimals with optional sign."""
        assert solution.isNumber("+3.14") is True
        assert solution.isNumber("-0.5") is True
        assert solution.isNumber("+.5") is True
        assert solution.isNumber("-5.") is True
    
    def test_scientific_notation(self, solution):
        """Test scientific notation (exponent form)."""
        assert solution.isNumber("1e2") is True
        assert solution.isNumber("1E2") is True
        assert solution.isNumber("1e-2") is True
        assert solution.isNumber("1E+2") is True
        assert solution.isNumber("5e10") is True
    
    def test_scientific_with_decimal(self, solution):
        """Test scientific notation with decimal point."""
        assert solution.isNumber("1.2e3") is True
        assert solution.isNumber("3.14e-2") is True
        assert solution.isNumber(".5e2") is True
        assert solution.isNumber("5.e3") is True
        assert solution.isNumber("1.2e+3") is True
    
    def test_signed_scientific_notation(self, solution):
        """Test signed scientific notation."""
        assert solution.isNumber("+1e2") is True
        assert solution.isNumber("-1E-5") is True
        assert solution.isNumber("+3.14E+2") is True
        assert solution.isNumber("-0.5e-10") is True
    
    # ===== INVALID NUMBERS =====
    def test_empty_string(self, solution):
        """Test empty string is invalid."""
        assert solution.isNumber("") is False
    
    def test_only_sign(self, solution):
        """Test that sign alone is invalid (Rule 1: must have digit or dot)."""
        assert solution.isNumber("+") is False
        assert solution.isNumber("-") is False
    
    def test_only_dot(self, solution):
        """Test that dot alone is invalid (Rule 5: must have digit)."""
        assert solution.isNumber(".") is False
    
    def test_only_exp(self, solution):
        """Test that exponent marker alone is invalid (Rule 1)."""
        assert solution.isNumber("e") is False
        assert solution.isNumber("E") is False
    
    def test_exp_without_number(self, solution):
        """Test exponent without preceding number (violates Rule 5)."""
        assert solution.isNumber("e5") is False
        assert solution.isNumber("E10") is False
        assert solution.isNumber(".e2") is False
    
    def test_exp_without_exponent_digits(self, solution):
        """Test exponent without following digits (violates end condition)."""
        assert solution.isNumber("1e") is False
        assert solution.isNumber("1E") is False
        assert solution.isNumber("1.2e") is False
        assert solution.isNumber("1e+") is False
        assert solution.isNumber("1e-") is False
    
    def test_multiple_dots(self, solution):
        """Test multiple decimal points (violates Rule 4)."""
        assert solution.isNumber("1.2.3") is False
        assert solution.isNumber(".1.2") is False
        assert solution.isNumber("1.2.") is False
    
    def test_dot_after_exp(self, solution):
        """Test decimal point after exponent (invalid transition)."""
        assert solution.isNumber("1e2.5") is False
        assert solution.isNumber("1.2e.5") is False
    
    def test_multiple_exponents(self, solution):
        """Test multiple exponent markers (violates Rule 3)."""
        assert solution.isNumber("1e2e3") is False
        assert solution.isNumber("1E2E3") is False
        assert solution.isNumber("1e2e+3") is False
    
    def test_multiple_signs(self, solution):
        """Test multiple signs (invalid)."""
        assert solution.isNumber("++1") is False
        assert solution.isNumber("--1") is False
        assert solution.isNumber("+-1") is False
        assert solution.isNumber("1+2") is False
    
    def test_sign_in_middle(self, solution):
        """Test sign not at start (invalid position)."""
        assert solution.isNumber("1+2") is False
        assert solution.isNumber("1-2") is False
        assert solution.isNumber("1.+2") is False
        assert solution.isNumber("1e+2e") is False
    
    def test_invalid_characters(self, solution):
        """Test strings with invalid characters."""
        assert solution.isNumber("1a2") is False
        assert solution.isNumber("1 2") is False
        assert solution.isNumber("1.2.3a") is False
        assert solution.isNumber("abc") is False
    
    def test_trailing_characters(self, solution):
        """Test invalid characters at the end."""
        assert solution.isNumber("123a") is False
        assert solution.isNumber("1.2 ") is False
        assert solution.isNumber("1e2x") is False
    
    # ===== EDGE CASES =====
    def test_zero_variants(self, solution):
        """Test various representations of zero."""
        assert solution.isNumber("0") is True
        assert solution.isNumber("+0") is True
        assert solution.isNumber("-0") is True
        assert solution.isNumber("0.0") is True
        assert solution.isNumber(".0") is True
        assert solution.isNumber("0.") is True
        assert solution.isNumber("0e0") is True
        assert solution.isNumber("0E+0") is True
    
    def test_leading_zeros(self, solution):
        """Test numbers with leading zeros."""
        assert solution.isNumber("00123") is True
        assert solution.isNumber("0.0.0") is False  # Multiple dots
        assert solution.isNumber("00.00") is True
    
    def test_very_large_exponent(self, solution):
        """Test large exponent values (valid as long as format correct)."""
        assert solution.isNumber("1e100") is True
        assert solution.isNumber("1e999") is True
        assert solution.isNumber("1E-999") is True
    
    def test_negative_exponent(self, solution):
        """Test valid negative exponents."""
        assert solution.isNumber("1e-1") is True
        assert solution.isNumber("1e-100") is True
        assert solution.isNumber("0.5e-5") is True
    
    def test_positive_exponent_explicit(self, solution):
        """Test explicitly positive exponents with + sign."""
        assert solution.isNumber("1e+1") is True
        assert solution.isNumber("1E+100") is True
        assert solution.isNumber("2.5e+3") is True
    
    def test_leetcode_examples(self, solution):
        """Test examples from LeetCode problem 65."""
        # Valid examples
        assert solution.isNumber("0") is True
        assert solution.isNumber("e") is False
        assert solution.isNumber(".") is False
        assert solution.isNumber(".8") is True
        assert solution.isNumber("2e10") is True
        assert solution.isNumber(" 0.1 ") is False  # No whitespace handling
        assert solution.isNumber("2e-9") is True
        assert solution.isNumber("2e-9873") is True
