// 3.0x: DENNIS'S RICH SEAM (phase162's natural-ground tables, phase163's bm.dwrs), as a regular (non-op) player, every block
// mined by a real dig packet (rcon only sets the stage: a floor, the blocks to mine, the tools, Ava's honour on bm.hn_dennis,
// the test hook #dwrs_test bm.cfg that makes the 1 in 10 every time):
//   his ways, honoured only to rank II: "Rich Seam (locked)" and how it's unlocked; at rank III: Rich Seam, unlocked;
//   rank III, Dennis out (sat, within 24) and the hook on: bm.dwrs 2 - stone, dirt and an oak log each drop twice (cobblestone,
//   dirt, logs); stone by a silk-touch pickaxe: two stone (silk touch kept); diamond ore by the silk-touch pickaxe: one ore
//   apiece (ores are Fortune V's, never Rich Seam's); a TNT blast in the stone beside you: never more than a block apiece;
//   the hook off: the real 1 in 10 (60 stone: more cobblestone than stone mined, and nothing like twice);
//   rank II (hook on): nothing extra; rank III but Dennis sent home: nothing extra, the mark gone.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const plain = async (iid) => +(((await run(`clear TestRat minecraft:${iid} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const ground = async (iid, x, y, z, r = 10) => ((await run(`${O}execute as @e[type=minecraft:item,x=${x},y=${y},z=${z},distance=..${r}] if items entity @s contents minecraft:${iid} run data get entity @s Item.count`))
    .match(/data: \d+/g) || []).reduce((a, m) => a + +m.slice(6), 0);
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const sneakMenu = async (slot) => { await sleep(1000); const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const press = async (re) => { await sleep(1000); return A.press(re); };
  const click = async (re) => { await sleep(1000); return A.click(re); };
  const dd = (d) => d && (d.data || d);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  const X = 16740, Y = 100, Z = 16000;
  const PET = '@e[type=minecraft:wolf,tag=bm.dwpet,tag=!bm.ffpet,limit=1]';
  const ITEMS = `@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`;
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.dwpet]');
  await run('scoreboard players set TestRat bm.dwcd 0'); await run('scoreboard players set #dwrs_test bm.cfg 0');
  await run('tag TestRat add bm.dwmet');
  const hn0 = await score('bm.hn_dennis');                         // (put back at the end)
  await run('scoreboard players set TestRat bm.hn_dennis 1444');   // (blessed, rank II: Vitality, Bulwark, Might IV)
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 30);
  const tool = (t, ench) => `minecraft:${t}[minecraft:enchantments={${ench}}]`;
  await run('loot replace entity TestRat hotbar.0 loot bm:items/dw_horn');
  await run(`item replace entity TestRat hotbar.5 with ${tool('diamond_pickaxe', '"minecraft:efficiency":5,"minecraft:silk_touch":1')}`);
  await run(`item replace entity TestRat hotbar.6 with ${tool('diamond_pickaxe', '"minecraft:efficiency":5')}`);
  await run(`item replace entity TestRat hotbar.7 with ${tool('diamond_shovel', '"minecraft:efficiency":5')}`);
  await run(`item replace entity TestRat hotbar.8 with ${tool('diamond_axe', '"minecraft:efficiency":5')}`);
  await run('effect give TestRat minecraft:haste 900 1 true');
  await sleep(1200);

  // ---------------------------------------------------------------- Dennis called, sat beside you
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('his horn used: Dennis comes', (await cnt(PET)) === 1);
  await sneakMenu(0); await click(/Sit \/ follow/); await sleep(1200);
  ok('...sat from his menu (he stays out of the dig)', /1b/.test(await nbt(PET, 'Sitting')));

  // ---------------------------------------------------------------- his ways: locked at rank II, unlocked at rank III
  const ways = async () => { await sneakMenu(0); const pr = await press(/Dennis.s ways/); const t = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {}); await press(/Back/); return [pr, t]; };
  let [pr, pw] = await ways();
  ok('rank II - his ways: "Rich Seam (locked)", and how to unlock it', pr && pr.next && pw.includes('Rich Seam (locked)') && /rank III/.test(pw) && /Queen Ava/.test(pw), pw.slice(0, 120));
  await sleep(1500);
  await run('scoreboard players set #dwrs_test bm.cfg 1');
  ok('...and no Rich Seam on you (bm.dwrs 0), hook or not', await wait(2500, async () => (await score('bm.dwrs')) === 0) && (await score('bm.dwft')) === 1);

  // (each block set beside you and mined with a real dig; what it dropped counted - in your pockets and on the ground)
  const dig = async (blk, n, slot, iid, ms = 200) => {
    await run(`${O}kill ${ITEMS}`); await run(`clear TestRat minecraft:${iid}`); A.slot(slot); await sleep(300);
    let mined = 0;
    for (let i = 0; i < n; i++) {
      const bx = X + 1, by = Y + 1, bz = Z + 1 + (i % 2);
      await run(`${O}setblock ${bx} ${by} ${bz} minecraft:${blk}`); await sleep(150); await A.mine(bx, by, bz, ms); await sleep(500);
      if (/passed/.test(await run(`${O}execute if block ${bx} ${by} ${bz} minecraft:air`))) mined++;
    }
    await sleep(1500); const got = (await plain(iid)) + (await ground(iid, X, Y + 1, Z));
    await run(`${O}kill ${ITEMS}`); await run(`clear TestRat minecraft:${iid}`); return [mined, got];
  };
  let [m, g] = await dig('stone', 8, 6, 'cobblestone');
  ok('rank II, hook on: 8 stone mined - 8 cobblestone, nothing extra', m === 8 && g === 8, `${g} from ${m}`);

  // ---------------------------------------------------------------- rank III, the hook on: every block twice
  await run('scoreboard players set TestRat bm.hn_dennis 1555');
  [pr, pw] = await ways();
  ok('rank III - his ways: Rich Seam, unlocked', pr && pr.next && pw.includes('Rich Seam') && !pw.includes('Rich Seam (locked)') && pw.includes('Fortune V'), pw.slice(0, 120));
  ok('...Rich Seam on you (bm.dwrs 2: the test hook)', await wait(3000, async () => (await score('bm.dwrs')) === 2));
  [m, g] = await dig('stone', 8, 6, 'cobblestone');
  ok('...8 stone by a plain pickaxe: 16 cobblestone', m === 8 && g === 16, `${g} from ${m}`);
  [m, g] = await dig('dirt', 6, 7, 'dirt');
  ok('...6 dirt by a shovel: 12 dirt', m === 6 && g === 12, `${g} from ${m}`);
  [m, g] = await dig('oak_log', 4, 8, 'oak_log', 400);
  ok('...4 oak logs by an axe: 8 logs', m === 4 && g === 8, `${g} from ${m}`);
  [m, g] = await dig('stone', 4, 5, 'stone');
  ok('...4 stone by a silk-touch pickaxe: 8 stone (silk touch kept)', m === 4 && g === 8, `${g} from ${m}`);
  [m, g] = await dig('diamond_ore', 4, 5, 'diamond_ore', 400);
  ok('...4 diamond ores by the silk-touch pickaxe: one ore apiece (ores are Fortune V\'s, not Rich Seam\'s)', m === 4 && g === 4, `${g} from ${m}`);
  [m, g] = await dig('chest', 2, 8, 'chest', 600);
  ok('...2 chests: one apiece (nothing that holds anything)', m === 2 && g === 2, `${g} from ${m}`);

  // (a blast is no miner: the TNT is the loot's `this`, never you - a 5x5 slab of stone up in the air, out of the blast's reach of
  //  anything else, so every cobblestone on the floor came from it)
  const BX = X - 8, BZ = Z - 8, BY = Y + 7;
  await run(`${O}fill ${BX - 2} ${BY} ${BZ - 2} ${BX + 2} ${BY} ${BZ + 2} minecraft:stone`); await run(`${O}kill ${ITEMS}`);
  await run(`${O}summon minecraft:tnt ${BX + 0.5} ${BY + 1} ${BZ + 0.5} {fuse:1}`); await sleep(3500);
  let blown = 0; for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) if (/passed/.test(await run(`${O}execute if block ${BX + dx} ${BY} ${BZ + dz} minecraft:air`))) blown++;
  const cob = await ground('cobblestone', BX, Y + 1, BZ, 8);
  ok('...TNT in the stone beside you: never more than a cobblestone a block', blown > 0 && cob <= blown, `${cob} cobblestone from ${blown} blown (of 25 in the blast; ${await score('bm.dwrs')} on you)`);
  await run(`${O}kill ${ITEMS}`); await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`);

  // ---------------------------------------------------------------- the hook off: the real 1 in 10
  await run('scoreboard players set #dwrs_test bm.cfg 0');
  ok('the hook off: bm.dwrs 1', await wait(2500, async () => (await score('bm.dwrs')) === 1));
  [m, g] = await dig('stone', 60, 6, 'cobblestone');
  ok('...60 stone: more cobblestone than stone mined, nothing like twice (1 in 10)', m === 60 && g > m && g <= m + 18, `${g} from ${m} (${g - m} extra)`);

  // ---------------------------------------------------------------- Dennis sent home: nothing extra
  await run('scoreboard players set #dwrs_test bm.cfg 1');
  await sneakMenu(0); await click(/Send him home/); await sleep(1500);
  ok('Dennis sent home (his menu): the mark gone', (await cnt(PET)) === 0 && await wait(2500, async () => (await score('bm.dwrs')) === 0));
  [m, g] = await dig('stone', 8, 6, 'cobblestone');
  ok('...8 stone, hook on, rank III: 8 cobblestone', m === 8 && g === 8, `${g} from ${m}`);

  // ---------------------------------------------------------------- clean up
  await run('scoreboard players set #dwrs_test bm.cfg 0'); await run(`scoreboard players set TestRat bm.hn_dennis ${hn0 === -99 ? 0 : hn0}`);
  if (hn0 === -99) await run('scoreboard players reset TestRat bm.hn_dennis');
  await run('kill @e[type=minecraft:wolf,tag=bm.dwpet]'); await run('scoreboard players set TestRat bm.dwcd 0');
  await run(`${O}kill ${ITEMS}`); await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
