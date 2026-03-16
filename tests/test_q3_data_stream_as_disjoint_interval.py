"""
Unit tests for Q3. Data Stream as Disjoint Intervals.
Tests get_interval and update_intervals on the SummaryRanges class.
"""

import pytest
from pathlib import Path


def _load_marimo_classes() -> dict:
    """Extract classes from the Marimo notebook .py file by exec-ing cell bodies."""
    file_path = Path(__file__).parent.parent / "Q3 Data Stream as Disjoint Interval.py"
    source = file_path.read_text(encoding="utf-8")
    namespace: dict = {}
    for part in source.split("@app.cell\n")[1:]:
        lines = part.splitlines()
        body_lines = []
        for line in lines[1:]:  # skip `def _(...):` header
            if line and not line.startswith(" "):
                break
            body_lines.append(line[4:] if line.startswith("    ") else "")
        # Only strip cell-level (zero-indent) return statements, not returns
        # inside nested functions or methods.
        code = "\n".join(
            l for l in body_lines
            if not (l.startswith("return ") or l == "return")
        )
        try:
            exec(code, namespace)
        except Exception:
            pass
    return namespace


_ns = _load_marimo_classes()
interval = _ns["interval"]
SummaryRanges = _ns["SummaryRanges"]


# ---------------------------------------------------------------------------
# get_interval
# ---------------------------------------------------------------------------

class TestGetInterval:

    @pytest.fixture
    def sr(self):
        s = SummaryRanges()
        s.intervals = [interval(1, 3), interval(6, 8), interval(10, 10)]
        return s

    def test_empty_intervals_returns_none(self):
        s = SummaryRanges()
        assert s.get_interval(5, from_left=True) is None
        assert s.get_interval(5, from_left=False) is None

    def test_find_by_start(self, sr):
        """from_left=True matches an interval whose start equals the value."""
        assert sr.get_interval(6, from_left=True) == [6, 8]

    def test_find_by_end(self, sr):
        """from_left=False matches an interval whose end equals the value."""
        assert sr.get_interval(3, from_left=False) == [1, 3]

    def test_returns_none_when_not_a_boundary(self, sr):
        """Values inside an interval but not at a boundary should not match."""
        assert sr.get_interval(2, from_left=True) is None
        assert sr.get_interval(7, from_left=False) is None

    def test_returns_none_when_value_absent(self, sr):
        assert sr.get_interval(5, from_left=True) is None
        assert sr.get_interval(5, from_left=False) is None

    def test_single_element_interval_found_by_start(self, sr):
        assert sr.get_interval(10, from_left=True) == [10, 10]

    def test_single_element_interval_found_by_end(self, sr):
        assert sr.get_interval(10, from_left=False) == [10, 10]

    def test_returns_correct_interval_among_many(self, sr):
        """Verify the right interval object is returned, not just any match."""
        result = sr.get_interval(1, from_left=True)
        assert result == [1, 3]
        result = sr.get_interval(8, from_left=False)
        assert result == [6, 8]


# ---------------------------------------------------------------------------
# update_intervals
# ---------------------------------------------------------------------------

class TestUpdateIntervals:

    @pytest.fixture
    def sr(self):
        return SummaryRanges()

    def test_isolated_value_creates_new_interval(self, sr):
        """A value with no adjacent intervals should create [value, value]."""
        sr.update_intervals(5)
        assert [5, 5] in sr.intervals

    def test_extends_interval_to_the_right(self, sr):
        """value == end+1 of an existing interval extends it rightward."""
        sr.intervals = [interval(1, 3)]
        sr.update_intervals(4)
        assert [1, 4] in sr.intervals
        assert len(sr.intervals) == 1

    def test_extends_interval_to_the_left(self, sr):
        """value == start-1 of an existing interval extends it leftward."""
        sr.intervals = [interval(5, 8)]
        sr.update_intervals(4)
        assert [4, 8] in sr.intervals
        assert len(sr.intervals) == 1

    def test_merges_two_adjacent_intervals(self, sr):
        """value bridging [a,b] and [b+2, c] merges them into [a, c]."""
        sr.intervals = [interval(1, 3), interval(5, 8)]
        sr.update_intervals(4)
        assert [1, 8] in sr.intervals
        assert len(sr.intervals) == 1

    def test_non_adjacent_intervals_unchanged(self, sr):
        """Intervals far from the value must not be affected."""
        sr.intervals = [interval(10, 15)]
        sr.update_intervals(5)
        assert [10, 15] in sr.intervals


