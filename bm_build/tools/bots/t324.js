// 3.0: THE KEEPER OF BONDS (phase254) as a regular (non-op) player - the owner's checklist (rigpet_t), its meeting in the Loom
// Sanctuary (phase253): the stage (rcon) - the island woven into the sky (its chunks held while the test runs), TestRat set on its
// landing circle. Without the Compass nobody is at the loom; met anyway (rcon places it) it turns TestRat gently away ("Not yet").
// The Compass given (rcon: admin/keeper/compass): the Keeper appears on the dais, tending its loom; TestRat climbs up and speaks
// to it - the send-off counts the threads, it bows and weaves, a second word while it weaves is "a moment more", and the Bond
// Thread is put in TestRat's hands, the Keeper along with it. Then: no second Keeper (bm.tkmet). Rcon carries TestRat and the
// Keeper home together. Then TUG (yanked in), THE WEAVE (bound, held fast), MEND (TestRat and the Mireling, out beside it:
// Regeneration II), BOND (one other follower near: Luck), GIFT (out of a fight: "a little gift"), the motes' spin; then the
// shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
const IX = -2600, IY = 262, IZ = 2600;                              // (phase253: the template's corner)
const AX = IX + 13.5, AY = IY + 20, AZ = IZ + 23.5;                 // (keeper_sanctuary.ARRIVAL: the landing circle)
const DX = IX + 13.5, DY = IY + 22, DZ = IZ + 13.5;                 // (keeper_sanctuary.SPAWN: the dais, before the loom)
const BOX = `x=${IX},y=${IY},z=${IZ},dx=26,dy=30,dz=26`;
runT({ W: 'keeper', NAME: 'The Keeper of Bonds', ab: 'tk', q: 'qb', pfx: 'p254', prefix: 'kb_', item: 'bond_thread', parts: 20, figParts: 18, hp: 40, X: 19000, Z: 16000, pron: 'it',
  called: /glides back to your side/, home: /unravels into a hundred bright threads/, sit: /kneels on its robe/, stand: /Shall we go on/,
  ways: ['Tug', 'Mend', 'The Weave', 'Gift', 'Bond', 'The Motes'], plain: 'Cream and gold', looks: ['Dawn Weave', 'Twilight Weave', 'Meadow Weave'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, X, Y, Z, cnt, entOf, at, score, PET } = ctx;
    const ENC = `@e[type=minecraft:interaction,tag=bm.tkenc,${BOX},limit=1]`;
    const PARTS = `@e[type=minecraft:item_display,tag=bm.tkencp,${BOX}]`;
    const qsq = async () => score('bm.qbsq', ENC);
    // ---- the stage: the island in the sky, TestRat on its landing circle - no Compass, no thread
    await run(`${O}forceload add ${IX - 4} ${IZ - 4} ${IX + 30} ${IZ + 30}`);
    await run('advancement revoke TestRat only bm:met/mireling');      // (one friend short of all: the test world's player has met everyone - the Compass would come by itself)
    await run('tag TestRat remove bm.kbcomp'); await run('tag TestRat remove bm.tkmet'); await run('clear TestRat');
    await run('scoreboard players set #kbwant bm.p2 1');
    ok('the Loom Sanctuary is woven into the sky (#kbver, its markers)', await wait(20000, async () => (await score('bm.p2', '#kbver')) >= 1 &&
       (await cnt(`@e[type=minecraft:marker,tag=bm.kb_spawn,tag=bm.kbm,${BOX}]`)) === 1, 500));
    await run(`${O}execute as @e[type=minecraft:interaction,tag=bm.tkenc,${BOX}] at @s run function bm:p254/enc/gone`);
    await at(AX, AY, AZ, 180, 0); await sleep(3000);
    ok('on the island without the Compass: nobody at the loom', (await cnt(ENC)) === 0,
       `enc ${await cnt(ENC)} kbcomp ${await cnt('@a[name=TestRat,tag=bm.kbcomp]')} compass ${await has('bond_compass')} allmet ${await run('execute as TestRat if function bm:p253/all_met run scoreboard players get TestRat bm.pid')}`);
    ok('...and TestRat is in Adventure mode there', (await cnt('@a[name=TestRat,gamemode=adventure]')) === 1);
    // ---- met anyway (rcon places it, as admin/keeper_meet does): turned gently away
    await run('execute as TestRat at @s run function bm:admin/keeper_meet');
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1200);
    ok('no Compass: "Not yet, little one" - no thread given', A.chats.some(c => /Not yet, little one/.test(c)) && (await has('bond_thread')) === 0, A.chats.slice(-1).join('').slice(0, 160));
    await run(`${O}execute as ${ENC} at @s run function bm:p254/enc/gone`); await sleep(500);
    // ---- the Compass: the Keeper is at its loom
    await run('advancement grant TestRat only bm:met/mireling'); await run('clear TestRat bond_compass');
    await run('execute as TestRat at @s run function bm:admin/keeper/compass'); await sleep(400);
    ok('the Compass of Bonds in the pack', (await has('bond_compass')) === 1);
    ok('...and the Keeper appears on the dais, before its loom', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       Math.abs((await ctx.num(ENC, 'Pos[1]')) - DY) < 0.6 && Math.abs((await ctx.num(ENC, 'Pos[2]')) - DZ) < 0.6, `y ${await ctx.num(ENC, 'Pos[1]')}`);
    ok('...its rig: 20 parts', (await cnt(PARTS)) === 20, `${await cnt(PARTS)} in box; anywhere ${await cnt('@e[type=minecraft:item_display,tag=bm.tkencp]')}; kb parts ${await cnt('@e[type=minecraft:item_display,tag=bm.tkp]')}`);
    // ---- up onto the dais; spoken to
    await at(DX, DY, DZ + 2, 180, 15);
    eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1200);
    ok('spoken to: the send-off - "There you are"', A.chats.some(c => /There you are/.test(c)), A.chats.slice(0, 1).join('').slice(0, 160));
    ok('...it counts the threads - your friends', A.chats.some(c => /threads/.test(c) && /friends? who were glad you came/.test(c)), A.chats.slice(2, 3).join('').slice(0, 160));
    ok('...and it bows, and begins to weave (bm.qbsq)', (await qsq()) > 1);
    A.bars.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(700);
    ok('...a second word while it weaves: "only a moment more"', A.bars.some(b => /only a moment more/.test(b)), A.bars.slice(-1).join(''));
    A.chats.length = 0;
    ok('...the last thread woven: the Bond Thread in TestRat\'s hands', await wait(10000, async () => (await has('bond_thread')) === 1), A.chats.slice(-1).join('').slice(0, 160));
    ok('..."Wherever you go now, I go with you" - and it joins you', A.chats.some(c => /Wherever you go now/.test(c)) && A.chats.some(c => /joins you/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('...the Keeper at the dais gone into the follower', await wait(3000, async () => (await cnt(ENC)) === 0 && (await cnt(PARTS)) === 0) &&
       await wait(4000, async () => (await cnt(PET)) === 1));
    await sleep(3000);
    ok('once: with its thread, no second Keeper at the loom (bm.tkmet)', (await cnt(ENC)) === 0 && /bm\.tkmet/.test(await run('tag TestRat list')));
    // ---- home together (rcon: the stage)
    await run('tag TestRat add bm.tktp'); await run(`${O}tag ${PET} add bm.tktp`);
    await run(`${O}tp @e[tag=bm.tktp] ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`${O}tag @e[tag=bm.tktp] remove bm.tktp`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - X - 0.5) < 0.05, 100);
    ok('...off the island: back in survival', await wait(4000, async () => (await cnt('@a[name=TestRat,gamemode=survival]')) === 1));
    await run('clear TestRat *[minecraft:custom_data~{bm:"bond_compass"}]');
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait, O, cnt, num, nbt, A, sleep, PET, use } = ctx; const K = kit(ctx, 'qb');
    const amp = (fxs, e, a) => new RegExp(`${e}[^}]*amplifier: ?${a}b|amplifier: ?${a}b[^}]*${e}`).test(fxs);
    ok('TUG - a foe 7 off: a thread cast, hurt, and yanked in', await K.move('rc', [[0, 7]], 'bm.trpt', async () => (await K.hp('bm.trpt')) < 300 &&
       (await num('@e[tag=bm.trpt,limit=1]', 'Pos[2]')) < Z + 6.5, 7000));
    ok('THE WEAVE - two foes near: bound (held fast), hurt twice', await K.move('gc', [[3, 3], [-3, 3]], 'bm.trpw', async () => (await K.hp('bm.trpw')) < 288 &&
       amp(await K.fxOf('bm.trpw'), 'slowness', 6), 9000));
    // ---- another follower out beside it (the Mireling, called with its Seed as the player would)
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10);
    await run('loot replace entity TestRat hotbar.4 loot bm:items/mire_seed'); await use(4);
    const ML = '@e[type=minecraft:wolf,tag=bm.mlpet,tag=!bm.ffpet,limit=1]';
    ok('the Mireling called out beside it', await wait(4000, async () => (await cnt(ML)) === 1));
    for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await run(`${O}scoreboard players set ${ML} bm.mj${o} 900`);   // (its own powers kept quiet)
    await run('effect clear TestRat'); await sleep(2500);
    ok('BOND - one other follower near: Luck', await wait(4000, async () => /luck/.test(await fx())), await fx());
    await run('effect clear TestRat'); await run('damage TestRat 6 minecraft:generic'); await run(`${O}damage ${ML} 8 minecraft:generic`);
    await run(`${O}effect clear ${ML} minecraft:regeneration`); await ctx.zom(0, 8, 'bm.trpm'); await K.cd('sc', 0);
    ok('MEND - you hurt, a foe about: Regeneration II', await wait(6000, async () => amp(await fx(), 'regeneration', 1)), await fx());
    ok('...and the Mireling beside you too', amp(await nbt(ML, 'active_effects'), 'regeneration', 1), await nbt(ML, 'active_effects'));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat');
    A.bars.length = 0; await K.cd('k', 0);
    ok('GIFT - out of a fight beside you: a little gift', await wait(6000, async () => A.bars.some(b => /a little gift/.test(b))), A.bars.slice(-1).join(''));
    const MOTE = '@e[type=minecraft:item_display,tag=bm.tkp_pet,tag=bm.tkp_motes,limit=1]';
    const r1 = await nbt(MOTE, 'transformation.right_rotation'); await sleep(2500); const r2 = await nbt(MOTE, 'transformation.right_rotation');
    ok('THE MOTES - its ring of bonds turns (right_rotation, a step a second)', r1 !== r2 && /f/.test(r1), `${r1} -> ${r2}`);
    await run('execute as TestRat at @s run function bm:p252/home'); await sleep(500);
    await run('clear TestRat *[minecraft:custom_data~{bm:"mire_seed"}]'); await run('scoreboard players set TestRat bm.mlcd 0');
    await K.calm();
  } });
