// Use every right-click / consumable item once as a real player and record what visibly happened.
// (3.1t) active.json: every item an advancement fires on when used or eaten (regenerate it from out_p2 - see the README);
// a dialog, a sound or particles count as something happening; START/END (env) pick a slice, so a cut-off sweep resumes;
// IDS=a,b,c sweeps just those. Each item is held for its own use time, from full health.
// (3.1u) STAGE sets up what an item needs, on a stone floor: mob (a husk that can't walk, 4 blocks ahead), wall (a stone wall 3 ahead),
// floor (looking down, used on the floor), sneak (used while sneaking). A staged run also counts blocks changed nearby and a hurt,
// frozen or moved husk.
const { bot, rcon, sleep } = require('./lib_resp');
const ids = process.env.IDS ? process.env.IDS.split(',') : require('./active.json').slice(+(process.env.START || 0), +(process.env.END || 1e9));
const X = 5000, Y = 100, Z = 5000, STAGE = process.env.STAGE || '';
const BOX = `${X - 6} ${Y - 1} ${Z - 6} ${X + 10} ${Y + 5} ${Z + 6}`, REF = `${X - 6} ${Y + 40} ${Z - 6}`;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(800);
  await run('deop TestRat');
  let snd = 0, ptc = 0, spn = 0;
  A.on('sound_effect', () => snd++); A.on('entity_sound_effect', () => snd++); A.on('world_particles', () => ptc++);
  // (a bolt or fireball that's gone by the after-snapshot still counts - only what appears right by the player: mobs wandering into view don't)
  A.on('spawn_entity', (p) => { if (Math.hypot(p.x - X - 0.5, p.y - Y - 1, p.z - Z - 0.5) < 4) spn++; });
  const rows = [];
  // (the background: what particles and sounds reach an empty-handed player here in 3 s - only well above it counts)
  await run('clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await sleep(1500);
  snd = 0; ptc = 0; spn = 0; await sleep(3000); const bgP = ptc / 3000, bgS = snd / 3000, bgN = spn / 3000;
  console.log(`background: ${(bgP * 1000).toFixed(0)} particles and ${(bgS * 1000).toFixed(1)} sounds a second`);
  const snap = async () => ({
    inv: await run('data get entity TestRat Inventory'), pos: await run('data get entity TestRat Pos'),
    fx: (await run('data get entity TestRat active_effects')).replace(/duration: -?\d+, /g, ''), hp: await run('data get entity TestRat Health'),
    xp: await run('xp query TestRat levels'), veh: await run('execute as TestRat on vehicle run data get entity @s id'),
    ents: await run(`execute store result score #e bm.rng if entity @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`),
    mob: STAGE === 'mob' ? await (async () => { let o = (await run(`execute if entity @e[type=minecraft:husk,tag=bm.swmob]`)) + '|'; for (const k of ['Health', 'NoAI', 'Fire', 'HurtTime', 'Pos', 'active_effects']) o += (await run(`data get entity @e[type=minecraft:husk,tag=bm.swmob,limit=1] ${k}`)).replace(/duration: -?\d+, /g, '').replace(/(\d+\.\d)\d*/g, '$1') + '|'; return o; })() : ''});
  for (const id of ids) {
    await run('ride TestRat dismount'); await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode survival TestRat');
    await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:saturation infinite 0 true'); await run('effect give TestRat minecraft:instant_health 1 5 true');   // (full health: some items want it)
    await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 ${STAGE === 'floor' ? 90 : 0}`); await run('kill @e[type=minecraft:item,x=5000,y=100,z=5000,distance=..40]');
    if (STAGE) {      // (a clean stage each time: what the last item poured, placed or summoned is gone)
      await run(`kill @e[type=!minecraft:player,tag=!bm.npc,x=${X},y=${Y},z=${Z},distance=..14]`);
      await run(`fill ${X - 6} ${Y - 1} ${Z - 6} ${X + 10} ${Y - 1} ${Z + 6} minecraft:stone`); await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 10} ${Y + 5} ${Z + 6} minecraft:air`);
      if (STAGE === 'wall') await run(`fill ${X + 3} ${Y} ${Z - 3} ${X + 3} ${Y + 3} ${Z + 3} minecraft:stone`);
      // (seen and tiered: no elite or champion roll changes it mid-test)
      if (STAGE === 'mob') await run(`summon minecraft:husk ${X + 4.5} ${Y} ${Z + 0.5} {Tags:["bm.swmob","bm.seen","bm.tiered"],PersistenceRequired:1b,Silent:1b,Rotation:[90f,0f],attributes:[{id:"minecraft:movement_speed",base:0.0d}]}`);
      await run(`clone ${BOX} ${REF}`);
    }
    await run(`loot give TestRat loot bm:items/${id}`); await run('give TestRat minecraft:diamond_sword'); // an item in the off hand for items that need one
    await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.1'); await run('item replace entity TestRat hotbar.1 with minecraft:air');
    A.slot(0);
    const fd = await run('data get entity TestRat SelectedItem.components."minecraft:food"');
    if (/data:/.test(fd) && !/can_always_eat: 1b/.test(fd)) { await run('effect clear TestRat minecraft:saturation'); await run('effect give TestRat minecraft:hunger 3 255 true'); await sleep(3200); }   // (food can't be eaten on a full stomach - Saturation's store goes first)
    await sleep(1500);       // (settle: an effect or heal pulsed onto every player isn't the item's)
    A.bars = []; A.chats = []; A.windows = []; const nd = A.dialogs.length; snd = 0; ptc = 0; spn = 0;
    const before = await snap();
    // (held as long as the item takes - a 3 s effigy let go at 2 s does nothing)
    const cs = +(((await run('data get entity TestRat SelectedItem.components."minecraft:consumable".consume_seconds')).match(/data: ([\d.]+)/) || [0, 0])[1]);
    const held = Math.min(5600, Math.max(2000, cs * 1000 + 600));      // (hold-to-use items say 100000 s)
    if (STAGE === 'sneak') { A.input({ shift: true }); await sleep(300); }
    if (STAGE === 'floor') A.useOn(X, Y - 1, Z, 1);
    A.use(); await sleep(held); A.release(); await sleep(400);
    if (STAGE === 'sneak') A.input({});
    const after = await snap();
    const ch = [];
    if (A.bars.length) ch.push('bar: ' + [...new Set(A.bars)].join(' | ').slice(0, 110));
    if (A.chats.length) ch.push('chat: ' + A.chats.map(c => c.replace(/\[Black Market\] /, '')).join(' | ').slice(0, 110));
    if (before.inv !== after.inv) ch.push('inventory changed');
    if (before.pos !== after.pos) ch.push('moved');
    if (before.fx !== after.fx) ch.push('effects: ' + ((after.fx.match(/id: "minecraft:([a-z_]+)"/g) || []).map(s => s.slice(15, -1)).filter(e => !['resistance', 'saturation'].includes(e)).join(',') || 'changed'));
    // (health isn't counted: pulses from the world - a Heartstone's boost, regeneration - move it on their own)
    if (before.xp !== after.xp) ch.push('xp changed');
    if (before.veh !== after.veh) ch.push('riding');
    if (before.ents !== after.ents) ch.push('entities nearby changed');
    if (A.windows.length) ch.push('window opened');
    if (process.env.DBG && before.mob !== after.mob) console.log(before.mob + '\n' + after.mob);
    if (before.mob !== after.mob) ch.push('the husk ' + (/^Test failed/.test(after.mob) ? 'is gone' : 'changed'));
    if (STAGE && !/passed/i.test(await run(`execute if blocks ${BOX} ${REF} all`))) ch.push('blocks changed');
    if (A.dialogs.length > nd) ch.push('dialog');
    const t_ = held + 400;
    if (snd > bgS * t_ * 1.5 + 0.5) ch.push(`${snd} sounds`);      // (one note from an ocarina is the item working)
    if (spn > bgN * t_ * 1.5 + 0.5) ch.push(`${spn} entities spawned`);
    if (ptc > bgP * t_ * 1.5 + 30) ch.push(`${ptc} particles`);
    rows.push([id, ch]); console.log((ch.length ? 'OK   ' : 'NONE ') + id.padEnd(26) + ch.join('; '));
    await run('kill @e[type=!minecraft:player,tag=!bm.npc,x=5000,y=100,z=5000,distance=..40,type=!minecraft:marker]');
  }
  console.log(`\n${rows.filter(r => r[1].length).length}/${rows.length} items did something visible`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
