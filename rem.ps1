# REM Command Launcher for PowerShell
# Unified interface for REM + OpenClaw services

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RemScript = Join-Path $ScriptDir "rem"

# Run Python script with all arguments
& python $RemScript @Arguments

exit $LASTEXITCODE
