"""2.79: a painting the Fence sells - a portrait of two, pixelated from a picture the owner sent (5 blocks wide, 4 tall).

It's a real painting: a painting variant (bm:portrait) hung from its item like any other - the item carries the variant,
so it always hangs this picture. It isn't in #minecraft:placeable, so a plain painting never rolls it.
The picture is vendor/portrait_of_two.png (80 x 64: 16 pixels a block, as vanilla's paintings are - shrunk from the
original with its ink lines darkened first so they survive, full colour so both pairs of green eyes do)."""
import os
from items import item, T

VARIANT = 'bm:portrait'
W, H = 5, 4
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor', 'portrait_of_two.png')
PRICE = ('token', 6)

item('portrait_painting', 'minecraft:painting', 'Portrait of Two', '#ffcf6a',
     ['Two faces the Fence won\'t name.', 'Pixels, gilt and a little mystery.', ('Hang it on a wall: 5 blocks wide, 4 tall.', 'blue')],
     stack=16, cat='fun', comps={'minecraft:painting/variant': VARIANT})


def extend_offers(O, offer):
    O['fence'].append(offer(PRICE, ('portrait_painting', 1)))


def generate(G):
    fn = G.fn
    G.wjson('bm/painting_variant/portrait.json', {'asset_id': VARIANT, 'width': W, 'height': H,
                                                  'title': T('Portrait of Two', '#ffcf6a'), 'author': T('from the Fence\'s back room', 'gray')})
    # a painting taken down drops a plain painting (the game forgets its picture) - so each portrait hung gets a marker, and when
    # it comes down its drop is made the portrait again (every 5 ticks: before the drop can be picked up, half a second)
    fast = G.FUNCS['loop/fast']
    fast[-1:-1] = ['execute as @e[type=minecraft:painting,tag=!bm.ptseen] at @s run function bm:p146/seen',
                   f'execute as @e[type=minecraft:marker,tag=bm.ptm] at @s unless entity @e[type=minecraft:painting,distance=..0.3,nbt={{variant:"{VARIANT}"}}] run function bm:p146/down']
    fn('p146/seen', ['tag @s add bm.ptseen', f'execute if data entity @s {{variant:"{VARIANT}"}} run summon minecraft:marker ~ ~ ~ {{Tags:["bm.ptm"]}}'])
    fn('p146/down', ['execute as @e[type=minecraft:item,distance=..3,nbt={Item:{id:"minecraft:painting"}},nbt=!{Item:{components:{}}},limit=1,sort=nearest] '
                     'run loot replace entity @s contents loot bm:items/portrait_painting',
                     'kill @s'])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:marker,tag=bm.ptm]')


def rp(R):
    def post(R2):
        from PIL import Image
        Image.open(SRC).convert('RGBA').save(R2.p('assets', 'bm', 'textures', 'painting', 'portrait.png'))
    R.POST.append(post)
