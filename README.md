# Seaside Dream House

A 3D dream house built with VPython: a two-story seaside house on top of a grassy hill, with mountains around it and the ocean behind it. You can look inside it, jump straight into any room, and stargaze from the second-floor deck.

## How to run

You need Python 3.12 or similar. Install the libraries once:

```
pip install vpython "setuptools<81"
```

VPython 7.6.5 still relies on a part of `setuptools` that newer versions are removing, which is why the version is limited.

Then run the project:

```
python ag-ag_dream_house_finalproject.py
```

The scene opens in a new browser tab after a few seconds. To stop it, close the tab and press Ctrl+C in the terminal.

## Controls

| Control | What it does |
|---|---|
| See-through walls | Makes the outer walls transparent, or solid again |
| Open house | Lifts the roof, upper floor, and deck to show the ground floor, or sets them back |
| Switch to night / day | Changes the sky and lighting, with stars, a moon, glowing windows, and string lights at night |
| Front, Sea side, Aerial | Jumps to a preset view of the house |
| Stargazing | Puts the camera on the deck, looking at the sky over the sea |
| Ground floor: Entry hall, Living room, Kitchen, Dining room, Veranda | Jumps inside that part of the house |
| Upper floor: Landing, Bedroom 1, Bedroom 2, Bathroom, Deck | Jumps inside that part of the house |
| Right mouse drag | Rotates the view |
| Mouse scroll | Zooms |

Inside a room, right-drag turns the view around the middle of the room. Turning far enough can take the camera through a wall, so click the room's button again to get back. On the veranda, the deck, and in the Stargazing view, the camera can see much farther, so right-dragging swings it away from where it stands. Click the button again to return.

## Good to know

Zooming in very close can hide distant scenery, such as the mountains and stars, because of how VPython limits how far the camera can see. Zoom back out or click a view button to bring it back. For the same reason, windows in the indoor room views show the yard and the sky color, but not the far sea, mountains, or stars.
