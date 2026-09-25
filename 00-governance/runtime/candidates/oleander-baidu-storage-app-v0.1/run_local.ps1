$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

if (-not $env:BAIDU_NETDISK_ACCESS_TOKEN -and -not $env:BAIDU_NETDISK_ACCESS_TOKEN_FILE) {
    Write-Warning "BAIDU_NETDISK_ACCESS_TOKEN is not set. The app will start with local status tools only."
}

py -3.13 -m app.server
