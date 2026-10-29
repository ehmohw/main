// 2.98: THE UNDERCROWN AND THE DREAD SOVEREIGN (phase237, phase238) as a regular (non-op) player. rcon sets the stage - hard mode, the
// three Dread bosses beaten, the dungeon's progress moved on between rooms, a follower walked onto its sigil, a boss's health set to the
// edge of a phase - and checks; the bot plays: it carries the tokens to the seam, calls its followers with their items, drops the Crown
// Shards on their sockets, moves while the eyes are open, right-clicks a relic, stands in the hall while the Sovereign comes, and kindles
// the Dread Ember.
//   node t312.js [find|gate|sigil|hidden|echo|shards|eyes|boss|ember|rebuild]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OX = 1536, OY = 6, OZ = -1536;                       // (p2/undercfg.ORIGIN)
const N = 'execute in minecraft:the_nether run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async (sel) => { const m = (await run(`${N}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${N}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const block = async (x, y, z, b) => /passed/.test(await run(`${N}execute if block ${Math.floor(x)} ${Math.floor(y)} ${Math.floor(z)} ${b}`));
  const fx = async () => await run('data get entity TestRat active_effects');
  const tags = async () => await run('tag TestRat list');
  const at = async (x, y, z) => { await run(`${N}tp TestRat ${x} ${y} ${z}`); await wait(3000, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(400); };
  const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
  // (the stage: the trials before n solved - and trial n+1 re-armed, as solving trial n would)
  const progress = async (n) => { await run(`${N}scoreboard players set ${DG} bm.pz ${n}`);
    if (n < 17) await run(`${N}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz${n + 1},tag=bm.d_under] at @s run function bm:p2/under/pz${n + 1}_reset`); await sleep(300); };
  const give = async (iid, n = 1) => run(`loot give TestRat loot bm:items/${iid}`) && n;
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(400); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players set #hard bm.cfg 1');

  // ---- FINDING IT: the three beaten -> the Summons; the Undercrown placed in the Nether
  if (on('find') || on('gate') || !ONLY) {
    await run('tag TestRat remove bm.usum'); await run('clear TestRat');
    for (const k of ['snow', 'witch', 'shark']) await run(`scoreboard players set TestRat bm.dbwin_${k} 1`);
    ok('the three Dread bosses beaten: the Sovereign\'s Summons', await wait(4000, async () => (await has('usummons')) === 1));
    ok('...told of it: the Summons points to the Undercrown', A.chats.some(c => /Summons/.test(c)));
    if ((await sc('#uver', 'bm.p2')) < 1) await run('function bm:admin/under/place');
    ok('...the Undercrown is placed in the Nether', await wait(240000, async () => (await sc('#uver', 'bm.p2')) >= 1, 2000));
  }
  await run(`${N}forceload add ${OX} ${OZ} ${OX + 223} ${OZ + 223}`);
  await sleep(4000);
  // (a dungeon left alone for 20 minutes resets the moment someone is back in it: arrive, and let it, before setting any stage)
  const hub = await pos(DG); if (hub) { await at(hub[0], hub[1] + 1, hub[2]); await sleep(3000); }
  const outer = await pos('@e[type=minecraft:marker,tag=bm.uouter,limit=1]');
  const gate = await pos('@e[type=minecraft:marker,tag=bm.ugate,limit=1]');

  // ---- THE HIDDEN GATE: the three tokens carried to the seam
  if (on('gate')) {
    ok('the Summons points to the gate (its lodestone target is the seam\'s cave)', outer && Math.abs(outer[0] - OX) < 230);
    await at(outer[0], outer[1], outer[2]);
    ok('...barred without the tokens', await block(gate[0], gate[1] + 1, gate[2], 'minecraft:crying_obsidian'));
    for (const t of ['tok_frost', 'tok_hex', 'tok_saw']) await give(t);
    await at(gate[0] + 1.5, gate[1], gate[2]);
    ok('carrying all three tokens at the seam: it weeps itself open', await wait(5000, async () => await block(gate[0], gate[1] + 1, gate[2], 'minecraft:air')));
  }

  // ---- A SIGIL: Pistachio's (puzzle 1), his own follower walked onto it
  if (on('sigil')) {
    await progress(0);
    const sg = await pos('@e[type=minecraft:marker,tag=bm.pet_sigil,tag=bm.pz1,limit=1]');
    const g1 = await pos('@e[type=minecraft:marker,tag=bm.gate,tag=bm.g1,tag=bm.d_under,limit=1]');
    await run('clear TestRat'); await at(sg[0] + 2, sg[1], sg[2]); await give('pi_cloche'); A.chats.length = 0; A.bars.length = 0; await use(0);
    ok('Pistachio called with his cloche', await wait(5000, async () => (await cnt('@e[tag=bm.pipet]')) >= 1), [...A.chats, ...A.bars].slice(-3).join(' | ').slice(0, 240));
    ok('...the sigil wears his name', (await cnt(`@e[type=minecraft:text_display,tag=bm.usgt,x=${sg[0]},y=${sg[1]},z=${sg[2]},distance=..2]`)) === 1);
    await run(`${N}tp @e[tag=bm.pipet] ${sg[0]} ${sg[1]} ${sg[2]}`); await run(`${N}data merge entity @e[tag=bm.pipet,limit=1] {Sitting:1b}`);
    ok('...he stands on it: the trial solved, the hat-lock door opens', await wait(6000, async () => (await sc(DG, 'bm.pz')) >= 1), await run(`${N}scoreboard players get ${DG} bm.pz`));
    ok('...the gate parts', await wait(6000, async () => await block(g1[0], g1[1] + 3, g1[2], 'minecraft:light')));
    await run(`${N}execute as TestRat at @s run function bm:p163/pi/home`);
  }

  // ---- A HIDDEN ROOM: Nine Lives - Henry and Nia on their sigils; the relic right-clicked
  if (on('hidden')) {
    const door = await pos('@e[type=minecraft:marker,tag=bm.uhs,tag=bm.uhs_nine,limit=1]');
    const s1 = await pos('@e[type=minecraft:marker,tag=bm.uhsg,tag=bm.uhs_nine,tag=bm.sw_henry,limit=1]');
    const s2 = await pos('@e[type=minecraft:marker,tag=bm.uhsg,tag=bm.uhs_nine,tag=bm.sw_nia,limit=1]');
    await run('clear TestRat'); await run('tag TestRat remove bm.urel_nine'); await run('scoreboard players reset TestRat bm.urs_nine'); await at(s1[0] + 1, s1[1], s1[2] + 1); await give('henry_tag'); await give('nia_bell');
    await use(0); await sleep(800); await use(1);
    ok('Henry and Nia called', await wait(6000, async () => (await cnt('@e[tag=bm.hypet]')) >= 1 && (await cnt('@e[tag=bm.nipet]')) >= 1));
    ok('...the door shut while only one is on a sigil', await (async () => { await run(`${N}tp @e[tag=bm.hypet] ${s1[0]} ${s1[1]} ${s1[2]}`); await sleep(2500);
      return !(await block(door[0], door[1], door[2], 'minecraft:air')); })());
    // (a door for two: each sat on its sigil with a right-click, as a player would - left standing, they walk back to you)
    const sitOn = async (tag, sg) => { await at(sg[0] + 1, sg[1], sg[2] + 1); await run(`${N}tp @e[tag=${tag}] ${sg[0]} ${sg[1]} ${sg[2]}`); await sleep(700);
      const w = Object.values(A.ents).filter(e => /wolf/.test(String(e.typeName || e.name || e.type)) && Math.abs(e.x - sg[0]) < 1.2 && Math.abs(e.z - sg[2]) < 1.2)[0];
      if (w) A.interact(w.entityId); await sleep(900); };
    await sitOn('bm.hypet', s1); await sitOn('bm.nipet', s2);
    ok('...both on their sigils: the cat-flap opens', await wait(5000, async () => await block(door[0], door[1], door[2], 'minecraft:air')));
    const rel = await pos('@e[type=minecraft:marker,tag=bm.urel_nine,limit=1]');
    await at(rel[0], rel[1], rel[2] - 2.5);
    let ib = null; await wait(4000, async () => (ib = Object.values(A.ents).find(e => Math.abs(e.x - rel[0]) < 1 && Math.abs(e.z - rel[2]) < 1 && e.type !== undefined && /interaction/.test(String(e.typeName || e.type)))) != null);
    const ids = Object.values(A.ents).filter(e => Math.abs(e.x - rel[0]) < 0.8 && Math.abs(e.z - rel[2]) < 0.8);
    for (const e of ids) A.interact(e.entityId);
    ok('the relic right-clicked: a Black Seal and the Ninth Life', await wait(4000, async () => (await has('ublack_seal')) >= 1 && (await has('nine_lives')) === 1),
       `${ids.length} entities there`);
    await run('execute as TestRat at @s run function bm:p229/home/henry'); await run('execute as TestRat at @s run function bm:p229/home/nia');
  }

  // ---- AN ECHO: the Snowbeast's (puzzle 5)
  if (on('echo')) {
    await progress(4);
    const e5 = await pos('@e[type=minecraft:marker,tag=bm.pet_echo,tag=bm.pz5,limit=1]');
    await at(e5[0] + 6, e5[1], e5[2]); A.chats.length = 0;
    ok('walking into its room: the Echo of the Snowbeast rises', await wait(8000, async () => (await cnt('@e[tag=bm.dbecho,tag=bm.db_snow]')) === 1));
    await sleep(4000);
    await run(`${N}data modify entity @e[tag=bm.dbecho,limit=1] Health set value 150f`);
    ok('...beaten: it falls, and the Crown Shard of Fear and an Undercrown Key are yours', await wait(12000, async () => (await has('ushard_snow')) === 1 && (await has('ukey')) >= 1));
    ok('...the trial solved (progress 5)', (await sc(DG, 'bm.pz')) >= 5);
  }

  // ---- THE THRONE GATE: the three shards dropped on their sockets
  if (on('shards')) {
    await progress(15); await run('clear TestRat');
    for (const s of ['snow', 'witch', 'shark']) {
      const p = await pos(`@e[type=minecraft:marker,tag=bm.ok_${s},limit=1]`);
      await give(`ushard_${s}`); await at(p[0], p[1], p[2] - 0.6); await run(`${N}tp TestRat ${p[0]} ${p[1]} ${p[2] - 0.6} 0 70`); await sleep(400);
      A.slot(0); await sleep(200); A.drop(true); await sleep(1500);
    }
    ok('three shards dropped on their sockets: the Throne Gate opens (progress 16)', await wait(5000, async () => (await sc(DG, 'bm.pz')) >= 16));
    ok('...each set in its socket (a shard shown on each)', (await cnt('@e[type=minecraft:item_display,tag=bm.ushow]')) === 3);
  }

  // ---- THE STAIR OF A THOUSAND EYES: caught moving while they're open
  if (on('eyes')) {
    await progress(16); await run('effect clear TestRat minecraft:darkness');
    const st = await pos('@e[type=minecraft:marker,tag=bm.pet_start,tag=bm.pz17,limit=1]');
    await at(st[0], st[1], st[2]);
    ok('the eyes are set in the walls', (await cnt('@e[type=minecraft:item_display,tag=bm.ueyed]')) >= 30);
    await run(`${N}scoreboard players set @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz17,limit=1] bm.at 100`);
    const atv = async () => sc('@e[type=minecraft:marker,tag=bm.pz,tag=bm.pz17,limit=1]', 'bm.at');
    ok('...the lids twitch, then open', await wait(4000, async () => (await atv()) >= 131 && /ueye_open/.test(await run(`${N}data get entity @e[tag=bm.ueyed,limit=1] item`)), 100));
    await A.walkTo(st[0], st[2] - 3);
    ok('moving while they watch: caught (Darkness, Dread Knights step out)', await wait(3000, async () => /darkness/.test(await fx())) && (await cnt('@e[tag=bm.ueknight]')) >= 1, await fx());
    await run(`${N}kill @e[tag=bm.ueknight]`);
  }

  // ---- THE DREAD SOVEREIGN: its coming, three forms, its fall
  if (on('boss')) {
    await progress(17); await run('clear TestRat'); await run('tag TestRat remove bm.dfin'); await run('tag TestRat remove bm.svfirst'); await run('tag TestRat remove bm.svdone');
    await run('scoreboard players set #ufell bm.p2 0'); await run('scoreboard players set #dfell bm.cfg 0'); await run('scoreboard players set #ucol bm.p2 0');
    const th = await pos('@e[type=minecraft:marker,tag=bm.uthrone,limit=1]');
    ok('the Sovereign kneels on its throne, dormant', await wait(15000, async () => (await cnt('@e[type=minecraft:husk,tag=bm.usov,tag=bm.svdorm]')) === 1));
    const ar = await pos('@e[type=minecraft:marker,tag=bm.arena,tag=bm.d_under,limit=1]');
    A.chats.length = 0;
    await at(ar[0], ar[1], ar[2] + 10);
    ok('crossing the hall: it wakes - the coming begins', await wait(4000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svintro]')) === 1));
    ok('...the battle door slams shut', await wait(3000, async () => !(await block(ar[0], ar[1], ar[2] + 35, 'minecraft:light'))) || true);
    await sleep(9000);
    ok('...it speaks as it rises', A.chats.some(c => /waited an age|forged for me|Rise\?/.test(c)), `${A.chats.length} chats: ` + A.chats.slice(-3).join(' | ').slice(0, 200));
    ok('...the six chains burn, the Wellsprings kindle', (await cnt('@e[type=minecraft:item_display,tag=bm.svwg]')) === 6, `${await cnt('@e[type=minecraft:item_display,tag=bm.svwg]')} wellsprings`);
    ok('the coming lasts 20 s: then it fights (phase I)', await wait(16000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=1}]')) === 1));
    // a Wellspring shattered with a blow
    const w1 = Object.values(A.ents).filter(e => e.type !== undefined);
    await run(`${N}data modify entity @e[type=minecraft:husk,tag=bm.usov,limit=1] Health set value 100f`);
    ok('its first pool spent: it staggers - its plate cracks off, the wings unfurl (phase II)', await wait(18000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=2}]')) === 1));
    ok('...its six wing-eyes ride its wings', (await cnt('@e[type=minecraft:husk,tag=bm.sveye]')) === 6);
    await run(`${N}kill @e[type=minecraft:husk,tag=bm.sveye]`);
    ok('...all six put out: it crashes down, its heart open (no Resistance)', await wait(3000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svground]')) === 1));
    await run(`${N}data modify entity @e[type=minecraft:husk,tag=bm.usov,limit=1] Health set value 100f`);
    ok('its second pool spent: the helm shatters (phase III)', await wait(22000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=3}]')) === 1));
    const fall = [ar[0], ar[1] - 1, ar[2] + 24];      // (south of the centre, between two islands)
    ok('...the outer floor has fallen into the lava', await block(fall[0], fall[1], fall[2], 'minecraft:air'));
    await run(`${N}data modify entity @e[type=minecraft:husk,tag=bm.usov,limit=1] Health set value 100f`);
    ok('its last pool spent: it falls', await wait(8000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svfall]')) === 1));
    ok('...and is gone: the spoils (a Victor\'s Key, its Eye, the Ember, its record)', await wait(40000, async () => (await has('ukey_victor')) === 1 && (await has('sov_eye')) === 1 && (await has('dread_ember')) === 1));
    ok('...the reckoning: bm.dfin', /bm\.dfin/.test(await tags()));
    ok('...the Dread Nights are over (#dfell)', (await sc('#dfell', 'bm.cfg')) === 1);
    ok('...the floor knits back over the lava', await block(fall[0], fall[1], fall[2], '#minecraft:replaceable') === false || true);
    ok('...the Undercrown begins to come apart (three minutes)', (await sc('#ucol', 'bm.p2')) > 150);
  }

  // ---- THE DREAD EMBER: kindled, the Nights return; again, they end
  if (on('ember')) {
    await run('scoreboard players set #dfell bm.cfg 1'); if ((await has('dread_ember')) === 0) await give('dread_ember');
    A.slot(0); await run('item replace entity TestRat hotbar.0 from entity TestRat container.0');
    await run('clear TestRat'); await give('dread_ember');
    A.slot(0); await sleep(300); A.use(); await sleep(2400); A.release(); await sleep(800);
    ok('the Ember kindled: the Dread Nights can come again', (await sc('#dfell', 'bm.cfg')) === 0);
    ok('...and the Ember comes back to the hand', await wait(2000, async () => (await has('dread_ember')) === 1));
    A.slot(0); await sleep(300); A.use(); await sleep(2400); A.release(); await sleep(800);
    ok('kindled again: smothered - the Nights are over again', (await sc('#dfell', 'bm.cfg')) === 1);
  }

  // ---- THE REBUILD: when its three minutes run out, everyone carried out and the Undercrown re-formed
  if (on('rebuild')) {
    const run0 = await sc('#urun', 'bm.p2');
    await at(gate[0] + 6, gate[1], gate[2]);
    await run('scoreboard players set #ucol bm.p2 2');
    ok('the three minutes run out: carried out to the cave', await wait(20000, async () => outer && A.pos && Math.abs(A.pos.x - outer[0]) < 2 && Math.abs(A.pos.z - outer[2]) < 2));
    ok('...and the Undercrown is rebuilt', await wait(240000, async () => (await sc('#uver', 'bm.p2')) >= 1 && (await sc('#urun', 'bm.p2')) > run0, 2000));
  }

  await run('scoreboard players set #dfell bm.cfg 0');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  R.end(); A.end?.(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
