// 2.97: THE DOODLE DRAGON (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): Kettle's crayon drawing climbs
// off the page (rcon places him, as walking with Kettle would); asked empty-handed he wants crayons; given a dye he's yours (Kettle's
// Dragon Drawing). CLAW; CRAYON FIRE (a foe 6 off: hurt and set alight); STOMP (two foes near: slowed); BIG BLAZE (hurt, alight);
// WARM (out of a fight: Fire Resistance for you). Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'dragon', NAME: 'The Doodle Dragon', ab: 'dd', q: 'dz', pfx: 'p235d', prefix: 'dd_', item: 'doodle_drawing', parts: 12, figParts: 9, hp: 34, X: 17300, Z: 16000, pron: 'him',
  called: /scrambles back to you/, home: /folds himself back into a drawing/, sit: /curls up like a cat/, stand: /Adventure/,
  ways: ['Claw', 'Crayon Fire', 'Stomp', 'Big Blaze', 'Warm'], plain: "Kettle's own green", looks: ['Fire-Red Scales', 'Ocean-Blue Scales', 'Sunset-Purple Scales'],
  encounter: async (ctx) => {
    const K = kit(ctx, 'dz');
    const r = await K.meet(ctx, 'p235d/enc/place', /crayons/, 'minecraft:green_dye', /sniffs the dye/, 'doodle_drawing');
    ctx.ok('Kettle\'s drawing climbs off the page (his rig and a click box)', r.placed && ctx.A.chats.length >= 0);
    ctx.ok('right-clicked empty-handed: he wants crayons', r.asked, r.lastBar);
    ctx.ok('right-clicked holding a dye: his drawing given - he\'s yours', r.got && !/Found [1-9]/.test(await ctx.run('clear TestRat minecraft:green_dye 0')), r.chat);
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
  } });
