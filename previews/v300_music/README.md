# v3.00 music previews: the market's nights and the two ships

Each mp3 is the in-game loop played **twice**, with the second pass fading out over its last 6 s, so you can hear the seam.
The game itself plays the .ogg files from `bm_build/vendor/`. All tracks are synthesised (no samples) and mastered to
-15 LUFS integrated, with the sample peak under -1 dBFS after the Vorbis encode.

## The market's theme, "Members Only", one variant per custom night (tools/market_music.py)

Every variant keeps the theme's tune, chart and form, and its 40 bars / 75 s, so phase250's loop logic is shared.

| file | night | length | LUFS | peak | the dressing |
|---|---|---|---|---|---|
| `market_lucky.mp3` | Lucky Night | 75 s | -15.0 | -1.2 dBFS | C major, a lighter swing, open trumpet, glockenspiel on the hook, chimes, wind chimes, tambourine, triangle |
| `market_blood.mp3` | Blood Moon | 75 s | -15.0 | -1.4 dBFS | CmM7 and flat-nine dominants, a low string pedal, pipe organ, war drums and timpani, a growling trumpet, a bass clarinet, a tolling bell |
| `market_invasion.mp3` | Invasion Night | 75 s | -15.0 | -1.6 dBFS | an arpeggiated synth bass, a drum machine, a pulse-wave lead, a gliding theremin, synth-brass stabs, two-tone alarms, laser zaps |
| `market_dread.mp3` | Dread Night | 75 s | -15.0 | -1.8 dBFS | 35 cents flat with tape wow, a music box on the hook, dissonant violins, a glassy cluster, a celesta, a heartbeat, a ticking clock |

The original theme is unchanged (it re-renders bit for bit): `../v299a_music/market_theme.mp3`, 75 s, -15.3 LUFS, -1.3 dBFS.

## The ships (tools/ship_music.py)

| file | where | length | LUFS | peak | |
|---|---|---|---|---|---|
| `ship_mothership.mp3` | aboard an alien mothership | 72 s | -15.0 | -2.9 dBFS | "Tractor Beam Bossa": A dorian at 120 BPM, a bossa synth bass, a drum machine's clave and shaker, a wobbling pad, FM-bell bubbles, bloops, a theremin lead |
| `ship_mothership_inv.mp3` | the same, on an invasion night | 72 s | -15.0 | -2.5 dBFS | "Red Alert": an alarm, a kick on every beat, sixteenth-note hats and arpeggios, a gated pad, zaps, stabs, a jumpier theremin |
| `ship_dreadnought.mp3` | aboard a Vorn Dreadnought | 80 s | -15.0 | -1.7 dBFS | "The Deep Hive" (rewritten: was "Hive Iron March", which read as a pirate ship): slow and alien, 72 BPM around a D that never leaves - a sub drone, an engine pulse, a breathing machine hum, a formant hive choir on chords moving by minor thirds, detuned glass, a chittering in the dark, far-off bulkhead clanks and servos; the hook is octatonic (it opens with the Armada's CALL, D-A-Eb), its held notes bending flat, sung by one wordless gliding voice with ring-modulated bells striking each note; no gallop, no horns, no snare |
| `ship_dreadnought_inv.mp3` | the same, on an invasion night | 80 s | -15.0 | -2.1 dBFS | "Battle Stations" (rewritten): the same ship woken - a synth pulse driven in sixteenths (with the flat second), the hull beaten, metal ticks, the choir's breath pulsing, ring-modulated alarm stabs, a tritone ring-mod alarm |
