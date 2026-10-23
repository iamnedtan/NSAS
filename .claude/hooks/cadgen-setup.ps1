# SessionStart hook: make cadgen ready and keep the CAD Viewer running.
#
# Keeps a venv with the pinned cadgen in the user profile (not LOCALAPPDATA:
# the Claude desktop app is packaged, so its LOCALAPPDATA writes are
# redirected), installs or updates cadgen when the version differs, removes
# stray viewers and leftover session daemons, then starts the CAD Viewer on
# port 3245 or reuses the one already running. The viewer is left open
# between sessions; cadgen-stop.ps1 closes it when a session is archived.
# Prints one JSON line: hook context for Claude.

$ErrorActionPreference = 'Continue'

$CadgenVersion = '0.7.25'
$Port = 3245
$Root = Join-Path $env:USERPROFILE '.nsas-cadgen'
$Venv = Join-Path $Root 'venv'
$Python = Join-Path $Venv 'Scripts\python.exe'
$Cadgen = Join-Path $Venv 'Scripts\cadgen.exe'
$Log = Join-Path $Root 'setup.log'
$NodeDir = 'C:\Program Files\nodejs'

function Out-Context([string]$text) {
    @{
        hookSpecificOutput = @{
            hookEventName = 'SessionStart'
            additionalContext = $text
        }
    } | ConvertTo-Json -Compress -Depth 4
}

# Stray: a viewer not from our venv or not on our port, or a cadgen daemon
# left behind by a session scratch venv under Temp. Only process-tree roots
# are killed; taskkill /T takes their children with them.
function Stop-StrayCadgen {
    $procs = @(Get-CimInstance Win32_Process |
        Where-Object { $_.CommandLine -match '-m cadgen\.(viewer|daemon)\b' })
    $ids = $procs | ForEach-Object { $_.ProcessId }
    $stopped = 0
    foreach ($p in $procs) {
        if ($ids -contains $p.ParentProcessId) { continue }
        $cmd = $p.CommandLine
        $ours = $cmd -like "$Python *"
        $stray = $false
        if ($cmd -match 'cadgen\.viewer') {
            $otherPort = ($cmd -match '--new') -or
                ($cmd -match '--port\s+(\d+)' -and $Matches[1] -ne "$Port")
            $stray = (-not $ours) -or $otherPort
        } elseif ($cmd -match '\\Temp\\') {
            $stray = $true
        }
        if ($stray) {
            & taskkill /PID $p.ProcessId /T /F *>> $Log
            $stopped++
        }
    }
    $stopped
}

try {
    New-Item -ItemType Directory -Force $Root | Out-Null
    if (Test-Path $NodeDir) { $env:Path = "$NodeDir;$env:Path" }

    if (-not (Test-Path $Python)) {
        & py -3 -m venv $Venv *>> $Log
        if (-not (Test-Path $Python)) { throw "venv creation failed (see $Log)" }
    }

    $have = & $Python -c "import importlib.metadata as m; print(m.version('cadgen'))" 2>$null
    if ($have -ne $CadgenVersion) {
        & $Python -m pip install -q --disable-pip-version-check "cadgen==$CadgenVersion" *>> $Log
        if ($LASTEXITCODE -ne 0) { throw "cadgen install failed (see $Log)" }
    }

    $stray = Stop-StrayCadgen

    # Start from outside the repo: the viewer locks its start folder.
    # A running viewer on the port is reused, not restarted.
    Set-Location $Root
    $viewer = & $Cadgen viewer --detach --port $Port 2>&1 | Out-String
    $url = if ($viewer -match 'CAD Viewer URL: (\S+)') { $Matches[1] } else { "http://127.0.0.1:$Port/" }

    Out-Context (
        "cadgen $CadgenVersion is ready. Python: $Python (run model scripts with " +
        "it, e.g. `"$Python`" -I model.py, with Node on PATH: $NodeDir). CLI: $Cadgen. " +
        "CAD Viewer is running at $url (stray cadgen processes stopped: $stray); open a model " +
        "in the browser pane with ${url}?file=<absolute path to .step/.stl>. " +
        "Do not stop the viewer: it stays open across sessions and is closed only " +
        "when a session is archived. It starts in $Root, so it locks no repo folder. " +
        "If cadgen's STL export fails with NodeUnavailable, export the STL with " +
        "build123d's export_stl instead."
    )
} catch {
    Out-Context "cadgen setup failed: $($_.Exception.Message). Log: $Log"
}
