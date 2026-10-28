// 2.78: a doll of every follower, as a regular (non-op) player: each of the thirteen (Cecil, Celi, Leo, Democratus, KillerWatt,
// Apophiss, Tullius, Zib, Pearlman, Donado, Wilfrey, the Frog with Mustache; 2.79, Fishy) - Emma's chibi style - used on a block's top (a real use packet, looking at it) sets the doll down there - its
// model, standing on the block; right-clicking it (a real interact packet on its box) turns it; sneak + punch picks it up
// again, into the inventory. And Cecil sells all thirteen (his trades). rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)(?:[dfbsL])?\s*$/) || [0, NaN])[1]);
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const DOLLS = ['doll_cecil', 'doll_celi', 'doll_leo', 'doll_demo', 'doll_kw', 'doll_apo', 'doll_tul', 'doll_zib', 'doll_pearl', 'doll_don', 'doll_wil', 'doll_frog', 'doll_fishy', 'doll_dennis', 'doll_pistachio', 'doll_omega', 'doll_ashur', 'doll_chef', 'doll_neighbor', 'doll_ava', 'doll_pearlq', 'doll_bloo', 'doll_stalker', 'doll_lantern', 'doll_bender', 'doll_bones', 'doll_capshun', 'doll_sky', 'doll_pxemma', 'doll_pxleo', 'doll_pxcecil', 'doll_kettle', 'doll_rufus', 'doll_henry', 'doll_nia', 'doll_gem', 'doll_batty', 'doll_eggbert', 'doll_count', 'doll_dragon', 'doll_eraser', 'doll_cursor', 'doll_inkblot', 'doll_speech', 'doll_lightbringer', 'doll_dryad', 'doll_sovereign'];
  const X = 16400, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 14} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 14} ${Y + 6} ${Z + 8} minecraft:air`);   // (a doll a block: room for them all)
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  // (Cecil's trades: all thirteen)
  const trades = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/' + 'npc/wizard.mcfunction', 'utf8').toString();
  ok(`Cecil sells all ${DOLLS.length} dolls`, DOLLS.every(d => trades.includes(`bm:"${d}"`)), DOLLS.filter(d => !trades.includes(`bm:"${d}"`)).join(','));
  for (const [i, d] of DOLLS.entries()) {
    const bx = X - 6 + (i % 20), bz = Z - 6 + 5 * Math.floor(i / 20);   // (2.97: rows of twenty - forty-six dolls run off one row's floor)
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${d}`);
    // (standing two back from the block, looking down at its top)
    await run(`${O}tp TestRat ${bx + 0.5} ${Y + 1} ${bz + 2.5} 180 45`); await wait(2000, async () => A.pos && Math.abs(A.pos.z - (bz + 2.5)) < 0.05, 100); await sleep(300);
    A.slot(0); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(500);
    const D = `@e[type=minecraft:item_display,tag=bm.${d}d,x=${bx + 0.5},y=${Y + 1},z=${bz + 0.5},distance=..0.3,limit=1]`;
    const H = `@e[type=minecraft:interaction,tag=bm.${d}hit,x=${bx + 0.5},y=${Y + 1},z=${bz + 0.5},distance=..0.3,limit=1]`;
    ok(`[${d}] used on a block's top: the doll stands there (out of the hand)`, (await cnt(D)) === 1 && (await cnt(H)) === 1 && (await has(d)) === 0,
       `${await cnt(D)} ${await cnt(H)} ${await has(d)}`);
    ok(`[${d}] ...its own model`, (await run(`${O}data get entity ${D} item.components`)).includes(`bm:${d}`));
    const y0 = await num(`${O}data get entity ${D} Rotation[0]`);
    const box = await entOf(H); if (box) A.interact(box.entityId); await sleep(700);
    const y1 = await num(`${O}data get entity ${D} Rotation[0]`);
    ok(`[${d}] right-clicked: it twirls`, !!box && Math.abs(((y1 - y0 + 540) % 360) - 180) > 30, `${y0} -> ${y1}`);
    A.input({ shift: true }); await sleep(250); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
    ok(`[${d}] sneak + punch: back in the inventory, nothing left standing`, (await has(d)) === 1 && (await cnt(D)) === 0 && (await cnt(H)) === 0);
  }
  await run('clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
