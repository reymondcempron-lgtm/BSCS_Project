# Verification record — 3 November 2026

## Direct room buttons and mouse-controlled room views

- Added 16 direct room/outdoor buttons, including Master Suite, both guest rooms,
  bathrooms, office, lounge, balcony, kitchen, pool, pavilion and garage.
- Each button cancels previous camera activity, applies the appropriate cutaway,
  sets a room-centred pivot and enables supported native spin, zoom and pan.
- Camera updates leave room views untouched, so mouse changes persist. Exiting
  a room to another mode restores Full exterior and synchronizes the cutaway menu.
- **15 automated tests pass**. New checks exercise every actual room-button binding,
  all room presets, persistence of simulated mouse camera changes and mode exits.
  These tests use real VPython vectors with a fake scene and native-widget substitutes;
  they do not establish graphical rendering or browser gesture behavior.
- Browser inspection remains unverified under the previously recorded URL restriction.

## KITOFU HOUSE redesign — current revision

- Renamed the project and address plaque; added pitched roof wings, gable infill,
  entrance portal, facade frames, a guarded dining void and upstairs office.
- Added room furnishings, curtains, joinery, table settings, practical fixtures,
  terrace seating, landscape beds, lanterns, a parasol and subtle water animation.
- Reorganized native controls with primary/secondary colors, explicit Visit Space
  and Show View actions, and entrance/estate camera presets.
- **12 unittest tests pass**, including the new dining-void floor check and the
  existing sampled clearances against the actual architecture/furniture builders.
- A new live smoke launch waited for its browser connection before construction;
  it did not complete. This redesign has not received a fresh graphical review.
  Prior browser checks and primitive counts below apply to the earlier design only.
- The browser URL was previously denied by the computer-use policy. No browser
  automation was attempted to bypass that restriction for this revision.

## Earlier baseline verification (before redesign)

## Environment actually used

- Windows; CPython **3.12.14**.
- Real **vpython 7.6.5**, with **setuptools 80.9.0** providing its required
  `pkg_resources` compatibility API.
- Local default-browser launch in Microsoft Edge, with an active Python process.
- An isolated test environment was used outside the source tree. No virtual
  environment, installed dependency, cache, machine path or browser asset is
  included in the deliverable.

## Automated checks performed

- Parsed all **14 Python files** and imported all `house` modules successfully.
- **11 unittest tests passed**. They cover site ordering; dog/butterfly bounds;
  stair rise and rejection of sideways jumps onto/off the stair; collision;
  tour-graph connectivity; sampled wall/furniture/vehicle route clearances;
  camera-mode/input resets; tour completion; pause/retarget; frame-independent
  walking; and exit from dog-follow.
- `python -m pip check`: **No broken requirements found**.
- Normal-detail `viewer.py --smoke-seconds 5`: **exit code 0**, including when
  launched by absolute entry-file path from a different working directory.
- Low-detail `viewer.py --low-detail --smoke-seconds 5`: **exit code 0**.
- Both smoke runs used actual VPython objects and passed assertions that pet
  dimensions survive animation, paused animation does not move, and each cutaway
  hides/restores the intended floor/roof groups.
- Startup reported **1,085 construction primitives** in normal detail and
  **1,030** in low detail, before compounding; **343 collision volumes** in both.
  These are object counts, **not measured frame rates**.
- Source scan found no hardcoded machine-specific paths or unfinished TODOs.

## Graphical checks actually performed

Inspected the rendered scene in Edge and exercised these controls:

- Front overview and Reset view: enclosed deep lot, front garden, side drive,
  two-storey facade, balcony and solar roof visible.
- Backyard: pool and separate covered BBQ pavilion visibly behind the mansion,
  with terrace, coping, water, ladder, deck seating and planting.
- Follow dog: procedural white/cream dog and butterfly visible in the front
  garden; the camera tracks the animated dog.
- Roof off: upstairs room layout and furniture visible, roof/solar hidden.
- Ground floor: upper assembly hidden, downstairs rooms/furniture retained;
  garden, garage and pavilion remain visible.
- Full exterior: restored the complete two-storey shell.
- Evening: changed sky, ambient/directional illumination and warm pavilion light.

## Problems found and fixed

- Fresh Python 3.12 environments lacked `pkg_resources`: added the explicit
  compatible setuptools pin to the install requirements.
- Tour waypoints clipped a stair-guard clearance, a bedside table and a balcony
  table: adjusted the route; all sampled routes now pass collision checks.
- VPython axis assignment can resize ellipsoids: preserved each shape's length
  while rotating pet and palm components; real-object smoke assertions pass.
- Prevented stepping sideways into a high stair segment or dropping from the
  upper floor into the stairwell using a bounded floor-height change.
- Made the pool basin genuinely recessed by splitting the surrounding terrain.
- Reduced the viewport width so the full scene fits a typical browser window.

## Verification limits

- The full tour was executed by a controller test; every stop was reached and
  the final stop paused. A human did not watch every second of the entire tour.
- Manual walking speed, collisions and stair logic were tested computationally;
  a full human keyboard walk through every room and stair tread was not recorded.
- The Concept 03 image and dog photo were absent from the available attachment;
  no exact visual resemblance to those references is claimed.
- No FPS measurement, photorealism claim, other OS/browser test or broad Python
  version compatibility claim is made.
- `pkg_resources` emits a deprecation warning, but tested startup completes.

Before classroom presentation, run a complete guided tour and walk the stairs
on the teacher's machine. The README includes controls and recovery shortcuts.
No GitHub publishing or commits were performed.
