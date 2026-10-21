// 2.87: QUEEN PEARL, as a regular (non-op) player - the owner's checklist (rigpet_t): having befriended Emma, a cake set down on a
// beach by day: the queen regent pops out of the surf; asked, she wants more cake; given one, she joins (her pearls). Casual: a ROYAL
// WHIM, THE WINK (a foe smitten), the ROYAL PROCLAMATION (a holiday - Strength, emeralds); regal: the ROYAL DECREE (Strength and
// Resistance), BY ROYAL DECREE. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'pearlq', NAME: 'Queen Pearl', ab: 'pq', q: 'pk', pfx: 'p190', prefix: 'pq_', item: 'pq_pearls', parts: 9, hp: 44, X: 16700, Z: 16000,
  called: /Hold your seahorses/, home: /Back to the throne/, sit: /Wake me if there/, stand: /Adventure awaits/, story: /Her story/,
  ways: ['Royal Whim', 'Pearl Flick', 'The Wink', 'Royal Proclamation', 'Royal Decree'],
  form: { button: /Casual \/ regal outfit/, suffix: '_r', score: 'bm.pqform' }, plain: 'Her own aqua', looks: ['Coral Pink', 'Sunset Gold', 'Starlit Navy'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    await run(`${O}fillbiome ${X - 16} ${Y - 4} ${Z - 16} ${X + 16} ${Y + 12} ${Z + 16} minecraft:beach`);
    await run('advancement grant TestRat only bm:story/emma_friend'); await run(`${O}time set 1000`);
    await run('item replace entity TestRat hotbar.1 with minecraft:cake');      // (a cake doesn't stack)
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 50); A.chats.length = 0; A.slot(1); await sleep(300); A.useOn(X, Y, Z + 3, 1); await sleep(500);
    if (process.env.DBG) { console.log('block:', await run(`${O}execute if block ${X} ${Y + 1} ${Z + 3} minecraft:cake`), '| beach:', await run(`execute in minecraft:overworld positioned ${X} ${Y + 1} ${Z} if biome ~ ~ ~ #minecraft:is_beach`),
      '| adv:', await run('execute if entity @a[name=TestRat,advancements={bm:story/emma_friend=true}]'), '| enc:', await run('execute if entity @e[type=minecraft:interaction,tag=bm.pqenc]')); }
    ok('a cake set down on a beach by day: the queen regent pops out of the surf (her rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.pqencp]')) === 9 && A.chats.some(c => /pops up out of the surf/.test(c)), A.chats.slice(-1).join(''));
    await run(`${O}setblock ${X} ${Y + 1} ${Z + 3} minecraft:air`);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2, 0, 20);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: she wants MORE cake', A.bars.some(b => /Bring me another/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.1 with minecraft:cake'); A.slot(1); await sleep(400); A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding a cake: the cake taken, her pearls given', (await has('pq_pearls')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:cake 0')) &&
       A.chats.some(c => /Queen Pearl\. Emma's aunt/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, model, zom, sneakMenu, X, Y, Z, sleep }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.pk${o} ${v}`);
    for (const o of ['gc', 'bc', 'sc', 'rc', 'mc']) await cd(o, 900);
    A.bars.length = 0; await cd('sc', 0);
    ok('casual: a ROYAL WHIM - a buff for you, and why', await wait(5000, async () => A.bars.some(b => /Speed!|Hop!|Haste|Luck!|Swim with me|Night vision|Fire resistance|Slow falling/.test(b))) &&
       /speed|jump_boost|haste|luck|dolphins_grace|night_vision|fire_resistance|slow_falling/.test(await fx()), A.bars.slice(-1).join(''));
    await cd('sc', 900); await zom(6, 0, 'bm.trpw'); await cd('bc', 0);
    ok('casual: THE WINK - the foe smitten (stopped dead, glowing)', await wait(6000, async () => (await cnt('@e[tag=bm.trpw,nbt={active_effects:[{id:"minecraft:slowness",amplifier:6b}]}]')) === 1));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('bc', 900); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..12]`);
    await zom(5, 0, 'bm.trph'); await cd('gc', 0); A.bars.length = 0;
    ok('casual: the ROYAL PROCLAMATION - "I declare a HOLIDAY!"', await wait(8000, async () => A.bars.some(b => /HOLIDAY/.test(b))), A.bars.slice(-1).join(''));
    ok('...Strength for you, and emeralds', /strength/.test(await fx()) && (await cnt(`@e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..12,nbt={Item:{id:"minecraft:emerald"}}]`)) >= 1);
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await sneakMenu(0); A.bars.length = 0; await A.press(/Casual \/ regal outfit/); await sleep(1500);
    ok('the menu: Casual / regal outfit - the gown (pq_body_r), and she hates it', /pq_body_r$/.test(await model()) && A.bars.some(b => /wedding cake/.test(b)), await model());
    ok('regal: the ROYAL DECREE - Strength for you, steady', await wait(4000, async () => /strength/.test(await fx())), (await fx()).slice(0, 160));
    await zom(5, 0, 'bm.trpd'); await cd('gc', 0); A.bars.length = 0;
    ok('regal: BY ROYAL DECREE', await wait(8000, async () => A.bars.some(b => /BY ROYAL DECREE/.test(b))), A.bars.slice(-1).join(''));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    await sneakMenu(0); await A.press(/Casual \/ regal outfit/); await sleep(1500);
    ok('...and back in her shift (pq_body)', /pq_body$/.test(await model()), await model());
  } });
