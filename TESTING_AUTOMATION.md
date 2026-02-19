# Automated Testing System

This project includes automated testing that runs whenever code changes are made.

## Components

### 1. **run_tests_auto.py** - Automated Test Runner
- Supports **smart test selection** - only runs tests for changed files
- Logs results with timestamps to `test_log.txt`
- Returns exit code (0 = pass, non-zero = fail)

**Usage:**
```bash
# Run all tests (default - used by git hooks)
python run_tests_auto.py

# Smart mode: only run tests for specific changed files
python run_tests_auto.py --files "42. Trapping Rain Water.ipynb"

# Run tests for multiple changed files
python run_tests_auto.py --files "42. Trapping Rain Water.ipynb" "tests/test_42_trapping_rain_water.py"
```

### 2. **Git Pre-Commit Hook** - Prevents Bad Commits
- Located at `.githooks/pre-commit`
- Automatically runs tests before each commit
- Blocks commits if tests fail
- Logs all test results

**The hook is already configured** via `git config core.hooksPath .githooks`

### 3. **test_log.txt** - Test History Log
- Contains timestamped test results
- Appends after each test run
- Excluded from git via `.gitignore`
- Useful for tracking test history

## How It Works

### When GitHub Copilot Changes Code
When Copilot makes changes to your code:
1. Copilot modifies files (e.g., notebook, test files)
2. Copilot runs `python run_tests_auto.py --files <changed-files>`
3. **Smart mode activates** - only relevant tests run
4. Results logged with file tracking
5. Fast feedback on specific changes

### Automatic Testing on Commits
When you run `git commit`, the pre-commit hook:
1. Runs `run_tests_auto.py` (default mode = all tests)
2. **All tests run** for comprehensive validation
3. Logs results to `test_log.txt`
4. If tests pass ✅ - commit proceeds
5. If tests fail ❌ - commit is blocked

### Manual Testing
Run tests manually anytime:
```bash
# All tests (comprehensive)
python run_tests_auto.py

# Smart mode (specific files)
python run_tests_auto.py --files "42. Trapping Rain Water.ipynb"
```

### Copilot-Assisted Development
When GitHub Copilot makes code changes:
1. Copilot modifies the code (e.g., edits a notebook)
2. Copilot runs `python run_tests_auto.py --files <changed-files>`
3. **Smart test selection** - only relevant tests run
4. Test results are logged with file tracking
5. You can review the log file to see test history

## Smart Test Selection

The test runner automatically maps changed files to their tests:

**Notebook → Test Mapping:**
- `42. Trapping Rain Water.ipynb` → `tests/test_42_trapping_rain_water.py`
- Pattern: `{number}. {name}.ipynb` → `tests/test_{number}_{snake_case_name}.py`

**Benefits:**
- ⚡ **Faster feedback** - only run relevant tests after edits
- 🎯 **Targeted testing** - see exactly which tests relate to your changes
- 📊 **Better logging** - tracks which files triggered which tests

## Test Log Format

Each entry in `test_log.txt` includes:
- Timestamp
- **Mode** (all or smart)
- **Changed files** (in smart mode)
- **Test files run** (in smart mode)
- Exit code
- Full pytest output (stdout/stderr)
- Separators for readability

**Example (Smart Mode):**
```
================================================================================
Test Run: 2026-02-19 16:16:03
Mode: smart (1 test file(s))
Changed Files: 42. Trapping Rain Water.ipynb
Test Files: tests/test_42_trapping_rain_water.py
Exit Code: 0
================================================================================
STDOUT:
============================= test session starts ==============================
...
```

**Example (All Tests Mode):**
```
================================================================================
Test Run: 2026-02-19 16:16:20
Mode: all
Exit Code: 0
================================================================================
STDOUT:
============================= test session starts ==============================
...
```

## Test Failure Notifications 🔔

**NEW:** Automatic notifications when tests fail!

When tests fail, the system now:
1. **Creates `TEST_FAILURES.md`** - A visible file in your workspace root with:
   - Summary of failed/passed tests
   - List of changed files that triggered the failure
   - Quick links and commands to fix the issue
   - Excerpt of failure details
2. **Prints a prominent alert** in the terminal
3. **Auto-deletes** the notification file when tests pass again

**Why this helps:**
- 🚨 **No more silent failures** - You'll immediately know when your changes break tests
- 📄 **Visible indicator** - The `TEST_FAILURES.md` file appears in your file explorer
- 🔍 **Quick diagnosis** - Key failure info right in the notification file
- ✅ **Auto-cleanup** - File disappears once you fix the issues

**Example TEST_FAILURES.md:**
```markdown
# ⚠️ TEST FAILURES DETECTED ⚠️

**Timestamp:** 2026-02-19 16:28:42

## Summary
- ❌ **7 test(s) FAILED**
- ✅ 10 test(s) passed

## Changed Files
- `42. Trapping Rain Water.ipynb`

## Quick Actions
1. Check the detailed output in `test_log.txt`
2. Review your recent changes
3. Run tests manually to verify fixes
```

## Benefits

✅ **Smart test selection** - Copilot runs only relevant tests for fast feedback  
✅ **Test failure notifications** - Never miss a test failure with visible alerts  
✅ **Comprehensive validation** - All tests run on commits for safety  
✅ **Comprehensive validation** - All tests run on commits for safety  
✅ **History tracking** - All test results logged with timestamps and file tracking  
✅ **Git safety** - Pre-commit hook prevents committing broken code  
✅ **Manual override** - You can still commit with `--no-verify` if needed  
✅ **Scalable** - As you add more LeetCode problems, tests remain fast  
✅ **CI/CD ready** - Easy to integrate into continuous integration pipelines

## Disabling the Pre-Commit Hook (Not Recommended)

If you need to commit without running tests:
```bash
git commit --no-verify -m "your message"
```

Or temporarily disable hooks:
```bash
git config core.hooksPath ""
```

To re-enable:
```bash
git config core.hooksPath .githooks
```
