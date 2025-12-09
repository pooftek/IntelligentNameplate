# Automatic GitHub Push Setup

This repository includes scripts to automatically push changes to GitHub. You have three options:

## Option 1: Git Post-Commit Hook (Fully Automatic) ⚡

The post-commit hook automatically pushes to GitHub after every commit you make.

**To enable it:**
1. On Windows, you may need to make the hook executable (it should work by default)
2. The hook is already created at `.git/hooks/post-commit`
3. Just commit normally: `git commit -m "your message"`
4. It will automatically push to GitHub!

**To disable it:**
- Delete or rename `.git/hooks/post-commit`

## Option 2: PowerShell Script (Manual Trigger) 🪟

Run the PowerShell script whenever you want to commit and push:

```powershell
# Basic usage (auto-generates commit message)
.\auto_push.ps1

# With custom commit message
.\auto_push.ps1 -Message "Your custom commit message"

# Just push (skip commit if nothing to commit)
.\auto_push.ps1 -SkipCommit
```

## Option 3: Python Script (Cross-Platform) 🐍

Run the Python script:

```bash
python auto_push.py
```

## Option 4: Windows Batch File (Simple) 📝

Double-click or run:

```cmd
auto_push.bat
```

## First Time Setup

If you haven't committed yet, you'll need to make your first commit:

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

After that, the automation will work!

## Notes

- The scripts automatically stage all changes (`git add -A`)
- They commit with a timestamp message if you don't provide one
- They push to the `main` branch on `origin`
- Make sure you have GitHub credentials configured (SSH key or personal access token)

## Troubleshooting

**Push fails with authentication error:**
- Set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Or use a Personal Access Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

**Hook doesn't run automatically:**
- On Windows, ensure Git Bash or WSL is handling the hook
- You can always use the PowerShell or Python scripts instead

