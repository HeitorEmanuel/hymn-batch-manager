$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath ".venv")) {
    py -m venv .venv
}
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Write-Host "Ambiente pronto. Execute .\scripts\run.ps1"

