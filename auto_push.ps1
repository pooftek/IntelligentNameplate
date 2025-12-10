# Auto-push script for GitHub
# This script automatically commits all changes and pushes to GitHub

param(
    [string]$Message = "Auto-update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [switch]$SkipCommit = $false
)

Write-Host "[*] Auto-pushing to GitHub..." -ForegroundColor Cyan

# Check if there are any changes
$status = git status --porcelain
if (-not $status -and -not $SkipCommit) {
    Write-Host "[OK] No changes to commit." -ForegroundColor Green
    exit 0
}

# Stage all changes
if (-not $SkipCommit) {
    Write-Host "[*] Staging changes..." -ForegroundColor Yellow
    git add -A
    
    # Commit changes
    Write-Host "[*] Committing changes..." -ForegroundColor Yellow
    git commit -m $Message
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Commit failed!" -ForegroundColor Red
        exit 1
    }
}

# Push to GitHub
Write-Host "[*] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Successfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Push failed! Check your git credentials and network connection." -ForegroundColor Red
    exit 1
}

