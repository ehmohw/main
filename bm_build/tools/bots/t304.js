// 2.97: THE DOODLE DRAGON (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): Kettle's crayon drawing climbs
// off the page (rcon places him, as walking with Kettle would); asked empty-handed he wants crayons; given a dye he's yours (Kettle's
// Dragon Drawing). CLAW; CRAYON FIRE (a foe 6 off: hurt and set alight); STOMP (two foes near: slowed); BIG BLAZE (hurt, alight);
// WARM (out of a fight: Fire Resistance for you). Then the shared list.
// 3.0a: HOW HE'S MET - with Kettle and the Gem of Creativity out (rcon summons them, TestRat's own), a dye handed to Kettle (a right-
// click holding it; without the Gem only a hint, the dye kept): the Gem brings the drawing to life - his entrance, quiet till it's over - and
// right-clicked, he comes along.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'dragon', NAME: 'The Doodle Dragon', ab: 'dd', q: 'dz', pfx: 'p235d', prefix: 'dd_', item: 'doodle_drawing', parts: 12, figParts: 9, hp: 34, X: 17300, Z: 16000, pron: 'him',
  called: /scrambles back to you/, home: /folds himself back into a drawing/, sit: /curls up like a cat/, stand: /Adventure/,
  ways: ['Claw', 'Crayon Fire', 'Stomp', 'Big Blaze', 'Warm'], plain: 'Ender black', looks: ['Fire-Red Scales', 'Ocean-Blue Scales', 'Sunset-Purple Scales'],
  encounter: async (ctx) => {
    // (3.0a) THE GEM BRINGS IT TO LIFE - handed something as a regular player; its entrance; right-clicked: it comes along
    const K = kit(ctx, 'dz');
    const o = { name: 'The Doodle Dragon', host: 'p227', hostAb: 'kt', hostTag: 'bm.ktpet', hostName: 'Kettle', gem: true, item: 'minecraft:green_dye',
      noGemRe: /if only something could bring it to life/, bornRe: /scribbles in the air/, joined: /hands you his drawing/, itemId: 'doodle_drawing',
      props: 'a pencil (a prop) drawing him in the air' };
    const r = await K.born(o); K.bornOks(ctx.ok, r, o);
  },
  abilities: async (ctx) => {
    const { ok, nbt, O, run } = ctx; const K = kit(ctx, 'dz');
    ok('CLAW - a foe at his side: clawed', await K.move('mc', [[1.5, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300));
    ok('CRAYON FIRE - a foe 6 off: crayon fire, hurt and alight', await K.move('rc', [[0, 6]], 'bm.trpf', async () => (await K.hp('bm.trpf')) < 300 && +((await nbt('@e[tag=bm.trpf,limit=1]', 'Fire')).match(/(-?\d+)/) || [0, -1])[1] > 0));
    ok('STOMP - two foes close: stomped, slowed', await K.move('k2', [[2, 0], [-2, 1]], 'bm.trps', async () => /slowness/.test(await K.fxOf('bm.trps')) && (await K.hp('bm.trps')) < 300));
    ok('BIG BLAZE - a foe 5 off: a long breath, hurt and alight', await K.move('gc', [[0, 5]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 290 && +((await nbt('@e[tag=bm.trpb,limit=1]', 'Fire')).match(/(-?\d+)/) || [0, -1])[1] > 0, 9000));
    await K.home(); await ctx.at(ctx.X + 0.5, ctx.Y + 1, ctx.Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await K.cd('k', 0);
    ok('WARM - out of a fight beside you: Fire Resistance for you', await ctx.wait(6000, async () => /fire_resistance/.test(await ctx.fx())));
    await K.calm();
    // ---- (3.0a) CRAYON GREEN - the Doodle ENDER Dragon's OG look, a costume row in his wardrobe (rigpet's FORM_WARDROBE, bm.ddog on the
    //      owner), chosen as a player would - sneak + use the drawing, Wardrobe, "Crayon Green": his parts wear their _og twins; and back
    const { A, sleep, cnt, score } = ctx;
    const part = (p) => `@e[type=minecraft:item_display,tag=bm.ddp_pet,tag=!bm.ddfade,tag=bm.ddp_${p},limit=1]`;
    const mdl = async (p) => (await nbt(part(p), 'item.components."minecraft:item_model"')).replace(/"/g, '');
    const row = () => A.buttons().find(b => /Crayon Green/.test(b.label));
    await run('scoreboard players set TestRat bm.ddog 0');
    await ctx.sneakMenu(0); const wd = await A.press(/Wardrobe/);
    ok('CRAYON GREEN - his wardrobe has the costume row: "Crayon Green  off"', wd && row() && /off/.test(row().label), A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/Crayon Green/); await sleep(1200);
    ok('...chosen: bm.ddog 1 - his body, head and wings wear their _og twins (dd_body_og, dd_wingr_og)', (await score('bm.ddog')) === 1 &&
       /^bm:dd_body_og(_c\d+)?$/.test(await mdl('body')) && /^bm:dd_wingr_og(_c\d+)?$/.test(await mdl('wingr')) && /_og(_c\d+)?$/.test(await mdl('head')),
       `${await mdl('body')} / ${await mdl('head')} / ${await mdl('wingr')}`);
    ok('...he scribbles himself over in green (his line)', A.bars.some(b => /scribbles himself over in green/.test(b)), A.bars.slice(-1).join(''));
    await ctx.sneakMenu(0); await A.press(/Wardrobe/); A.bars.length = 0; await A.press(/Crayon Green/); await sleep(1200);
    ok('...and back: bm.ddog 0, black crayon again (dd_body, dd_wingr)', (await score('bm.ddog')) === 0 &&
       /^bm:dd_body(_c\d+)?$/.test(await mdl('body')) && /^bm:dd_wingr(_c\d+)?$/.test(await mdl('wingr')) && A.bars.some(b => /back to black crayon/.test(b)),
       `${await mdl('body')} / ${await mdl('wingr')} | ${A.bars.slice(-1).join('')}`);
    await ctx.wait(1000, async () => (await cnt(ctx.PET)) === 1);
  } });
