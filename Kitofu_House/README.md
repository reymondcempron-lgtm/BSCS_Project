# KITOFU HOUSE

## Mansion design revision

The redesigned residence has stepped pitched roof wings, timber soffits, a stone
entrance portal, balcony screening and a closer entrance camera. The east-front
dining salon is now genuinely double-height, with a guarded upstairs gallery and
home office replacing the former front-east bedroom. The master, rear-east bedroom
and ground-floor guest bedroom remain. The gallery void has no walkable floor.

Interiors now include layered rugs, curtains, joinery, books, table settings,
pendants, kitchen stools and appliances, bedroom benches, bathroom accessories,
and furnished terraces. Landscaped beds, pool towels, a parasol and garden lanterns
complete the exterior. Pool color varies gently while the dog and butterfly animate.
Day/Evening also controls interior and garden practical lights.

The controls use primary green actions and neutral secondary buttons. Click any
of the 16 room/outdoor buttons to open its view immediately. **Master Suite**, for
example, opens the bedroom and removes the roof. Right-drag (or Ctrl-drag) rotates
around the room centre; scroll zooms; Shift-drag pans. The camera stays under mouse
control until you select another action. Ground-floor room buttons hide the upper
storey automatically. Leaving a room for a tour, walking, follow or overview restores
the exterior. These are room-centred orbit views; large rotations can take you through
walls because orbit cameras do not use walking collisions. Reclick a room to reset it.
Choose an exterior camera preset then **Show View**.
**Entire estate** retains the original aerial view. Native VPython controls retain
their platform typography and shape; no CSS widget overrides or injected scripts
are used. Roof removal also hides the gable infill so interiors remain inspectable.

An original, runnable VPython final project: a two-storey modern Philippine
tropical mansion on a spacious enclosed lot. Run **`viewer.py`** to open the
interactive 3D scene in your default browser. The geometry is procedural Python,
not a static image or a Three.js substitute.

## Install and run on Windows

Tested with **CPython 3.12.14, VPython 7.6.5, setuptools 80.9.0**, on Windows with
Microsoft Edge. Python 3.12 is recommended; other Python versions and operating
systems have not been verified. Install Python from [python.org](https://www.python.org/downloads/)
if needed, enabling its PATH option.

Download the repository's ZIP and extract it, or clone your teacher's repository.
Open the extracted project folder in VS Code. In its terminal:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe viewer.py
```

If Windows provides `py` instead of `python`, use `py -3.12 -m venv .venv` for the
first command. Activation is optional; the explicit commands above do not need
a PowerShell execution-policy change.

In VS Code, press **Ctrl+Shift+P → Python: Select Interpreter → Enter interpreter
path**, then choose `.venv\Scripts\python.exe`. Open a **new** terminal after
selecting the interpreter. With that environment active, the entry command is:

```powershell
python viewer.py
```

**Keep the Python process running while viewing the browser.** The local VPython
server and the animation loop live in that process. Wait for `Ready:` in the
terminal. The browser needs WebGL enabled. Stop with **Ctrl+C in the terminal**;
close the browser tab afterward. Do not refresh an old stopped scene: rerun the
entry command to get a fresh local session. No API keys or cloud services are used.
Dependencies are installed only by the explicit pip command, never at startup.

Optional reduced foliage:

```powershell
python viewer.py --low-detail
```

## Layout and rooms

One unit is one metre. **Y is up, -Z faces the street, +Z faces the backyard.**
The lot is **44 × 70 m**, extending from Z=-35 to Z=35. The street is beyond
Z=-35. The **24 × 20 m** house occupies X=-12..12 and Z=-4..16. Its only habitable
floor levels are **Y=0 and Y=3.6 m**. The roof is above Y=7.2 m; solar hardware is
not a third storey. Floor slabs are 0.24 m thick.

The arrangement is **street → gates and front lawn → mansion → rear terrace →
pool and separate BBQ pavilion**. The pool is 13 × 6 m, centred at (3,25), with a
recessed basin about 1.5 m deep. The 9 × 8 m pavilion is centred at (-13,26).
The driveway follows the west side to a 7 × 10 m covered garage. Gates are modeled
open; they are not motorized. Boundary palms, shrubs, and side paths keep the
centre of the front garden spacious. See [the schematic plan](assets/plan.svg).

| Level | West wing | Centre | East wing |
| --- | --- | --- | --- |
| Ground | Living room; rear guest bedroom and bathroom | Foyer, hall, open straight staircase | Dining room and open kitchen; rear terrace access |
| Upstairs | Master suite with ensuite and balcony; rear family lounge/shared bathroom | Hall, stair void, connected rear landing | Gallery / office beside dining void; rear bedroom |

The stairs run from X=0.45..2.65, Z=5..12.2 toward the rear. The upstairs slab
has a matching opening. Approach from the central ground hall at Z=4.6, face +Z,
and walk up; turn left after reaching the rear landing. On descent, approach the
same landing, turn to -Z, and follow the stairs. The narrow collision ramp tracks
the 24 visible treads continuously. Upstairs/Downstairs buttons are convenient
explicit transfers and recovery controls.

## Controls

Click inside the canvas before using movement keys. Buttons appear below it;
scroll down in a small browser window. Maximize the window if needed.

| Control | Behaviour |
| --- | --- |
| Start House Tour | Places the camera at the front entrance; starts the 13-stop routed tour |
| Pause Tour / Resume Tour | Freezes/resumes tour motion and dwell time |
| Previous / Next | Selects the adjacent stop; a mid-segment change returns along that clear segment first |
| Room / outdoor buttons | Immediately opens that space with native rotation, zoom and pan |
| Exit tour | Returns to front orbit overview |
| Explore Freely | Starts manual walking on the front path |
| Show View | Displays the selected entrance, estate, backyard or garage camera |
| Upstairs / Downstairs | Explicitly places a walking camera on the selected floor |
| Follow Kitofu | Tracks the small Shihpoo running after its butterfly |
| Reset view | Immediately restores front overview and exits every other mode |
| Day / Evening | Changes ambient/directional light and pavilion local light |
| Full exterior | Restores both floors and the roof |
| Roof off | Hides roof/solar hardware; retains both floors and their furniture |
| Ground floor | Additionally hides the second-floor assembly to inspect downstairs |
| Pause dog / Resume dog | Freezes/resumes the dog and butterfly together |
| W / S | Walk forward/backward |
| A / D | Strafe left/right |
| Left / Right arrows | Turn left/right |
| Up / Down arrows | Look up/down |
| Esc | Clears input and returns to the manual-walking entrance |
| Right-drag or Ctrl+left-drag | Orbit, in overview mode |
| Mouse wheel | Zoom, in overview mode |
| Shift+left-drag | Pan, in overview mode |

Tour route: front entrance → garage → foyer → living → dining/kitchen →
upstairs landing → master → balcony → rear terrace → pool → BBQ → dog lawn.
The tour pauses at its final stop. Tour movement uses doorway/stair waypoints;
it does not interpolate directly between distant rooms. Explicit entry/floor/reset
buttons reposition the camera rather than pretending to walk that transfer.
Only one camera mode updates at a time. Mode changes clear held-key state.

Cutaway changes visibility only. The selected floor's furniture remains visible;
collision/navigation remains active even when the upper assembly is hidden.
Restore `Full exterior` or `Roof off` before walking upstairs after ground-floor
inspection. The pavilion and garage remain visible in every cutaway.

## Project files and revision guide

```text
viewer.py                  entry point, lighting, bounded time-based animation loop
requirements.txt           pinned direct dependencies and compatibility dependency
house/
  config.py                title, dimensions, positions, colours, speeds, detail
  geometry.py              reusable shapes, wall openings, collision/cutaway groups
  architecture.py          two-floor shell, stairwell, balcony, roof, solar, garage
  interiors.py             reusable furniture and the furnished floor plan
  landscape.py             terrain/pool, paths, gates, planting, BBQ pavilion
  vehicles.py              procedural sports car and two distinct motorcycles
  dog.py                   Shihpoo, butterfly and coordinated animation
  navigation.py            pure collision, floor handling, pet path and tour graph
  cameras.py               exclusive camera modes and time-based motion
  controls.py              supported VPython widgets
tests/                     focused navigation/camera regression tests
assets/README.md           origins and reference limitations
assets/plan.svg            local, editable schematic site/floor plans
```

Start with `house/config.py`: change `TITLE`, `PALETTE`, `POOL`, `PAVILION`,
`GARAGE`, `TREE_POSITIONS`, `WALK_SPEED`, `TURN_SPEED`, `TOUR_SPEED`, `TOUR_DWELL`,
`DOG_SPEED`, `VIEW_WIDTH`, `VIEW_HEIGHT`, or `DETAIL`.
The dog route is an ellipse controlled by `DOG_CENTER` and `DOG_RADII`; keep its
entire body and the butterfly inside `LAWN`. `FPS` is a rate cap, not a measured
frame-rate claim. The default is 40; elapsed time is capped at 0.05 s per frame.

The floor plan is deliberately hand-authored and easy to explain. **Changing the
house footprint or moving walls requires updating interior coordinates and tour
waypoints too**; the dimension settings are not an automatic floor-plan generator.
Architecture dimensions start in config, wall openings are in `architecture.py`,
furniture positions are in `interiors.py`, and camera destinations/door routes are
in `navigation.py`. Vehicle placements are in `vehicles.py`. Rerun the tests after
layout edits. This avoids silently claiming that arbitrary layout changes are safe.

All paths are module-relative; no machine-specific paths appear in the project.
There are no runtime image/model files to locate. You may invoke `viewer.py` by
its absolute path from another directory.

## Verification

```powershell
python -m unittest discover -s tests -v
python -m pip check
python viewer.py --smoke-seconds 5
```

The focused tests cover backyard ordering, dog/butterfly route bounds, stair
continuity, wall/obstacle collision, all-pairs tour connectivity, sampled routes
against actual wall/furniture/vehicle volumes, mode input resets, full tour
completion, pause/retarget behaviour, walking speed, and leaving dog-follow.
They do not substitute for visual testing of the renderer.

For presentation, manually check a full guided tour, walk up and down the stairs,
inspect both cutaways, and try day/evening and dog-follow. Confirm that controls
are visible in the browser size used by the teacher. See `VERIFICATION.md` for
the checks actually performed during this build.

## Limitations and credits

- The Concept 03 image and dog photograph were not included in the available
  attachment. This is an original interpretation of the written brief, including
  the described white Shihpoo and cream/tan ears; visual matching is unverified.
- Real-time VPython geometry is stylized, with basic transparency and lighting.
  It has no photorealistic reflections, global illumination, or dynamic shadows.
  Water is static. Glass transparency may have sorting artifacts.
- Widget colours use supported VPython properties; the cream heading uses simple
  HTML in the documented canvas title. Native button shapes, font,
  menus and page background follow VPython/browser defaults; custom rounded
  buttons and a fully themed page are intentionally not implemented using DOM hacks.
- Collision uses conservative axis-aligned volumes and a 0.22 m camera radius.
  Decorative small objects and pet geometry are not physical simulation bodies.
  Cutaway is a visual inspection tool; invisible upper walls still collide.
- Low detail reduces foliage and wood slats, not the essential rooms/vehicles.
  No measured FPS or minimum hardware guarantee is claimed.
- All scene models and the schematic are original procedural work. The motorcycle
  colours are M1000RR-inspired, without logos or official affiliation. No classmate
  code, external 3D assets, remote fonts, paid assets or API services are used.
- VPython 7.6.5 still emits a `pkg_resources` deprecation warning. The pinned
  setuptools version supplies that API; the warning is not a startup failure.

References: [VPython](https://vpython.org/), [camera API](https://www.glowscript.org/docs/VPythonDocs/camera.html),
[canvas/widgets](https://www.glowscript.org/docs/VPythonDocs/canvas.html),
[compound objects](https://www.glowscript.org/docs/VPythonDocs/compound.html).

Upload the source folder and these documentation files to your teacher's repository.
Do not upload `.venv`, caches or logs; `.gitignore` excludes them. Nothing was
published to GitHub as part of this build.
