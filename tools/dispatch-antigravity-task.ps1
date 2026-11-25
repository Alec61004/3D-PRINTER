[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TaskPath,

    [string]$Session = 'pc/3dprinter-antigravity',

    [string]$ReasonNetworkPath = (Join-Path $env:USERPROFILE '.local\bin\reason-network.exe'),

    [string]$CodexSession = 'pc/3dprinter-codex',

    [string]$CodexThreadId,

    [string]$CodexRemoteEndpoint = 'ws://127.0.0.1:8765',

    [switch]$NoNotify,

    [switch]$NoCompletionWatcher
)

$ErrorActionPreference = 'Stop'

$workspacePath = (Get-Location).Path
$codexThreadRegistry = Join-Path $workspacePath 'bridge\coordinator\codex-thread.json'
if (-not $CodexThreadId -and (Test-Path -LiteralPath $codexThreadRegistry)) {
    try {
        $registry = Get-Content -LiteralPath $codexThreadRegistry -Raw | ConvertFrom-Json
        $CodexThreadId = [string]$registry.thread_id
    } catch {
        Write-Warning "Could not read Codex thread registry: $codexThreadRegistry"
    }
}
$resolvedTaskPath = (Resolve-Path -LiteralPath $TaskPath).Path
$taskText = Get-Content -LiteralPath $resolvedTaskPath -Raw

if ($taskText -notmatch '(?m)^owner:\s*antigravity\s*$') {
    throw "Task must have owner: antigravity: $resolvedTaskPath"
}

$statusMatch = [regex]::Match($taskText, '(?m)^status:\s*(\S+)\s*$')
if (-not $statusMatch.Success -or $statusMatch.Groups[1].Value -notin @('pending', 'in_progress')) {
    throw "Task must be pending or in_progress before dispatch: $resolvedTaskPath"
}

$taskIdMatch = [regex]::Match($taskText, '(?m)^task_id:\s*(\S+)\s*$')
$taskId = if ($taskIdMatch.Success) { $taskIdMatch.Groups[1].Value } else { Split-Path $resolvedTaskPath -Leaf }

if (-not (Test-Path -LiteralPath $ReasonNetworkPath)) {
    throw "Reason Network CLI not found: $ReasonNetworkPath"
}

$workspacePrefix = $workspacePath.TrimEnd('\') + '\'
if ($resolvedTaskPath.StartsWith($workspacePrefix, [StringComparison]::OrdinalIgnoreCase)) {
    $relativeTaskPath = $resolvedTaskPath.Substring($workspacePrefix.Length).Replace('\', '/')
} else {
    $relativeTaskPath = $resolvedTaskPath.Replace('\', '/')
}
$message = @"
Wake request for $taskId.

Please process the existing task file now:
$relativeTaskPath

Use the task file as the only source of task instructions. At the next tool/turn boundary, read it, do the work within its owner scope, then write the required result/report and update the task status. Do not reply with a simulated completion; leave the bridge artifacts as evidence.
"@.Trim()

$sendArgs = @('send', '--purpose', 'handoff')
if (-not $NoNotify) {
    $sendArgs += '--notify'
}
$sendArgs += @($Session, $message)
& $ReasonNetworkPath @sendArgs
if ($LASTEXITCODE -ne 0) {
    throw "Reason Network dispatch failed with exit code $LASTEXITCODE"
}

Write-Output "Dispatched $taskId to $Session using $relativeTaskPath"

if (-not $NoCompletionWatcher) {
    $watcherPath = Join-Path $workspacePath 'tools\watch-antigravity-task.ps1'
    if (-not (Test-Path -LiteralPath $watcherPath)) {
        throw "Completion watcher not found: $watcherPath"
    }

    $watcherHost = (Get-Command 'pwsh.exe' -ErrorAction SilentlyContinue).Source
    if (-not $watcherHost) {
        $watcherHost = (Get-Command 'powershell.exe' -ErrorAction SilentlyContinue).Source
    }
    if (-not $watcherHost) {
        throw 'No PowerShell host found for completion watcher.'
    }

    $watcherLogDir = Join-Path $workspacePath 'bridge\logs'
    New-Item -ItemType Directory -Force -Path $watcherLogDir | Out-Null
    $watcherStdout = Join-Path $watcherLogDir ("watcher-{0}.out.log" -f $taskId)
    $watcherStderr = Join-Path $watcherLogDir ("watcher-{0}.err.log" -f $taskId)

    $watcherProcess = Start-Process -FilePath $watcherHost -WorkingDirectory $workspacePath -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput $watcherStdout -RedirectStandardError $watcherStderr -ArgumentList @(
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-File', $watcherPath,
        '-TaskPath', $resolvedTaskPath,
        '-CodexSession', $CodexSession,
        '-CodexThreadId', $CodexThreadId,
        '-CodexRemoteEndpoint', $CodexRemoteEndpoint,
        '-ReasonNetworkPath', $ReasonNetworkPath
    )

    Start-Sleep -Milliseconds 250
    if ($watcherProcess.HasExited) {
        $watcherError = if (Test-Path -LiteralPath $watcherStderr) { Get-Content -LiteralPath $watcherStderr -Raw } else { '' }
        throw "Completion watcher exited immediately (code $($watcherProcess.ExitCode)). Log: $watcherStderr $watcherError"
    }

    Write-Output "Started completion watcher PID $($watcherProcess.Id) for $taskId -> $CodexSession"
    Write-Output "Watcher logs: $watcherStdout / $watcherStderr"
}
