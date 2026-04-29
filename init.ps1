# init.ps1 — One-shot setup for the noetic-proposals repo.
#
# Run from PowerShell in the repo root:
#   .\init.ps1
#
# What it does:
#   1. Cleans up any sandbox/agent leftovers (.git half-created, .claude/ stub).
#   2. Downloads brand assets from noetic.io into _assets/ (requires Python 3).
#   3. Installs the skill into your Cowork plugins folder.
#   4. Initializes git, makes the first commit on `main`.
#   5. Prints next steps (gh repo create, GitHub Pages config).

$ErrorActionPreference = 'Stop'

Write-Host "`n=== noetic-proposals init ===`n" -ForegroundColor Cyan

# --- 1. Clean sandbox leftovers ---------------------------------------------
$cleanup = @('.git', '.claude')
foreach ($path in $cleanup) {
    if (Test-Path $path) {
        Write-Host "Cleaning leftover $path ..." -ForegroundColor Yellow
        # Force remove read-only attrs first
        Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue |
            ForEach-Object { $_.Attributes = 'Normal' }
        Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
        if (Test-Path $path) {
            Write-Warning "Could not remove $path automatically. Delete it manually and re-run."
        }
    }
}

# --- 2. Download assets -----------------------------------------------------
Write-Host "`nDownloading brand assets from noetic.io ..." -ForegroundColor Cyan
$python = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if ($null -eq $python) {
    Write-Warning "Python not found on PATH. Skipping asset download."
    Write-Warning "Install Python 3 and run: python _assets\download-assets.py"
} else {
    & $python.Source "_assets\download-assets.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Asset download had failures. You can rerun later: python _assets\download-assets.py"
    }
}

# --- 3. Install skill into Cowork plugins folder ----------------------------
Write-Host "`nInstalling skill into Cowork plugins folder ..." -ForegroundColor Cyan
$skillSrc = Join-Path $PSScriptRoot "_skill\SKILL.md"
$pluginsRoot = Join-Path $env:APPDATA "Claude\local-agent-mode-sessions\skills-plugin"
if (-not (Test-Path $pluginsRoot)) {
    Write-Warning "Cowork plugins folder not found at: $pluginsRoot"
    Write-Warning "Skipping skill install. The skill is still available in this repo at _skill/SKILL.md."
} else {
    # Find the most-recently-modified skills/ directory under any session id
    $skillsDir = Get-ChildItem -Path $pluginsRoot -Directory -Recurse -Filter 'skills' -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '\\skills$' } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($null -eq $skillsDir) {
        Write-Warning "Couldn't locate a skills/ directory under $pluginsRoot"
        Write-Warning "Manually copy _skill\SKILL.md to <plugins>\skills\noetic-proposal-generator\SKILL.md"
    } else {
        $skillDest = Join-Path $skillsDir.FullName "noetic-proposal-generator"
        New-Item -ItemType Directory -Path $skillDest -Force | Out-Null
        Copy-Item $skillSrc -Destination (Join-Path $skillDest "SKILL.md") -Force
        Write-Host "  installed -> $skillDest\SKILL.md" -ForegroundColor Green
    }
}

# --- 4. Git init ------------------------------------------------------------
Write-Host "`nInitializing git repository ..." -ForegroundColor Cyan
git init -b main | Out-Null
git add .
git commit -m "Initial commit: noetic-proposals scaffold + skill + sample" | Out-Null

Write-Host "`n=== Done ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Create the GitHub repo and push:"
Write-Host "       gh repo create noetic-proposals --private --source=. --remote=origin --push"
Write-Host "     OR (manual):"
Write-Host "       git remote add origin git@github.com:<your-org>/noetic-proposals.git"
Write-Host "       git push -u origin main"
Write-Host ""
Write-Host "  2. Enable GitHub Pages:"
Write-Host "       Settings -> Pages -> Source: main / root"
Write-Host ""
Write-Host "  3. Preview locally:"
Write-Host "       python -m http.server 8000  # then visit http://localhost:8000/"
Write-Host ""
Write-Host "  4. Generate your first proposal in Cowork by saying:"
Write-Host '       "Make a Noetic proposal for <client> — slides, scroll-snap"' -ForegroundColor White
Write-Host ""
