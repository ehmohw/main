// Use every right-click / consumable item once as a real player and record what visibly happened.
const { bot, rcon, sleep } = require('./lib');
const ids = require('./active.json');
const X = 5000, Y = 100, Z = 5000;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(800);
  const rows = [];
  const snap = async () => ({
    inv: await run('data get entity TestRat Inventory'), pos: await run('data get entity TestRat Pos'),
    fx: (await run('data get entity TestRat active_effects')).replace(/duration: -?\d+, /g, ''), hp: await run('data get entity TestRat Health'),
    xp: await run('xp query TestRat levels'), veh: await run('execute as TestRat on vehicle run data get entity @s id'),
    ents: await run(`execute store result score #e bm.rng if entity @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`)});
  for (const id of ids) {
    await run('ride TestRat dismount'); await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode survival TestRat');
    await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:saturation infinite 0 true');
    await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('kill @e[type=minecraft:item,x=5000,y=100,z=5000,distance=..40]');
    await run(`loot give TestRat loot bm:items/${id}`); await run('give TestRat minecraft:diamond_sword'); // an item in the off hand for items that need one
    await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.1'); await run('item replace entity TestRat hotbar.1 with minecraft:air');
    A.slot(0); await sleep(250); A.bars = []; A.chats = []; A.windows = [];
    const before = await snap();
    A.use(); await sleep(2000); A.release(); await sleep(400);
    const after = await snap();
    const ch = [];
    if (A.bars.length) ch.push('bar: ' + [...new Set(A.bars)].join(' | ').slice(0, 110));
    if (A.chats.length) ch.push('chat: ' + A.chats.map(c => c.replace(/\[Black Market\] /, '')).join(' | ').slice(0, 110));
    if (before.inv !== after.inv) ch.push('inventory changed');
    if (before.pos !== after.pos) ch.push('moved');
    if (before.fx !== after.fx) ch.push('effects: ' + ((after.fx.match(/id: "minecraft:([a-z_]+)"/g) || []).map(s => s.slice(15, -1)).filter(e => !['resistance', 'saturation'].includes(e)).join(',') || 'changed'));
    if (before.hp !== after.hp) ch.push('health ' + after.hp.split(' ').pop());
    if (before.xp !== after.xp) ch.push('xp changed');
    if (before.veh !== after.veh) ch.push('riding');
    if (before.ents !== after.ents) ch.push('entities nearby changed');
    if (A.windows.length) ch.push('window opened');
    rows.push([id, ch]); console.log((ch.length ? 'OK   ' : 'NONE ') + id.padEnd(26) + ch.join('; '));
    await run('kill @e[type=!minecraft:player,tag=!bm.npc,x=5000,y=100,z=5000,distance=..40,type=!minecraft:marker]');
  }
  console.log(`\n${rows.filter(r => r[1].length).length}/${rows.length} items did something visible`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
