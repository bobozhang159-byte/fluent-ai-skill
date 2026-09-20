# Workbench-first geometry transfer

Use this procedure when the user wants a visible Workbench project and the geometry is created with SpaceClaim scripting. The route was verified on one Workbench 24.2 installation; recheck release-specific behavior on the target installation.

## Ownership and paths

1. Make Workbench the visible project owner before doing model work. Assign one automation controller to that session.
2. Create a fresh run folder using ASCII characters only. Store the `.scdoc`, `.wbpj`, logs, and stage evidence there. One Fluent 2024 R2 test failed to read a mesh addressed through a Chinese-character path, while a short ASCII path worked; verify this on the target installation.
3. Keep the source geometry script and all generated files separate from existing projects. Do not overwrite the previously solved CFD case.

## Create and verify the SpaceClaim surface

For a simple 2D axisymmetric straight pipe, the fluid section is a rectangle in the XY plane: axial length along +X and radius along +Y. The verified example uses 2000 mm by 10 mm. Generate a closed four-line loop, switch to Solid mode, then inspect bodies before calling `Fill`:

```python
# Replace this placeholder with a path inside the new run directory.
SCDOC_PATH = r"<RUN_DIR>\pipe-surface.scdoc"
ClearAll()
ViewHelper.SetSketchPlane(Plane.PlaneXY, None)
p0 = Point2D.Create(MM(0), MM(0))
p1 = Point2D.Create(MM(2000), MM(0))
p2 = Point2D.Create(MM(2000), MM(10))
p3 = Point2D.Create(MM(0), MM(10))
SketchLine.Create(p0, p1)
SketchLine.Create(p1, p2)
SketchLine.Create(p2, p3)
SketchLine.Create(p3, p0)
ViewHelper.SetViewMode(InteractionMode.Solid)

bodies = GetRootPart().Bodies
curves = GetRootPart().Curves
if bodies.Count == 0 and curves.Count > 0:
    result = Fill.Execute(Selection.Create(curves))
    if not result.Success:
        raise Exception("SpaceClaim Fill failed")
    bodies = GetRootPart().Bodies

if bodies.Count != 1:
    raise Exception("Expected one fluid sheet body")
body = bodies[0]
if body.Faces.Count != 1 or body.Edges.Count != 4:
    raise Exception("Unexpected pipe-section topology")
body.SetName("fluid")
DocumentSave.Execute(SCDOC_PATH, ExportOptions.Create())
```

The validated minimal sequence omits `StartConstraintSketching()`. On this release the closed loop was committed into a sheet body at the switch to Solid mode; afterward `Curves.Count` was 0 while `Bodies.Count` was 1. The observed false failure came from treating zero curves as failure and running Fill unconditionally; the diagnostic did not isolate `StartConstraintSketching()` as a cause by itself.

When launching the SpaceClaim script engine directly, preserve the quoted `/RunScript` and `/ScriptOutput` arguments as one Windows argument string. This PowerShell form was verified locally:

```powershell
$ansysRoot = $env:AWP_ROOT242
if (-not $ansysRoot) { throw 'Set AWP_ROOT242 or provide the SpaceClaim executable path.' }
$runDir = Join-Path $env:TEMP 'ansys-pipe'
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
$exe = Join-Path $ansysRoot 'scdm\SpaceClaim.exe'
$script = Join-Path $runDir 'create_pipe.py'
$output = Join-Path $runDir 'spaceclaim-output.txt'
$arguments = '/Headless=True /RunScript="' + $script + '" /ScriptAPI=V23 /ScriptAsync=False /ScriptOutput="' + $output + '" /ExitAfterScript=True'
$process = Start-Process -FilePath $exe -ArgumentList $arguments -WindowStyle Hidden -Wait -PassThru
```

A tiny script that writes a known evidence file is a cheap command-delivery check. Require both the script's own evidence and the expected `.scdoc`; a zero process exit code does not prove that the script ran.

## Import, transfer, and persistence check in Workbench

Use the Workbench Geometry container to import the saved native file and update the project:

```python
template = GetTemplate(TemplateName="Fluid Flow")
system = template.CreateSystem()
geometry = system.GetContainer(ComponentName="Geometry")
geometry.SetFile(FilePath=SCDOC_PATH)
geometry.Update()
```

Then open that same system's Mesh cell and inspect `ExtAPI.DataModel.GeoData` from the Meshing/Mechanical scripting context. For the rectangular smoke test, require:

- one body with type `GeoBodySheet`;
- one face and four edges;
- the body is the intended `fluid` domain;
- measured bounds match the requested length and radius, in the expected units.

The recorded smoke test checked the body type and 1/1/4 topology; production geometry checks must also compare measured bounds and units with the manifest.

Do not proceed to named boundaries, mesh generation, or solving until this transfer gate passes. Save the Workbench project, close the managed session, reopen the saved `.wbpj`, and repeat the body/topology check. A link that works only before save/reopen is not a completed geometry stage.

## Evidence and failure handling

Write a stage evidence file from inside each application. The SpaceClaim evidence should include body, face, and edge counts and the saved path. The Meshing evidence should include body name/type and actual counts. The Workbench driver must fail if either evidence file is missing or reports failure; do not infer success from `RunScript` returning, the process exit code, a saved project, or a nonempty geometry file.

If one evidence gate fails, keep its log and stop after one targeted repair. Diagnose whether failure occurred in script delivery, surface construction, Workbench import/update, Meshing transfer, or project reopen. Do not label the entire interface incompatible from an empty body inventory or a failed script launch. Ask the user before changing a requested Workbench workflow to another application/control route.
