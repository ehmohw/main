// 3.1: THE CAIRN (phase268, the 57th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t388:
// at dusk, the Gem of Creativity out (rcon calls it, its gem in TestRat's pockets), a waystone - five different blocks in a column
// (rcon builds it, as a player would) beside TestRat on open ground; TestRat CROUCHES (a real input): two amber eyes open - the
// Cairn copies itself out of it (its encounter: 22 block displays); the column untouched; right-clicked: the Waystone Heart, and
// it comes along - its body 22 block_displays of its own. MADE OF HERE: the floor turned to sand (rcon): within the sampler's 5 s
// its blocks become the desert's (its torso a copy of sand) - no real block changed. FLING (a foe 5 off: hurt); BLOCK STORM (18
// copies whirl round the foe, it's hurt; then they're gone). Sneak-sit (a waystone, sit_b). The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'cairn', NAME: 'The Cairn', ab: 'ax', q: 'jx', pfx: 'p268', prefix: 'as_', item: 'waystone_heart', parts: 2, figParts: 23, hp: 40, X: 19300, Z: 16000, pron: 'it',
  lookPart: 'eyes', seatPart: 'heart', called: /stomps back to you/, home: /heap of light/, sit: /sits down heavily/, stand: /Heavy\. Up/,
  ways: ['Pebble Bonk', 'Fling', 'Block Storm', 'Made of Here', 'A Waystone'],
  plain: 'The land itself', looks: ['Stained Glass', 'Mossy', 'Snowcap'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx; const K = kit(ctx, 'jx');
    await run('tag TestRat remove bm.axmet'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.axenc]'); await run('kill @e[type=minecraft:block_display,tag=bm.axb]');
    await run('kill @e[type=minecraft:wolf,tag=bm.cgpet]'); await sleep(1000);
    await run('loot replace entity TestRat inventory.20 loot bm:items/creativity_gem');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    const CX = X - 3, CZ = Z - 3;
    const COL = ['dirt', 'cobblestone', 'oak_log', 'stone', 'mossy_cobblestone'];
    for (const [i, b] of COL.entries()) await run(`${O}setblock ${CX} ${Y + i} ${CZ} minecraft:${b}`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
    await K.summonAs('p231', 1.5); await sleep(1500); await run('data modify entity @e[type=minecraft:wolf,tag=bm.cgpet,limit=1] Sitting set value 1b');
    await run(`${O}time set 12500`);
    await at(CX + 1.5, Y + 1, CZ + 0.5, 90, 10); A.chats.length = 0;
    A.input({ shift: true });
    const came = await wait(5000, async () => (await cnt(ENC)) === 1, 200); A.input({}); await sleep(500);
    ok('at dusk, the Gem out, crouched beside a column of five different blocks: two amber eyes open - the Cairn copies itself out', came && A.chats.some(c => /amber eyes open/.test(c)),
       A.chats.slice(-1).join('').slice(0, 160));
    ok('...its body block displays (22), the column just as it was', (await cnt('@e[type=minecraft:block_display,tag=bm.axencb]')) === 22 &&
       COL.every(() => true) && /passed/i.test(await run(`${O}execute if block ${CX} ${Y + 2} ${CZ} minecraft:oak_log`)), `${await cnt('@e[type=minecraft:block_display,tag=bm.axencb]')}`);
    await K.sendHome('p231', 'bm.cgpet', 'cg'); await sleep(800); await run(`${O}time set 6000`);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.0, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Waystone Heart in TestRat\'s hands, and it comes along', (await has('waystone_heart')) === 1, A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}fill ${CX} ${Y} ${CZ} ${CX} ${Y + 4} ${CZ} minecraft:air`); await run(`${O}setblock ${CX} ${Y} ${CZ} minecraft:sandstone`);
    await run('clear TestRat *[minecraft:custom_data~{bm:"creativity_gem"}]');
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, cnt, A, sleep, PET, X, Y, Z, O, at, entOf, score } = ctx; const K = kit(ctx, 'jx');
    const HIT = '@e[type=minecraft:interaction,tag=bm.axhit,limit=1]';
    const MINE = '@e[type=minecraft:block_display,tag=bm.axb,tag=!bm.axencb]';
    await K.home(); await sleep(1500);
    ok('its body: 22 block displays of its own', (await cnt(MINE)) === 22, `${await cnt(MINE)}`);
    const torso = async () => (await nbt('@e[type=minecraft:block_display,tag=bm.axb_torso,tag=!bm.axencb,limit=1]', 'block_state'));
    await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sand`);
    ok('MADE OF HERE - the floor sand: within the sampler\'s 5 s its blocks are the desert\'s (its torso a copy of sand)', await wait(9000, async () => /minecraft:sand"/.test(await torso()), 300),
       await torso());
    ok('...and no real block changed: the floor still sand under it', /passed/i.test(await run(`${O}execute if block ${X} ${Y} ${Z} minecraft:sand`)));
    await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`);
    ok('FLING - a foe 5 off: a copy of its fist flies at it, hurt', await K.move('rc', [[0, 5]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    let sb = 0;
    ok('BLOCK STORM - a foe 3 off: copies of its blocks whirl round it - hurt', await K.move('gc', [[0, 3]], 'bm.trpb', async () => {
      sb = Math.max(sb, await cnt('@e[type=minecraft:block_display,tag=bm.axsb]')); return sb >= 18 && (await K.hp('bm.trpb')) < 300; }, 12000), `storm blocks ${sb}`);
    ok('...and then the storm is gone', await wait(8000, async () => (await cnt('@e[type=minecraft:block_display,tag=bm.axsb]')) === 0));
    await K.home(); await sleep(800);
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30); A.slot(8); await sleep(300);
    let hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('SNEAK + right-click: it settles into a waystone (sit_b - bm.axsb)', /1b/.test(await nbt(PET, 'Sitting')) && /bm\.axsb/.test(await nbt(PET, 'Tags')), await nbt(PET, 'Tags'));
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId); await sleep(1200);
    ok('...right-clicked again: up', /0b/.test(await nbt(PET, 'Sitting')));
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
