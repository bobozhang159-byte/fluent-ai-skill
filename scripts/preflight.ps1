param(
    [string]$AnsysRoot = $env:AWP_ROOT242,
    [string]$AutomationPython = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($AnsysRoot)) {
    throw "Set AWP_ROOT242 or pass -AnsysRoot for the target installation."
}

$paths = [ordered]@{
    workbench = Join-Path $AnsysRoot "Framework\bin\Win64\RunWB2.exe"
    mechanical = Join-Path $AnsysRoot "aisol\bin\winx64\AnsysWBU.exe"
    mapdl = Join-Path $AnsysRoot "ansys\bin\winx64\ANSYS242.exe"
    fluent = Join-Path $AnsysRoot "fluent\ntbin\win64\fluent.exe"
    cfx = Join-Path $AnsysRoot "CFX\bin\cfx5solve.exe"
    spaceclaim = Join-Path $AnsysRoot "scdm\SpaceClaim.exe"
}

if ([string]::IsNullOrWhiteSpace($AutomationPython)) {
    $candidate = Join-Path (Get-Location) ".venv-ansys\Scripts\python.exe"
    if (Test-Path -LiteralPath $candidate) {
        $AutomationPython = $candidate
    }
}

$components = [ordered]@{}
foreach ($entry in $paths.GetEnumerator()) {
    $components[$entry.Key] = [bool](Test-Path -LiteralPath $entry.Value)
}

$licenseServices = Get-Service -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -match "ansys|ansysli|lmgrd" -or $_.DisplayName -match "ANSYS|Ansys"
} | Select-Object Name, DisplayName, Status, StartType

$pyWorkbench = $false
$pyFluent = $false
$pythonVersion = $null
if (-not [string]::IsNullOrWhiteSpace($AutomationPython) -and
    (Test-Path -LiteralPath $AutomationPython)) {
    $pythonVersion = & $AutomationPython -c "import sys; print(sys.version.split()[0])"
    & $AutomationPython -c "import ansys.workbench.core" 2>$null
    $pyWorkbench = ($LASTEXITCODE -eq 0)
    & $AutomationPython -c "import ansys.fluent.core" 2>$null
    $pyFluent = ($LASTEXITCODE -eq 0)
}

[ordered]@{
    status = if (($components.Values -notcontains $false) -and $licenseServices) {
        "installed"
    } else {
        "attention"
    }
    ansys_root_configured = $true
    ansys_version = "242"
    components = $components
    license_endpoint_configured = [bool]$env:ANSYSLMD_LICENSE_FILE
    license_service_observed = [bool]$licenseServices
    license_note = "Service discovery does not prove entitlement; perform a minimal checkout for each required ANSYS module."
    automation_python_configured = [bool]$AutomationPython
    python_version = $pythonVersion
    pyworkbench_importable = $pyWorkbench
    pyfluent_importable = $pyFluent
} | ConvertTo-Json -Depth 6
