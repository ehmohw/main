"""2.94: the effect sprites asked of PixelLab's effects artist (/v2/vfx, lite). name: (description, used for)"""
VFX = {
    # synergy attacks (phase208): one per role
    'syn_offense': ("A combined-strike burst seen from the front: crossed white-gold sword slashes flash at the centre, then a ring-shaped shockwave of "
                    "sharp white and gold light bursts outward and fades, with a few sparks flying off. Bright, punchy, about 0.6 seconds, no loop.", 'Combined Strike'),
    'syn_defense': ("A protective shield wall flaring up: a translucent pale-cyan hexagonal energy barrier blooms up from the centre into a dome, "
                    "its hex cells shimmering white at the edges, holds a moment, then breaks into glinting shards that fade. About 0.8 seconds, no loop.", 'Shield Wall'),
    'syn_speed': ("A blitz of speed: jagged yellow-white lightning streaks and motion lines burst outward from the centre in all directions with "
                  "crackling electric sparks, very fast, about 0.5 seconds, no loop.", 'Blitz'),
    'syn_healing': ("Mending light: a soft column of warm golden-green light rises from the ground, with small glowing plus signs and sparkles "
                    "drifting upward and gently fading. About 0.9 seconds, no loop.", 'Mending Light'),
    'syn_control': ("A binding spell: a glowing violet runic circle snaps into place, chains of purple light lash inward from its edge and "
                    "lock tight at the centre with a flash, then fade. About 0.8 seconds, no loop.", 'Binding'),
    # big special attacks
    'dennis_lode': ("The mother lode: a geyser of molten gold erupts straight up out of the ground, spraying glowing gold nuggets and coins "
                    "and bright sparks, then splashes down. Gold, orange and white-hot, about 0.9 seconds, no loop.", "Dennis's Mother Lode"),
    'dennis_sear': ("A searing hit: a red-hot chunk of metal slams into a target - a splash of molten orange metal, white-hot sparks and a "
                    "puff of dark smoke. Small and quick, about 0.4 seconds, no loop.", "Dennis's searing gems and ingots, on impact"),
    'capshun_rainbow': ("A huge painted rainbow brushstroke: a thick arc of wet paint is swept across from left to right in bands of red, "
                        "orange, yellow, green, blue and purple, with paint splatters flicking off its edge. Hand-painted look, about 0.8 seconds, no loop.",
                        "Mr. Capshun's Rainbow Stroke"),
    'apo_coil': ("A coil of black fire: tongues of near-black flame with deep violet bodies and a thin hot-violet rim spiral upward in a tight "
                 "coil, with a few small bright green sparks. Menacing, about 0.9 seconds, no loop.", "Apophiss's Black Flame Coil"),
    'ashur_inferno': ("An inferno: a roaring ring of orange and yellow flame erupts outward from the ground in all directions, with embers "
                      "and black smoke rising. About 0.8 seconds, no loop.", "Ashur's Inferno"),
    # the Sky Buddies
    'sky_sunbeam': ("A sunbeam: a focused column of blazing sunlight strikes straight down, a white-hot core inside a golden halo, short "
                    "sun rays flaring round it, then it narrows and fades. About 0.6 seconds, no loop.", "Sunny's Sunbeam"),
    'sky_zap': ("A zap: a jagged blue-white lightning bolt cracks straight down from a small dark storm cloud at the top, with a bright "
                "flash and crackling sparks where it lands. About 0.4 seconds, no loop.", "Nimbus's Zap"),
    'sky_star': ("A shooting star: a five-pointed yellow star streaks from left to right leaving a sparkling golden trail, then bursts into "
                 "little twinkling stars. About 0.5 seconds, no loop.", "Twinkle's Star Shot"),
    'sky_lullaby': ("A lullaby: soft pale-blue musical notes and little sleepy 'z' letters drift slowly upward and sway, with tiny "
                    "twinkling sparkles, gently fading. Calm, about 1 second, no loop.", "Snooze's Lullaby"),
    'sky_drizzle': ("A gentle drizzle: soft rain falls from a small grey cloud at the top, small blue droplets landing with little "
                    "splashes at the bottom. About 0.8 seconds, no loop.", "Nimbus's Drizzle"),
    'sky_forecast': ("The forecast, all at once: a swirling vortex where a blazing sun flare, a jagged lightning bolt, a shower of falling "
                     "stars and a crescent moon spin together and burst outward in a bright flash. Big and dramatic, about 1 second, no loop.",
                     "The Sky Buddies' The Forecast"),
    # the pixel twins (retro-game attacks)
    'px_fireball': ("A retro 8-bit fireball: a round blocky orange-and-yellow fireball with a flickering tail, flying from left to right, "
                    "classic NES style, chunky pixels, looping.", "8-Bit Emma's Fireball"),
    'px_star': ("A retro power-up: a blinking rainbow-flashing invincibility star sparkle burst, classic 8-bit style, chunky pixels, "
                "flashing colours, about 0.6 seconds, no loop.", "8-Bit Emma's Power Star"),
    'px_hearts': ("A retro heart pickup: little red 8-bit pixel hearts pop up and float upward with a white sparkle, classic NES style, "
                  "about 0.6 seconds, no loop.", "8-Bit Emma's Extra Life"),
    'px_beam': ("A retro sword beam: a white-and-cyan blocky sword-shaped energy beam flying from left to right and flashing, classic "
                "8-bit adventure style, chunky pixels, looping.", "8-Bit Leo's Sword Beam"),
    'px_boom': ("A retro 8-bit explosion: a chunky pixel explosion puff in white, yellow, orange and red that pops and breaks into "
                "squares, classic NES style, about 0.5 seconds, no loop.", "8-Bit hits and KOs"),
    'px_coin': ("A retro coin burst: spinning 8-bit gold coins pop up and scatter with sparkles, classic NES style, about 0.6 seconds, "
                "no loop.", "8-Bit Leo's Coin Block"),
    # Mr. Capshun's tools (2.94): the pencil's sketches, the brush's splash
    'capshun_scribble': ("A pencil-sketch explosion: a hand-drawn black-and-white cartoon blast, scribbly graphite lines and cross-hatching burst "
                         "outward in a jagged star, little sketched debris and curly smoke doodles fly off, all in pencil grey and black on nothing, "
                         "like a doodle in a notebook. About 0.6 seconds, no loop.", "Mr. Capshun's sketched bombs, going off"),
    'capshun_splash': ("A splash of wet paint: a big burst of bright paint in red, yellow and blue splatters outward from the centre, thick "
                       "drips and droplets flying, hand-painted look, about 0.5 seconds, no loop.", "Mr. Capshun's brush, up close"),
}
