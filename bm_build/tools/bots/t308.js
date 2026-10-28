// 2.97: THE SPEECH BUBBLE (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): Mr. Capshun's narration pops
// up (rcon places it); empty-handed it has nothing to say; given a book and quill (kept) it's yours (A Blank Caption Card). SHOUT
// (BAM!/POW!); ALARM (two foes: they glow, Speed for you); KRAK! ZAP! (foes round it hurt); THINK (Haste II and Luck).
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'speech', NAME: 'The Speech Bubble', ab: 'wb', q: 'wq', pfx: 'p235b', prefix: 'sbb_', item: 'caption_card', parts: 4, figParts: 3, hp: 28, X: 17700, Z: 16000, pron: 'it',
  seatPart: 'body', lookModel: 'sbb_body_speech', called: /hops back beside you/, home: /To be continued/, sit: /thought cloud/, stand: /Next panel/,
  ways: ['Shout', 'Alarm', 'KRAK! ZAP!', 'Think'], plain: 'Plain white', looks: ['Sky Paper', 'Pink Paper', 'Mint Paper'],
  encounter: async (ctx) => {
    const K = kit(ctx, 'wq');
    const r = await K.meet(ctx, 'p235b/enc/place', /nothing to SAY/, 'minecraft:writable_book', /shouts every word/, 'caption_card');
    ctx.ok('Mr. Capshun\'s narration pops up (its rig and a click box)', r.placed);
    ctx.ok('right-clicked empty-handed: nothing to say', r.asked, r.lastBar);
    ctx.ok('right-clicked holding a book and quill: its card given (the book kept)', r.got && /Found 1/.test(await ctx.run('clear TestRat minecraft:writable_book 0')), r.chat);
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z } = ctx; const K = kit(ctx, 'wq');
    ok('SHOUT - a foe at its side: BAM! (or POW!)', await K.move('mc', [[1.5, 0]], 'bm.trps', async () => (await K.hp('bm.trps')) < 300));
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    ok('ALARM - two foes near: "!" - they glow, and Speed for you', await K.move('k2', [[5, 0], [-4, 4]], 'bm.trpa', async () => /glowing/.test(await K.fxOf('bm.trpa')) && /speed/.test(await ctx.fx())));
    ok('KRAK! ZAP! - a foe near: blasted (hurt twice)', await K.move('gc', [[2.5, 0]], 'bm.trpk', async () => (await K.hp('bm.trpk')) <= 290, 10000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await K.cd('k', 0);
    ok('THINK - out of a fight beside you: Haste II and Luck (inspiration)', await ctx.wait(6000, async () => /haste/.test(await ctx.fx()) && /luck/.test(await ctx.fx())));
    await K.calm();
  } });
