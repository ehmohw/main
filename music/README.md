# The Ethereal Gem — music

| File | What |
|---|---|
| `democratus_battle.ogg` | Democratus's battle theme (2 min loop) |
| `killerwatt_battle.ogg` | KillerWatt's battle theme (2 min loop) |
| `emma_theme.ogg` | Emma's theme (2 min loop) |
| `*_15min.ogg`, `*_10min.ogg` | extended versions |
| `democratus_to_killerwatt_10min.ogg` | Democratus → storm-break → KillerWatt |
| `emma_democratus_killerwatt.ogg` | all three in story order |
| `kw_transition.ogg` | the 8 s storm-break between Democratus and KillerWatt |

## Rebuilding (needs numpy, scipy, ffmpeg)

    cd source
    python3 democratus_music.py democratus_battle.ogg
    python3 killerwatt11.py x killerwatt_battle.ogg
    python3 emma_music.py emma_theme.ogg
    python3 kw_transition.py kw_transition.ogg

The extended and hybrid files are made from these with ffmpeg (`-stream_loop`, `concat`, `acrossfade`).
