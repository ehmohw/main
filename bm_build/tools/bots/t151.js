// 2.78: Apophiss's phase II never skipped, and his den's dome whole - as a regular (non-op) player in the den: the boss brought
// near half health (rcon sets the stage - a long fight's worth), then the bot's own blows (a heavy sword, by real attack packets on
// his hitbox) take him under half: he transforms at once - mid-attack or not - his health held at half, and the ethereal king
// rises (phase II). Twice over: a second Serpent King, the same. And the den rebuilt with no chain holes in its ceiling.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = 'execute in bm:hollow_throne run ';
  const B = '@e[type=minecraft:husk,tag=bm.apboss,limit=1]';
  const num = async (c) => { const o = await run(c); const m = o.match(/has (-?\d+) \[/) || o.match(/(-?\d+(?:\.\d+)?)[a-z]?\s*$/i); return m ? +m[1] : NaN; };
  const uuidOf = async (sel) => { const m = (await run(`${H}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('attribute TestRat minecraft:max_health base set 1000'); await run('effect give TestRat minecraft:instant_health 1 40 true');
  await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:regeneration 900 4 true');
  await run('scoreboard players set TestRat bm.conq 6');
  // ---- the den: rebuilt (2.78), its dome whole over the chains
  await run('execute as TestRat run function bm:admin/apophiss_den'); await run('scoreboard players set #apwake bm.p2 0'); await sleep(1500); A.stand();
  ok('the den is the 2.78 build (version 3)', await wait(15000, async () => (await num('scoreboard players get #apver bm.p2')) === 3, 1000), `${await num('scoreboard players get #apver bm.p2')}`);
  const LX = 1046, LY = 2, LZ = 1046, CX = 30, CZ = 30;
  let holes = 0, chains = 0, detail = [];
  for (let k = 0; k < 8; k++) {
    const a = k * Math.PI / 4, x = LX + Math.round(CX + 12 * Math.cos(a)), z = LZ + Math.round(CZ + 12 * Math.sin(a));
    let top = -1;
    for (let y = LY + 15; y < LY + 36; y++) if (/passed/i.test(await run(`${H}execute if block ${x} ${y} ${z} minecraft:iron_chain`))) { top = y; chains++; }
    // above the chain: solid shell up to the outside (no air pocket, no chain sticking out above the dome)
    const above = /passed/i.test(await run(`${H}execute unless block ${x} ${top + 1} ${z} minecraft:air`));
    const outChain = /passed/i.test(await run(`${H}execute if block ${x} ${LY + 35} ${z} minecraft:iron_chain`));
    if (!above || outChain || top < 0) { holes++; detail.push(`${x},${top},${z}`); }
  }
  ok('every lantern chain hangs from a whole ceiling (no hole through the dome, none sticking out above)', holes === 0 && chains > 40, `holes ${holes} ${detail.join(' ')} chains ${chains}`);
  await run(`${H}tp TestRat 1076.5 3 1075.5 180 0`); await sleep(800); A.stand();
  await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]');
  await run('effect give TestRat minecraft:strength 900 3 true');
  for (const round of [1, 2]) {
    await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`); await run(`${H}kill @e[type=minecraft:interaction,tag=bm.bhit_ap]`);
    await sleep(500);
    await run('execute as TestRat at @s run function bm:admin/apophiss');
    await wait(30000, async () => (await num(`${H}scoreboard players get ${B} bm.apph`)) === 1 && (await num(`${H}scoreboard players get ${B} bm.apatk`)) !== 9, 500);
    const mx = await num(`${H}attribute ${B} minecraft:max_health get`);
    await run(`${H}data modify entity ${B} Health set value ${Math.round(mx * 0.53)}f`);         // (a long fight's worth)
    // the bot's own blows on his hitbox
    let hit = null; await wait(4000, async () => { const u = await uuidOf('@e[type=minecraft:interaction,tag=bm.bhit_ap,limit=1]'); hit = Object.values(A.ents).find(e => e.objectUUID === u); return !!hit; }, 300);
    ok(`round ${round}: his hitbox is there to strike`, !!hit);
    A.slot(0); await sleep(200);
    let low = 1e9, trans = false;
    for (let i = 0; i < 40 && !trans; i++) {
      const bp = (await run(`${H}data get entity ${B} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
      if (bp) await run(`${H}tp TestRat ${+bp[1] + 0.5} ${+bp[2]} ${+bp[3] + 2.5} 180 0`);
      if (hit) A.attack(hit.entityId); await sleep(350);
      const hp = await num(`${H}data get entity ${B} Health`); if (hp < low) low = hp;
      if ((await num(`${H}scoreboard players get ${B} bm.apatk`)) === 7) trans = true;
    }
    ok(`round ${round}: under half by the bot's blows - he transforms at once`, trans, `low ${low} of ${mx}`);
    ok(`round ${round}: ...his health held at half (no skipping past it)`, low >= Math.floor(mx / 2) - 1, `low ${low} of ${mx}`);
    ok(`round ${round}: ...and the ethereal king rises (phase II)`, await wait(20000, async () => (await num(`${H}scoreboard players get ${B} bm.apph`)) === 2, 500),
       `apph ${await num(`${H}scoreboard players get ${B} bm.apph`)}`);
  }
  await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`); await run(`${H}kill @e[type=minecraft:interaction,tag=bm.bhit_ap]`);
  await run(`${H}kill @e[type=minecraft:drowned,tag=bm.apcourt]`); await run('bossbar set bm:apob visible false');
  await run('attribute TestRat minecraft:max_health base set 20'); await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
