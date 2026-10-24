// 2.94: THE GLITCHED CARTRIDGE and the PIXEL COSTUMES (phase214), as a regular (non-op) player: a cartridge used with no follower
// near (it only buzzes, and is kept); used beside your Celi (called with her own charm): her pixel costume - the cartridge spent,
// a billboarded sprite on her, her own model hidden (view range 0); the sprite walks with her; the Pixel Wardrobe (sneak + use):
// "Celi: on" pressed - off (the sprite gone, her model back), pressed again - on; and the cartridge is in a won heist's finds.
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs');
const DP = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function';
(async () => {
  const res = []; const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const tags = async () => (await run('tag TestRat list'));
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05, 100); await sleep(300); };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const X = 17640, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(2500);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]');
  await run('tag TestRat remove bm.pxu_celi'); await run('tag TestRat remove bm.pxo_celi'); await run('scoreboard players set TestRat bm.cecd 0');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await run('loot replace entity TestRat hotbar.6 loot bm:items/glitch_cart');
  A.bars.length = 0; await use(6); await sleep(800);
  ok('the cartridge used with no follower near: it only buzzes (kept)', A.bars.some(b => /buzzes/.test(b)) && (await has('glitch_cart')) === 1, A.bars.slice(-1).join(''));
  await run('loot replace entity TestRat hotbar.7 loot bm:items/celi_charm'); await use(7); await sleep(2500);
  const CELI = '@e[type=minecraft:wolf,tag=bm.celipet,limit=1]';
  ok('Celi called (her own charm)', (await cnt(CELI)) === 1);
  await run(`${O}tp ${CELI} ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await sleep(500);
  A.chats.length = 0; await use(6); await sleep(1500);
  ok('the cartridge used beside her: her pixel costume (unlocked, on), the cartridge spent', /bm\.pxu_celi/.test(await tags()) && /bm\.pxo_celi/.test(await tags()) &&
     (await has('glitch_cart')) === 0 && A.chats.some(c => /sixteen colours/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  const COS = '@e[type=minecraft:item_display,tag=bm.pxcos_celi]';
  ok('...a sprite on her (billboarded, a frame playing)', await wait(3000, async () => (await cnt(COS)) === 1) && /center/.test(await nbt(`${COS.slice(0, -1)},limit=1]`, 'billboard')));
  const HID = '@e[type=minecraft:item_display,tag=bm.cep,tag=bm.pxhid]';
  ok('...and her own model hidden (view range 0)', await wait(3000, async () => (await cnt(HID)) >= 3) &&
     (await num(`${HID.slice(0, -1)},limit=1]`, 'view_range')) === 0, `hidden ${await cnt(HID)}`);
  const f0 = await nbt(`${COS.slice(0, -1)},limit=1]`, 'item.components."minecraft:custom_model_data"'); await sleep(900);
  ok('...the sprite animates (its frame changes)', (await nbt(`${COS.slice(0, -1)},limit=1]`, 'item.components."minecraft:custom_model_data"')) !== f0);
  await run(`${O}tp ${CELI} ${X + 4.5} ${Y + 1} ${Z + 2.5}`); await sleep(800);
  ok('...and stays on her when she moves', Math.abs((await num(`${COS.slice(0, -1)},limit=1]`, 'Pos[0]')) - (X + 4.5)) < 0.6);
  // the Pixel Wardrobe
  await run('loot replace entity TestRat hotbar.6 loot bm:items/glitch_cart');
  const n0 = A.dialogN.length; await use(6, true); await wait(3000, async () => A.dialogN.length > n0);
  ok('sneak + use: the Pixel Wardrobe - "Celi: on"', A.buttons().some(b => /Celi: on/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Celi: on/); await sleep(2000);
  ok('...pressed: off - the sprite gone, her own model back', (await cnt(COS)) === 0 && (await cnt(HID)) === 0 &&
     (await num('@e[type=minecraft:item_display,tag=bm.cep,limit=1]', 'view_range')) > 0 && !/bm\.pxo_celi/.test(await tags()));
  ok('...the wardrobe now reads "Celi: off"', A.buttons().some(b => /Celi: off/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Celi: off/); await sleep(2000);
  ok('...pressed again: on', (await cnt(COS)) === 1 && /bm\.pxo_celi/.test(await tags()));
  ok('a won heist can find one (the finds roll it, any tier)', /bm:p214\/find/.test(fs.readFileSync(`${DP}/p105/finds.mcfunction`, 'utf8')));
  await run('execute as TestRat run function bm:p98/home/celi'); await sleep(1500);
  ok('Celi sent home: the costume goes with her', await wait(3000, async () => (await cnt(COS)) === 0));
  await run('tag TestRat remove bm.pxo_celi'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
