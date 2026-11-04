// 3.1: THE HOLLOW STATUE KNIGHT (phase269, the 58th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied
// from t392: a won dread knight statue set up (rcon places it as its own placing would, TestRat's), Pistachio and King Omega out
// (rcon calls them, as TestRat's); TestRat walks up to the statue: Pistachio BARKS, "...Aldous?" - the armour steps down (its
// encounter); right-clicked: the Hollow Knight's Token, and he comes along - two rigs in one (the armour's displays and the
// serpent's, s_). FREED: a Totem of Undying in hand, a golden apple in the pack, Pistachio by - right-clicked: both spent, look 1
// earned (bm.wuknight bit 2) and worn. His ways: THE MACE (hurt), HISS (two foes: slowed), COIL (a foe 5 off: held - Slowness,
// tagged), THE SPIN (hurt). BROKEN: his health under a third - the armour heaped, the serpent out on the ground; then it mends.
// Sneak-sit (the statue stance, sit_b). The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'knight', NAME: 'The Hollow Statue Knight', ab: 'hx', q: 'iz', pfx: 'p269', prefix: 'hk_', item: 'knight_token', parts: 27, figParts: 13, hp: 46, X: 19340, Z: 16000, pron: 'him',
  lookPart: 'chest', lookModel: 'hk_hollow_chest', seatPart: 'head', called: /strides back to you/, home: /his soul withdraws/, sit: /kneels on one knee/, stand: /On my feet/,
  ways: ['The Mace', 'Hiss', 'Coil', 'The Spin', 'Broken', 'Companion Size', 'Freed'],
  plain: 'Palace violet', looks: ['Freed', 'Crimson Guard', 'Verdant Guard'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z, score } = ctx; const K = kit(ctx, 'iz');
    await run('tag TestRat remove bm.hxmet'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.hxenc]');
    await run('kill @e[type=minecraft:interaction,tag=bm.knst]'); await run('kill @e[type=minecraft:item_display,tag=bm.knsd]');
    await run('kill @e[type=minecraft:wolf,tag=bm.pipet]'); await run('kill @e[type=minecraft:wolf,tag=bm.ompet]'); await sleep(1200);
    await run('loot replace entity TestRat inventory.20 loot bm:items/pi_cloche'); await run('loot replace entity TestRat inventory.21 loot bm:items/om_monocle');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    const SX = X + 4, SZ = Z + 4;
    await at(SX + 0.5, Y + 1, SZ - 3.5, 0, 10);
    await run('tag TestRat add bm.placer'); await run(`${O}execute positioned ${SX + 0.5} ${Y + 1} ${SZ + 0.5} run function bm:p245/statue/place_dread`); await run('tag TestRat remove bm.placer');
    ok('a dread knight statue set up - TestRat\'s', (await cnt('@e[type=minecraft:interaction,tag=bm.knst_dread]')) === 1);
    await at(X + 0.5, Y + 1, Z - 6.5, 0, 10);                               // (away from it, while the two are called)
    await K.summonAs('p163/pi', -1.5); await sleep(1200); await K.summonAs('p170', 1.5); await sleep(1500);
    A.chats.length = 0;
    await at(SX + 0.5, Y + 1, SZ - 2.5, 0, 10);                             // (up to the statue: Pistachio and Omega follow)
    await run(`${O}tp @e[type=minecraft:wolf,tag=bm.pipet] ${SX - 1.5} ${Y + 1} ${SZ - 2}`); await run(`${O}tp @e[type=minecraft:wolf,tag=bm.ompet] ${SX + 2.5} ${Y + 1} ${SZ - 2}`);
    const came = await wait(5000, async () => (await cnt(ENC)) === 1, 200);
    ok('by the statue with Pistachio and King Omega: Pistachio BARKS - "...Aldous?" - the armour steps down (the encounter)', came && A.chats.some(c => /BARKS/.test(c) && /Aldous/.test(c)),
       A.chats.slice(-1).join('').slice(0, 160));
    ok('...the statue still there (it stays yours)', (await cnt('@e[type=minecraft:interaction,tag=bm.knst_dread]')) === 1);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.0, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: "Mind the door, Pip" - the Hollow Knight\'s Token in TestRat\'s hands, and he comes along', (await has('knight_token')) === 1 && A.chats.some(c => /Mind the door/.test(c)),
       A.chats.slice(-2).join(' | ').slice(0, 200));
    await run('kill @e[type=minecraft:interaction,tag=bm.knst]'); await run('kill @e[type=minecraft:item_display,tag=bm.knsd]');
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, cnt, A, sleep, PET, X, Y, Z, O, at, entOf, score, has } = ctx; const K = kit(ctx, 'iz');
    await run('scoreboard players set TestRat bm.hxcs 0');
    const HIT = '@e[type=minecraft:interaction,tag=bm.hxhit,limit=1]';
    const D = (p) => `@e[type=minecraft:item_display,tag=bm.hxp_pet,tag=bm.hxp_${p},tag=!bm.hxfade,limit=1]`;
    const scl = async (p) => num(D(p), 'transformation.scale[0]');
    ok('two rigs in one: the armour\'s displays (hk_hollow_chest) and the serpent\'s (hs_head)', /hk_hollow_chest/.test(await nbt(D('chest'), 'item.components."minecraft:item_model"')) &&
       /hs_head/.test(await nbt(D('s_head'), 'item.components."minecraft:item_model"')), await nbt(D('s_head'), 'item.components."minecraft:item_model"'));
    // FREED (Pistachio by: he serves it)
    await K.home(); await sleep(800);
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30);
    await run(`${O}tp @e[type=minecraft:wolf,tag=bm.pipet] ${wx - 1.5} ${Y + 1} ${wz - 1}`);
    await run('item replace entity TestRat hotbar.8 with minecraft:totem_of_undying'); await run('item replace entity TestRat inventory.5 with minecraft:golden_apple');
    A.slot(8); await sleep(400);
    let hb = await entOf(HIT); A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1500);
    const bits = await score('bm.wuknight');
    ok('FREED - a Totem of Undying handed to him, a golden apple in the pack, Pistachio by: both spent, look 1 earned and worn', (bits & 2) === 2 && (await score('bm.coshx')) === 1 &&
       +(((await run('clear TestRat minecraft:totem_of_undying 0')).match(/Found (\d+)/) || [0, 0])[1]) === 0 &&
       +(((await run('clear TestRat minecraft:golden_apple 0')).match(/Found (\d+)/) || [0, 0])[1]) === 0 && A.chats.some(c => /FREED/.test(c)), `bits ${bits} | ${A.chats.slice(-1).join('').slice(0, 120)}`);
    ok('...his plate in the Freed look (hk_hollow_chest_c1)', await wait(3000, async () => /hk_hollow_chest_c1/.test(await nbt(D('chest'), 'item.components."minecraft:item_model"'))),
       await nbt(D('chest'), 'item.components."minecraft:item_model"'));
    await run('scoreboard players set TestRat bm.coshx 0'); await run(`${O}execute as TestRat run function bm:p99/knight_now`);
    await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('THE MACE - a foe 2 off: hurt', await K.move('mc', [[0, 2]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    ok('HISS - two foes 3 off: the serpent out, cold mist - slowed', await K.move('k2', [[1, 3], [-1, 3]], 'bm.trpb', async () => /slowness/.test(await K.fxOf('bm.trpb')), 8000));
    ok('COIL - a foe 5 off: wound round - held (Slowness, tagged bm.hxheld)', await K.move('rc', [[0, 5]], 'bm.trpc', async () => /slowness/.test(await K.fxOf('bm.trpc')) &&
       (await cnt('@e[tag=bm.trpc,tag=bm.hxheld]')) === 1, 8000));
    ok('THE SPIN - a foe 2 off: hurt', await K.move('gc', [[0, 2]], 'bm.trpd', async () => (await K.hp('bm.trpd')) < 300, 8000));
    // BROKEN
    await K.home(); await run(`data modify entity ${PET} Health set value 10f`);
    ok('BROKEN - his health under a third: the armour falls apart (bm.hxbrk), the serpent out on the ground', await wait(4000, async () => /bm\.hxbrk/.test(await nbt(PET, 'Tags'))) &&
       await wait(4000, async () => (await scl('s_head')) > 0.5), `${await nbt(PET, 'Tags')} head ${await scl('s_head')}`);
    await run(`scoreboard players set ${PET} bm.izbk 1`);
    ok('...and when it\'s done the armour stands again, healed', await wait(4000, async () => !/bm\.hxbrk/.test(await nbt(PET, 'Tags')) && (await num(PET, 'Health')) > 20));
    await K.home(); await sleep(800);
    const x2 = await num(PET, 'Pos[0]'), z2 = await num(PET, 'Pos[2]');
    await at(x2 + 0.5, Y + 1, z2 - 1.8, 0, 30); A.slot(7); await sleep(300);
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('SNEAK + right-click: the statue stance (sit_b - bm.hxsb)', /1b/.test(await nbt(PET, 'Sitting')) && /bm\.hxsb/.test(await nbt(PET, 'Tags')), await nbt(PET, 'Tags'));
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('...right-clicked again: up', /0b/.test(await nbt(PET, 'Sitting')));
    // ---- COMPANION SIZE, from his menu (as the Rat King's): the statue knights' size by default; on, host and click box shrink with
    //      the rig - armour and serpent; kept across a send-home; and back
    const SC = async () => num(PET, 'attributes[{id:"minecraft:scale"}].base');
    await run('scoreboard players set TestRat bm.hxcs 0'); await sleep(800);
    ok('COMPANION SIZE - off: the statue knights\' size (host 1.6, click box 3.0 tall, his chest at scale 1)', Math.abs((await SC()) - 1.6) < 0.01 && (await num(HIT, 'height')) > 2.8 &&
       Math.abs((await scl('chest')) - 1.0) < 0.02, `${await SC()} / ${await num(HIT, 'height')} / ${await scl('chest')}`);
    await ctx.sneakMenu(0); A.bars.length = 0; await A.press(/Companion Size/); await sleep(1500);
    ok('...pressed on his menu: on (bm.hxcs 1)', (await score('bm.hxcs')) === 1 && A.bars.some(b => /Companion Size: on/.test(b)), A.bars.slice(-1).join(''));
    ok('...his host (0.9) and click box (1.5 tall, 0.65 wide) shrink with him', Math.abs((await SC()) - 0.9) < 0.01 && Math.abs((await num(HIT, 'height')) - 1.5) < 0.05 &&
       Math.abs((await num(HIT, 'width')) - 0.65) < 0.05, `${await SC()} / ${await num(HIT, 'width')} x ${await num(HIT, 'height')}`);
    ok('...the rig at half size, the serpent with it (chest 0.5, serpent 0.75)', await wait(3000, async () => Math.abs((await scl('chest')) - 0.5) < 0.02) &&
       await (async () => { await run(`data modify entity ${PET} Health set value 10f`); return wait(4000, async () => Math.abs((await scl('s_head')) - 0.75) < 0.03); })(),
       `${await scl('chest')} / ${await scl('s_head')}`);
    await run(`scoreboard players set ${PET} bm.izbk 1`); await sleep(2500);
    await ctx.sneakMenu(0); await A.press(/Send .* home/); await sleep(1500);
    await ctx.use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2500);
    ok('...sent home and called again: still companion-sized', Math.abs((await SC()) - 0.9) < 0.01 && Math.abs((await num(HIT, 'height')) - 1.5) < 0.05);
    await ctx.sneakMenu(0); A.bars.length = 0; await A.press(/Companion Size/); await sleep(1500);
    ok('...and off again: host 1.6, click box 3.0', (await score('bm.hxcs')) === 0 && Math.abs((await SC()) - 1.6) < 0.01 && (await num(HIT, 'height')) > 2.8, A.bars.slice(-1).join(''));
    await K.sendHome('p163/pi', 'bm.pipet', 'pi'); await K.sendHome('p170', 'bm.ompet', 'om');
    await run('clear TestRat *[minecraft:custom_data~{bm:"pi_cloche"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"om_monocle"}]');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
