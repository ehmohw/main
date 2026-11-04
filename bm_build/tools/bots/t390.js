// 3.1: THE SAPLING (phase266, the 55th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t388:
// by day, Kettle and the Pale Dryad out (rcon calls them, their items in TestRat's pockets); a Golden Apple handed to the Dryad (a
// right-click on her holding it): "A seed with a heartbeat", the apple spent - the golden pip planted at TestRat's feet (the mound);
// the mound right-clicked: "ready in 1 day"; a water bottle used on it: a day sooner (the bottle emptied) - so it sprouts at once:
// the Sprout climbs out (its encounter); right-clicked: the Golden Pip, stage 1 (sp1_ models). Its planting day moved back (rcon -
// the clock): it GROWS - stage 2, then the Tree Spirit (sp3_), its click box taller. Its ways: ROOTSNARE (slowed), SEED SHOT (hurt),
// GOLDEN SAP (TestRat hurt: Regeneration). Sneak + right-click: it takes root (sit_b). Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'sapling', NAME: 'The Sapling', ab: 'sx', q: 'sz', pfx: 'p266', prefix: 'sp3_', item: 'golden_pip', parts: 14, figParts: 9, hp: 32, X: 19220, Z: 16000, pron: 'it',
  lookPart: 'head', called: /toddles back to you/, home: /sinks into the ground/, sit: /plops down on the grass/, stand: /There's sun over there/,
  ways: ['Rootsnare', 'Seed Shot', 'Golden Sap', 'It Grows', 'Taking Root'],
  plain: 'Summer green', looks: ['Autumn Crown', 'Frost Crown', 'Twilight Crown'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, nbt, ENC, X, Y, Z, score } = ctx; const K = kit(ctx, 'sz');
    for (const t of ['bm.sxmet', 'bm.sxplant', 'bm.sxwet']) await run(`tag TestRat remove ${t}`);
    await run('scoreboard players set TestRat bm.szst 0'); await run('clear TestRat'); await run('kill @e[tag=bm.sxmound]'); await run('kill @e[type=minecraft:interaction,tag=bm.sxenc]');
    await run('kill @e[type=minecraft:wolf,tag=bm.ktpet]'); await run('kill @e[type=minecraft:wolf,tag=bm.pypet]'); await sleep(1200);
    await run('loot replace entity TestRat inventory.20 loot bm:items/kettle_plane'); await run('loot replace entity TestRat inventory.21 loot bm:items/dryad_cap');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await run(`${O}time set 3000`); await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
    await K.summonAs('p227', -1.5); await sleep(1200); await K.summonAs('p236p', 1.5); await sleep(1500);
    await run('data modify entity @e[type=minecraft:wolf,tag=bm.ktpet,limit=1] Sitting set value 1b'); await run('data modify entity @e[type=minecraft:wolf,tag=bm.pypet,limit=1] Sitting set value 1b');
    const HIT = '@e[type=minecraft:interaction,tag=bm.pyhit,limit=1]';
    await run('item replace entity TestRat hotbar.8 with minecraft:golden_apple'); A.slot(8); await sleep(500);
    let hb = await entOf(HIT); A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('a Golden Apple handed to the Pale Dryad, by day, Kettle out: "A seed with a heartbeat" - the apple spent', A.chats.some(c => /seed with a heartbeat/.test(c)) &&
       +(((await run('clear TestRat minecraft:golden_apple 0')).match(/Found (\d+)/) || [0, 0])[1]) === 0, A.chats.slice(-1).join('').slice(0, 160));
    const MB = '@e[type=minecraft:interaction,tag=bm.sxmbox,limit=1]';
    ok('...the golden pip planted at TestRat\'s feet (its mound)', await wait(2000, async () => (await cnt(MB)) === 1));
    await K.sendHome('p227', 'bm.ktpet', 'kt'); await K.sendHome('p236p', 'bm.pypet', 'py'); await sleep(800);
    const mx = await num(MB, 'Pos[0]'), mz = await num(MB, 'Pos[2]');
    await at(mx + 0.5, Y + 1, mz - 1.8, 0, 35);
    let mb = await entOf(MB); A.slot(7); await sleep(300); A.bars.length = 0; if (mb) A.interact(mb.entityId); await sleep(900);
    ok('the mound right-clicked: "It\'s growing - ready in 1 day(s)"', A.bars.some(b => /ready in/.test(b) && /1/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.6 with minecraft:potion[minecraft:potion_contents={potion:"minecraft:water"}]'); A.slot(6); await sleep(400);
    mb = await entOf(MB); A.bars.length = 0; if (mb) A.interact(mb.entityId); await sleep(900);
    ok('...watered (a water bottle on it): "a day sooner", the bottle emptied', A.bars.some(b => /a day sooner/.test(b)) &&
       +(((await run('clear TestRat minecraft:glass_bottle 0')).match(/Found (\d+)/) || [0, 0])[1]) === 1, A.bars.slice(-1).join(''));
    await run('clear TestRat minecraft:glass_bottle');
    ok('...so it sprouts: the mound gone, the Sprout climbing out (its encounter)', await wait(4000, async () => (await cnt(MB)) === 0 && (await cnt(ENC)) === 1));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.0, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await run('item replace entity TestRat hotbar.8 with minecraft:air'); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Golden Pip in TestRat\'s hands - stage 1, a Sprout', (await has('golden_pip')) === 1 && (await score('bm.szst')) === 1, A.chats.slice(-2).join(' | ').slice(0, 200));
    await run('clear TestRat *[minecraft:custom_data~{bm:"kettle_plane"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"dryad_cap"}]');
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, A, sleep, PET, X, Y, Z, at, entOf, fx, score } = ctx; const K = kit(ctx, 'sz');
    const HEAD = '@e[type=minecraft:item_display,tag=bm.sxp_pet,tag=bm.sxp_head,tag=!bm.sxfade,limit=1]';
    const HIT = '@e[type=minecraft:interaction,tag=bm.sxhit,limit=1]';
    const mdl = async () => (await nbt(HEAD, 'item.components."minecraft:item_model"')).replace(/"/g, '');
    ok('a Sprout: its head the Sprout\'s (sp1_head), its host tagged bm.sxs1', /^bm:sp1_head/.test(await mdl()) && /bm\.sxs1/.test(await nbt(PET, 'Tags')), await mdl());
    const h1 = await num(HIT, 'height');
    await run('scoreboard players remove TestRat bm.szpd 2');
    ok('its planting day two back: it GROWS - stage 2, the Sapling (sp2_head)', await wait(4000, async () => (await score('bm.szst')) === 2 && /^bm:sp2_head/.test(await mdl())), await mdl());
    await run('scoreboard players remove TestRat bm.szpd 2');
    ok('...and two more: the Tree Spirit (sp3_head), its click box taller', await wait(4000, async () => (await score('bm.szst')) === 3 && /^bm:sp3_head/.test(await mdl())) &&
       (await num(HIT, 'height')) > h1 + 0.3, `${await mdl()} box ${h1} -> ${await num(HIT, 'height')}`);
    ok('ROOTSNARE - a foe 5 off: roots round it, slowed', await K.move('mc', [[0, 5]], 'bm.trpa', async () => /slowness/.test(await K.fxOf('bm.trpa')), 8000));
    ok('SEED SHOT - a foe 6 off: hurt', await K.move('rc', [[0, 6]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 8000));
    await K.home(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(300);
    await run('damage TestRat 6 minecraft:magic'); await ctx.zom(0, 9, 'bm.trpc'); await K.cd('sc', 0);
    ok('GOLDEN SAP - TestRat hurt, a foe about: Regeneration', await wait(8000, async () => /regeneration/.test(await fx())), await fx());
    await run('effect give TestRat minecraft:resistance 900 4 true'); await K.home(); await sleep(800);
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30); A.slot(8); await sleep(300);
    let hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('SNEAK + right-click: it takes root (sit_b - bm.sxsb)', /1b/.test(await nbt(PET, 'Sitting')) && /bm\.sxsb/.test(await nbt(PET, 'Tags')), await nbt(PET, 'Tags'));
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('...right-clicked again: up', /0b/.test(await nbt(PET, 'Sitting')));
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
