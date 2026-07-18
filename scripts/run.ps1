$ErrorActionPreference = "Stop"
$env:HBM_DEVELOPMENT = "1"
& .\.venv\Scripts\python.exe -m app.main

