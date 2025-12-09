@echo off
REM Auto-push script for GitHub (Windows Batch)
REM Automatically commits all changes and pushes to GitHub

echo 🚀 Auto-pushing to GitHub...

REM Check if there are any changes
git status --porcelain >nul 2>&1
if %errorlevel% neq 0 (
    echo ✅ No changes to commit.
    exit /b 0
)

REM Stage all changes
echo 📦 Staging changes...
git add -A
if %errorlevel% neq 0 (
    echo ❌ Failed to stage changes!
    exit /b 1
)

REM Commit changes
echo 💾 Committing changes...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do set mytime=%%a:%%b
set commit_msg=Auto-update: %mydate% %mytime%
git commit -m "%commit_msg%"
if %errorlevel% neq 0 (
    echo ❌ Commit failed!
    exit /b 1
)

REM Push to GitHub
echo ⬆️  Pushing to GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo ✅ Successfully pushed to GitHub!
    exit /b 0
) else (
    echo ❌ Push failed! Check your git credentials and network connection.
    exit /b 1
)

