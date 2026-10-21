// 2.87: THE STALKER, as a regular (non-op) player - the owner's checklist (rigpet_t): HARD MODE ONLY - the dawn of a Dread Night
// survived wearing the Stalker's Grin: one doesn't come apart; asked empty-handed, it only waits; given Dread Essence, it follows
// (the Hollow Hook). Its fight, all through armour: REND (the third blow takes a quarter of a foe's health), STEP FROM THE DARK
// (behind its foe), THE STARE (frozen), THE HARROWING. KIN: it comes out on a Dread Night. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'stalker', NAME: 'The Stalker', ab: 'sv', q: 'sq', pfx: 'p193', prefix: 'st_', item: 'st_hook', parts: 8, hp: 60, X: 16760, Z: 16000, pron: 'it',
  called: /already behind you/, home: /folds into the dark/, sit: /sinks down/, stand: /unfolds, joint by joint/,
  ways: ['Rend', 'Step from the Dark', 'The Stare', 'The Harrowing', 'Night-Born', 'Kin'],
  plain: 'Its own sickly olive', looks: ['Bone White', 'Ashen Grey', 'Blood Moon'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    // (the stage: a Dread Night's dawn, TestRat hunted all night, never died, wearing the Grin)
    await run('loot replace entity TestRat armor.head loot bm:items/stalker_grin');
    await run('tag TestRat add bm.dnwas'); await run('scoreboard players set TestRat bm.dnt 400');
    await run('execute as TestRat store result score @s bm.dnd0 run scoreboard players get @s bm.deaths');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run('function bm:p181/end'); await sleep(800);
    ok('a Dread Night survived wearing the Grin: at dawn one stays behind (its rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.svencp]')) === 8 && A.chats.some(c => /doesn't come apart/.test(c)) && A.chats.some(c => /survived the Dread Night/.test(c)),
       `enc ${await cnt(ENC)} parts ${await cnt('@e[type=minecraft:item_display,tag=bm.svencp]')} | ` + A.chats.slice(-2).join(' | ').slice(0, 200));
    await run('item replace entity TestRat armor.head with minecraft:air');
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: it leans in close - and waits', A.bars.some(b => /It waits/.test(b)), A.bars.slice(-1).join(''));
    // (the dawn paid out Dread Essence already: hold one, and count it before and after)
    await run('clear TestRat *[minecraft:custom_data~{bm:"dread_essence"}]'); await run('loot replace entity TestRat hotbar.8 loot bm:items/dread_essence');
    await run('item modify entity TestRat hotbar.8 {function:"minecraft:set_count",count:1}'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding Dread Essence: the essence taken, the Hollow Hook given', (await has('st_hook')) === 1 && (await has('dread_essence')) === 0 &&
       A.chats.some(c => /swallows it/.test(c)), `hook ${await has('st_hook')} essence ${await has('dread_essence')} | ` + A.chats.slice(-4).join(' | ').slice(0, 300));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.sq${o} ${v}`);
    for (const o of ['gc', 'bc', 'rc', 'mc']) await cd(o, 900);
    await run(`${O}time set 18000`); await sleep(1500);                 // (the pack's clock (#tod) catches up once a second)
    // REND, through netherite: three blows - the third takes a quarter of its 300 more (capped at 20)
    await zom(3, 0, 'bm.trpr');
    for (const s of ['head', 'chest', 'legs', 'feet']) await run(`${O}item replace entity @e[tag=bm.trpr,limit=1] armor.${s} with minecraft:netherite_${{ head: 'helmet', chest: 'chestplate', legs: 'leggings', feet: 'boots' }[s]}`);
    await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~1.5 ~ ~`); await cd('mc', 0);
    ok('REND - through full netherite: the first blow takes its full 9 (6, +3 at night)', await wait(5000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) <= 291.5),
       `health ${await num('@e[tag=bm.trpr,limit=1]', 'Health')}`);
    ok('...THE THIRD BLOW: three rends take 47 (9 + 9 + 9 + 20)', await wait(6000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) <= 254), `health ${await num('@e[tag=bm.trpr,limit=1]', 'Health')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('mc', 900);
    // STEP FROM THE DARK: a foe 10 off - it's behind it
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(10, 0, 'bm.trpp'); await run(`${O}execute as @e[tag=bm.trpp] at @s run tp @s ~ ~ ~ 90 0`); await cd('rc', 0);
    ok('STEP FROM THE DARK - a foe 10 off: it unfolds right behind it (slowed)', await wait(6000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.svpet,x=${X + 10},y=${Y + 1},z=${Z},distance=..2.6]`)) === 1) &&
       await wait(3000, async () => /slowness/.test(await nbt('@e[tag=bm.trpp,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('rc', 900); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`);
    // THE STARE: two foes - frozen
    await zom(3, 2, 'bm.trpb'); await zom(3, -2, 'bm.trpb'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpb] ~3 ~ ~1`); await cd('bc', 0);
    ok('THE STARE - two foes near: frozen (Slowness VII), weakened', await wait(6000, async () => (await cnt('@e[tag=bm.trpb,nbt={active_effects:[{id:"minecraft:slowness",amplifier:6b}]}]')) >= 1) &&
       (await cnt('@e[tag=bm.trpb,nbt={active_effects:[{id:"minecraft:weakness"}]}]')) >= 1);
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('bc', 900);
    // THE HARROWING: foe after foe
    await zom(6, 3, 'bm.trph'); await zom(6, -3, 'bm.trph'); await cd('gc', 0);
    ok('THE HARROWING - both foes torn into (10s, through everything)', await wait(9000, async () => (await cnt('@e[tag=bm.trph,nbt={Health:300.0f}]')) === 0),
       `untouched ${await cnt('@e[tag=bm.trph,nbt={Health:300.0f}]')} of ${await cnt('@e[tag=bm.trph]')}, gc ${await score('bm.sqgc', PET)} a ${await score('bm.sqa', PET)} x ${await score('bm.sqx', PET)}`);
    await sleep(2000); await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    ok('NIGHT-BORN - you see in the dark beside it', await wait(3000, async () => /night_vision/.test(await fx())));
    // KIN: the only follower that comes out on a Dread Night
    await run('scoreboard players set #dnight bm.bm 1');
    await run('execute as TestRat run function bm:p193/home'); await sleep(800); await run('scoreboard players set TestRat bm.svcd 0');
    A.bars.length = 0; await use(0); await sleep(1500);
    ok('KIN - on a Dread Night it still comes when called', (await cnt(PET)) === 1 && !A.bars.some(b => /won't come out/.test(b)), A.bars.slice(-1).join(''));
    await sleep(1500);
    ok('...and stays out', (await cnt(PET)) === 1);
    await run('scoreboard players set #dnight bm.bm 0'); await run(`${O}time set 6000`);
  } });
