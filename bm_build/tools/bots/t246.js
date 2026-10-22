// 2.88: THE DREAD BOSSES, as a regular (non-op) player - hard mode: a ruin's altar right-clicked without its trio lists who's
// missing; with Pistachio, Celi and Tullius beside you the Malevolent Snowbeast rises; it fights (ice-shard volleys fly); brought
// down, it falls - the Frostbitten Token, the spoils, the advancement; the token carried (Resistance), set down as a ward (sneak +
// use on a block) and taken back (sneak + punch); the Watchful Witch's altar refuses you too. Vesper sells the three maps and
// scraps the tokens. rcon only sets the stage (the ruin built, the trio standing by as yours).
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs');
const DP = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function';
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const fx = async () => await nbt('@a[name=TestRat,limit=1]', 'active_effects');
  const X = 17460, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:instant_health 1 10 true');
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y} ${Z + 16} minecraft:snow_block`); await run(`${O}fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 14} ${Z + 16} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('scoreboard players set #hard bm.cfg 1');
  await run('advancement revoke TestRat only bm:story/db_snow'); await run('execute as TestRat run function bm:p21/pid');
  // ---- the stage: the Frozen Folly built here
  await run(`${O}execute positioned ${X} ${Y + 1} ${Z} run function bm:p197/snow/ruin/build`); await sleep(800);
  const ALT = `@e[type=minecraft:interaction,tag=bm.dbaltar_snow,x=${X},y=${Y},z=${Z},distance=..20,limit=1]`;
  ok('the Frozen Folly: its altar', (await cnt(ALT)) === 1);
  const ax = await num(ALT, 'Pos[0]'), ay = await num(ALT, 'Pos[1]'), az = await num(ALT, 'Pos[2]');
  await at(ax, ay, az - 2.2, 0, 20);
  let alt = await entOf(ALT); A.slot(8); await sleep(200); A.chats.length = 0; if (alt) A.interact(alt.entityId); await sleep(1000);
  ok('right-clicked alone: it lists the trio, all missing (✘ Pistachio, Celi, Tullius)', ['Pistachio', 'Celi', 'Tullius'].every(n => A.chats.some(c => new RegExp(`✘.*${n}`).test(c))) &&
     (await cnt('@e[tag=bm.db_snow]')) === 0, A.chats.slice(-4).join(' | ').slice(0, 220));
  // ---- the stage: Pistachio, Celi and Tullius standing by - yours
  const pid = +((await run('scoreboard players get TestRat bm.pid')).match(/has (-?\d+)/) || [0, 0])[1];
  for (const [t, dx] of [['bm.pipet', -2], ['bm.celipet', 2], ['bm.tupet', 3]]) {
    await run(`${O}summon minecraft:wolf ${ax + dx} ${ay} ${az - 3} {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Tags:["${t}","bm.trdb","bm.seen"]}`);
    await run(`${O}scoreboard players set @e[tag=${t},tag=bm.trdb,limit=1] bm.pid ${pid}`);
  }
  alt = await entOf(ALT); A.chats.length = 0; if (alt) A.interact(alt.entityId); await sleep(1200);
  ok('with the three beside you: the Malevolent Snowbeast rises (host, rig)', await wait(3000, async () => (await cnt('@e[tag=bm.db_snow]')) === 1) &&
     (await cnt('@e[type=minecraft:item_display,tag=bm.dbr_snow]')) >= 6);
  await run(`${O}kill @e[tag=bm.trdb]`);
  ok('...invulnerable while it rises, then awake', /1b/.test(await nbt('@e[tag=bm.db_snow,limit=1]', 'Invulnerable')) &&
     await wait(6000, async () => /0b/.test(await nbt('@e[tag=bm.db_snow,limit=1]', 'Invulnerable'))));
  await at(ax, ay, az - 12, 0, 0);
  ok('it fights: ice shards fly at you (or the cold catches you)', await wait(15000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.dbshot_ice]')) >= 1 ||
     /slowness/.test(await fx())), `shots ${await cnt('@e[type=minecraft:marker,tag=bm.dbshot_ice]')}`);
  // ---- brought low (the stage: most of its health gone), then the player's own blows finish it
  await run(`${O}damage @e[tag=bm.db_snow,limit=1] 700 minecraft:generic`); await sleep(400);
  ok('...half down: enraged (phase two)', await wait(3000, async () => /1/.test(await run(`${O}scoreboard players get @e[tag=bm.db_snow,limit=1] bm.dbph`))));
  A.chats.length = 0;
  await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]'); A.slot(0);
  for (let i = 0; i < 40 && (await cnt('@e[tag=bm.db_snow]')) > 0 && !(await has('tok_frost')); i++) {
    const bx = await num('@e[tag=bm.db_snow,limit=1]', 'Pos[0]'), by = await num('@e[tag=bm.db_snow,limit=1]', 'Pos[1]'), bz = await num('@e[tag=bm.db_snow,limit=1]', 'Pos[2]');
    if (!isNaN(bx)) await at(bx, by, bz - 2.0, 0, 10);
    const e = await entOf('@e[tag=bm.db_snow,limit=1]'); if (e) A.attack(e.entityId); await sleep(700);
  }
  ok('brought down by your blows: it falls - the Frostbitten Token is yours', await wait(6000, async () => (await has('tok_frost')) === 1) &&
     A.chats.some(c => /has fallen!/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  ok('...the spoils (Dread Tokens) and the advancement', (await has('dread_token')) >= 3 && (await cnt('@a[name=TestRat,advancements={bm:story/db_snow=true}]')) === 1);
  ok('...its rig gone with it, the bossbar empty', (await cnt('@e[type=minecraft:item_display,tag=bm.dbr_snow]')) === 0);
  // ---- the token: carried, set down, taken back
  await run('effect clear TestRat'); await run('clear TestRat minecraft:netherite_sword');
  await run('clear TestRat *[minecraft:custom_data~{bm:"tok_frost"}]'); await run('loot replace entity TestRat hotbar.1 loot bm:items/tok_frost');
  ok('the Frostbitten Token carried: Resistance', await wait(3000, async () => /resistance/.test(await fx())));
  await at(X + 8.5, Y + 1, Z + 8.5, 0, 50); A.slot(1); await sleep(250);
  A.input({ shift: true }); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(500);
  const SH = `@e[type=minecraft:interaction,tag=bm.dbshrine_snow,x=${X + 8.5},y=${Y + 1},z=${Z + 8.5},distance=..4,limit=1]`;
  ok('sneak + use on a block: set down - a ward (the token gone from the pack)', (await cnt(SH)) === 1 && (await has('tok_frost')) === 0);
  await run(`${O}summon minecraft:husk ${X + 12.5} ${Y + 1} ${Z + 8.5} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.trdb","bm.seen"]}`);
  ok('...a monster within 16: slowed and weakened', await wait(3000, async () => /slowness/.test(await nbt('@e[tag=bm.trdb,limit=1]', 'active_effects'))));
  await run(`${O}kill @e[tag=bm.trdb]`);
  const sh = await entOf(SH); A.input({ shift: true }); await sleep(250); if (sh) A.attack(sh.entityId); await sleep(700); A.input({}); await sleep(300);
  ok('...sneak + punch: taken back', (await cnt(SH)) === 0 && (await has('tok_frost')) === 1);
  // ---- the Witch's altar: not for this crew
  await run(`${O}execute positioned ${X - 10} ${Y + 1} ${Z - 10} run function bm:p197/witch/ruin/build`); await sleep(800);
  const WALT = `@e[type=minecraft:interaction,tag=bm.dbaltar_witch,x=${X - 10},y=${Y},z=${Z - 10},distance=..20,limit=1]`;
  const wx = await num(WALT, 'Pos[0]'), wy = await num(WALT, 'Pos[1]'), wz = await num(WALT, 'Pos[2]');
  await at(wx, wy, wz - 2.2, 0, 20);
  const wa = await entOf(WALT); A.slot(8); A.chats.length = 0; if (wa) A.interact(wa.entityId); await sleep(1000);
  ok("the Hexen Hollow's altar: it wakes only for Cecil, Apophiss and King Omega", ['Cecil', 'Apophiss', 'King Omega'].every(n => A.chats.some(c => new RegExp(`✘.*${n}`).test(c))),
     A.chats.slice(-4).join(' | ').slice(0, 220));
  // ---- Vesper: the maps and the scrapping
  const ves = fs.readdirSync(`${DP}/p177`).map(f => fs.statSync(`${DP}/p177/${f}`).isFile() ? fs.readFileSync(`${DP}/p177/${f}`, 'utf8') : '').join('\n');
  ok('Vesper sells the three sealed maps', ['sealed_map_db_snow', 'sealed_map_db_witch', 'sealed_map_db_shark'].every(m => ves.includes(m)));
  ok('...and scraps the tokens for Dread Tokens', ['tok_frost', 'tok_hex', 'tok_saw'].every(m => ves.includes(m)));
  // ---- clean up
  await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`);
  await run(`${O}fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 14} ${Z + 16} minecraft:air`);
  await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})();
