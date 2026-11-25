[CmdletBinding()]
param(
    [ValidateSet('repair', 'record-audit', 'status')]
    [string]$Action = 'repair',
    [string]$BuildScript = 'reports/build_detailed_industrial_glb.py',
    [string]$InputGlb,
    [string]$ModelPath = 'assets/models/optimized/deltrol_p2s_optimized.glb',
    [string]$WebsiteModelPath = 'website/public/models/deltrol_p2s_optimized.glb',
    [string]$ReferencePath = 'assets/source/printer-hero-reference-2026-11-23.png',
    [string]$ScreenshotPath,
    [ValidateSet('PASS', 'REVISION_REQUIRED', 'PIVOT_REQUIRED')]
    [string]$Verdict,
    [int]$MaxVisualFailures = 3,
    [switch]$SkipWebsiteBuild,
    [switch]$AllowPivot
)

$ErrorActionPreference = 'Stop'
$workspacePath = (Get-Location).Path
$resolvedBuildScript = Join-Path $workspacePath $BuildScript
$resolvedModelPath = Join-Path $workspacePath $ModelPath
$resolvedWebsiteModelPath = Join-Path $workspacePath $WebsiteModelPath
$resolvedReferencePath = Join-Path $workspacePath $ReferencePath
$statePath = Join-Path $workspacePath 'reports\glb-pipeline-state.json'
$manifestPath = Join-Path $workspacePath 'reports\glb-pipeline-latest.json'
$backupRoot = Join-Path $workspacePath 'reports\glb-pipeline\backups'

function Resolve-WorkspacePath([string]$PathValue) {
    if ([IO.Path]::IsPathRooted($PathValue)) { return $PathValue }
    return Join-Path $workspacePath $PathValue
}

function Get-Sha256([string]$PathValue) {
    if (-not (Test-Path -LiteralPath $PathValue)) { return $null }
    return (Get-FileHash -LiteralPath $PathValue -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-JsonState {
    if (Test-Path -LiteralPath $statePath) {
        try { return (Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json) }
        catch { throw "Invalid pipeline state JSON: $statePath" }
    }
    return [pscustomobject]@{
        visualFailureCount = 0
        maxVisualFailures = $MaxVisualFailures
        pivotRequired = $false
        visualVerdict = 'PENDING'
        repairRuns = 0
        history = @()
    }
}

function Save-Json([string]$PathValue, $Value) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $PathValue) | Out-Null
    $Value | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $PathValue -Encoding UTF8
}

function Read-GlbSummary([string]$PathValue) {
    if (-not (Test-Path -LiteralPath $PathValue)) { throw "GLB missing: $PathValue" }
    $bytes = [IO.File]::ReadAllBytes($PathValue)
    if ($bytes.Length -lt 20) { throw "GLB is too small: $PathValue" }
    $magic = [Text.Encoding]::ASCII.GetString($bytes, 0, 4)
    $version = [BitConverter]::ToUInt32($bytes, 4)
    $declaredLength = [BitConverter]::ToUInt32($bytes, 8)
    if ($magic -ne 'glTF' -or $version -ne 2 -or $declaredLength -ne $bytes.Length) {
        throw "Invalid GLB header: $PathValue"
    }

    $offset = 12
    $jsonText = $null
    $binBytes = 0
    while ($offset + 8 -le $bytes.Length) {
        $chunkLength = [BitConverter]::ToUInt32($bytes, $offset)
        $chunkType = [Text.Encoding]::ASCII.GetString($bytes, $offset + 4, 4).Trim([char]0)
        $chunkStart = $offset + 8
        $chunkEnd = $chunkStart + $chunkLength
        if ($chunkEnd -gt $bytes.Length) { throw "GLB chunk exceeds file length: $PathValue" }
        if ($chunkType -eq 'JSON') {
            $jsonText = [Text.Encoding]::UTF8.GetString($bytes, $chunkStart, $chunkLength).TrimEnd([char]0, [char]32)
        } elseif ($chunkType -eq 'BIN') {
            $binBytes = $chunkLength
        }
        $offset = $chunkEnd
    }
    if (-not $jsonText) { throw "GLB JSON chunk missing: $PathValue" }
    $json = $jsonText | ConvertFrom-Json
    $nodeNames = @($json.nodes | ForEach-Object { $_.name } | Where-Object { $_ })
    $requiredNodes = @('enclosure', 'door', 'printHead', 'printBed', 'front_glass_door')
    $missingNodes = @($requiredNodes | Where-Object { $_ -notin $nodeNames })
    if ($missingNodes.Count -gt 0) { throw "GLB missing required nodes: $($missingNodes -join ', ')" }
    if (-not $json.meshes -or -not $json.materials -or -not $json.buffers) { throw "GLB has incomplete scene tables: $PathValue" }
    if ([int]$json.buffers[0].byteLength -gt $binBytes) { throw "GLB buffer exceeds BIN chunk: $PathValue" }

    return [ordered]@{
        path = $PathValue.Substring($workspacePath.Length).TrimStart('\').Replace('\', '/')
        bytes = $bytes.Length
        sha256 = Get-Sha256 $PathValue
        nodeCount = @($json.nodes).Count
        meshCount = @($json.meshes).Count
        materialCount = @($json.materials).Count
        imageCount = @($json.images).Count
        hasRequiredNodes = $true
    }
}

function Invoke-Repair {
    if (-not (Test-Path -LiteralPath $resolvedBuildScript)) { throw "GLB builder missing: $resolvedBuildScript" }
    $state = Get-JsonState
    if ([bool]$state.pivotRequired) {
        if (-not $AllowPivot -or -not $InputGlb) {
            throw "Visual pivot is required after $($state.visualFailureCount) failed audits. Pass -AllowPivot with a new -InputGlb asset; the locked pipeline cannot be repaired."
        }
        $resolvedPivotInput = Resolve-WorkspacePath $InputGlb
        if (-not (Test-Path -LiteralPath $resolvedPivotInput)) { throw "Pivot input GLB missing: $resolvedPivotInput" }
        $previousInput = if ($state.lastRepair) { [string]$state.lastRepair.inputAsset } else { $null }
        $normalizedPivotInput = $InputGlb.Replace('\', '/')
        if ($previousInput -and $normalizedPivotInput -eq $previousInput -and $state.visualVerdict -ne 'PENDING') {
            throw "-AllowPivot requires a different InputGlb than the locked failed asset: $previousInput"
        }
        if ($previousInput -and $normalizedPivotInput -eq $previousInput) {
            Write-Output "Visual pivot already staged: revalidating new asset $normalizedPivotInput"
        } else {
            Write-Output "Visual pivot accepted: integrating new asset $normalizedPivotInput"
        }
        # A new asset/method starts a fresh visual gate. The failed pipeline
        # remains preserved in history and backups, but its strike counter
        # must not lock the replacement pipeline.
        $state.visualFailureCount = 0
        $state.pivotRequired = $false
        $state.visualVerdict = 'PENDING'
    }

    $runId = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backupPath = Join-Path $backupRoot $runId
    New-Item -ItemType Directory -Force -Path $backupPath | Out-Null
    foreach ($path in @($resolvedModelPath, $resolvedWebsiteModelPath)) {
        if (Test-Path -LiteralPath $path) { Copy-Item -LiteralPath $path -Destination (Join-Path $backupPath (Split-Path -Leaf $path)) }
    }

    if ($InputGlb) {
        $resolvedInputGlb = Resolve-WorkspacePath $InputGlb
        if (-not (Test-Path -LiteralPath $resolvedInputGlb)) { throw "Input GLB missing: $resolvedInputGlb" }
        Write-Output "[1/4] Integrating external GLB: $InputGlb"
        $inputSummary = Read-GlbSummary $resolvedInputGlb
        Copy-Item -LiteralPath $resolvedInputGlb -Destination $resolvedModelPath -Force
        Copy-Item -LiteralPath $resolvedInputGlb -Destination $resolvedWebsiteModelPath -Force
    } else {
        Write-Output "[1/4] Regenerating GLB: $BuildScript"
        & python $resolvedBuildScript
        if ($LASTEXITCODE -ne 0) { throw "GLB builder failed with exit code $LASTEXITCODE" }
    }

    Write-Output '[2/4] Validating generated GLB files'
    $sourceSummary = Read-GlbSummary $resolvedModelPath
    $websiteSummary = Read-GlbSummary $resolvedWebsiteModelPath
    if ($sourceSummary.sha256 -ne $websiteSummary.sha256) { throw 'Source and website GLB hashes differ after generation.' }

    if (-not $SkipWebsiteBuild) {
        Write-Output '[3/4] Running website production build'
        Push-Location (Join-Path $workspacePath 'website')
        try {
            & npm run build
            if ($LASTEXITCODE -ne 0) { throw "Website build failed with exit code $LASTEXITCODE" }
        } finally { Pop-Location }
    } else { Write-Output '[3/4] Website build skipped by request' }

    $state.repairRuns = [int]$state.repairRuns + 1
    $state.maxVisualFailures = $MaxVisualFailures
    $state.visualVerdict = 'PENDING'
    $lastRepair = [ordered]@{
        runId = $runId
        timestamp = (Get-Date).ToString('o')
        backupPath = $backupPath.Substring($workspacePath.Length).TrimStart('\').Replace('\', '/')
        source = $sourceSummary
        website = $websiteSummary
        inputAsset = if ($InputGlb) { $InputGlb.Replace('\', '/') } else { $null }
        websiteBuild = (-not $SkipWebsiteBuild)
        visualGate = 'PENDING_SCREENSHOT_AUDIT'
    }
    $state | Add-Member -NotePropertyName lastRepair -NotePropertyValue $lastRepair -Force
    Save-Json $statePath $state
    Save-Json $manifestPath $lastRepair
    Write-Output '[4/4] Pipeline complete; visual audit still required'
    Write-Output "Manifest: $manifestPath"
    Write-Output "State: $statePath"
}

function Invoke-RecordAudit {
    if (-not $Verdict) { throw '-Verdict is required for -Action record-audit.' }
    if (-not $ScreenshotPath) { throw '-ScreenshotPath is required for -Action record-audit.' }
    $resolvedScreenshotPath = Resolve-WorkspacePath $ScreenshotPath
    if (-not (Test-Path -LiteralPath $resolvedScreenshotPath)) { throw "Screenshot missing: $resolvedScreenshotPath" }
    if (-not (Test-Path -LiteralPath $resolvedReferencePath)) { throw "Reference missing: $resolvedReferencePath" }

    $state = Get-JsonState
    $entry = [ordered]@{
        timestamp = (Get-Date).ToString('o')
        verdict = $Verdict
        screenshot = $ScreenshotPath.Replace('\', '/')
        screenshotSha256 = Get-Sha256 $resolvedScreenshotPath
        reference = $ReferencePath.Replace('\', '/')
        referenceSha256 = Get-Sha256 $resolvedReferencePath
    }

    if ($Verdict -eq 'PASS') {
        $state.visualFailureCount = 0
        $state.pivotRequired = $false
        $state.visualVerdict = 'PASS'
    } elseif ($Verdict -eq 'PIVOT_REQUIRED') {
        $state.pivotRequired = $true
        $state.visualVerdict = 'PIVOT_REQUIRED'
    } else {
        $state.visualFailureCount = [int]$state.visualFailureCount + 1
        $state.visualVerdict = 'REVISION_REQUIRED'
        if ([int]$state.visualFailureCount -ge $MaxVisualFailures) {
            $state.pivotRequired = $true
            $state.visualVerdict = 'PIVOT_REQUIRED'
            $entry.pivotReason = "No material visual improvement after $($state.visualFailureCount) failed audits."
        }
    }

    $history = @($state.history)
    $state.history = @($history + [pscustomobject]$entry)
    $state.maxVisualFailures = $MaxVisualFailures
    Save-Json $statePath $state
    Write-Output ($entry | ConvertTo-Json -Depth 8)
    Write-Output "visualFailureCount=$($state.visualFailureCount) pivotRequired=$($state.pivotRequired) verdict=$($state.visualVerdict)"
    if ($state.pivotRequired) { exit 12 }
}

switch ($Action) {
    'repair' { Invoke-Repair }
    'record-audit' { Invoke-RecordAudit }
    'status' {
        if (Test-Path -LiteralPath $statePath) { Get-Content -LiteralPath $statePath -Raw }
        else { Write-Output '{"visualVerdict":"PENDING","visualFailureCount":0,"pivotRequired":false}' }
    }
}
