// 2.97: THE INK BLOT (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): a drop off Mr. Capshun's page
// (rcon places it); empty-handed it makes a "?"; given an ink sac it's yours (A Little Ink Pot). PUNCH (a fist); QUILL SPIKE (a foe
// 5 off); SPLASH (two foes: blinded, slowed); INK SHIELD (Resistance II and Absorption for you); WONDER (Luck and Haste).
// 3.0a: HOW IT'S MET - with Mr. Capshun and the Gem of Creativity out (rcon summons them, TestRat's own), an ink sac handed to Mr.
// Capshun (without the Gem only a hint, the ink kept): a drop off his pen, given life by the Gem - its entrance, quiet till it's over - and
// right-clicked, it comes along.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'inkblot', NAME: 'The Ink Blot', ab: 'ib', q: 'iq', pfx: 'p235i', prefix: 'ib_', item: 'ink_pot', parts: 7, figParts: 2, hp: 30, X: 17600, Z: 16000, pron: 'it',
  lookModel: 'ib_body_(?:blot|drop)',   // (a regex: caught mid-hop it's a drop, not a blot)
  called: /slides back to you/, home: /soaks into the ground/, sit: /melts into a puddle/, stand: /gathers itself back up/,
  ways: ['Punch', 'Quill Spike', 'Splash', 'Ink Shield', 'Wonder'], plain: 'Black ink', looks: ['Royal Blue Ink', 'Crimson Ink', 'Emerald Ink'],
  encounter: async (ctx) => {
    // (3.0a) THE GEM BRINGS IT TO LIFE - handed something as a regular player; its entrance; right-clicked: it comes along
    const K = kit(ctx, 'iq');
    const o = { name: 'The Ink Blot', host: 'p198', hostAb: 'mz', hostTag: 'bm.mzpet', hostName: 'Mr. Capshun', gem: true, item: 'minecraft:ink_sac',
      noGemRe: /If only something could bring it to life/, bornRe: /dips his pen in the ink/, joined: /pours itself into a pot/, itemId: 'ink_pot',
      props: 'a drop of ink and a "?" (props) in the show' };
    const r = await K.born(o); K.bornOks(ctx.ok, r, o);
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z } = ctx; const K = kit(ctx, 'iq');
    ok('PUNCH - a foe at its side: a fist', await K.move('mc', [[1.5, 0]], 'bm.trpp', async () => (await K.hp('bm.trpp')) < 300));
    ok('QUILL SPIKE - a foe 5 off: spiked', await K.move('rc', [[0, 5]], 'bm.trpq', async () => (await K.hp('bm.trpq')) < 300));
    ok('SPLASH - two foes near: blinded and slowed', await K.move('k2', [[2, 0], [-2, 1]], 'bm.trps', async () => /blindness/.test(await K.fxOf('bm.trps')) && /slowness/.test(await K.fxOf('bm.trps'))));
    await run('effect clear TestRat');
    ok('INK SHIELD - a foe near: Resistance II and Absorption for you', await K.move('gc', [[3, 1]], 'bm.trpg', async () => /resistance[^}]*amplifier: ?1b|amplifier: ?1b[^}]*resistance/.test(await ctx.fx()) && /absorption/.test(await ctx.fx())));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await K.cd('k', 0);
    ok('WONDER - out of a fight beside you: Luck and Haste', await ctx.wait(10000, async () => /luck/.test(await ctx.fx()) && /haste/.test(await ctx.fx())),
       `a ${await ctx.score('bm.iqa', ctx.PET)} x ${await ctx.score('bm.iqx', ctx.PET)} k ${await ctx.score('bm.iqk', ctx.PET)} s ${await ctx.score('bm.iqs', ctx.PET)} sit ${await ctx.nbt(ctx.PET, 'Sitting')} foes ${await ctx.cnt('@e[tag=bm.trpz]')} fx ${(await ctx.fx()).slice(0, 120)}`);
    await K.calm();
  } });
