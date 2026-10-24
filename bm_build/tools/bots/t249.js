// 2.90: MR. CAPSHUN, the narrator, as a regular (non-op) player - the owner's checklist (rigpet_t): by a hung painting a doodle
// peels off the canvas and steps out; asked empty-handed, he wants colour; given a dye, he joins (his pencil). His fight: BRUSH
// SWIPE (2.94: the brush in his hand, a splash of colour), DRAWN TO LIFE (2.94: the pencil - a sketched bomb, anvil or arrows,
// made real), PAINT SPLAT, SKETCH, WET PAINT, THE RAINBOW STROKE; his support: the PALETTE (his menu) and FRESH COAT; THE STORY
// SO FAR (his menu); NARRATION when you're badly hurt. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'capshun', NAME: 'Mr. Capshun', ab: 'mz', q: 'zq', pfx: 'p198', prefix: 'mz_', item: 'capshun_pencil', parts: 11, hp: 40, X: 17120, Z: 16000, pron: 'him',
  called: /came running|ENTER: MR\. CAPSHUN/, home: /Exit, stage left/, sit: /most relatable thing/, stand: /Back on my feet/,
  ways: ['Fresh Coat', 'Palette', 'Brush Swipe', 'Drawn to Life', 'Paint Splat', 'Sketch', 'Wet Paint', 'The Rainbow Stroke', 'Narration'],
  plain: 'Plain black ink', looks: ['Blue Ballpoint', 'Red Pen', 'Green Marker'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    // (the stage: a wall with a painting on it - and the roll come up; he steps out as he would)
    await run(`${O}fill ${X - 2} ${Y + 1} ${Z + 6} ${X + 2} ${Y + 4} ${Z + 6} minecraft:stone`);
    await run(`${O}summon minecraft:painting ${X} ${Y + 2} ${Z + 5} {facing:2b,variant:"minecraft:kebab",Tags:["bm.trpz"]}`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    ok('the stage: a painting hung on the wall', (await cnt(`@e[type=minecraft:painting,x=${X},y=${Y + 2},z=${Z + 5},distance=..3]`)) === 1);
    await run(`${O}execute as @e[type=minecraft:painting,x=${X},y=${Y + 2},z=${Z + 5},distance=..3,limit=1] at @s rotated as @s positioned ^ ^ ^1 run function bm:p198/enc/drop1`);
    ok('by the painting: a doodle peels off the canvas and steps out (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.mzencp]')) === 11 && A.chats.some(c => /peels itself off the painting/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: he would love a bit of colour', A.bars.some(b => /a dye would do wonders/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.8 with minecraft:blue_dye'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding a dye: the dye taken, his pencil given', (await has('capshun_pencil')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:blue_dye 0')) &&
       A.chats.some(c => /gets a narrator/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}kill @e[type=minecraft:painting,tag=bm.trpz]`); await run(`${O}fill ${X - 2} ${Y + 1} ${Z + 6} ${X + 2} ${Y + 4} ${Z + 6} minecraft:air`);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.zq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    await calm();
    await zom(2.5, 0, 'bm.trpr'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~1.5 ~ ~`); await cd('mc', 0);
    const TOOL = '@e[type=minecraft:item_display,tag=bm.mzp_pet,tag=bm.mzp_tool,limit=1]';
    const tools = new Set(); let splash = false;
    const look = async () => { tools.add(await nbt(TOOL, 'item.components."minecraft:item_model"')); if ((await cnt('@e[type=minecraft:item_display,tag=bm.fxs_capshun_splash]')) >= 1) splash = true; };
    ok('BRUSH SWIPE - the foe hurt', await wait(5000, async () => { await look(); return (await num('@e[tag=bm.trpr,limit=1]', 'Health')) < 300; }, 100));
    for (let i = 0; i < 6; i++) { await look(); await sleep(100); }
    ok('...the brush in his hand for it (one tool at a time)', [...tools].some(t => /mz_tool_brush/.test(t)), [...tools].join(' '));
    ok('...and a splash of colour (the effect sprite)', splash);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(1500);
    ok('...back to the pencil when he\'s done', /mz_tool_pencil/.test(await nbt(TOOL, 'item.components."minecraft:item_model"')), await nbt(TOOL, 'item.components."minecraft:item_model"'));
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(10, 0, 'bm.trpd', 600); await cd('k2', 0);
    let drawn = 0;
    for (let i = 0; i < 3; i++) { const h0 = await num('@e[tag=bm.trpd,limit=1]', 'Health'); await cd('k2', 0);
      if (await wait(7000, async () => (await num('@e[tag=bm.trpd,limit=1]', 'Health')) < h0)) drawn++; await sleep(500); }
    ok('DRAWN TO LIFE - a foe 10 off: his sketches (bomb, anvil or arrows) hit it, three times running', drawn === 3, `${drawn}/3`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(9, 0, 'bm.trps'); await cd('rc', 0);
    ok('PAINT SPLAT - a foe 9 off takes a glob of paint', await wait(6000, async () => (await num('@e[tag=bm.trps,limit=1]', 'Health')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(6, 0, 'bm.trpk'); await cd('sc', 0);
    ok('SKETCH - an outline scribbled round a foe 6 off: it can barely move (Slowness IV) or hit', await wait(6000, async () =>
      /slowness/.test(await nbt('@e[tag=bm.trpk,limit=1]', 'active_effects')) && /weakness/.test(await nbt('@e[tag=bm.trpk,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    for (const [dx, dz] of [[3, 2], [3, -2], [-3, 2]]) await zom(dx, dz, 'bm.trpw');
    await run(`${O}execute at ${PET} run tp @e[tag=bm.trpw] ~3 ~ ~1`); await cd('bc', 0);
    ok('WET PAINT - three foes near: stuck in the puddle (Slowness III)', await wait(6000, async () => (await cnt('@e[tag=bm.trpw,nbt={active_effects:[{id:"minecraft:slowness",amplifier:2b}]}]')) >= 2),
       `${await cnt('@e[tag=bm.trpw,nbt={active_effects:[{id:"minecraft:slowness"}]}]')} slowed`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await zom(5, 0, 'bm.trpg'); await zom(-4, 3, 'bm.trpg'); await cd('gc', 0);
    ok('THE RAINBOW STROKE - every foe under the arc hurt, Strength for you', await wait(8000, async () => (await cnt('@e[tag=bm.trpg,nbt={Health:300.0f}]')) === 0) &&
       /strength/.test(await fx()), `untouched ${await cnt('@e[tag=bm.trpg,nbt={Health:300.0f}]')}`);
    await sleep(2500); await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    // ---- the PALETTE (his menu): blue - then FRESH COAT: Speed for you
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await sneakMenu(0); await A.press(/^Palette/); await sleep(600);
    A.bars.length = 0; await A.press(/^Blue/); await sleep(600);
    ok('his menu -> Palette -> Blue: chosen ("Bold choice")', (await score('bm.mzpal')) === 4 && A.bars.some(b => /Bold choice/.test(b)), `bm.mzpal ${await score('bm.mzpal')}`);
    A.bars.length = 0; await cd('k', 0);
    ok('FRESH COAT - he paints you blue: Speed for you', await wait(6000, async () => /speed/.test(await fx())) && A.bars.some(b => /fresh coat of/.test(b)), A.bars.slice(-1).join(''));
    // ---- THE STORY SO FAR (his menu)
    await sleep(1500); await sneakMenu(0); A.chats.length = 0; await A.press(/The story so far/); await sleep(800);
    ok('his menu -> The story so far: he narrates ("Previously: ...")', A.chats.some(c => /Previously/.test(c)), A.chats.slice(-1).join('').slice(0, 200));
    // ---- NARRATION: badly hurt, he says so
    await run('effect clear TestRat'); await run('scoreboard players set TestRat bm.mznr 0'); await run('tag TestRat remove bm.hush');
    await run('damage TestRat 15 minecraft:generic'); A.bars.length = 0;
    ok('NARRATION - badly hurt: he narrates it', await wait(4000, async () => A.bars.some(b => /narrates/.test(b))), A.bars.slice(-1).join('').slice(0, 160));
    await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('effect give TestRat minecraft:resistance 900 4 true');
  } });
