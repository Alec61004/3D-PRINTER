[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TaskPath,

    [string]$CodexSession = 'pc/3dprinter-codex',

    [string]$CodexThreadId,

    [string]$CodexRemoteEndpoint = 'ws://127.0.0.1:8765',

    [string]$CodexCliPath = 'codex',

    [string]$ReasonNetworkPath = (Join-Path $env:USERPROFILE '.local\bin\reason-network.exe'),

    [int]$PollSeconds = 5,

    [int]$MaxHours = 12

    ,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$workspacePath = (Get-Location).Path
$resolvedTaskPath = (Resolve-Path -LiteralPath $TaskPath).Path
$codexThreadRegistry = Join-Path $workspacePath 'bridge\coordinator\codex-thread.json'
if (-not $CodexThreadId -and (Test-Path -LiteralPath $codexThreadRegistry)) {
    try {
        $registry = Get-Content -LiteralPath $codexThreadRegistry -Raw | ConvertFrom-Json
        $CodexThreadId = [string]$registry.thread_id
    } catch {
        Write-Warning "Could not read Codex thread registry: $codexThreadRegistry"
    }
}
$taskText = Get-Content -LiteralPath $resolvedTaskPath -Raw
$taskIdMatch = [regex]::Match($taskText, '(?m)^task_id:\s*(\S+)\s*$')
$taskId = if ($taskIdMatch.Success) { $taskIdMatch.Groups[1].Value } else { Split-Path $resolvedTaskPath -Leaf }
$deadline = [DateTime]::UtcNow.AddHours($MaxHours)

function Get-TaskField([string]$Text, [string]$Field) {
    $match = [regex]::Match($Text, "(?m)^${Field}:\s*(.+?)\s*$")
    if ($match.Success) { return $match.Groups[1].Value.Trim() }
    return $null
}

function Ensure-CodexRemoteServer {
    $healthUrl = $CodexRemoteEndpoint -replace '^ws://', 'http://'
    $healthUrl = "$healthUrl/readyz"
    try {
        Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2 | Out-Null
        return $true
    } catch {
        try {
            Start-Process -FilePath $CodexCliPath -WorkingDirectory $workspacePath -WindowStyle Hidden -ArgumentList @(
                'app-server', '--listen', $CodexRemoteEndpoint
            ) | Out-Null
        } catch {
            Write-Warning "Could not start Codex app-server: $($_.Exception.Message)"
            return $false
        }
    }

    for ($attempt = 0; $attempt -lt 12; $attempt++) {
        Start-Sleep -Milliseconds 500
        try {
            Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2 | Out-Null
            return $true
        } catch { }
    }
    Write-Warning "Codex app-server did not become ready at $CodexRemoteEndpoint"
    return $false
}

function Resume-CodexThread([string]$Message) {
    if (-not $CodexThreadId) {
        Write-Warning 'Codex thread id is not configured; skipping automatic queue/resume.'
        return $false
    }
    if (-not (Ensure-CodexRemoteServer)) { return $false }

    & $CodexCliPath queue --remote $CodexRemoteEndpoint --thread $CodexThreadId --message $Message --resume
    if ($LASTEXITCODE -eq 0) {
        Write-Output "Queued and resumed Codex thread $CodexThreadId"
        return $true
    }
    Write-Warning "Codex queue/resume returned exit code $LASTEXITCODE"
    return $false
}

while ([DateTime]::UtcNow -lt $deadline) {
    $taskText = Get-Content -LiteralPath $resolvedTaskPath -Raw
    $status = Get-TaskField $taskText 'status'
    $resultPath = Get-TaskField $taskText 'result_path'

    if ($status -in @('completed', 'blocked', 'cancelled')) {
        $relativeResult = ($resultPath -replace '^[''\"]|[''\"]$','') -replace '/', '\'
        $resultFile = if ($relativeResult) { Join-Path $workspacePath $relativeResult } else { $null }
        $responseFile = Join-Path $workspacePath ("bridge\outbox\{0}-antigravity-response.md" -f $taskId)

        if ($resultFile -and (Test-Path -LiteralPath $resultFile) -and (Test-Path -LiteralPath $responseFile)) {
            $message = @"
Antigravity task terminal notification.
task_id: $taskId
status: $status
report: $relativeResult
response: bridge/outbox/$taskId-antigravity-response.md
Codex must read and audit the files before accepting the result.
"@.Trim()

            if ($DryRun) {
                Write-Output $message
            } else {
                $resumeMessage = @"
Antigravity task terminal event: $taskId ($status).
Read the task report and outbox response now, audit the artifact, then continue the project loop. Do not trust the verdict without reading the files.
Report: $relativeResult
Response: bridge/outbox/$taskId-antigravity-response.md
"@.Trim()
                $codexQueued = Resume-CodexThread $resumeMessage
                if (-not $codexQueued) {
                    Write-Warning "Direct Codex queue was not confirmed for $taskId; trying Reason Network fallback."
                    & $ReasonNetworkPath send --purpose status --notify $CodexSession $message
                    if ($LASTEXITCODE -ne 0) {
                        Write-Warning "Reason Network fallback failed for $taskId with exit code $LASTEXITCODE"
                    }
                } else {
                    Write-Output "Direct Codex queue accepted $taskId; Reason Network fallback is not required."
                }
            }
            exit 0
        }
    }

    Start-Sleep -Seconds $PollSeconds
}

Write-Error "Watcher timed out after $MaxHours hours for $taskId"
exit 2
