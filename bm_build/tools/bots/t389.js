// 3.1: THE DOODLE MOB (phase263 - the Doodle Dragon renamed, his crayon mob forms) as a regular (non-op) player. rcon sets the stage:
// TestRat a new friend of his (met after 3.1: the Zombie, no Ender Dragon). Called with his drawing: the Doodle ZOMBIE (his cards
// dmzo_). A BONE handed to him (a right-click holding it): spent, unlocked, the SKELETON. A block of IRON: the IRON GOLEM, his click
// box refitted. An EGG before he has killed a baby zombie: refused, kept. His ways (the menu) are the golem's. His wardrobe: the
// Skeleton row switches him back; the Ender Dragon row locked. An OLD friend (met before 3.1): the Ender Dragon kept, on.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => {
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const tags = async () => (await run('tag TestRat list'));
  const held = async (id) => +(((await run(`clear TestRat ${id} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const X = 19180, Y = 100, Z = 16000;
  const PET = '@e[type=minecraft:wolf,tag=bm.ddpet,tag=!bm.ffpet,limit=1]';
  const HIT = '@e[type=minecraft:interaction,tag=bm.ddhit,limit=1]';
  const mdl = async (p) => (await nbt(`@e[type=minecraft:item_display,tag=bm.ddp_pet,tag=bm.ddp_${p},tag=!bm.ddfade,limit=1]`, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05, 100); await sleep(300); };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // ---- the stage: a floor; TestRat a friend of his from after 3.1 (the Zombie; no Ender Dragon, no other form, no baby zombie killed)
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(1500);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await run('kill @e[type=minecraft:wolf,tag=bm.ddpet]');
  for (const t of ['bm.ddend', 'bm.ddbz', 'bm.ddu_sk', 'bm.ddu_jo', 'bm.ddu_go', 'bm.ddu_ax', 'bm.ddu_en']) await run(`tag TestRat remove ${t}`);
  for (const t of ['bm.ddmet', 'bm.ddmob', 'bm.ddu_zo']) await run(`tag TestRat add ${t}`);
  for (const [o, v] of [['bm.ddf', 1], ['bm.ddcr', 0], ['bm.ddog', 0], ['bm.dducd', 0], ['bm.cosdd', 0]]) await run(`scoreboard players set TestRat ${o} ${v}`);
  await run('scoreboard players set TestRat bm.ddcd 0');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/doodle_drawing');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0); await sleep(2300);
  A.slot(0); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(2500);
  ok('his drawing used: the Doodle Mob comes - as the Doodle ZOMBIE (his body dmzo_body, the host tagged bm.ddmf1)', (await cnt(PET)) === 1 && /^bm:dmzo_body$/.test(await mdl('body')) &&
     (await cnt('@e[type=minecraft:wolf,tag=bm.ddpet,tag=bm.ddmf1]')) === 1, await mdl('body'));
  await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await run(`data modify entity ${PET} Sitting set value 1b`); await sleep(1500);
  const hand = async (id) => { await run(`item replace entity TestRat hotbar.8 with ${id}`); A.slot(8); await sleep(400);
    const hb = await entOf(HIT); A.bars.length = 0; A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1200); return !!hb; };
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 30);
  // ---- a bone: the Skeleton
  ok('a BONE handed to him: spent - "the Doodle Skeleton!" - his cards dmsk_ (unlocked, bm.ddf 2)', await hand('minecraft:bone') && (await held('minecraft:bone')) === 0 &&
     A.chats.some(c => /Doodle Skeleton/.test(c)) && /bm\.ddu_sk/.test(await tags()) && (await score('bm.ddf')) === 2 && await wait(2000, async () => /^bm:dmsk_body$/.test(await mdl('body'))),
     `${await mdl('body')} | ${A.chats.slice(-1).join('').slice(0, 120)}`);
  // ---- a block of iron: the Iron Golem - his own pivots, his click box refitted
  const h0 = await num(HIT, 'width');
  ok('a block of IRON: the Doodle Iron Golem (dmgo_), his click box refitted wider', await hand('minecraft:iron_block') && (await score('bm.ddf')) === 4 &&
     await wait(2000, async () => /^bm:dmgo_body$/.test(await mdl('body'))) && (await num(HIT, 'width')) > h0 + 0.05, `${await mdl('body')} box ${h0} -> ${await num(HIT, 'width')}`);
  // ---- an egg, before he has killed a baby zombie: refused, kept
  ok('an EGG, no baby zombie killed yet: refused ("I need to SEE one first"), the egg kept', await hand('minecraft:egg') && A.bars.some(b => /SEE one first/.test(b)) &&
     (await held('minecraft:egg')) === 1 && (await score('bm.ddf')) === 4, A.bars.slice(-1).join(''));
  await run('clear TestRat minecraft:egg');
  // ---- his ways, from his menu: the golem's
  A.slot(0); await sleep(2300); const n0 = A.dialogN.length; A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); A.input({}); await wait(3000, async () => A.dialogN.length > n0);
  ok('sneak + use: his menu - "The Doodle Mob"', A.dialogN.length > n0 && /The Doodle Mob/.test(JSON.stringify(A.dialogN[A.dialogN.length - 1])), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
  let pr = await A.press(/ways/);
  ok('...his ways: the Iron Golem\'s (Iron Fist, Iron Toss, Ground Slam)', pr && ['Iron Fist', 'Iron Toss', 'Ground Slam'].every(w => JSON.stringify(A.dialogN[A.dialogN.length - 1]).includes(w)));
  await A.press(/Back/); await sleep(500);
  pr = await A.press(/Wardrobe/);
  ok('...his wardrobe: a row per form (the Ender Dragon, Zombie, Skeleton, Chicken Jockey, Iron Golem, Axolotl, Enderman)',
     pr && ['Doodle Ender Dragon', 'Doodle Zombie', 'Doodle Skeleton', 'Doodle Chicken Jockey', 'Doodle Iron Golem', 'Doodle Axolotl', 'Doodle Enderman'].every(l => A.buttons().some(b => b.label.includes(l))),
     A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  A.bars.length = 0; await A.press(/Doodle Ender Dragon/); await sleep(800);
  ok('...the Ender Dragon row, locked: a hint, nothing changed', A.bars.some(b => /Locked/.test(b)) && (await score('bm.ddf')) === 4, A.bars.slice(-1).join(''));
  await A.press(/Doodle Skeleton/); await sleep(1500);
  ok('...the Skeleton row: back to the Doodle Skeleton', (await score('bm.ddf')) === 2 && await wait(2000, async () => /^bm:dmsk_body$/.test(await mdl('body'))), await mdl('body'));
  // ---- a blow as the Skeleton (a foe in reach, his claw's cooldown cleared): hurt
  await run(`data modify entity ${PET} Sitting set value 0b`);
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 4.5} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t389z","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 2.6}`);
  for (const o of ['gc', 'k2', 'rc', 'k', 'sc']) await run(`scoreboard players set ${PET} bm.dz${o} 900`); await run(`scoreboard players set ${PET} bm.dzmc 0`);
  ok('...his blow as the Skeleton (Bone Bonk): the husk hurt', await wait(6000, async () => (await num('@e[tag=bm.t389z,limit=1]', 'Health')) < 300));
  await run(`${O}kill @e[tag=bm.t389z]`);
  // ---- an old friend (met before 3.1): the Ender Dragon kept
  await run('tag TestRat remove bm.ddmob'); await run('scoreboard players reset TestRat bm.ddf');
  ok('an OLD friend of his (met before the Doodle Mob): the Ender Dragon kept - unlocked and on (bm.ddend, bm.ddf 0)', await wait(3000, async () => /bm\.ddend/.test(await tags()) && (await score('bm.ddf')) === 0));
  // ---- clean up
  for (const t of ['bm.ddu_sk', 'bm.ddu_go']) await run(`tag TestRat remove ${t}`);
  await run('kill @e[type=minecraft:wolf,tag=bm.ddpet]'); await run('clear TestRat'); await run('effect clear TestRat');
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})();
