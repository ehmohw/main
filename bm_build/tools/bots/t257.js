// 2.94: THE SKY BUDDIES, the first trio follower, as a regular (non-op) player - the owner's checklist (rigpet_t): WITNESS THE SKY
// (a clear noon: Sunny shows himself; a full-moon midnight: Snooze and Twinkle; a rainstorm: Nimbus - each once, a sprite in the
// sky), then all three drift down; right-clicked, they hand over the Sky Mobile. Their fight: SUNBEAM (fire), STAR SHOT (glowing),
// ZAP, LULLABY (three foes slowed to a crawl), THE FORECAST (every foe near hurt and alight); their support: DRIZZLE (badly hurt:
// Regeneration and Fire Resistance), WHAT THE SKY GIVES (Haste by day); Today's Forecast (their menu); the rays turning on their own
// clock. Then the shared list (the look is on Snooze's nightcap).
const runT = require('./rigpet_t');
runT({ W: 'sky', NAME: 'The Sky Buddies', ab: 'yb', q: 'yq', pfx: 'p211', prefix: 'yb_', item: 'sky_mobile', parts: 7, hp: 60, X: 17400, Z: 16000, pron: 'them',
  lookPart: 'cap',
  called: /Coming through/, home: /Clearing up/, sit: /A nap/, stand: /back to shining/,
  ways: ['Sunbeam', 'Star Shot', 'Zap', 'Lullaby', 'Drizzle', 'What the Sky Gives', 'The Forecast'],
  plain: "Snooze's old blue", looks: ['Bubblegum Pink', 'Mint Dream', 'Lavender Night'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, has, tags, X, Y, Z, ENC, sleep }) => {
    for (const t of ['bm.ybs1', 'bm.ybs2', 'bm.ybs3']) await run(`tag TestRat remove ${t}`);
    await run('kill @e[type=minecraft:item_display,tag=bm.ybvis]');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, -20); A.chats.length = 0;
    await run(`${O}weather clear`); await run(`${O}time set 6000`);
    ok('a clear noon under the open sky: Sunny shows himself, once (a sprite high in the sky)', await wait(5000, async () => /bm\.ybs1/.test(await tags())) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.ybvis]')) >= 2 && A.chats.some(c => /winks at you/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    await run(`${O}time set 18000`); A.chats.length = 0;
    ok('a full-moon midnight: Snooze and Twinkle', await wait(5000, async () => /bm\.ybs2/.test(await tags())) && A.chats.some(c => /full moon yawns/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    await run(`${O}weather rain`); A.chats.length = 0;
    ok('a rainstorm: Nimbus - and all three seen', await wait(5000, async () => /bm\.ybs3/.test(await tags())) && A.chats.some(c => /smiles down at you/.test(c)) &&
       A.chats.some(c => /seen the whole sky/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    ok('...and they drift down together (the trio and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.ybencp]')) === 7);
    await run(`${O}weather clear`); await run(`${O}time set 6000`);
    await sleep(5000);
    ok('the sky sprites fade away', await wait(8000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.ybvis]')) === 0));
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: they hand over the Sky Mobile', (await has('sky_mobile')) === 1 && A.chats.some(c => /be your weather/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.yq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    await calm(); await run(`${O}time set 6000`); await run(`${O}weather clear`);
    // the rays turn on their own clock
    const RAYS = '@e[type=minecraft:item_display,tag=bm.ybp_pet,tag=bm.ybp_rays,limit=1]';
    const r0 = await nbt(RAYS, 'transformation.right_rotation'); await sleep(1500);
    ok("Sunny's rays turn on their own", (await nbt(RAYS, 'transformation.right_rotation')) !== r0);
    await zom(8, 0, 'bm.trpb'); await cd('rc', 0);
    ok('SUNBEAM - a foe 8 off: burned by a beam of sunlight', await wait(5000, async () => (await hp('bm.trpb')) < 300 && (await num('@e[tag=bm.trpb,limit=1]', 'Fire')) > 0),
       `hp ${await hp('bm.trpb')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(10, 0, 'bm.trps'); await cd('mc', 0);
    ok('STAR SHOT - a foe 10 off: hit, and glowing', await wait(5000, async () => (await hp('bm.trps')) < 300 && /glowing/.test(await nbt('@e[tag=bm.trps,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(6, 0, 'bm.trpq'); await cd('sc', 0);
    ok('ZAP - a foe 6 off: struck by a bolt', await wait(5000, async () => (await hp('bm.trpq')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    for (const [dx, dz] of [[3, 2], [3, -2], [-3, 2]]) await zom(dx, dz, 'bm.trpl');
    await cd('bc', 0);
    ok('LULLABY - three foes near: slowed to a crawl (Slowness IV) and weakened', await wait(7000, async () =>
      (await cnt('@e[tag=bm.trpl,nbt={active_effects:[{id:"minecraft:slowness",amplifier:3b}]}]')) >= 2), `${await cnt('@e[tag=bm.trpl,nbt={active_effects:[{id:"minecraft:slowness"}]}]')} slowed`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(5, 0, 'bm.trpf'); await zom(-4, 3, 'bm.trpf'); await cd('gc', 0);
    ok('THE FORECAST - every foe within 9 hurt and set alight', await wait(8000, async () => (await cnt('@e[tag=bm.trpf,nbt={Health:300.0f}]')) === 0 &&
       (await cnt('@e[tag=bm.trpf,nbt={Fire:-1s}]')) === 0), `untouched ${await cnt('@e[tag=bm.trpf,nbt={Health:300.0f}]')}`);
    await sleep(2500); await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    // DRIZZLE: badly hurt - Regeneration and Fire Resistance
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('damage TestRat 10 minecraft:generic'); A.bars.length = 0; await cd('k', 0);
    ok('DRIZZLE - badly hurt: Nimbus rains on you (Regeneration, Fire Resistance)', await wait(6000, async () => /regeneration/.test(await fx()) && /fire_resistance/.test(await fx())) &&
       A.bars.some(b => /Drizzle/.test(b)), A.bars.slice(-1).join(''));
    await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await calm(); await cd('k2', 0); A.bars.length = 0;
    ok("WHAT THE SKY GIVES - by day, no fight near: Haste", await wait(6000, async () => /haste/.test(await fx())) && A.bars.some(b => /Sun's out/.test(b)), A.bars.slice(-1).join(''));
    await calm();
    // Today's forecast (their menu)
    await sleep(1500); await sneakMenu(0); A.chats.length = 0; await A.press(/Today's forecast/); await sleep(800);
    ok("their menu -> Today's forecast: Sunny tells you the sky (clear and sunny)", A.chats.some(c => /Clear and sunny/.test(c)), A.chats.slice(-1).join('').slice(0, 200));
  } });
