#!/usr/bin/env python3
"""
Auto-push script for GitHub
Automatically commits all changes and pushes to GitHub
"""

import subprocess
import sys
from datetime import datetime
import os

def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def main():
    print("🚀 Auto-pushing to GitHub...")
    
    # Check if there are any changes
    success, stdout, stderr = run_command("git status --porcelain", check=False)
    if success and not stdout.strip():
        print("✅ No changes to commit.")
        return 0
    
    # Stage all changes
    print("📦 Staging changes...")
    success, _, _ = run_command("git add -A")
    if not success:
        print("❌ Failed to stage changes!")
        return 1
    
    # Commit changes
    commit_message = f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print("💾 Committing changes...")
    success, _, _ = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print("❌ Commit failed!")
        return 1
    
    # Push to GitHub
    print("⬆️  Pushing to GitHub...")
    success, _, stderr = run_command("git push origin main")
    if success:
        print("✅ Successfully pushed to GitHub!")
        return 0
    else:
        print("❌ Push failed! Check your git credentials and network connection.")
        print(f"Error: {stderr}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

