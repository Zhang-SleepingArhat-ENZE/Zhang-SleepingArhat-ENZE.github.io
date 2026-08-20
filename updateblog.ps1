```powershell
# PowerShell Script for Windows
# Obsidian -> Hugo -> GitHub Pages

# ============================================================
# 1. Set variables
# ============================================================

# Obsidian posts folder
$sourcePath = "E:\HuaweiMoveData\Users\Administrator\Documents\Obsidian Vault\posts"

# Hugo posts folder
$destinationPath = "E:\zeblog\zeblog\content\post"

# GitHub repository
$myrepo = "git@github.com:Zhang-SleepingArhat-ENZE/Zhang-SleepingArhat-ENZE.github.io.git"


# ============================================================
# 2. Error handling
# ============================================================

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest


# ============================================================
# 3. Change to Hugo project directory
# ============================================================

$HugoProjectPath = "E:\zeblog\zeblog"

if (-not (Test-Path $HugoProjectPath)) {
    Write-Error "Hugo project does not exist: $HugoProjectPath"
    exit 1
}

Set-Location $HugoProjectPath

Write-Host ""
Write-Host "============================================"
Write-Host "Hugo project:"
Write-Host $HugoProjectPath
Write-Host "============================================"
Write-Host ""


# ============================================================
# 4. Check required commands
# ============================================================

$requiredCommands = @("git", "hugo")

foreach ($cmd in $requiredCommands) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Error "$cmd is not installed or not in PATH."
        exit 1
    }
}


# Check Python
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $pythonCommand = "python"
}
elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
    $pythonCommand = "python3"
}
else {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}


# ============================================================
# 5. Check paths
# ============================================================

if (-not (Test-Path $sourcePath)) {
    Write-Error "Obsidian source path does not exist:"
    Write-Error $sourcePath
    exit 1
}

if (-not (Test-Path $destinationPath)) {
    Write-Error "Hugo destination path does not exist:"
    Write-Error $destinationPath
    exit 1
}


# ============================================================
# 6. Initialize Git if necessary
# ============================================================

if (-not (Test-Path ".git")) {

    Write-Host "Initializing Git repository..."

    git init

    git remote add origin $myrepo
}
else {

    Write-Host "Git repository already initialized."

    $remotes = git remote

    if (-not ($remotes -contains "origin")) {

        Write-Host "Adding remote origin..."

        git remote add origin $myrepo
    }
    else {

        Write-Host "Checking GitHub remote..."

        $currentRemote = git remote get-url origin

        if ($currentRemote -ne $myrepo) {

            Write-Host "Updating origin remote..."

            git remote set-url origin $myrepo
        }
    }
}


# ============================================================
# 7. Sync Obsidian posts -> Hugo
# ============================================================

Write-Host ""
Write-Host "============================================"
Write-Host "Syncing posts from Obsidian..."
Write-Host "============================================"
Write-Host ""

$robocopyOptions = @(
    "/MIR",
    "/Z",
    "/W:5",
    "/R:3"
)

robocopy $sourcePath $destinationPath @robocopyOptions

if ($LASTEXITCODE -ge 8) {

    Write-Error "Robocopy failed with exit code $LASTEXITCODE"

    exit 1
}

Write-Host "Obsidian posts synchronized successfully."


# ============================================================
# 8. Process image links
# ============================================================

Write-Host ""
Write-Host "============================================"
Write-Host "Processing image links..."
Write-Host "============================================"
Write-Host ""

$imagesScript = Join-Path $PSScriptRoot "images.py"

if (-not (Test-Path $imagesScript)) {

    Write-Error "images.py not found:"
    Write-Error $imagesScript

    exit 1
}

try {

    & $pythonCommand $imagesScript

    if ($LASTEXITCODE -ne 0) {
        throw "images.py returned exit code $LASTEXITCODE"
    }

}
catch {

    Write-Error "Failed to process image links."

    exit 1
}


# ============================================================
# 9. Test Hugo configuration
# ============================================================

Write-Host ""
Write-Host "============================================"
Write-Host "Checking Hugo configuration..."
Write-Host "============================================"
Write-Host ""

try {

    hugo --gc --minify --quiet

}
catch {

    Write-Error "Hugo build failed."

    exit 1
}

Write-Host "Hugo build completed successfully."


# ============================================================
# 10. Check Git changes
# ============================================================

Write-Host ""
Write-Host "============================================"
Write-Host "Checking Git changes..."
Write-Host "============================================"
Write-Host ""

$gitStatus = git status --porcelain

if ([string]::IsNullOrWhiteSpace($gitStatus)) {

    Write-Host "No changes detected."

}
else {

    Write-Host "Changes detected."

    git add .

    $commitMessage = "Update blog on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

    git commit -m $commitMessage
}


# ============================================================
# 11. Push Hugo source to GitHub
# ============================================================

Write-Host ""
Write-Host "============================================"
Write-Host "Deploying to GitHub..."
Write-Host "============================================"
Write-Host ""

try {

    # Detect current branch
    $currentBranch = git branch --show-current

    if ([string]::IsNullOrWhiteSpace($currentBranch)) {

        Write-Host "No current branch detected."

        Write-Host "Creating main branch..."

        git checkout -b main

        $currentBranch = "main"
    }

    Write-Host "Current branch: $currentBranch"

    git push -u origin $currentBranch

}
catch {

    Write-Error "Failed to push to GitHub."

    exit 1
}


# ============================================================
# 12. Finish
# ============================================================

Write-Host ""
Write-Host "============================================"
Write-Host "DEPLOYMENT COMPLETE"
Write-Host "============================================"
Write-Host ""

Write-Host "Your GitHub repository:"
Write-Host "https://github.com/Zhang-SleepingArhat-ENZE/Zhang-SleepingArhat-ENZE.github.io"

Write-Host ""

Write-Host "Your GitHub Pages website:"
Write-Host "https://Zhang-SleepingArhat-ENZE.github.io"

Write-Host ""
Write-Host "Done!"
```
