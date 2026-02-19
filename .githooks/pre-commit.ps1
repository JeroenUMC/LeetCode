# Pre-commit hook for Windows PowerShell: Run all tests before commit

Write-Host "Running unit tests before commit..." -ForegroundColor Cyan
& ".\.venv\Scripts\pytest.exe" tests/ --tb=short

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Tests failed! Commit aborted." -ForegroundColor Red
    Write-Host "Fix the failing tests and try again."
    exit 1
}

Write-Host ""
Write-Host "✅ All tests passed!" -ForegroundColor Green
exit 0
