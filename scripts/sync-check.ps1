param(
    [int]$SinceDays = 7,
    [int]$MaxResults = 50
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $scriptDir = if ($PSScriptRoot) {
        $PSScriptRoot
    } elseif ($PSCommandPath) {
        Split-Path -Parent $PSCommandPath
    } else {
        throw "Unable to resolve script directory."
    }
    $root = git -C $scriptDir rev-parse --show-toplevel 2>$null
    if (-not $root) {
        throw "Unable to resolve repo root from $scriptDir"
    }
    return $root.Trim()
}

function Get-WorktreeRecords {
    param(
        [string]$RepoRoot
    )

    $records = @()
    $current = [ordered]@{}
    foreach ($line in git -C $RepoRoot worktree list --porcelain) {
        if (-not $line.Trim()) {
            if ($current.path) {
                $records += [pscustomobject]@{
                    Path   = $current.path
                    Branch = $current.branch
                    Head   = $current.HEAD
                }
            }
            $current = [ordered]@{}
            continue
        }

        $parts = $line -split " ", 2
        $key = $parts[0]
        $value = if ($parts.Count -gt 1) { $parts[1].Trim() } else { "" }
        $current[$key] = $value
    }

    if ($current.path) {
        $records += [pscustomobject]@{
            Path   = $current.path
            Branch = $current.branch
            Head   = $current.HEAD
        }
    }

    return $records
}

function Get-FileFingerprint {
    param(
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }

    $item = Get-Item -LiteralPath $Path
    $hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    return [pscustomobject]@{
        Length        = $item.Length
        LastWriteTime = $item.LastWriteTime
        Hash          = $hash
    }
}

function Get-RecentRawInputFiles {
    param(
        [string]$RawRoot,
        [datetime]$Cutoff
    )

    if (-not (Test-Path -LiteralPath $RawRoot -PathType Container)) {
        return @()
    }

    return Get-ChildItem -LiteralPath $RawRoot -Recurse -File |
        Where-Object { $_.LastWriteTime -ge $Cutoff } |
        Sort-Object FullName
}

function Get-BranchSyncState {
    param(
        [string]$RepoRoot
    )

    $state = [ordered]@{
        Summary    = ""
        Ahead      = 0
        Behind     = 0
        HasUpstream = $false
    }

    $branchName = (git -C $RepoRoot branch --show-current 2>$null).Trim()
    if (-not $branchName) {
        return [pscustomobject]$state
    }

    $upstream = (git -C $RepoRoot rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>$null).Trim()
    if (-not $upstream) {
        $state.Summary = "## $branchName"
        return [pscustomobject]$state
    }

    $state.HasUpstream = $true
    $counts = (git -C $RepoRoot rev-list --left-right --count "$upstream...HEAD" 2>$null).Trim()
    if ($counts -match "^(\d+)\s+(\d+)$") {
        $state.Behind = [int]$Matches[1]
        $state.Ahead = [int]$Matches[2]
    }

    $state.Summary = "## $branchName...$upstream"
    return [pscustomobject]$state
}

$repoRoot = Get-RepoRoot
$canonicalRawRoot = Join-Path $repoRoot "codex\2026\raw-input"
$cutoff = (Get-Date).AddDays(-1 * $SinceDays)
$worktrees = Get-WorktreeRecords -RepoRoot $repoRoot
$branchSync = Get-BranchSyncState -RepoRoot $repoRoot

Write-Host "sync-check: canonical repo = $repoRoot"
Write-Host "sync-check: looking for raw-input drift since $($cutoff.ToString("yyyy-MM-dd HH:mm"))"
Write-Host ""

$currentBranch = (git -C $repoRoot branch --show-current).Trim()
if ($currentBranch -ne "main") {
    Write-Warning "Current checkout branch is '$currentBranch'. Raw-input publishing is safest from 'main'."
    Write-Host ""
}

$syncWarnings = @()
if (-not $branchSync.HasUpstream) {
    $syncWarnings += "Current branch has no upstream tracking branch."
} elseif ($branchSync.Ahead -gt 0 -and $branchSync.Behind -gt 0) {
    $syncWarnings += "Canonical checkout has diverged from origin/main (ahead $($branchSync.Ahead), behind $($branchSync.Behind))."
} elseif ($branchSync.Ahead -gt 0) {
    $syncWarnings += "Canonical checkout is ahead of origin/main by $($branchSync.Ahead) commit(s)."
} elseif ($branchSync.Behind -gt 0) {
    $syncWarnings += "Canonical checkout is behind origin/main by $($branchSync.Behind) commit(s)."
} else {
    Write-Host "sync-check: branch sync = main aligned with origin/main"
}

if ($syncWarnings.Count -gt 0) {
    Write-Warning "Branch sync status:"
    $syncWarnings | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
}

$mainStatus = git -C $repoRoot status --short -- "codex/2026/raw-input"
if ($mainStatus) {
    Write-Warning "Canonical checkout has pending raw-input changes:"
    $mainStatus | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
}

$driftRows = @()
foreach ($wt in $worktrees) {
    $wtPath = $wt.Path
    if (-not $wtPath) {
        continue
    }

    $resolvedWt = [System.IO.Path]::GetFullPath($wtPath)
    $resolvedRepo = [System.IO.Path]::GetFullPath($repoRoot)
    if ($resolvedWt -eq $resolvedRepo) {
        continue
    }

    $rawRoot = Join-Path $resolvedWt "codex\2026\raw-input"
    $recentFiles = Get-RecentRawInputFiles -RawRoot $rawRoot -Cutoff $cutoff
    foreach ($file in $recentFiles) {
        $relative = $file.FullName.Substring($rawRoot.Length + 1)
        $canonicalPath = Join-Path $canonicalRawRoot $relative
        $sourceFp = Get-FileFingerprint -Path $file.FullName
        $canonicalFp = Get-FileFingerprint -Path $canonicalPath

        if (-not $canonicalFp) {
            $status = "missing"
        } elseif ($canonicalFp.Hash -ne $sourceFp.Hash) {
            $status = "different"
        } else {
            continue
        }

        $driftRows += [pscustomobject]@{
            Status        = $status
            Branch        = if ($wt.Branch) { $wt.Branch -replace "^refs/heads/", "" } else { "(detached)" }
            Worktree      = $resolvedWt
            RelativePath  = $relative
            LastWriteTime = $file.LastWriteTime
        }
    }
}

$ordered = $driftRows |
    Sort-Object `
        @{ Expression = "LastWriteTime"; Descending = $true }, `
        @{ Expression = "Branch"; Descending = $false }, `
        @{ Expression = "RelativePath"; Descending = $false }

$hasBranchProblem = $syncWarnings.Count -gt 0
$hasRawInputChanges = [bool]$mainStatus
$hasDrift = $ordered.Count -gt 0

if ($hasDrift) {
    Write-Warning ("Found {0} recent raw-input file(s) in other worktrees that are missing or different in this checkout." -f $ordered.Count)
    Write-Host ""
    Write-Host "Suggested next step:"
    Write-Host "  Copy the listed files into $canonicalRawRoot, then commit/push from this checkout."
    Write-Host ""

    $ordered |
        Select-Object -First $MaxResults Status, Branch, LastWriteTime, RelativePath, Worktree |
        Format-Table -AutoSize

    if ($ordered.Count -gt $MaxResults) {
        Write-Host ""
        Write-Host ("... {0} more omitted; rerun with -MaxResults {1} to see more." -f ($ordered.Count - $MaxResults), $ordered.Count)
    }
    Write-Host ""
}

if (-not $hasDrift) {
    Write-Host "sync-check: raw-input drift = none"
}

if (-not $hasRawInputChanges) {
    Write-Host "sync-check: canonical raw-input worktree = clean"
}

Write-Host ""
if (-not $hasBranchProblem -and -not $hasRawInputChanges -and -not $hasDrift) {
    Write-Host "OK: raw-input continuity is clean."
    exit 0
}

Write-Warning "Continuity attention needed before or after push."
exit 1
