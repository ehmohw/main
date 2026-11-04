// 3.1: THE SPAWNER (phase267, the 56th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t388:
// a monster spawner set down by rcon (a dungeon's, as it were); a Soul Lantern PLACED beside it (a real block placement): "three
// waves are coming" (the vigil); each wave there, then cleared (rcon kills the vigil's own monsters - the fighting isn't under test);
// after the third: its pilot light hops out (the encounter); right-clicked: the Pilot Light, and it comes along. The spawner block
// still there. FEEDING: string handed to it (a right-click holding it): spent, bm.nzfd 2, its ember violet (sw_core_s). CONJURE:
// a foe near - a SPIDER minion (a display, its own), the foe hurt; sent home: its minions gone. Sneak-sit (sit_b). The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'spawner', NAME: 'The Spawner', ab: 'nx', q: 'nz', pfx: 'p267', prefix: 'sw_', item: 'pilot_light', parts: 10, figParts: 7, hp: 30, X: 19260, Z: 16000, pron: 'it',
  lookPart: 'body', seatPart: 'flame', called: /clanks back to you/, home: /dims to a pilot light/, sit: /settles, feet tucked/, stand: /Who needs a friend/,
  ways: ['Conjure', 'Zombie minions', 'Spider minions', 'Blaze minions', 'Pop', 'Pilot Light'],
  plain: 'Old iron', looks: ['Oxidised', 'Amethyst', 'Soot Black'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx;
    await run('tag TestRat remove bm.nxmet'); await run('clear TestRat'); await run('kill @e[type=minecraft:marker,tag=bm.nxvig]'); await run('kill @e[type=minecraft:interaction,tag=bm.nxenc]');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    const SX = X + 3, SZ = Z + 3;
    await run(`${O}setblock ${SX} ${Y + 1} ${SZ} minecraft:spawner`);
    await at(SX + 0.5, Y + 1, SZ - 1.5, 0, 30);
    await run('item replace entity TestRat hotbar.5 with minecraft:soul_lantern'); A.slot(5); await sleep(400); A.chats.length = 0;
    A.useOn(SX + 1, Y, SZ, 1); await sleep(1500);                    // (on the floor beside the spawner: the top face of the block east of it)
    ok('a Soul Lantern placed beside a monster spawner: "three waves are coming" (the vigil)', A.chats.some(c => /three waves are coming/.test(c)) &&
       (await cnt('@e[type=minecraft:marker,tag=bm.nxvig]')) === 1, A.chats.slice(-1).join('').slice(0, 160));
    let waves = 0;
    for (let w = 1; w <= 3; w++) {
      const came = await wait(8000, async () => (await cnt('@e[tag=bm.nxwv]')) >= 1, 250);
      if (came) waves++;
      await sleep(500); await run(`${O}kill @e[tag=bm.nxwv]`);
    }
    ok('...three waves came (and were held)', waves === 3, `${waves}`);
    ok('...after the third: its pilot light hops out (the encounter)', await wait(8000, async () => (await cnt(ENC)) === 1));
    ok('...the spawner block untouched', /passed/i.test(await run(`${O}execute if block ${SX} ${Y + 1} ${SZ} minecraft:spawner`)));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.0, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Pilot Light in TestRat\'s hands, and it comes along', (await has('pilot_light')) === 1, A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}setblock ${SX} ${Y + 1} ${SZ} minecraft:air`); await run(`${O}setblock ${SX + 1} ${Y + 1} ${SZ} minecraft:air`);
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, cnt, A, sleep, PET, X, Y, Z, at, entOf, score } = ctx; const K = kit(ctx, 'nz');
    const CORE = '@e[type=minecraft:item_display,tag=bm.nxp_pet,tag=bm.nxp_core,tag=!bm.nxfade,limit=1]';
    const HIT = '@e[type=minecraft:interaction,tag=bm.nxhit,limit=1]';
    await K.home(); await sleep(800);
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30);
    await run('item replace entity TestRat hotbar.8 with minecraft:string'); A.slot(8); await sleep(400);
    let hb = await entOf(HIT); A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1500);
    ok('FEEDING - string handed to it: spent, SPIDER minions (bm.nzfd 2), its ember violet (sw_core_s)', (await score('bm.nzfd')) === 2 &&
       +(((await run('clear TestRat minecraft:string 0')).match(/Found (\d+)/) || [0, 0])[1]) === 0 && /sw_core_s/.test(await nbt(CORE, 'item.components."minecraft:item_model"')),
       `${await nbt(CORE, 'item.components."minecraft:item_model"')} | ${A.chats.slice(-1).join('').slice(0, 120)}`);
    await run(`data modify entity ${PET} Sitting set value 0b`);
    let mins = 0;
    ok('CONJURE - a foe 4 off: its ghost minions come (spiders) - and the foe is hurt', await K.move('sc', [[0, 4]], 'bm.trpa', async () => {
      mins = Math.max(mins, await cnt('@e[type=minecraft:item_display,tag=bm.nxm_spider]')); return mins >= 1 && (await K.hp('bm.trpa')) < 300; }, 12000), `minions ${mins}`);
    await sleep(1500);
    ok('...minions are displays (no loot, no fire): none left once their foe is gone and they\'ve popped', await (async () => { await run(`${ctx.O}kill @e[tag=bm.trpz]`);
      return ctx.wait(9000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.nxmin]')) === 0); })());
    await K.home(); await sleep(800);
    const x2 = await num(PET, 'Pos[0]'), z2 = await num(PET, 'Pos[2]');
    await at(x2 + 0.5, Y + 1, z2 - 1.8, 0, 30); A.slot(7); await sleep(300);
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('SNEAK + right-click: turned down to a pilot light (sit_b - bm.nxsb)', /1b/.test(await nbt(PET, 'Sitting')) && /bm\.nxsb/.test(await nbt(PET, 'Tags')), await nbt(PET, 'Tags'));
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('...right-clicked again: up', /0b/.test(await nbt(PET, 'Sitting')));
    await run('scoreboard players set TestRat bm.nzfd 0'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
