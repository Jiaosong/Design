[CmdletBinding()]
param(
    [switch]$Apply,
    [string]$CoSPluginsPath = "$env:APPDATA\chat-on-steroids\state\plugins.json",
    [string]$RegistryPath = "D:\Desgin\.mcp-runtime\registry\OLEANDER_INTEGRATION_REGISTRY_CURRENT.json",
    [int]$WsPort = 19999
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Package = '@jiujiang/jishi-mcp-server'
$Version = '1.2.0'
$PluginName = 'JiShi Design MCP'
$RegistryId = 'jishi_design_mcp'
$Timestamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')

function Read-JsonFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { throw "Missing JSON file: $Path" }
    $raw = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($raw)) { throw "Empty JSON file: $Path" }
    return ($raw | ConvertFrom-Json)
}

function Write-JsonFile([string]$Path, $Value) {
    $json = $Value | ConvertTo-Json -Depth 32
    [IO.File]::WriteAllText($Path, $json + [Environment]::NewLine, (New-Object Text.UTF8Encoding($false)))
}

function Backup-File([string]$Path) {
    $backup = "$Path.backup.$Timestamp"
    Copy-Item -LiteralPath $Path -Destination $backup -Force
    return $backup
}

function Get-PropValue($Object, [string]$Name) {
    if ($null -eq $Object) { return $null }
    $p = $Object.PSObject.Properties[$Name]
    if ($null -eq $p) { return $null }
    return $p.Value
}

function Merge-Object($Existing, $Desired) {
    if ($null -eq $Existing) { return $Desired }
    foreach ($p in $Desired.PSObject.Properties) {
        $current = $Existing.PSObject.Properties[$p.Name]
        if ($null -eq $current) {
            $Existing | Add-Member -NotePropertyName $p.Name -NotePropertyValue $p.Value
        } elseif (($p.Value -is [pscustomobject]) -and ($current.Value -is [pscustomobject])) {
            $current.Value = Merge-Object $current.Value $p.Value
        } else {
            $current.Value = $p.Value
        }
    }
    return $Existing
}

function Upsert-ArrayEntry([object[]]$Items, [scriptblock]$Match, $Desired) {
    $list = @($Items)
    $found = $false
    for ($i = 0; $i -lt $list.Count; $i++) {
        if (& $Match $list[$i]) {
            $list[$i] = Merge-Object $list[$i] $Desired
            $found = $true
            break
        }
    }
    if (-not $found) { $list += $Desired }
    return ,$list
}

function Update-CoSPlugins($Root, $Desired) {
    $match = {
        param($x)
        ((Get-PropValue $x 'name') -eq $PluginName) -or ((Get-PropValue $x 'package') -eq $Package)
    }

    if ($Root -is [System.Array]) {
        return (Upsert-ArrayEntry @($Root) $match $Desired)
    }

    if ($null -ne $Root.PSObject.Properties['plugins']) {
        $Root.plugins = Upsert-ArrayEntry @($Root.plugins) $match $Desired
        return $Root
    }

    throw 'Unsupported Chat On Steroids plugins.json shape: expected root array or root.plugins array. No write performed.'
}

function Update-RuntimeRegistry($Root, $Desired) {
    $candidateNames = @(
        'integrations', 'entries', 'runtimes', 'deployments', 'registry',
        'servers', 'mcp_servers', 'mcpServers', 'tools'
    )
    $match = {
        param($x)
        ((Get-PropValue $x 'id') -eq $RegistryId) -or ((Get-PropValue $x 'name') -eq $PluginName)
    }

    foreach ($name in $candidateNames) {
        $prop = $Root.PSObject.Properties[$name]
        if (($null -ne $prop) -and (($prop.Value -is [System.Array]) -or ($null -eq $prop.Value))) {
            $prop.Value = Upsert-ArrayEntry @($prop.Value) $match $Desired
            return $Root
        }
    }

    if ($Root -is [System.Array]) {
        return (Upsert-ArrayEntry @($Root) $match $Desired)
    }

    throw 'Unsupported OLEANDER runtime registry shape: no recognized execution-entry array found. No write performed.'
}

$npx = Get-Command npx -ErrorAction SilentlyContinue
$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $npx -or $null -eq $node) { throw 'Node.js 18+ / npx is required.' }
$nodeVersion = (& node --version).Trim().TrimStart('v')
$nodeMajor = [int]($nodeVersion.Split('.')[0])
if ($nodeMajor -lt 18) { throw "Node.js 18+ required; found $nodeVersion" }

$desiredPlugin = [pscustomobject][ordered]@{
    name = $PluginName
    package = $Package
    version = $Version
    enabled = $true
    status = 'ready'
    source = [pscustomobject][ordered]@{ kind = 'command' }
    launch = [pscustomobject][ordered]@{
        command = 'npx'
        args = @('-y', "$Package@$Version")
        env = [pscustomobject][ordered]@{ JISHI_MCP_WSS_PORT = "$WsPort" }
    }
}

$desiredRegistry = [pscustomobject][ordered]@{
    id = $RegistryId
    name = $PluginName
    command = 'npx'
    args = @('-y', "$Package@$Version")
    cwd = $null
    env = [pscustomobject][ordered]@{ JISHI_MCP_WSS_PORT = "$WsPort" }
    status = 'STAGED'
    capabilities = @(
        'READ_CANVAS',
        'READ_SELECTION',
        'EXPORT_PNG_JPG_SVG_PDF',
        'MULTI_CLIENT_ADDRESSING',
        'EXECUTE_SCRIPT_GATED'
    )
    authority = 'EXECUTION_CAPABILITY_ONLY'
    gates = [pscustomobject][ordered]@{
        read = 'ALLOW_AFTER_TARGET_RESOLUTION'
        export = 'OLEANDER_OUTPUT_CONTRACT'
        write_canvas = 'OLEANDER_RESOLVER_REQUIRED'
        execute_script = 'EXPLICIT_SIDE_EFFECT_GATE_REQUIRED'
    }
    registered_at = (Get-Date).ToUniversalTime().ToString('o')
    health = [pscustomobject][ordered]@{
        state = 'UNVERIFIED'
        websocket = "ws://127.0.0.1:$WsPort"
        plugin_required = '九匠即时MCP'
    }
    notes = 'Machine-local transport/health evidence only. Does not create Project/Source/Design/Knowledge Authority, promotion state, or a second control plane.'
}

$pluginsBefore = Read-JsonFile $CoSPluginsPath
$registryBefore = Read-JsonFile $RegistryPath
$pluginsAfter = Update-CoSPlugins $pluginsBefore $desiredPlugin
$registryAfter = Update-RuntimeRegistry $registryBefore $desiredRegistry

$summary = [pscustomobject][ordered]@{
    mode = $(if ($Apply) { 'APPLY' } else { 'DRY_RUN' })
    node = $nodeVersion
    package = "$Package@$Version"
    cos_plugins = $CoSPluginsPath
    runtime_registry = $RegistryPath
    websocket = "127.0.0.1:$WsPort"
    restart_cos = $false
    authority_ceiling = 'EXECUTION_CAPABILITY_ONLY'
    runtime_state = 'STAGED_UNVERIFIED'
}

$summary | ConvertTo-Json -Depth 8

if (-not $Apply) {
    Write-Host 'DRY-RUN only. No files changed. Re-run with -Apply after review.'
    exit 0
}

$pluginsBackup = Backup-File $CoSPluginsPath
$registryBackup = Backup-File $RegistryPath
try {
    Write-JsonFile $CoSPluginsPath $pluginsAfter
    Write-JsonFile $RegistryPath $registryAfter
} catch {
    Copy-Item -LiteralPath $pluginsBackup -Destination $CoSPluginsPath -Force
    Copy-Item -LiteralPath $registryBackup -Destination $RegistryPath -Force
    throw
}

Write-Host "Applied. Backups:`n  $pluginsBackup`n  $registryBackup"
Write-Host 'No Chat On Steroids restart was requested or performed.'
Write-Host 'Next runtime proof: open 九匠即时MCP inside JiShi Design, confirm green connected state, then probe list_plugin_clients/get_page_nodes before any write action.'
