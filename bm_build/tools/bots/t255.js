// 2.93b: BENDER'S BONDS AND THE SYNERGY ATTACKS, as a regular (non-op) player - followers called with their own items (real
// uses): Bender and Emma make "Princess and Pup" (its hidden achievement, Regeneration and Speed); in a fight the pair charges
// and sets off its synergy attack (healing: "Mending Light" on the bar, you healed); Leo joins: "The Royal Guard Dog" trio (its
// achievement, Resistance II), its trio synergy ("Shield Wall": Resistance IV) and its bark; Bender's own RAGE! - he leaps on a
// monster, mauls it and backflips onto the next, three in a chain, and lands on his feet. (rcon sets the stage: a floor, the
// items, no cooldowns, the charge wound forward, the monsters.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const fx = async () => await run('data get entity TestRat active_effects');
  const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2400); };
  const X = 16900, Y = 100, Z = 16000;
  const BV = '@e[type=minecraft:wolf,tag=bm.bvpet,limit=1]';
  // (bm.seen: never made Elite or Lucky; still - NoAI - for the rage, whose chain lands him among them: a tiered one's blows could knock him out)
  const zom = async (dx, dz, tag, hp = 300, still = false) => run(`${O}summon minecraft:zombie ${X + dx} ${Y + 1} ${Z + dz} {Tags:["${tag}","bm.t255z","bm.seen"],PersistenceRequired:1b,Silent:1b,${still ? 'NoAI:1b,' : ''}` +
                                          `attributes:[{id:"minecraft:max_health",base:${hp}d},{id:"minecraft:movement_speed",base:0d},{id:"minecraft:knockback_resistance",base:1d}],Health:${hp}f}`);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:sandstone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]'); await sleep(2000);
  const cds = ['bm.bvcd', 'bm.emcd', 'bm.lecd'];
  for (const o of cds) await run(`scoreboard players set TestRat ${o} 0`);
  for (const a of ['pair_pup', 'trio_guarddog']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.bvmet', 'bm.leomet']) await run(`tag TestRat add ${t}`);
  for (const [i, iid] of ['bv_ball', 'emma_ribbon', 'leo_crest'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  await run('scoreboard players set TestRat bm.syn2 0'); await run('scoreboard players set TestRat bm.syn3 0');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);

  // ---------------------------------------------------------------- a pair: Bender and Emma
  A.chats.length = 0; A.bars.length = 0;
  await use(0); await use(1);
  ok('Bender\'s Ball and Emma\'s Ribbon used: both come', (await cnt('@e[type=minecraft:wolf,tag=bm.bvpet]')) === 1 && (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) === 1,
     A.bars.slice(-3).join(' | '));
  await run(`scoreboard players set ${BV} bm.bvrg 9000`);                    // (his Rage held back until its own turn)
  ok('...side by side: "Princess and Pup" - its hidden achievement and their intro', await wait(5000, async () => adv('pair_pup')) &&
     A.chats.some(c => /Princess and Pup!/.test(c)), A.chats.slice(-3).join(' | ').slice(0, 200));
  ok('...Regeneration and Speed for you', await wait(3000, async () => { const e = await fx(); return /regeneration/.test(e) && /minecraft:speed/.test(e); }));
  // the pair's synergy: charged in a fight (wound forward here), set off by a monster near
  await run('effect clear TestRat minecraft:resistance'); await run('effect clear TestRat minecraft:regeneration'); await run('damage TestRat 8 minecraft:generic'); await sleep(300);
  const hp0 = +(await run('data get entity TestRat Health')).match(/(-?[\d.]+)f/)[1];
  await run('scoreboard players set TestRat bm.syn2 19'); A.bars.length = 0;
  await zom(4, 4, 'bm.t255a');
  ok('a monster near, the pair charged: SYNERGY - "Princess and Pup - Mending Light" on the bar', await wait(5000, async () => A.bars.some(b => /Synergy!.*Princess and Pup.*Mending Light/.test(b))),
     A.bars.slice(-2).join(' | '));
  ok('...you healed, and the charge spent', await wait(2000, async () => +(await run('data get entity TestRat Health')).match(/(-?[\d.]+)f/)[1] > hp0) && (await score('bm.syn2')) <= 2);
  await run(`${O}kill @e[tag=bm.t255z]`);

  // ---------------------------------------------------------------- the trio: Leo joins
  await use(2);
  ok('Leo\'s crest used: Leo comes too', await wait(3000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1));
  ok('...all three: "The Royal Guard Dog" - its hidden achievement, Resistance II', await wait(5000, async () => adv('trio_guarddog')) &&
     await wait(3000, async () => /resistance/.test(await fx())));
  await run('effect clear TestRat minecraft:resistance');
  await run('scoreboard players set TestRat bm.syn3 34'); A.bars.length = 0;
  await zom(-4, 4, 'bm.t255b', 1000);
  ok('...a monster near, the trio charged: TRIO SYNERGY - "The Royal Guard Dog - Shield Wall"', await wait(5000, async () => A.bars.some(b => /Trio Synergy!.*Royal Guard Dog.*Shield Wall/.test(b))),
     A.bars.slice(-2).join(' | '));
  ok('...Resistance IV and Absorption for you', await wait(2000, async () => { const e = await fx(); return /amplifier: 3b, id: "minecraft:resistance"/.test(e) && /absorption/.test(e); }),
     (await fx()).slice(0, 240));
  await run('scoreboard players set TestRat bm.p207 18');                     // (the trio's 20 s clock wound forward)
  ok('...and every 20 s Bender barks them down (the monster weakened)', await wait(8000, async () => (await cnt('@e[tag=bm.t255b,nbt={active_effects:[{id:"minecraft:weakness"}]}]')) === 1),
     `alive ${await cnt('@e[tag=bm.t255b]')}, clock ${await score('bm.p207')}, trio ${await score('bm.trio')}`);
  await run(`${O}kill @e[tag=bm.t255z]`);

  // ---------------------------------------------------------------- RAGE!: three monsters, a chain (Emma and Leo sent home: they'd fight them too)
  await run('execute as TestRat run scoreboard players operation #me bm.pid = @s bm.pid');
  for (const w of ['emma', 'leo']) await run(`execute as TestRat run function bm:p98/home/${w}`);
  await wait(8000, async () => (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) + (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 0); await sleep(1000);
  ok('Emma and Leo sent home (Bender alone for his rage)', (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) + (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 0);
  await run(`${O}tp ${BV} ${X + 0.5} ${Y + 1} ${Z + 3.5}`);
  for (const [dx, dz] of [[0, 8], [2.5, 10], [-2.5, 10]]) await zom(dx, dz, 'bm.t255r', 300, true);
  await sleep(500); A.bars.length = 0;
  await run(`scoreboard players set ${BV} bm.bvrg 0`);
  ok('RAGE! - he growls and launches at a monster (his rage begun)', await wait(4000, async () => (await score('bm.dqa', BV)) === 15), `state ${await score('bm.dqa', BV)}`);
  for (let i = 0; i < 40 && process.env.DBG; i++) { await sleep(200); console.log('   ', await score('bm.bvrp', BV), await score('bm.bvrn', BV), await score('bm.bvrt', BV), (await run(`data get entity ${BV} Pos`)).slice(-50), await run('execute as @e[tag=bm.t255r] run data get entity @s Tags'), await run('execute as @e[tag=bm.t255r] run data get entity @s Pos')); }
  ok('...latched on its head, mauling it (it is bitten)', await wait(5000, async () => (await cnt('@e[tag=bm.t255r,nbt={Health:300.0f}]')) <= 2));
  if (process.env.DBG) console.log('   pets', await cnt('@e[type=minecraft:wolf,tag=bm.bvpet]'), await run(`data get entity @e[tag=bm.t255r,limit=1,sort=random] Health`), await run('execute as @e[tag=bm.t255r] run data get entity @s Health'), await run(`scoreboard players get ${BV} bm.bvrn`));
  ok('...backflips from one to the next: all three bitten, the chain three long', await wait(12000, async () => (await cnt('@e[tag=bm.t255r,nbt={Health:300.0f}]')) === 0) &&
     (await score('bm.bvrn', BV)) === 3, `untouched ${await cnt('@e[tag=bm.t255r,nbt={Health:300.0f}]')}, chain ${await score('bm.bvrn', BV)}`);
  ok('...a last backflip off - and he lands on his feet, the rage over (gravity back, on the ground)', await wait(10000, async () =>
     (await score('bm.bvrp', BV)) === 0 && /NoGravity:0b|^((?!NoGravity:1b).)*$/s.test(await run(`data get entity ${BV}`)) && /1b/.test(await run(`data get entity ${BV} OnGround`))),
     `phase ${await score('bm.bvrp', BV)}`);
  ok('...and his cooldown set (40 s)', (await score('bm.bvrg', BV)) > 600, `${await score('bm.bvrg', BV)}`);
  ok('...no stray landing marker left behind', (await cnt('@e[type=minecraft:marker,tag=bm.bvrfrom]')) === 0);

  // ---------------------------------------------------------------- clean up
  await run(`${O}kill @e[tag=bm.t255z]`);
  await run('clear TestRat'); await run('effect clear TestRat');
  for (const s of ['wolf,tag=bm.bvpet', 'cat,tag=bm.emmapet', 'wolf,tag=bm.leopet']) await run(`kill @e[type=minecraft:${s}]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
