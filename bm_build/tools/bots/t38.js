// v2.35: the chestplate essences/resonances against a real attacker (a husk with AI: the damage command never triggers on-hit enchantments)
const { bot, rcon, sleep } = require('./lib');
const X = 7000, Y = 100, Z = 7000;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/); return m ? parseFloat(m[1]) : NaN; };
  const eff = async (who, id) => (await run(`data get entity ${who} active_effects`)).includes(`minecraft:${id}`);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 300 3 true'); await run('effect give TestRat regeneration 300 2 true');
  await run('time set day'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2000);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  const trial = async (ench, check, name) => {
    await run(`item replace entity TestRat armor.chest with minecraft:netherite_chestplate[minecraft:enchantments=${ench}]`);
    await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`);
    await run(`summon husk ${X + 0.5} ${Y + 1} ${Z + 2.5} {Tags:["t_h"],PersistenceRequired:1b,Silent:1b,Health:100f,attributes:[{id:"minecraft:max_health",base:100d}]}`);
    await run(`summon husk ${X + 3.5} ${Y + 1} ${Z + 0.5} {Tags:["t_b"],NoAI:1b,PersistenceRequired:1b,Silent:1b,Health:100f,attributes:[{id:"minecraft:max_health",base:100d}]}`);
    const p0 = await run('data get entity TestRat Pos');
    let pass = false, info = '';
    for (let i = 0; i < 40 && !pass; i++) { await sleep(250); [pass, info] = await check(p0); }
    ok(name, pass, info);
    await run('kill @e[tag=t_h]'); await run('kill @e[tag=t_b]'); await sleep(300);
  };
  await trial('{"bm:ess_colossus":1}', async () => { const f = await num('data get entity @e[tag=t_h,limit=1] Fire'); return [f > 0, `Fire ${f}`]; }, "Colossus's Essence: the husk that hits you burns");
  await trial('{"bm:ess_treant":1,"bm:res_treant":1}', async () => { const s = await eff('@e[tag=t_h,limit=1]', 'slowness'); const h = await num('data get entity @e[tag=t_h,limit=1] Health'); return [s && h < 100, `slowed ${s}, ${h}`]; },
    'Thornmail: the husk that hits you is torn and rooted');
  await trial('{"bm:ess_voidwalker":1,"bm:res_voidwalker":1}', async (p0) => { const l = await eff('@e[tag=t_b,limit=1]', 'levitation'); const p = await run('data get entity TestRat Pos'); return [l && p !== p0, `float ${l}, ${p.slice(-40)}`]; },
    'Void Shroud: when hit you blink away and the foes near you float');
  await run('item replace entity TestRat armor.chest with air'); await run('effect clear TestRat');
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
