// 3.00: THE MIRELING (phase252) as a regular (non-op) player - the owner's checklist (rigpet_t): the Seed comes from the wild Dread
// Mires (phase246) - the stage (rcon): hard mode, a Mire risen beside TestRat, worn down to its last few hits, a sword in hand; the
// player strikes the blow. Two slain before it (bm.mlk 2): the third only stirs ("watches you go"); the fourth leaves the Seed in its
// puddle, for TestRat alone; a fifth leaves none (bm.mlseed). Then LASH, PUDDLE SNARE (held fast), THE GRAB (dragged in, stabbed),
// SHADOW VEIL (you hurt: Resistance, Regeneration), GLOWPOOL (out of a fight: Night Vision, Water Breathing), SHADOW KIN (probed), and
// FULL-GROWN: the menu's Grown / Little refused below Queen Ava's rank III, then (the rank set by rcon) pressed: the grown Mire's 23
// parts at the host, the little rig hidden (view_range 0); pressed again: gone, the little one back. Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'mireling', NAME: 'The Mireling', ab: 'ml', q: 'mj', pfx: 'p252', prefix: 'ml_', item: 'mire_seed', parts: 14, figParts: 14, hp: 36, X: 18400, Z: 16000, pron: 'it',
  called: /slides back to your side/, home: /sinks into the ground/, sit: /only the eye poking up/, stand: /ready to go/,
  ways: ['Lash', 'Puddle Snare', 'The Grab', 'Shadow Veil', 'Glowpool', 'Light-Shy', 'Shadow Kin', 'Full-Grown'], plain: 'Blood-red veins', looks: ['Ember Mire', 'Void Mire', 'Frost Mire'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, X, Y, Z, cnt, entOf, at, num } = ctx;
    const dfell = +(((await run('scoreboard players get #dfell bm.cfg')).match(/has (-?\d+)/)) || [0, 0])[1];
    await run('scoreboard players set #dfell bm.cfg 0'); await run(`${O}time set 18000`);
    await run('tag TestRat remove bm.mlseed'); await run('scoreboard players set TestRat bm.mlk 2'); await run('clear TestRat');
    await run('item replace entity TestRat hotbar.8 with minecraft:netherite_sword');
    const MIRE = `@e[type=minecraft:husk,tag=bm.mire,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..3,limit=1]`;
    const slay = async () => {         // (a Mire set down 3 ahead and risen; worn to its last hits; the player swings until it falls)
      await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
      await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} run function bm:p246/spawn`);
      await run(`${O}execute as ${MIRE} at @s run function bm:p246/rise0`); await sleep(2600);
      await run(`${O}data merge entity ${MIRE} {Health:104f}`); A.slot(8); await sleep(300);
      for (let k = 0; k < 6 && (await cnt(`${MIRE.slice(0, -1)},scores={bm.ms=7}]`)) === 0; k++) {
        const e = await entOf(MIRE); if (e) A.attack(e.entityId); await sleep(700);
      }
      const fell = await wait(3000, async () => (await cnt(`${MIRE.slice(0, -1)},scores={bm.ms=7}]`)) === 1);
      await wait(5000, async () => (await cnt(MIRE)) === 0); await sleep(600);
      return fell;
    };
    A.chats.length = 0;
    ok('the third Mire TestRat slays: it falls to the player\'s blow', await slay());
    ok('...and only stirs - "something small in its puddle watches you go" (no Seed yet)', A.chats.some(c => /watches you go/.test(c)) && (await has('mire_seed')) === 0, A.chats.slice(-1).join(''));
    A.chats.length = 0;
    ok('the fourth: it falls', await slay());
    const seed = `@e[type=minecraft:item,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..4,limit=1]`; await sleep(500);
    ok('...and leaves a Mireling\'s Seed in its puddle, for TestRat alone (Owner set, never despawns)',
       /Owner/.test(await run(`${O}data get entity ${seed}`)) || (await has('mire_seed')) === 1);
    await at(X + 0.5, Y + 1, Z + 3.5, 0, 10);
    ok('...picked up by walking over it', await wait(4000, async () => (await has('mire_seed')) === 1));
    ok('...and the player is told (only you can pick it up)', A.chats.some(c => /Only you can pick it up/.test(c)), A.chats.slice(-1).join(''));
    A.chats.length = 0;
    await run('item replace entity TestRat hotbar.8 with minecraft:netherite_sword');
    ok('a fifth Mire: it falls', await slay());
    await sleep(800);
    ok('...and leaves no second Seed (bm.mlseed): still the one', (await has('mire_seed')) === 1 && (await cnt(`@e[type=minecraft:item,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..5]`)) === 0);
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await run('clear TestRat minecraft:netherite_sword');
    await run(`scoreboard players set #dfell bm.cfg ${dfell}`);
    // (the Seed used: it comes)
    const sl = +(((await run('clear TestRat *[minecraft:custom_data~{bm:"mire_seed"}] 0')).match(/Found (\d+)/)) || [0, 0])[1];
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/mire_seed'); A.slot(0); await sleep(300);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.use(); await sleep(400); A.release(); await sleep(1500);
    ok('the Seed used: the Mireling rises out of a puddle', sl === 1);
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait, O, cnt, num, sneakMenu, A, sleep, PET } = ctx; const K = kit(ctx, 'mj');
    ok('LASH - a foe at its side: struck', await K.move('mc', [[2, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300));
    ok('PUDDLE SNARE - two foes near: hurt, held fast', await K.move('k2', [[2, 1], [-2, 1]], 'bm.trps', async () => (await K.hp('bm.trps')) < 300 &&
       /slowness[^}]*amplifier: ?3b|amplifier: ?3b[^}]*slowness/.test(await K.fxOf('bm.trps')), 9000));
    ok('THE GRAB - a foe 6 off: dragged in to the maw, and stabbed', await K.move('gc', [[0, 6]], 'bm.trpg', async () => (await K.hp('bm.trpg')) < 300 &&
       (await num('@e[tag=bm.trpg,limit=1]', 'Pos[2]')) < Z + 5, 9000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat');
    await run('damage TestRat 6 minecraft:generic'); await ctx.zom(0, 8, 'bm.trpw'); await K.cd('sc', 0);
    ok('SHADOW VEIL - you hurt, a foe about: Resistance and Regeneration', await wait(6000, async () => /resistance/.test(await fx()) && /regeneration/.test(await fx())), await fx());
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await K.cd('k', 0);
    ok('GLOWPOOL - out of a fight beside you: Night Vision and Water Breathing', await wait(6000, async () => /night_vision/.test(await fx()) && /water_breathing/.test(await fx())), await fx());
    ok('SHADOW KIN - it\'s out near you: the Stalkers\' check sees it (probe)', /Test passed|count: 1/i.test(await run('execute as TestRat at @s if function bm:p252/near_q')));
    await K.calm(); await run('effect give TestRat minecraft:resistance 900 4 true');
    // ---- FULL-GROWN: refused below rank III, then grown, then little again (the menu, as the player)
    const GR = '@e[type=minecraft:item_display,tag=bm.mlu]';
    const SMALL = '@e[type=minecraft:item_display,tag=bm.mlp_pet,tag=bm.mlp_head,limit=1]';
    await run('scoreboard players set TestRat bm.mlub 0'); await run('scoreboard players set TestRat bm.hn_mireling 1444');
    await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10);
    ok('the menu: a Grown / Little button', await sneakMenu(0) && A.buttons().some(b => /Grown \/ Little/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/Grown \/ Little/); await sleep(1200);
    ok('...below Queen Ava\'s rank III: refused - "Honoured by Queen Ava to rank III, it grows"', A.bars.some(b => /rank III/.test(b)) && (await cnt(GR)) === 0, A.bars.slice(-1).join(''));
    await run('scoreboard players set TestRat bm.hn_mireling 1555');
    await sneakMenu(0); A.bars.length = 0; await A.press(/Grown \/ Little/);
    ok('...at rank III (V, V, V): FULL-GROWN - the grown Mire\'s 23 parts at its side', await wait(4000, async () => (await cnt(GR)) === 23), `${await cnt(GR)} parts`);
    ok('...the little rig hidden (view_range 0)', /^0(\.0)?f?$/.test((await ctx.nbt(SMALL, 'view_range')).trim()), await ctx.nbt(SMALL, 'view_range'));
    ok('...and it says so', A.bars.some(b => /FULL-GROWN/.test(b)), A.bars.slice(-1).join(''));
    ok('...none of the wild Mire\'s tags (no husk, no bm.mr): phase246 never counts it', (await cnt('@e[tag=bm.mlu,tag=bm.mr]')) === 0 && (await cnt(`@e[type=minecraft:husk,tag=bm.mire,x=${X},y=${Y},z=${Z},distance=..16]`)) === 0);
    await K.move('mc', [[2, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300);
    ok('...grown, it still fights (its lash)', (await K.hp('bm.trpc')) < 300);
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10);
    await sneakMenu(0); A.bars.length = 0; await A.press(/Grown \/ Little/);
    ok('pressed again: little again - the grown rig gone, the little one shown', await wait(4000, async () => (await cnt(GR)) === 0) &&
       /1\.6/.test(await ctx.nbt(SMALL, 'view_range')), await ctx.nbt(SMALL, 'view_range'));
    await run('scoreboard players set TestRat bm.hn_mireling 0'); await run('scoreboard players set TestRat bm.mlub 0');
    await K.calm();
  } });
