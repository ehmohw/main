"""2.94d: THE ARCADE (phase216) - the 8-bit corner's art, asked of PixelLab: its two traders (characters, front and back) and every
item's 32 x 32 icon (create-image-pixflux; props become voxel models of theirs). Homages, never the games' own names."""
STYLE = 'retro 8-bit video game pixel art, bold black outline, bright limited palette'
CHARS = {
    'bit_rat': ('Bit, a cheerful grey rat merchant in 8-bit video game style: big round ears, pink nose, buck teeth, a red cap worn '
                'backwards, a green apron over a striped shirt, a coin pouch at his belt', 64),
    'px_villager': ('a blocky Minecraft-style villager in 8-bit pixel art: a big bald head, one long unibrow, a very big nose, green eyes, '
                    'arms folded into its sleeves, a long brown robe with a green trim', 64),
}
ANIMS = {'idle': ('standing idle, breathing gently, looking friendly', 4)}
ICONS = {
    # the four armour sets
    'hunter_helm': 'a sci-fi bounty hunter helmet, rounded orange-red armor with a green visor, side view',
    'hunter_plate': 'a sci-fi orange-red power suit chestplate with huge round shoulder pauldrons and a green light',
    'hunter_greaves': 'orange-red sci-fi armored leg greaves with yellow knee plates',
    'hunter_boots': 'a pair of heavy orange-red sci-fi armored boots with yellow trim',
    'bomber_helm': 'a round blue robot boy helmet with cyan side discs and a light blue faceplate',
    'bomber_chest': 'a blue robot boy chest armor with light blue trim',
    'bomber_legs': 'blue robot armored leggings with light blue thighs',
    'bomber_boots': 'big chunky blue robot boots with light blue cuffs',
    'plumber_cap': 'a red plumber cap with a white circle emblem on the front',
    'plumber_shirt': 'a red long-sleeved shirt with blue overall straps and yellow buttons',
    'plumber_overalls': 'blue denim overalls trousers',
    'plumber_boots': 'a pair of brown work boots',
    'vhunter_band': 'a red cloth headband with trailing ends, a vampire hunter\'s',
    'vhunter_cuirass': 'a brown leather vampire hunter cuirass with a red sash and a silver cross clasp',
    'vhunter_legs': 'brown leather vampire hunter trousers with straps',
    'vhunter_boots': 'tall brown leather vampire hunter boots with silver buckles',
    # weapons
    'pixel_blade': 'a heroic 8-bit sword with a blue hilt, golden crossguard and a shining silver blade, diagonal',
    'vampire_killer': 'a coiled leather chain whip with a silver morning-star tip, vampire hunter weapon',
    'arm_buster': 'a blue robot arm cannon, a buster gun with a glowing barrel',
    'fire_flower': 'a fire flower power-up: a flower with red and orange fiery petals, a yellow center with eyes and a green stem',
    # upgrades
    'chip_glitch': 'a corrupted game cartridge chip with glitchy colorful static and broken pixels',
    'chip_missingno': 'a glitched game chip shaped like a scrambled block of random pixels, a missing number glitch',
    'chip_genie': 'a golden cheat device cartridge with a genie lamp emblem',
    'chip_turbo': 'a red game controller chip with a turbo button and speed lines',
    # props and display pieces
    'q_block': 'a golden question mark block from a platform game, a yellow square block with a white question mark',
    'warp_pipe': 'a short green warp pipe from a platform game, wide rim on top, front view',
    'arcade_cabinet': 'a retro arcade cabinet machine with a glowing screen, joystick and buttons, front view',
    'blade_stone': 'a legendary sword stuck in a stone pedestal, glowing blue hilt',
    'power_triangles': 'three golden triangles stacked into one big triangle, a sacred relic',
    'save_point': 'a glowing blue save point crystal floating above a small pedestal',
    # practical items
    'heart_container': 'a big red heart container from an adventure game, shiny with a gold rim',
    'super_star': 'a smiling golden invincibility star with two black eyes, glowing',
    'power_mushroom': 'a red mushroom power-up with white spots and a cream stem with two eyes',
    'oneup_mushroom': 'a green 1-up mushroom power-up with white spots and a cream stem with two eyes',
}
