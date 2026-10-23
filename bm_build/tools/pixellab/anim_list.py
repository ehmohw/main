"""2.94: the pixel twins' animations (south - toward you; they're billboarded), asked of PixelLab (/v2/characters/animations, v3)"""
ANIMS = {
    'emma': {'idle': ('standing idle, breathing gently, ponytail swaying', 4),
             'walk': ('walking forward toward the viewer', 8),
             'fireball': ('throwing a fireball forward with one hand, retro game hero', 8),
             'stomp': ('jumping straight up and stomping down hard', 8),
             'power': ('raising both arms high in a victory pose, glowing with power', 6),
             'sit': ('sitting down on the ground, legs crossed', 4),
             'hurt': ('recoiling backward from a hit', 4)},
    'leo': {'idle': ('standing at attention, breathing gently', 4),
            'walk': ('marching forward toward the viewer', 8),
            'slash': ('drawing a short sword and slashing it down overhead', 8),
            'block': ('raising a round shield in front of himself to block', 6),
            'beam': ('thrusting a short sword forward, the blade flashing with light', 8),
            'sit': ('sitting down on the ground, resting', 4),
            'hurt': ('recoiling backward from a hit', 4)},
}
