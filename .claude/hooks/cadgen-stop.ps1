# SessionEnd hook: close the CAD Viewer when the session really ends
# (archived or exited). A /clear also ends a session but work goes on, so
# the viewer is kept then.

$ErrorActionPreference = 'Continue'

$Root = Join-Path $env:USERPROFILE '.nsas-cadgen'
$Cadgen = Join-Path $Root 'venv\Scripts\cadgen.exe'

$reason = ''
try { $reason = ([Console]::In.ReadToEnd() | ConvertFrom-Json).reason } catch {}

if ($reason -ne 'clear' -and (Test-Path $Cadgen)) {
    & $Cadgen viewer stop --port 3245 *>> (Join-Path $Root 'setup.log')
}
