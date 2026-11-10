# Etherava: Omega Island (playable demo)

A first playable slice: Emma, Leo and Bender fight through the Lantern Woods on Omega Island to the Arachno-Lantern nest.

## Play

1. Install [Godot 4.4 or newer](https://godotengine.org/download) (the standard build).
2. Open Godot, choose **Import**, and pick `game/project.godot`.
3. Press **F5**.

| Action | Keys |
| --- | --- |
| Move | WASD or arrow keys |
| Attack | Space, J or left click |
| Switch hero | Tab or E (next), Q (previous) |
| Restart (after winning or losing) | R |

## What's in it

- **A party of three.** You control one hero; the other two follow and fight on their own. Switch at any time.
  - **Emma** is fragile. Her slingshot does little damage but stuns, and stunned enemies take half again as much damage.
  - **Leo** is the front line: high health, a trident thrust that hits everything in front of him.
  - **Bender** is fast, with quick bites.
- **Four areas**, each sealed by a web gate until it is cleared: Arachno-Lanterns, Stalkers (they hunt whoever is weakest), egg sacs that hatch unless you break them, and the Brood Lantern boss.
- **Shared experience and levels**, soul embers and hearts as drops. Downed heroes get back up when an area is cleared.

## Art

All sprites are placeholders generated with PixelLab from the concept art, to be replaced by art drawn from scratch.
`tools/trio.py` and `tools/props.py` are the requests that made them; `tools/prep.py` packs frames into `assets/` and writes `scripts/manifest.gd`.

## Automated playtest

`godot -- --shots=<folder>` plays the level by itself, saves a screenshot every five seconds, and prints how each area went.
