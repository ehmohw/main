// 2.87: QUEEN AVA, as a regular (non-op) player - the owner's checklist (rigpet_t): HARD MODE ONLY - a Conduit set down at night
// with Emma (called with her own ribbon) beside you: the ghost of the queen rises; right-clicked, she joins (her locket). Her two
// forms: living - the ROYAL WARD (Absorption II), TIDAL LASH, UNDERTOW (Slowness III), the TIDE OF CROWNS (Conduit Power); ghostly -
// REQUIEM, MOTHER'S WATCH (Resistance IV at 4 hearts). Then the shared list: menu, story, sit, looks (and on her ghost), aura,
// contract, wheel, frame, case, doll, faint.
const runT = require('./rigpet_t');
runT({ W: 'ava', NAME: 'Queen Ava', ab: 'av', q: 'aq', pfx: 'p189', prefix: 'av_', item: 'av_locket', parts: 10, figParts: 9, sitPart: 'pool', hp: 50, X: 16740, Z: 16000,
  called: /I am here, dear one/, home: /in the deep, watching/, sit: /Even queens tire/, stand: /Gently/, story: /Her story/,
  ways: ['Royal Ward', 'Tidal Lash', 'Undertow', 'Tide of Crowns', 'Mother', 'Requiem'],
  form: { button: /Living \/ ghostly form/, suffix: '_g', score: 'bm.avform' }, plain: 'Her royal blue', looks: ['Coral Reef', 'Abyssal Violet', 'Kelp Forest'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, use, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    await run(`${O}time set 18000`); await run('scoreboard players set #hard bm.cfg 0'); await run('scoreboard players set #hardoff bm.cfg 1');   // (held off: a conqueror online would wake it again)
    await run('loot replace entity TestRat hotbar.7 loot bm:items/emma_ribbon'); await run('advancement grant TestRat only bm:story/emma_friend');
    await run('scoreboard players set TestRat bm.emcd 0'); await use(7); const EM = '@e[type=minecraft:cat,tag=bm.emmapet]';
    ok('Emma called with her ribbon (she comes)', await wait(5000, async () => (await cnt(EM)) === 1));
    await run('item replace entity TestRat hotbar.1 with minecraft:conduit 2');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 50); A.slot(1); await sleep(300); A.useOn(X, Y, Z + 3, 1); await sleep(1500);
    ok('a Conduit set down at night, Emma there - but the world isn\'t in hard mode: nobody rises (2.94: and Emma says why)', (await cnt(ENC)) === 0 && A.chats.some(c => /isn\'t dark enough/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    await run(`${O}setblock ${X} ${Y + 1} ${Z + 3} minecraft:air`); await run('scoreboard players set #hardoff bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1');
    A.chats.length = 0; A.slot(1); await sleep(300); A.useOn(X, Y, Z + 3, 1); await sleep(500);
    ok('in hard mode: the ghost of a queen rises (her rig, ghostly, and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.avencp]')) === 10 && A.chats.some(c => /pale queen rises/.test(c)), A.chats.slice(-1).join(''));
    ok('...she\'s her ghost', /av_body_g/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.avencp,tag=bm.avp_body,limit=1] item`)));
    await run(`${O}setblock ${X} ${Y + 1} ${Z + 3} minecraft:air`);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2, 0, 20);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked with Emma beside you: mother and daughter - her locket given', (await has('av_locket')) === 1 && A.chats.some(c => /My little Emma/.test(c)) && A.chats.some(c => /Mama/.test(c)),
       A.chats.slice(-3).join(' | ').slice(0, 200));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, model, zom, sneakMenu, X, Y, Z, sleep }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.aq${o} ${v}`);
    for (const o of ['gc', 'bc', 'sc', 'rc', 'mc']) await cd(o, 900);
    await cd('sc', 0);
    ok('living: the ROYAL WARD - an Absorption II shield on you', await wait(4000, async () => /absorption/.test(await fx())), (await fx()).slice(0, 160));
    await cd('sc', 900);
    await zom(9, 0, 'bm.trpa'); await cd('rc', 0);
    ok('living: TIDAL LASH - a foe 8 off, hurt and slowed', await wait(6000, async () => (await num('@e[tag=bm.trpa,limit=1]', 'Health')) < 300) && /slowness/.test(await nbt('@e[tag=bm.trpa,limit=1]', 'active_effects')));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('rc', 900);
    await zom(3, 2, 'bm.trpb'); await zom(3, -2, 'bm.trpb'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpb] ~3 ~ ~1`); await cd('bc', 0);
    ok('living: two foes near - UNDERTOW drags them in and holds them (Slowness III)', await wait(8000, async () => (await cnt('@e[tag=bm.trpb,nbt={active_effects:[{id:"minecraft:slowness",amplifier:2b}]}]')) >= 1));
    await run(`${O}kill @e[tag=bm.trpz]`); await zom(5, 0, 'bm.trpc'); await cd('gc', 0); A.bars.length = 0;
    ok('living: the charge ready - the TIDE OF CROWNS', await wait(8000, async () => A.bars.some(b => /tide of crowns/i.test(b))), A.bars.slice(-1).join(''));
    ok('...Conduit Power and Dolphin\'s Grace for you', await wait(3000, async () => { const e = await fx(); return /conduit_power/.test(e) && /dolphins_grace/.test(e); }));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    await sneakMenu(0); await A.press(/Living \/ ghostly form/); await sleep(1500);
    ok('the menu: Living / ghostly form - she becomes her ghost (av_body_g)', /av_body_g$/.test(await model()), await model());
    await zom(5, 0, 'bm.trpd'); await cd('gc', 0); A.bars.length = 0;
    ok('ghost: REQUIEM', await wait(8000, async () => A.bars.some(b => /Requiem/.test(b))), A.bars.slice(-1).join(''));
    ok('...the foe withers and glows', await wait(4000, async () => /glowing/.test(await nbt('@e[tag=bm.trpd,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    await run('scoreboard players set TestRat bm.avwatch 0'); await run('effect clear TestRat'); await sleep(300); A.bars.length = 0; await run('damage TestRat 15 minecraft:generic'); await sleep(100);
    const hp0 = await num('@a[name=TestRat,limit=1]', 'Health');
    ok('ghost: MOTHER\'S WATCH - down to 4 hearts, she shields you (Resistance IV)', await wait(4000, async () => A.bars.some(b => /NEVER again/.test(b))) &&
       /amplifier: ?3b[^}]*minecraft:resistance|minecraft:resistance[^}]*amplifier: ?3b/.test(await fx()), `health ${hp0} ` + (await fx()).slice(0, 200));
    await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:instant_health 1 3 true');
    await sneakMenu(0); await A.press(/Living \/ ghostly form/); await sleep(1500);
    ok('...and back to her living form (av_body)', /av_body$/.test(await model()), await model());
  } });
