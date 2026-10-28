// 2.98: THE BOUND SOVEREIGN (phase239) as a regular (non-op) player - the owner's checklist (rigpet_t): its Eye comes from the Dread
// Sovereign's ashes (the stage: its fall's reward, run for TestRat - t312 fights it for real); then CLEAVE, EYE BOLT (withering), CHAINS
// (held fast), DREAD WARD (you hurt in a fight: Resistance, Absorption), VIGIL (out of a fight: Night Vision, Fire Resistance) and THE DREAD
// BOW (the Dread near it weakened). Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'sovereign', NAME: 'The Bound Sovereign', ab: 'xv', q: 'xq', pfx: 'p239', prefix: 'ds_', item: 'sov_eye', parts: 19, figParts: 18, hp: 60, X: 18100, Z: 16000, pron: 'him',
  lookModel: 'ds_body_a',
  called: /strides back to your side/, home: /draws? it away into the dark/, sit: /knight at a vigil/, stand: /As you will/,
  ways: ['Cleave', 'Eye Bolt', 'Chains', 'Dread Ward', 'Vigil', 'The Dread Bow'], plain: 'Void plate', looks: ['Bone Plate', 'Ashen Plate', 'Dawn Plate'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep } = ctx;
    await run('scoreboard players set #hard bm.cfg 1'); await run('tag TestRat remove bm.svfirst'); await run('scoreboard players set TestRat bm.svwin 0'); await run('clear TestRat');
    A.chats.length = 0;
    await run('execute as TestRat at @s run function bm:p238/reward');
    await sleep(800);
    ok('the Sovereign falls: its Eye is in the ashes (hard mode, the first time)', (await has('sov_eye')) === 1);
    ok('...with the Dread Ember and its record', (await has('dread_ember')) === 1 && (await has('music_disc_sovereign')) === 1);
    ok('...and the reckoning: bm.dfin (the Lightbringer is no longer to be found)', /bm\.dfin/.test(await run('tag TestRat list')));
    await run('execute as TestRat at @s run function bm:p238/reward'); await sleep(500);
    ok('a second fall: no second Eye, but Aurel\'s record', (await has('sov_eye')) === 1 && (await has('music_disc_aurel')) === 1);
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait } = ctx; const K = kit(ctx, 'xq');
    ok('CLEAVE - a foe at its side: cleft', await K.move('mc', [[2, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300));
    ok('EYE BOLT - a foe at range: hurt, withering', await K.move('rc', [[0, 9]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300 && /wither/.test(await K.fxOf('bm.trpb')), 9000));
    ok('CHAINS - a foe near: chained - hurt, held fast', await K.move('gc', [[4, 2]], 'bm.trpn', async () => (await K.hp('bm.trpn')) < 300 && /slowness[^}]*amplifier: ?3b|amplifier: ?3b[^}]*slowness/.test(await K.fxOf('bm.trpn')), 9000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat');
    await run('damage TestRat 6 minecraft:generic'); await ctx.zom(0, 8, 'bm.trpw'); await K.cd('sc', 0);
    ok('DREAD WARD - you hurt, a foe about: Resistance and Absorption', await wait(6000, async () => /resistance/.test(await fx()) && /absorption/.test(await fx())), await fx());
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await K.cd('k', 0);
    ok('VIGIL - out of a fight beside you: Night Vision and Fire Resistance', await wait(6000, async () => /night_vision/.test(await fx()) && /fire_resistance/.test(await fx())));
    await ctx.zom(3, 3, 'bm.trpd'); await run('execute in minecraft:overworld run tag @e[tag=bm.trpd] add bm.dread');
    ok('THE DREAD BOW - a Dread near it: weakened', await wait(4000, async () => /weakness/.test(await K.fxOf('bm.trpd'))));
    await K.calm();
  } });
