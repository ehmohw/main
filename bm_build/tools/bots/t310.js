// 2.97: THE PALE DRYAD (phase236) as a regular (non-op) player - the owner's checklist (rigpet_t): in a Pale Garden at night she sits
// up in the moss (rcon places her); empty-handed she'd like a mushroom; given one she's yours (A Glowing Mushroom). SWIPE; SPORES
// (two foes: poisoned, slowed); ROOTS (held fast); HEAL (you hurt in a fight: Regeneration II); BLOOM (out of a fight); and by
// night she GLOWS (her night loop). Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
const fs = require('fs');
runT({ W: 'dryad', NAME: 'The Pale Dryad', ab: 'py', q: 'qd', pfx: 'p236p', prefix: 'pd_', item: 'dryad_cap', parts: 15, figParts: 15, hp: 28, X: 17900, Z: 16000, pron: 'her',
  called: /pitter-patters back to you/, home: /sinks back into the moss/, sit: /ring of mushrooms/, stand: /Up we go/,
  ways: ['Swipe', 'Spores', 'Roots', 'Heal', 'Bloom', 'Night Glow'], plain: 'Pale Garden blue', looks: ['Toadstool Cap', 'Violet Cap', 'Amber Cap'],
  encounter: async (ctx) => {
    const K = kit(ctx, 'qd');
    await ctx.run('time set midnight');
    const r = await K.meet(ctx, 'p236p/enc/place', /like mushrooms/, 'minecraft:red_mushroom', /starts to glow/, 'dryad_cap');
    ctx.ok('in the pale moss at night, a little mushroom-capped girl sits up (her rig and a click box)', r.placed);
    K.showOks(ctx.ok, r, "The Pale Dryad's entrance", null);
    ctx.ok('right-clicked empty-handed: she\'d like a mushroom', r.asked, r.lastBar);
    ctx.ok('right-clicked holding a mushroom: her glowing mushroom given', r.got && !/Found [1-9]/.test(await ctx.run('clear TestRat minecraft:red_mushroom 0')), r.chat);
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait } = ctx; const K = kit(ctx, 'qd');
    ok('SWIPE - a foe at her side: swiped', await K.move('mc', [[1.5, 0]], 'bm.trpw', async () => (await K.hp('bm.trpw')) < 300));
    ok('SPORES - two foes near: spored - hurt and slowed (the undead shrug off the poison)', await K.move('k2', [[2, 0], [-2, 1]], 'bm.trps', async () => (await K.hp('bm.trps')) < 300 && /slowness/.test(await K.fxOf('bm.trps'))));
    ok('ROOTS - a foe near: roots burst up - hurt, held fast', await K.move('gc', [[3, 1]], 'bm.trpr', async () => (await K.hp('bm.trpr')) < 300 && /slowness[^}]*amplifier: ?4b|amplifier: ?4b[^}]*slowness/.test(await K.fxOf('bm.trpr')), 9000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat');
    await run('damage TestRat 6 minecraft:generic'); await ctx.zom(0, 8, 'bm.trph'); await K.cd('sc', 0);
    ok('HEAL - you hurt, a foe about: Regeneration II', await wait(6000, async () => /regeneration[^}]*amplifier: ?1b|amplifier: ?1b[^}]*regeneration/.test(await fx())), await fx());
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await K.cd('k', 0);
    ok('BLOOM - out of a fight beside you: Regeneration', await wait(6000, async () => /regeneration/.test(await fx())));
    const DP = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function';
    ok('NIGHT GLOW - by night, her glow loop runs each second', /bm\.pypet[^\n]*p236\/night[^\n]*p236p\/glow/.test(fs.readFileSync(`${DP}/loop/second.mcfunction`, 'utf8')) &&
       /dust\{color:\[0\.4,0\.66,1\.0\]/.test(fs.readFileSync(`${DP}/p236p/glow.mcfunction`, 'utf8')));
    await K.calm(); await run('time set noon');
  } });
