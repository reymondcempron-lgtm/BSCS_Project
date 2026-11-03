# Modern Tropical House — VPython

An interactive VPython model of a two-storey tropical home with a white facade,
timber upper-floor accents, a flat overhanging roof, a glazed balcony, a covered
carport, and a landscaped front yard with a pool, tropical plants, driveway,
stepping stones, and timber perimeter fence.

## Run

1. Install Python 3 and VPython if needed:

   ```powershell
   python -m pip install vpython
   ```

2. Open `3DDreamHouse.py` in VS Code and select **Run Python File**.
   VPython opens the interactive scene in your web browser.

## Controls

| Key/action | Result |
| --- | --- |
| Mouse drag | Orbit around the house |
| Left / Right arrows | Orbit horizontally through a full 360° |
| Up / Down arrows | Adjust the camera elevation |
| `Home` | Reset the camera view |
| Scroll wheel | Zoom in or out |
| Shift + mouse drag | Pan the view |

The model is built entirely with VPython primitives and directional/ambient
lighting. VPython provides real-time interactive rendering; physically based
materials, ray-traced reflections, global illumination, and soft shadows are
not available in this renderer.
