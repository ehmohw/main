// 3.1: THE GLITCH (phase264, the 53rd follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t384:
// TestRat's 8-bit trio out (rcon calls them, their cartridges in its pockets, as walking with them would); a Glitched Cartridge
// USED (a real use) - the screen tears: "H3LL0 PL4YER 0NE", the cartridge spent, the Glitch's encounter in front; the trio sent home
// (the cap is three); the Glitch right-clicked: A Cracked Cartridge, and it comes along. Its ways: PUNCH, TELEPORT-STUTTER (it
// blinks to a foe 5 off - afterimages and the RGB split seen on the way), CORRUPT (the ERR cage round the foe, weakened and
// slowed), SEGFAULT (foes near hurt). HOW IT MOVES: its poses SNAP (interpolation 0 on its idle frames - only its sitting eases).
// SITTING TWO WAYS: right-click (sit_a), SNEAK + right-click (sit_b, bm.gxsb). Then the shared list (menu, sitting, wardrobe -
// the CRT Bezel looks, aura, contract, frame, display case, Cecil's doll, fainting).
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
const TRIO = [['p213e', 'bm.xmpet', 'xm', 'cart_emma'], ['p213l', 'bm.xlpet', 'xl', 'cart_leo'], ['p213c', 'bm.xcpet', 'xc', 'cart_cecil']];
runT({ W: 'glitch', NAME: 'The Glitch', ab: 'gx', q: 'gz', pfx: 'p264', prefix: 'gl_', item: 'glitch_rom', parts: 11, figParts: 9, hp: 34, X: 19100, Z: 16000, pron: 'it',
  lookPart: 'head', called: /skips three frames/, home: /rewinds itself out of existence/, sit: /happy little heap of pixels/, stand: /C0NT1NU3/,
  ways: ['Punch', 'Teleport-Stutter', 'Corrupt', 'SEGFAULT', 'Never Smooth'],
  plain: 'Midnight plastic', looks: ['Beige 1989', 'Clear Purple', 'Atomic Teal'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z, use, score } = ctx; const K = kit(ctx, 'gz');
    await run('tag TestRat remove bm.gxmet'); await run('clear TestRat'); await run(`kill @e[type=minecraft:interaction,tag=bm.gxenc]`);
    for (const [, tag] of TRIO) await run(`kill @e[type=minecraft:wolf,tag=${tag}]`);
    for (const [i, [, , , it]] of TRIO.entries()) await run(`loot replace entity TestRat inventory.${20 + i} loot bm:items/${it}`);
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
    for (const [i, [pfx, tag]] of TRIO.entries()) { await K.summonAs(pfx, -2 + 2 * i); await sleep(900); await run(`data modify entity @e[type=minecraft:wolf,tag=${tag},limit=1] Sitting set value 1b`); }
    ok('the stage: 8-Bit Emma, Leo and Cecil out - TestRat\'s own', (await cnt('@e[type=minecraft:wolf,tag=bm.xmpet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.xlpet]')) === 1 &&
       (await cnt('@e[type=minecraft:wolf,tag=bm.xcpet]')) === 1);
    // ---- a Glitched Cartridge, used (a real item use, facing south - away from the trio)
    await at(X + 0.5, Y + 1, Z + 0.5, 180, 10);
    await run('loot replace entity TestRat hotbar.4 loot bm:items/glitch_cart'); await sleep(400);
    await wait(3000, async () => !((await score('bm.gvhc')) > 0));
    A.chats.length = 0; await use(4); await sleep(800);
    ok('a Glitched Cartridge used with all three out: the screen tears - "H3LL0 PL4YER 0NE"', A.chats.some(c => /H3LL0 PL4YER 0NE/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    ok('...the cartridge spent, the Glitch there (its encounter)', (await has('glitch_cart')) === 0 && await wait(3000, async () => (await cnt(ENC)) === 1));
    // ---- the trio home (the cap is three), then the Glitch right-clicked, empty-handed
    for (const [pfx, tag, ab] of TRIO) await K.sendHome(pfx, tag, ab); await sleep(800);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez + 2.5, 180, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: "%%THANK Y0U%%" - A Cracked Cartridge in TestRat\'s hands', (await has('glitch_rom')) === 1 && A.chats.some(c => /THANK Y0U/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    for (const [, , , it] of TRIO) await run(`clear TestRat *[minecraft:custom_data~{bm:"${it}"}]`);
    await run('clear TestRat *[minecraft:custom_data~{bm:"glitch_rom"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/glitch_rom');
  },
  abilities: async (ctx) => {
    const { ok, run, wait, cnt, num, nbt, A, sleep, PET, X, Y, Z, at, entOf } = ctx; const K = kit(ctx, 'gz');
    const HEAD = '@e[type=minecraft:item_display,tag=bm.gxp_pet,tag=bm.gxp_head,limit=1]';
    await K.home(); await sleep(1500);
    ok('HOW IT MOVES: its poses snap - an idle frame lands with no interpolation', await wait(5000, async () => /^0$/.test((await nbt(HEAD, 'interpolation_duration')).trim()), 100),
       await nbt(HEAD, 'interpolation_duration'));
    ok('PUNCH - a foe in reach: hurt', await K.move('mc', [[0, 2]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 6000));
    let fx = 0;
    ok('TELEPORT-STUTTER - a foe 5 off: it blinks over and punches (hurt)', await K.move('rc', [[0, 5]], 'bm.trpb', async () => { fx = Math.max(fx, await cnt('@e[type=minecraft:item_display,tag=bm.gxfx]'));
      return (await K.hp('bm.trpb')) < 300; }, 8000));
    ok('...on the way, its afterimages and RGB split (bm.gxfx copies)', fx >= 1, `${fx}`);
    let cage = 0;
    ok('CORRUPT - a foe near: the ERR cage round it, weakened and slowed', await K.move('k2', [[0, 3]], 'bm.trpc', async () => { cage = Math.max(cage, await cnt('@e[type=minecraft:item_display,tag=bm.gxcage]'));
      const f = await K.fxOf('bm.trpc'); return /weakness/.test(f) && /slowness/.test(f); }, 8000) && cage >= 1, `cages ${cage}`);
    ok('SEGFAULT - foes near: torn apart, hurt', await K.move('gc', [[1, 1], [-1, 1]], 'bm.trpd', async () => (await K.hp('bm.trpd')) < 300, 8000));
    await K.home(); await sleep(1000);
    // ---- sitting two ways: a right-click (sit_a), a SNEAK + right-click (sit_b - it dozes)
    const HIT = '@e[type=minecraft:interaction,tag=bm.gxhit,limit=1]';
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30); A.slot(8); await sleep(300);
    let hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('SNEAK + right-click: it sits the other way (sit_b - bm.gxsb)', /1b/.test(await nbt(PET, 'Sitting')) && /bm\.gxsb/.test(await nbt(PET, 'Tags')), await nbt(PET, 'Tags'));
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('...right-clicked again: up', /0b/.test(await nbt(PET, 'Sitting')));
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
