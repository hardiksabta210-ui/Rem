param(
    [string]$ProjectPath = "C:\Users\hardi\Chat bot\Rem_project"
)

# Navigate to project folder
Set-Location -Path $ProjectPath -ErrorAction Stop
Write-Host "Working directory: $(Get-Location)"

# Clone OpenClaw
Write-Host "Cloning OpenClaw repository..."
git clone https://github.com/openclaw/openclaw.git

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] OpenClaw cloned successfully"
    Write-Host "OpenClaw path: $(Join-Path $ProjectPath 'openclaw')"
    
    # List contents
    if (Test-Path "openclaw") {
        Write-Host "`nOpenClaw directory contents:"
        Get-ChildItem -Path "openclaw" -Force | Select-Object Name, Mode | Format-Table
    }
} else {
    Write-Host "`n[ERROR] Failed to clone OpenClaw (exit code: $LASTEXITCODE)"
}
