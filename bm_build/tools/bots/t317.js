// 2.99: VEXIS, THE UNLINKED (phase243) as a regular (non-op) player - the owner's checklist (rigpet_t): the Severed Link comes from the
// quiet after Admiral Vexis's fall (the stage: its fall's reward, run for TestRat - t318 fights it for real); then HIVE-GRIP, PLASMA BOLT,
// GRAVITY WELL (held, slowed), DEFLECTOR (you hurt in a fight: Resistance, Absorption), SCOUT DRONE (out of a fight: Night Vision) and THE
// HIVE HESITATES (the Vorn near it slowed and weakened). Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'vexis', NAME: 'Vexis, the Unlinked', ab: 'xb', q: 'qx', pfx: 'p243', prefix: 'vx_', item: 'vexis_link', parts: 20, figParts: 15, hp: 50, X: 18300, Z: 16000, pron: 'it',
  lookModel: 'vx_body_h',
  called: /drifts back to your side/, home: /folds it away into the dark/, sit: /cross-legged/, stand: /learning to rest/,
  ways: ['Hive-Grip', 'Plasma Bolt', 'Gravity Well', 'Deflector', 'Scout Drone', 'The Hive Hesitates'], plain: 'Hive red', looks: ['Hive Mantle', 'Donadian Mantle', 'Starfire Mantle'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep } = ctx;
    await run('scoreboard players set #hard bm.cfg 1'); await run('tag TestRat remove bm.vxfirst'); await run('tag TestRat remove bm.xbwar');
    await run('scoreboard players set TestRat bm.vxwin 0'); await run('clear TestRat');
    A.chats.length = 0;
    await run('execute as TestRat at @s run function bm:p242/reward');
    await sleep(800);
    ok('Vexis falls: the Severed Link is in the quiet (hard mode, the first time)', (await has('vexis_link')) === 1);
    ok('...with its record and the Victor\'s Key', (await has('music_disc_vexis')) === 1 && (await has('akey_victor')) === 1);
    ok('...and it won\'t rise for you again until you attack a Dreadnought (bm.vxdone)', /bm\.vxdone/.test(await run('tag TestRat list')));
    await run('execute as TestRat at @s run function bm:p242/reward'); await sleep(500);
    ok('a second fall: no second Link - but its warframe remembered (bm.xbwar)', (await has('vexis_link')) === 1 && /bm\.xbwar/.test(await run('tag TestRat list')));
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait } = ctx; const K = kit(ctx, 'qx');
    ok('HIVE-GRIP - a foe at its side: struck', await K.move('mc', [[2, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300));
    ok('PLASMA BOLT - a foe at range: hurt', await K.move('rc', [[0, 9]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 9000));
    ok('GRAVITY WELL - a foe near: dragged in - hurt, held slowed', await K.move('gc', [[4, 2]], 'bm.trpn', async () => (await K.hp('bm.trpn')) < 300 && /slowness[^}]*amplifier: ?3b|amplifier: ?3b[^}]*slowness/.test(await K.fxOf('bm.trpn')), 9000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat');
    await run('damage TestRat 6 minecraft:generic'); await ctx.zom(0, 8, 'bm.trpw'); await K.cd('sc', 0);
    ok('DEFLECTOR - you hurt, a foe about: Resistance and Absorption', await wait(6000, async () => /resistance/.test(await fx()) && /absorption/.test(await fx())), await fx());
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await K.cd('k', 0);
    ok('SCOUT DRONE - out of a fight beside you: Night Vision', await wait(6000, async () => /night_vision/.test(await fx())));
    await ctx.zom(3, 3, 'bm.trpd'); await run('execute in minecraft:overworld run tag @e[tag=bm.trpd] add bm.vorn');
    ok('THE HIVE HESITATES - a Vorn near it: slowed and weakened', await wait(4000, async () => /weakness/.test(await K.fxOf('bm.trpd')) && /slowness/.test(await K.fxOf('bm.trpd'))));
    await K.calm();
  } });
