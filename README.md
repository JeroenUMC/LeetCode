# LeetCode
My LeetCode solutions with comprehensive testing and profiling infrastructure.

## Project Structure

```
├── .devcontainer/          # Dev container configuration
├── .githooks/              # Git pre-commit hooks
├── tests/                  # Unit tests
├── *.ipynb                 # Jupyter notebooks with Solution classes
├── profiler.py             # Performance profiling tool
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Quick Start

### Option 1: Using Dev Container (Recommended)

1. Install VS Code "Dev Containers" extension
2. Open the command palette (Ctrl+Shift+P)
3. Run "Dev Containers: Reopen in Container"
4. Wait for the container to build and install dependencies
5. Start working!

### Option 2: Local Setup with Virtual Environment

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   pytest --version
   python profiler.py
   ```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_42_trapping_rain_water.py -v
```

### Run with coverage report
```bash
pytest --cov=tests
```

### Run a single test
```bash
pytest tests/test_42_trapping_rain_water.py::TestTrappingRainWater::test_basic_example_1 -v
```

## Performance Profiling

### Profile all Solution classes
```bash
python profiler.py
```

### Profile specific notebook
```bash
python profiler.py --notebook "42. Trapping Rain Water.ipynb"
```

### Profile with custom input
```bash
python profiler.py --notebook "42. Trapping Rain Water.ipynb" --input "[100000,0,99999,0]"
```

```bash
python profiler.py --notebook "42. Trapping Rain Water.ipynb" --input-file input.json
```

### Line-by-line profiling
```bash
python profiler.py --notebook "42. Trapping Rain Water.ipynb" --input "[100000,0,99999,0]" --line-profile
```

### Profile with memory tracking
```bash
python profiler.py --memory
```

### Profile notebooks in specific directory
```bash
python profiler.py --dir ./solutions --memory
```

## Setting Up Git Hooks (Optional)

Enable automatic test running before commits:

```bash
git config core.hooksPath .githooks
```

Now when you try to commit, tests will run automatically. If tests fail, the commit is blocked.

## Creating Tests for New Problems

1. Create a Jupyter notebook: `<problem_number>. <problem_name>.ipynb`
   - Add a `Solution` class with the main method

2. Create a test file: `tests/test_<problem_number>_<problem_name>.py`
   ```python
   import pytest
   from .conftest import NotebookSolutionLoader
   
   class TestMyProblem:
       @pytest.fixture(scope="class")
       def solution_class(self):
           notebook_path = NotebookSolutionLoader.find_notebook("<notebook_name>.ipynb")
           solution = NotebookSolutionLoader.load_solution_from_notebook(notebook_path)
           assert solution is not None
           return solution
       
       @pytest.fixture
       def solution(self, solution_class):
           return solution_class()
       
       def test_example(self, solution):
           # Your test here
           assert solution.main_method(input) == expected
   ```

3. Run tests:
   ```bash
   pytest tests/test_<problem_number>_<problem_name>.py -v
   ```

## Dependencies

- `pytest` & `pytest-cov` - Unit testing and coverage reporting
- `jupyter` & `ipykernel` - Jupyter notebook support
- `memory-profiler` & `line-profiler` - Performance profiling
- `psutil` - System resource monitoring
