# Etherava: Omega Island (playable demo)

A first playable slice: Emma, Leo and Bender fight through the Lantern Woods on Omega Island to the Arachno-Lantern nest.

## Play

1. Install [Godot 4.4 or newer](https://godotengine.org/download) (the standard build).
2. Open Godot, choose **Import**, and pick `game/project.godot`.
3. Press **F5**.

| Action | Keyboard | Controller |
| --- | --- | --- |
| Move | WASD or arrow keys | Left stick or D-pad |
| Attack | Space, J or left click | A, X or right trigger |
| Take over a computer ally | Tab or E (next), Q (previous) | Bumpers |
| Restart after winning or losing (host only) | R | Start |
| Back to the main menu from the end screen | Esc | |

## One to four players

The party is always four heroes: Emma, Leo, Bender and Cecil. Each player picks one, and the computer plays the rest.

- **Play on this computer:** up to four players share the screen, one on the keyboard and the others on controllers.
  In the hero room, each player presses Space (keyboard) or A (controller) to join, and left / right to change hero.
- **Host an online game:** the room shows your address on your home network. Friends choose **Join** and type it in.
  - Over the internet, the host forwards **UDP port 24565** on their router to their computer and gives friends their public IP address,
    or everyone uses a virtual network tool such as Tailscale or ZeroTier and joins with that address.
  - Several players can share one of the computers in an online game.
- A player who leaves is replaced by the computer. Joining after the game has started isn't supported yet.

## How it stays in step

One machine is the host. It runs the enemies, damage, drops and progress, and sends everyone a snapshot 20 times a second.
Each machine moves its own players' heroes and tells the host where they are; attacks are requests the host carries out.

## What's in it

- **Four heroes.**
  - **Emma** is fragile. Her slingshot does little damage but stuns, and stunned enemies take half again as much damage.
  - **Leo** is the front line: high health, a trident thrust that hits everything in front of him.
  - **Bender** is fast, with quick bites.
  - **Cecil** throws poison from his staff, which keeps hurting for a few seconds.
- **Four areas**, each sealed by a web gate until it is cleared: Arachno-Lanterns, Stalkers (they hunt whoever is weakest), egg sacs that hatch unless you break them, and the Brood Lantern boss.
- **Shared experience and levels**, soul embers and hearts as drops. Downed heroes get back up when an area is cleared, and enemies are tougher with more players.

## Art

All sprites are placeholders generated with PixelLab from the concept art, to be replaced by art drawn from scratch.
`tools/trio.py` and `tools/props.py` are the requests that made them; `tools/prep.py` packs frames into `assets/` and writes `scripts/manifest.gd`.

## Automated playtest

`godot -- --shots=<folder>` plays the level by itself, saves a screenshot every five seconds, and prints how each area went.

`godot --headless -- --net-test=host` and, in a second terminal, `godot --headless -- --net-test=client` play an online game between two
instances on one computer, each printing what it sees every ten seconds so the two can be compared.
