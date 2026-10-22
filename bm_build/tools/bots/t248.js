// 2.89: THE OLD STORIES, as a regular (non-op) player - the lore of the war a thousand years gone, the broken Ethereal Gem, the
// rogue prince, the curse on Omega's island and the serpent's new campaign, where a player meets it:
//   the nine gems and the Ethereal Gem carry it in their lore (an elemental gem: a shard of the Ethereal Gem; the Ethereal Gem:
//     the heart of a kingdom that was not always under the sea), and an old gem in the pack is re-synced to it;
//   the Dread Court (Apophiss, KillerWatt, Democratus, each called with their own item) talk of it - the trio's banter now draws
//     from its whole pool (five exchanges), not just the first three: the serpent's campaign comes up.
// (King Omega's chapters VI and IX are offered as gifts from his court in t200.) rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const lore = async slot => await run(`data get entity TestRat Inventory[{Slot:${slot}b}].components."minecraft:lore"`);
  const use = async (C, slot) => { C.slot(slot); await sleep(250); C.use(); await sleep(400); C.release(); };
  const PETS = { kw: ['wolf', 'bm.kxpet', 'kw_spark'], demo: ['wolf', 'bm.dmpet', 'demo_seal'], apo: ['wolf', 'bm.appet', 'apo_oath'] };
  const sel = k => `@e[type=minecraft:${PETS[k][0]},tag=${PETS[k][1]},limit=1]`;
  const A = await bot('TestRat'); await sleep(2500);
  A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const X = 13640, Y = 121, Z = 13060;
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`);
  for (let y = Y; y < Y + 12; y += 6) await run(`${O}fill ${X - 20} ${y} ${Z - 20} ${X + 20} ${y + 5} ${Z + 20} minecraft:air`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  for (const k in PETS) await run(`${O}kill @e[tag=${PETS[k][1]}]`);
  await sleep(1500);
  for (const o of ['bm.kxcd', 'bm.dmcd', 'bm.apcd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();

  // ================================================================== 1. the gems
  await run('loot replace entity TestRat hotbar.0 loot bm:items/gem_fire'); await run('loot replace entity TestRat hotbar.1 loot bm:items/ethereal_gem');
  await sleep(500);
  ok('A Fire Gem: "A shard of the Ethereal Gem"', /A shard of the Ethereal Gem/.test(await lore(0)), (await lore(0)).slice(-160));
  const el = await lore(1);
  ok('The Ethereal Gem: the heart of a kingdom that was not always under the sea, broken in the great war', /not always under/.test(el) && /Broken in the great war/.test(el) &&
     /found a power with it/.test(el), el.slice(-220));
  // (an old gem in the pack: its old lore, an old version stamp - re-synced to the new)
  await run('item modify entity TestRat hotbar.0 [{type:"minecraft:set_lore",lore:[{text:"Odd... it hums when its kin are near."}],mode:"replace_all"},{type:"minecraft:set_custom_data",tag:"{bmv:1}"}]');
  ok('...an old Fire Gem in the pack is re-synced to the new lore', await wait(6000, async () => /A shard of the Ethereal Gem/.test(await lore(0)), 500), (await lore(0)).slice(-120));
  await run('clear TestRat');

  // ================================================================== 2. the Dread Court talks of the gem
  for (const [i, k] of ['apo', 'kw', 'demo'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${PETS[k][2]}`);
  for (const [i, k] of ['apo', 'kw', 'demo'].entries()) { const t0 = Date.now(); await use(A, i); await wait(4000, async () => (await cnt(sel(k))) === 1);
    await sleep(Math.max(400, 2300 - (Date.now() - t0))); }
  ok('The Dread Court: Apophiss, KillerWatt and Democratus, each called with their own item', (await cnt(sel('apo'))) + (await cnt(sel('kw'))) + (await cnt(sel('demo'))) === 3);
  await run('tag TestRat remove bm.hush');                                    // (chatter on)
  // (the banter comes every two minutes or so: the wait is skipped - its clock set to the brink - and the trio's exchange heard, again
  //  and again, until the serpent's campaign comes up)
  const heard = new Set(); A.chats.length = 0; let gem = false;
  for (let n = 0; n < 40 && !gem; n++) {
    await run('scoreboard players set TestRat bm.triob 120'); await sleep(1300);
    for (const c of A.chats) { const m = c.match(/^(Democratus|Apophiss|KillerWatt): /); if (m) heard.add(c.slice(0, 40)); if (/what is left of their gem|still dying/.test(c)) gem = true; }
    A.chats.length = 0;
  }
  // (those two exchanges are the trio's fourth and fifth: heard at all, the banter draws from the whole pool, not its first three)
  ok('...and they talk of the old war: "where the sea-folk keep what is left of their gem" - "My land is still dying" (past the first three exchanges)', gem,
     [...heard].join(' | ').slice(0, 300));

  // ---- put things back
  for (const k in PETS) await run(`${O}kill @e[tag=${PETS[k][1]}]`);
  await sleep(1500); for (const o of ['bm.kxcd', 'bm.dmcd', 'bm.apcd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('advancement revoke TestRat only bm:story/trio_dread');
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat');
  await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y + 11} ${Z + 20} minecraft:air`);
  await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
