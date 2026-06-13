#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Installs E++ CLI globally on Windows.
.DESCRIPTION
    Installs the E++ interpreter to user-local directory and adds it to the system PATH.
    If no -Source is provided, downloads from GitHub releases.
.PARAMETER InstallDir
    Optional: Custom install directory. Defaults to "$env:LOCALAPPDATA\epp".
.PARAMETER Source
    Optional: Local path to epp.exe. If provided, installs from local file instead of downloading.
#>

param(
    [string]$InstallDir = "$env:LOCALAPPDATA\epp",
    [string]$Source
)

$ErrorActionPreference = "Stop"

Write-Host "Installing E++ CLI..." -ForegroundColor Cyan

# Determine exe path
if ($Source) {
    $ExePath = $Source
    if (-not (Test-Path -LiteralPath $ExePath)) {
        Write-Host "Source file not found: $ExePath" -ForegroundColor Red
        exit 1
    }
    Write-Host "Installing from local source: $ExePath" -ForegroundColor Gray
} else {
    $Url = "https://github.com/epp-lang/epp-lang/releases/latest/download/epp-windows.exe"
    $TempDir = Join-Path $env:TEMP "epp-install"
    $ExePath = $null
    
    Write-Host "Downloading epp.exe from releases..." -ForegroundColor Gray
    try {
        if (-not (Test-Path -LiteralPath $TempDir)) {
            New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
        }
        $ExePath = Join-Path $TempDir "epp.exe"
        Invoke-WebRequest -Uri $Url -OutFile $ExePath -UseBasicParsing
    } catch {
        Write-Host "Download failed. Using local build..." -ForegroundColor Yellow
        $LocalExe = Join-Path (Get-Location) "dist\epp.exe"
        $BuildExe = Join-Path (Get-Location) "epp.exe"
        if (Test-Path -LiteralPath $LocalExe) {
            $ExePath = $LocalExe
        } elseif (Test-Path -LiteralPath $BuildExe) {
            $ExePath = $BuildExe
        } else {
            Write-Host "No local epp.exe found. Build with: pyinstaller --onefile --name epp epp.py" -ForegroundColor Red
            exit 1
        }
    }
}

# Create install directory
if (-not (Test-Path -LiteralPath $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

# Copy exe
Copy-Item -Path $ExePath -Destination (Join-Path $InstallDir "epp.exe") -Force
Write-Host "Installed to: $InstallDir\epp.exe" -ForegroundColor Green

# Add to PATH (user level)
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$PathEntries = $CurrentPath -split ";" | Where-Object { $_ -and $_.Trim() }
if ($InstallDir -notin $PathEntries) {
    $NewPath = ($PathEntries + $InstallDir) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "Added $InstallDir to user PATH" -ForegroundColor Green
} else {
    Write-Host "$InstallDir already in PATH" -ForegroundColor Yellow
}

# Cleanup temp if we downloaded
if (Test-Path -LiteralPath "$env:TEMP\epp-install") {
    Remove-Item -Path "$env:TEMP\epp-install" -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "`nInstallation complete! Restart your Code Editor (or Terminal) and run 'epp --help' to verify." -ForegroundColor Cyan