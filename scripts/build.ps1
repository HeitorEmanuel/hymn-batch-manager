$ErrorActionPreference = "Stop"
& .\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean packaging\hymn_batch_manager.spec
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Write-Host "Build concluído em dist\HymnBatchManager"
