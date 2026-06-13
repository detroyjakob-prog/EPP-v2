#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Uninstalls E++ CLI from Windows.
.DESCRIPTION
    Removes E++ from PATH and deletes the installation directory.
#>

$InstallDir = "$env:LOCALAPPDATA\epp"

Write-Host "Uninstalling E++ CLI..." -ForegroundColor Cyan

# Remove from PATH
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$NewPath = ($CurrentPath -split ";" | Where-Object { $_ -and $_ -ne $InstallDir }) -join ";"
[Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
Write-Host "Removed $InstallDir from user PATH" -ForegroundColor Green

# Delete install directory
if (Test-Path -LiteralPath $InstallDir) {
    Remove-Item -Path $InstallDir -Recurse -Force
    Write-Host "Deleted $InstallDir" -ForegroundColor Green
} else {
    Write-Host "$InstallDir not found" -ForegroundColor Yellow
}

Write-Host "`nUninstall complete! Restart your terminal." -ForegroundColor Cyan