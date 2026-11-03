// 3.0g: FOLLOWERS NEVER TURN ON WILFREY (allies.py - his body is a wither skeleton, every "nearest monster" skips it) and EMMA'S
// AXE ROLL ONLY IN HER ETHEREAL FORM (phase226), as a regular (non-op) player: Emma called with her ribbon, Wilfrey with his
// locket (items used as items); rcon sets the stage (a floor, a NoAI husk - the monster nearby - Emma made a Champion, her
// ethereal form started) and reads health, scores and tags.
//   wil    Emma and Wilfrey out, a husk 5 blocks off, Emma in her Ethereal Form (striking every second): for 30 s Wilfrey's wolf
//          keeps its full health, Emma's strike never lands on him (her aim marker never at his body), and the husk IS struck
//   slam   Emma a Champion (Honours III), a husk near, NOT ethereal: for 25 s her Axe Roll never starts (bm.prgo / bm.ksg);
//          made ethereal: within 25 s it does
//   node t350.js [wil|slam]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const O = 'execute in minecraft:overworld run ';
const X = 21400, Y = 100, Z = 16400;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)[a-z]?$/) || [0, NaN])[1]);
  const sc = async (who, o) => +((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(2400); };
  const EMMA = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]', WOLF = '@e[type=minecraft:wolf,tag=bm.wilfrey,limit=1]', BODY = '@e[type=minecraft:wither_skeleton,tag=bm.wil_body,limit=1]';
  const HUSK = `@e[type=minecraft:husk,tag=t350,limit=1]`;
  const home = async () => { await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p62/emma_go`);
    await run('execute as TestRat run function bm:p138/home/wil'); await sleep(1500);
    for (const t of ['wolf', 'cat', 'wither_skeleton']) await run(`${O}execute as @e[type=minecraft:${t},x=${X},y=${Y},z=${Z},distance=..40] if score @s bm.pid = TestRat bm.pid run tp @s ~ -300 ~`);
    await run('scoreboard players set TestRat bm.emcd 0'); await run('scoreboard players set TestRat bm.wlcd 0'); await sleep(1500); };
  const husk = async (dz) => { await run(`${O}kill @e[type=minecraft:husk,tag=t350]`);
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + dz + 0.5} {Tags:["t350","bm.seen"],NoAI:1b,PersistenceRequired:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d}]}`); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`); await sleep(1500);
  await run(`${O}fill ${X - 14} ${Y - 1} ${Z - 14} ${X + 14} ${Y - 1} ${Z + 14} minecraft:stone`); await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y + 10} ${Z + 14} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30,type=!minecraft:item_display]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z - 4.5} 0 0`); await sleep(1200); A.stand();
  await home();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon'); await run('loot replace entity TestRat hotbar.1 loot bm:items/wilfrey_locket');
  await run('scoreboard players set TestRat bm.emwf 0'); await run('scoreboard players set TestRat bm.emst 0'); await sleep(600);
  await use(0); await use(1);
  ok('Emma and Wilfrey called with their own items', await wait(6000, async () => (await cnt(EMMA)) === 1 && (await cnt(WOLF)) === 1 && (await cnt(BODY)) === 1),
     `emma ${await cnt(EMMA)} wolf ${await cnt(WOLF)} body ${await cnt(BODY)}`);

  if (on('wil')) {
    await husk(5);
    await run(`${O}execute as ${EMMA} at @s run function bm:p57/ascend`);
    const hp0 = await num(`${O}data get entity ${WOLF} Health`), h0 = await num(`${O}data get entity ${HUSK} Health`);
    let minHp = hp0, onHim = 0, aims = 0; const t0 = Date.now();
    while (Date.now() - t0 < 30000) {
      await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 30`);      // (her form held for the whole half minute)
      const hp = await num(`${O}data get entity ${WOLF} Health`); if (!isNaN(hp)) minHp = Math.min(minHp, hp);
      const b = await pos(BODY), a = await pos(`@e[type=minecraft:marker,tag=bm.emaim,x=${X},y=${Y},z=${Z},distance=..30,limit=1]`);
      if (a) { aims++; if (b && Math.hypot(a[0] - b[0], a[2] - b[2]) < 0.8) onHim++; }
      await sleep(300);
    }
    const h1 = await num(`${O}data get entity ${HUSK} Health`);
    ok('Emma ethereal for 30 s, a husk near: Wilfrey never hurt (his wolf at full health throughout)', minHp >= hp0 && hp0 > 0, `wolf ${hp0} -> lowest ${minHp}`);
    ok('...and her strike never aimed at him (her aim marker never at his body)', onHim === 0, `${aims} aims seen, ${onHim} on Wilfrey`);
    ok('...while the husk was struck', h1 < h0, `husk ${h0} -> ${h1}`);
    await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 1`); await sleep(2500);
  }

  if (on('slam')) {
    await husk(4);
    await run(`${O}tag ${EMMA} add bm.champ`);
    await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 0`); await sleep(1500);
    await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.prcd 0`); await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.prgo 0`);
    let started = false; const t0 = Date.now();
    while (Date.now() - t0 < 25000) {
      await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.emc 0`);         // (no charge: she stays out of her form)
      if ((await sc(EMMA, 'bm.prgo')) === 1) started = true;
      await sleep(400);
    }
    ok('Emma a Champion, a husk near, NOT ethereal: her Axe Roll never starts in 25 s', !started && (await sc(EMMA, 'bm.eme')) <= 0, `eme ${await sc(EMMA, 'bm.eme')}`);
    await run(`${O}execute as ${EMMA} at @s run function bm:p57/ascend`);
    await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.prcd 0`);
    const go = await wait(25000, async () => { await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 30`); return (await sc(EMMA, 'bm.prgo')) === 1 || (await sc(EMMA, 'bm.prcd')) > 1; }, 300);
    ok('...made ethereal: her Axe Roll comes (bm.prgo, its cooldown set)', go, `prgo ${await sc(EMMA, 'bm.prgo')} prcd ${await sc(EMMA, 'bm.prcd')}`);
    await run(`${O}tag @e[type=minecraft:cat,tag=bm.emmapet] remove bm.champ`); await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 1`);
  }

  await run(`${O}kill @e[type=minecraft:husk,tag=t350]`); await home(); await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
