# Safe Windows 11 + WSL + Docker Disk-Space Audit
# Non-destructive: this script does not prune, delete, unregister, compact, clean, or modify Docker/WSL data.
# Compatible with Windows PowerShell 5.1+ and PowerShell 7+.

$ErrorActionPreference = 'Continue'

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host ("=" * 78)
    Write-Host $Title
    Write-Host ("=" * 78)
}

function Format-Bytes {
    param([double]$Bytes)
    if ($Bytes -ge 1TB) { return ('{0:N2} TB' -f ($Bytes / 1TB)) }
    if ($Bytes -ge 1GB) { return ('{0:N2} GB' -f ($Bytes / 1GB)) }
    if ($Bytes -ge 1MB) { return ('{0:N2} MB' -f ($Bytes / 1MB)) }
    if ($Bytes -ge 1KB) { return ('{0:N2} KB' -f ($Bytes / 1KB)) }
    return ('{0:N0} B' -f $Bytes)
}

function Get-DirectorySize {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }

    $sum = [double]0
    try {
        Get-ChildItem -LiteralPath $Path -Force -File -Recurse -ErrorAction SilentlyContinue |
            ForEach-Object { $sum += $_.Length }
        return [int64]$sum
    }
    catch {
        return [int64]$sum
    }
}

Write-Section "1. WINDOWS FIXED DRIVES"
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" |
    ForEach-Object {
        $used = [double]$_.Size - [double]$_.FreeSpace
        [pscustomobject]@{
            Drive = $_.DeviceID
            Total = Format-Bytes $_.Size
            Used  = Format-Bytes $used
            Free  = Format-Bytes $_.FreeSpace
            UsedPercent = if ($_.Size) { '{0:N1}%' -f (($used / $_.Size) * 100) } else { 'n/a' }
        }
    } | Format-Table -AutoSize

Write-Section "2. WSL DISTRIBUTIONS"
$wslExe = Get-Command wsl.exe -ErrorAction SilentlyContinue
$distros = @()

if (-not $wslExe) {
    Write-Host "WSL is not installed or wsl.exe is not on PATH."
}
else {
    & wsl.exe --list --verbose

    $distros = @(
        & wsl.exe --list --quiet 2>$null |
            ForEach-Object { ($_ -replace "`0",'').Trim() } |
            Where-Object { $_ }
    )
}

Write-Section "3. WSL VHDX FILES ON WINDOWS"
$wslVhds = @{}

if (Test-Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss') {
    Get-ChildItem 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss' |
        ForEach-Object {
            $name = $_.GetValue('DistributionName')
            $base = $_.GetValue('BasePath')
            if ($name -and $base) {
                $vhd = Join-Path $base 'ext4.vhdx'
                $wslVhds[$name] = $vhd

                if (Test-Path -LiteralPath $vhd) {
                    $f = Get-Item -LiteralPath $vhd -ErrorAction SilentlyContinue
                    [pscustomobject]@{
                        Distribution = $name
                        VHDX_Size_On_Windows = Format-Bytes $f.Length
                        VHDX_Bytes = $f.Length
                        Path = $vhd
                    }
                }
                else {
                    [pscustomobject]@{
                        Distribution = $name
                        VHDX_Size_On_Windows = 'not found'
                        VHDX_Bytes = ''
                        Path = $vhd
                    }
                }
            }
        } | Format-Table -AutoSize -Wrap
}
else {
    Write-Host "No WSL Lxss registry key found."
}

Write-Section "4. SPACE USED INSIDE EACH WSL DISTRO"
foreach ($distro in $distros) {
    if ($distro -match '^docker-desktop') {
        Write-Host ""
        Write-Host "[$distro] Docker-managed distro detected; Docker storage is audited separately below."
        continue
    }

    Write-Host ""
    Write-Host "----- $distro -----"

    $dfLine = & wsl.exe -d $distro -- sh -lc "df -B1 -P / 2>/dev/null | tail -n 1" 2>$null
    $dfLine = (($dfLine | Select-Object -Last 1) -replace "`0",'').Trim()

    if ($dfLine) {
        $parts = $dfLine -split '\s+'
        if ($parts.Count -ge 6) {
            $fsSize = [double]$parts[1]
            $fsUsed = [double]$parts[2]
            $fsAvail = [double]$parts[3]

            [pscustomobject]@{
                Distribution = $distro
                Filesystem_Size = Format-Bytes $fsSize
                Filesystem_Used = Format-Bytes $fsUsed
                Filesystem_Available = Format-Bytes $fsAvail
                UsePercent = $parts[4]
                VHDX_Size_On_Windows = if ($wslVhds.ContainsKey($distro) -and (Test-Path -LiteralPath $wslVhds[$distro])) {
                    Format-Bytes (Get-Item -LiteralPath $wslVhds[$distro]).Length
                } else { 'unknown' }
            } | Format-Table -AutoSize
        }
        else {
            Write-Host $dfLine
        }
    }

    Write-Host "Largest top-level directories in /:"
    & wsl.exe -d $distro -u root -- sh -lc "du -x -h -d 1 / 2>/dev/null | sort -hr 2>/dev/null | head -n 20"

    Write-Host ""
    Write-Host "Largest directories under /home (depth 2):"
    & wsl.exe -d $distro -u root -- sh -lc "du -x -h -d 2 /home 2>/dev/null | sort -hr 2>/dev/null | head -n 30"
}

Write-Section "5. DOCKER DESKTOP BACKING DISK(S) ON WINDOWS"
$dockerVhdRoots = @(
    (Join-Path $env:LOCALAPPDATA 'Docker'),
    (Join-Path $env:ProgramData 'DockerDesktop')
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

$dockerVhds = @()
foreach ($root in $dockerVhdRoots) {
    $dockerVhds += Get-ChildItem -LiteralPath $root -Filter '*.vhdx' -File -Recurse -ErrorAction SilentlyContinue
}

if ($dockerVhds.Count -eq 0) {
    Write-Host "No Docker Desktop .vhdx files found in the standard Windows locations."
}
else {
    $dockerVhds |
        Sort-Object Length -Descending |
        ForEach-Object {
            [pscustomobject]@{
                Size = Format-Bytes $_.Length
                Bytes = $_.Length
                Path = $_.FullName
            }
        } | Format-Table -AutoSize -Wrap
}

Write-Section "6. DOCKER ENGINE DISK ACCOUNTING"
$dockerExe = Get-Command docker.exe -ErrorAction SilentlyContinue
if (-not $dockerExe) {
    $dockerExe = Get-Command docker -ErrorAction SilentlyContinue
}

if (-not $dockerExe) {
    Write-Host "Docker CLI was not found on PATH."
}
else {
    & docker version --format 'Client: {{.Client.Version}} | Server: {{.Server.Version}}' 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker CLI exists, but the Docker daemon is not reachable. Start Docker Desktop and rerun this section."
    }
    else {
        Write-Host ""
        Write-Host "Docker summary:"
        & docker system df

        Write-Host ""
        Write-Host "Docker detailed usage (images, containers, volumes, build cache):"
        & docker system df -v

        Write-Host ""
        Write-Host "BuildKit / Buildx cache detail:"
        & docker buildx du 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "docker buildx du was unavailable or the selected builder could not be queried."
        }
    }
}

Write-Section "7. WINDOWS USER-PROFILE STORAGE HOTSPOTS"
Write-Host "These directory figures are diagnostic buckets and may overlap; do NOT add them together."

$profileTargets = @(
    @{ Name = 'Downloads'; Path = (Join-Path $env:USERPROFILE 'Downloads') },
    @{ Name = 'Desktop'; Path = (Join-Path $env:USERPROFILE 'Desktop') },
    @{ Name = 'Documents'; Path = (Join-Path $env:USERPROFILE 'Documents') },
    @{ Name = 'Pictures'; Path = (Join-Path $env:USERPROFILE 'Pictures') },
    @{ Name = 'Videos'; Path = (Join-Path $env:USERPROFILE 'Videos') },
    @{ Name = '.codex'; Path = (Join-Path $env:USERPROFILE '.codex') },
    @{ Name = '.claude'; Path = (Join-Path $env:USERPROFILE '.claude') },
    @{ Name = '.cache'; Path = (Join-Path $env:USERPROFILE '.cache') }
)

$profileResults = foreach ($target in $profileTargets) {
    if (Test-Path -LiteralPath $target.Path) {
        $bytes = Get-DirectorySize $target.Path
        [pscustomobject]@{
            Area = $target.Name
            Size = Format-Bytes $bytes
            Bytes = $bytes
            Path = $target.Path
        }
    }
}

$profileResults | Sort-Object Bytes -Descending | Format-Table -AutoSize -Wrap

Write-Host ""
Write-Host "Largest immediate children of AppData\Local:"
$local = $env:LOCALAPPDATA
if (Test-Path -LiteralPath $local) {
    $localResults = foreach ($dir in Get-ChildItem -LiteralPath $local -Directory -Force -ErrorAction SilentlyContinue) {
        $bytes = Get-DirectorySize $dir.FullName
        [pscustomobject]@{
            Name = $dir.Name
            Size = Format-Bytes $bytes
            Bytes = $bytes
            Path = $dir.FullName
        }
    }
    $localResults | Sort-Object Bytes -Descending | Select-Object -First 25 | Format-Table -AutoSize -Wrap
}

Write-Section "8. LARGEST INDIVIDUAL FILES IN THE USER PROFILE"
Write-Host "Top 30 files. Permission-denied paths are skipped."
Get-ChildItem -LiteralPath $env:USERPROFILE -File -Recurse -Force -ErrorAction SilentlyContinue |
    Sort-Object Length -Descending |
    Select-Object -First 30 |
    ForEach-Object {
        [pscustomobject]@{
            Size = Format-Bytes $_.Length
            Bytes = $_.Length
            Path = $_.FullName
        }
    } | Format-Table -AutoSize -Wrap

Write-Section "AUDIT COMPLETE"
Write-Host "No prune/delete/unregister/compact/cleanup commands were run."
Write-Host ""
Write-Host "For Windows' system-managed categories (Installed apps, System & reserved,"
Write-Host "Temporary files, Other), also open: Settings > System > Storage."
Write-Host "That view is preferable to recursively summing C:\Windows because Windows uses"
Write-Host "hard links and other storage mechanisms that can make naive directory totals misleading."
