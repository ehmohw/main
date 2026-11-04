// 3.1: THE CAKE (phase265, the 54th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t384:
// Queen Pearl out (rcon calls her, her pearls in TestRat's pockets); a cake handed to her (a right-click on her holding it) with no
// Chef out - only her hint, the cake kept; the Chef called too, the cake handed again - "I always wanted someone to finish the
// cake", the cake spent, the Cake there; both sent home (the cap is three); the Cake right-clicked: its Candle, and it comes along.
// Its ways: TINY FORK, HOP + BOOP (slowed), LAYER SLAM (hurt, slowed), SPRINKLE SHOWER (TestRat hurt: Regeneration and Speed).
// SITTING TWO WAYS: right-click (sit_a), SNEAK + right-click (sit_b, bm.czsb). Then the shared list (the Flavours: Mint, Lemon,
// Chocolate).
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'cake', NAME: 'The Cake', ab: 'cz', q: 'kz', pfx: 'p265', prefix: 'ck_', item: 'cake_candle', parts: 13, figParts: 9, hp: 30, X: 19140, Z: 16000, pron: 'it',
  lookPart: 'base', seatPart: 'hat', called: /hops back to you/, home: /blows out its own candle/, sit: /plonks down on its plate/, stand: /Places to hop/,
  ways: ['Tiny Fork', 'Hop + Boop', 'Layer Slam', 'Sprinkle Shower', 'A Little Hop'],
  plain: 'Strawberry and vanilla', looks: ['Mint', 'Lemon', 'Chocolate'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx; const K = kit(ctx, 'kz');
    await run('tag TestRat remove bm.czmet'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.czenc]');
    await run('kill @e[type=minecraft:wolf,tag=bm.pqpet]'); await run('kill @e[type=minecraft:wolf,tag=bm.kkpet]'); await sleep(1200);
    await run('loot replace entity TestRat inventory.20 loot bm:items/pq_pearls'); await run('loot replace entity TestRat inventory.21 loot bm:items/chef_ladle');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
    await K.summonAs('p190', 1.5); await sleep(1500);
    await run('data modify entity @e[type=minecraft:wolf,tag=bm.pqpet,limit=1] Sitting set value 1b');
    const HIT = '@e[type=minecraft:interaction,tag=bm.pqhit,limit=1]';
    const held = async () => +(((await run('clear TestRat minecraft:cake 0')).match(/Found (\d+)/) || [0, 0])[1]);
    const give = async () => { await run('item replace entity TestRat hotbar.8 with minecraft:cake'); A.slot(8); await sleep(500);
      const hb = await entOf(HIT); A.bars.length = 0; A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000); return !!hb; };
    ok('a cake handed to Queen Pearl, no Chef out: only her hint ("isn\'t FINISHED"), the cake kept', await give() && A.bars.some(b => /isn't FINISHED/.test(b)) && (await held()) === 1 &&
       (await cnt(ENC)) === 0, A.bars.slice(-1).join(''));
    await K.summonAs('p186', -1.5); await sleep(1500);
    await run('data modify entity @e[type=minecraft:wolf,tag=bm.kkpet,limit=1] Sitting set value 1b');
    ok('...the Chef out too: "I always wanted someone to finish the cake" - the cake spent, the Cake there', await give() && A.chats.some(c => /finish the cake/.test(c)) &&
       (await held()) === 0 && await wait(3000, async () => (await cnt(ENC)) === 1), A.chats.slice(-1).join('').slice(0, 160));
    await K.sendHome('p190', 'bm.pqpet', 'pq'); await K.sendHome('p186', 'bm.kkpet', 'kk'); await sleep(800);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250);
    await run('item replace entity TestRat hotbar.8 with minecraft:air'); A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: "make a wish!" - the Cake\'s Candle in TestRat\'s hands', (await has('cake_candle')) === 1 && A.chats.some(c => /make a wish/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    await run('clear TestRat *[minecraft:custom_data~{bm:"pq_pearls"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"chef_ladle"}]');
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, A, sleep, PET, X, Y, Z, at, entOf, fx } = ctx; const K = kit(ctx, 'kz');
    ok('TINY FORK - a foe in reach: hurt', await K.move('mc', [[0, 2]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 6000));
    ok('HOP + BOOP - a foe near: booped, slowed', await K.move('k2', [[0, 2]], 'bm.trpb', async () => /slowness/.test(await K.fxOf('bm.trpb')), 7000));
    ok('LAYER SLAM - foes near: hurt and slowed', await K.move('gc', [[1, 1], [-1, 1]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300 && /slowness/.test(await K.fxOf('bm.trpc')), 8000));
    // SPRINKLE SHOWER: TestRat hurt, a monster about - a sugar rush
    await K.home(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(300);
    await run('damage TestRat 6 minecraft:magic'); await ctx.zom(0, 9, 'bm.trpd');
    await K.cd('sc', 0);
    ok('SPRINKLE SHOWER - TestRat hurt, a foe about: Regeneration and Speed (a sugar rush)', await wait(8000, async () => { const f = await fx(); return /regeneration/.test(f) && /speed/.test(f); }),
       await fx());
    await run('effect give TestRat minecraft:resistance 900 4 true'); await K.home(); await sleep(800);
    const HIT = '@e[type=minecraft:interaction,tag=bm.czhit,limit=1]';
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30); A.slot(8); await sleep(300);
    let hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('SNEAK + right-click: it dozes (sit_b - bm.czsb)', /1b/.test(await nbt(PET, 'Sitting')) && /bm\.czsb/.test(await nbt(PET, 'Tags')), await nbt(PET, 'Tags'));
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('...right-clicked again: up', /0b/.test(await nbt(PET, 'Sitting')));
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
