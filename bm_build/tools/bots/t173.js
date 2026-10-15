// 2.80: the coat check at the Fixer's Lounge's door, the lounge's rest, and a heist planned from the lounge - as a regular
// (non-op) player: the Ledger used, its buttons pressed as shown, the walk out through the door.
// (rcon only sets the stage: a platform, gear in the pack, a death, what the lounge's shops would have sold.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/i.test(await run(c));
  const fnTrue = async (pre, f) => /returned [1-9]/.test(await run(`execute ${pre} run function ${f}`));
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const has = async (id, slot = 'container.*') => passes(`execute if items entity TestRat ${slot} minecraft:${id}`);
  const hasBm = async (id) => passes(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}"}]`);
  const pos = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const show = (tag) => console.log(`   [${tag}] ` + A.buttons().map(b => `${b.label.replace(/[^\x20-\x7e·]/g, '').trim()} <${b.command.replace('/trigger bm.act set ', '')}>`).join(' | '));
  const O = 'execute in minecraft:overworld run ';
  const HX = 13100, HY = 121, HZ = 13100;
  const A = await bot('TestRat'); await sleep(2500);
  // ---- the stage: a platform, the Ledger, Tokens - and gear that belongs to the overworld
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`spawnpoint TestRat ${HX} ${HY} ${HZ}`);
  for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.lgch', 'bm.lkch', 'bm.lgbag', 'bm.lgstart']) await run(`tag TestRat remove ${t}`);
  await run('execute store result storage bm:lg tmp.pid int 1 run scoreboard players get TestRat bm.pid');
  const pid = await sc('TestRat', 'bm.pid');
  await run(`data remove storage bm:gv bag.p${pid}`); await run(`data remove storage bm:gv cb.p${pid}`);
  const kit = async () => {
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
    for (let k = 0; k < 4; k++) await run('loot give TestRat loot bm:items/token');
    await run('item replace entity TestRat hotbar.5 with minecraft:diamond_sword'); await run('item replace entity TestRat armor.head with minecraft:iron_helmet');
  };
await kit(); await run('effect give TestRat minecraft:hunger 8 150 true'); await sleep(8500); A.stand(); await sleep(500);
  const food0 = +((await run('data get entity TestRat foodLevel')).match(/data: (\d+)/) || [0, NaN])[1];
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player (no operator commands)', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  const toLounge = async () => {
    A.slot(0); await sleep(300); await A.useWait(); A.chats.length = 0;
    A.click(/Fixer's Lounge/); await wait(7000, async () => /gutter/.test(await dim())); await sleep(1200); A.stand();
    return /gutter/.test(await dim()) && fnTrue('as TestRat', 'bm:p121/inside');
  };

  // ================================================================== 1. in through the Ledger: the coat check at the door
  ok('The Ledger\'s "Fixer\'s Lounge" (hold still): you\'re in the lounge', await toLounge(), await dim());
  ok('...the Fixer checks your gear at the door (he says so)', /checks your gear at the door/i.test(A.chats.join(' ')), A.chats.slice(-2).join(' / ').slice(0, 200));
  ok('...your sword and helmet stay with him', !(await has('diamond_sword')) && !(await has('iron_helmet', 'armor.head')));
  const inv = async () => (await run('data get entity TestRat Inventory')).replace(/.*data: /, '').match(/id: "[^"]+"|bm: "[^"]+"/g)?.join(' ') || '';
  ok('...your Ledger and Tokens come in with you', (await hasBm('fixers_ledger')) && (await hasBm('token')), await inv());
  const foodNow = async () => +((await run('data get entity TestRat foodLevel')).match(/data: (\d+)/) || [0, NaN])[1];
  await wait(10000, async () => (await foodNow()) >= 20, 400);
  const regen = await run('data get entity TestRat active_effects[{id:"minecraft:regeneration"}].amplifier');
  const food = await foodNow();
  ok('The lounge heals as the den does: Regeneration II, and Saturation fills you up', /: 1b?$/.test(regen.trim()) && food0 < 20 && food - food0 >= 10, `regen amp ${regen.replace(/.*data: /, '')}, food ${food} (was ${food0} at the door)`);

  // ================================================================== 2. out through the Fixer's Door: home, gear back
  const ex = (await run('execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.lgexit,limit=1] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (ex) await A.walkTo(+ex[1], +ex[3]);
  await wait(5000, async () => /overworld/.test(await dim())); await sleep(3500); A.stand();
  let p = await pos();
  ok('Through the Lounge\'s door: home where you stood', /overworld/.test(await dim()) && p && Math.abs(p[0] - HX - 0.5) < 2 && Math.abs(p[2] - HZ - 0.5) < 2, `${await dim()} ${p}`);
  ok('...and the Fixer hands your gear back: sword in the pack, helmet on your head', (await has('diamond_sword')) && (await has('iron_helmet', 'armor.head')));

  // ================================================================== 3. out another way - a death: the gear still comes home
  ok('In again', await toLounge());
  await run('kill TestRat'); await wait(8000, async () => /overworld/.test(await dim())); await sleep(4000); A.stand();
  ok('Dying in the lounge: you wake at home, and your gear is handed back there', /overworld/.test(await dim()) && (await has('diamond_sword')) && (await has('iron_helmet', 'armor.head')),
     `${await dim()} sword ${await has('diamond_sword')} helmet ${await has('iron_helmet', 'armor.head')}`);
  ok('...nothing left with the Fixer', !(await passes(`execute if data storage bm:gv bag.p${pid}`)) && !/bm.lgbag/.test(await run('tag TestRat list')));

  // ================================================================== 4. a heist planned from the lounge
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await kit(); await sleep(1500); A.stand();
  ok('In again for a heist', await toLounge());
  await run('give TestRat minecraft:diamond 3');                                        // (what the lounge's shops would have sold)
  await A.useWait(); show('ledger'); await A.press(/Plan a Heist/); show('plan'); await A.press(/Tier I\b(?!I)/); show('tier'); A.chats.length = 0; await A.press(/^3\b|3 tries/i); show('tries');
  const inV = await wait(60000, async () => /gutter/.test(await dim()) && await passes('execute if entity @a[name=TestRat,tag=bm.gvp]'));
  ok('Plan a Heist from the lounge: into the vault', inV, A.chats.slice(-3).join(' / ').slice(0, 240));
  if (inV) {
    await sleep(2000); A.stand();
    ok('...what you picked up in the lounge (the diamonds) waits with the Fixer', !(await has('diamond')) && /waits with the Fixer/i.test(A.chats.join(' ')), A.chats.slice(-3).join(' / ').slice(0, 200));
    ok('...your own gear is still checked (no sword, no helmet)', !(await has('diamond_sword')) && !(await has('iron_helmet', 'armor.head')));
    const ret = await run(`data get storage bm:gv ret.p${pid}`);
    ok('...the way home is where you came into the lounge from', ret.includes(`x: ${HX}`) && ret.includes(`z: ${HZ}`) && /overworld/.test(ret), ret.replace(/.*data: /, ''));
    const sp = await run(`data get storage bm:gv sp.p${pid}`);
    ok('...and your own respawn point is saved (not lost to the den)', /pos/.test(sp) && /overworld/.test(sp), sp.replace(/.*data: /, '').slice(0, 120));
    // leave the heist from the Ledger
    await A.useWait(); await A.press(/Leave the heist/); show('leave?'); await A.press(/Leave now/);
    await wait(8000, async () => /overworld/.test(await dim())); await sleep(4500); A.stand();
    p = await pos();
    ok('Leave the heist: home - to the spot you came into the lounge from (not the world spawn)', /overworld/.test(await dim()) && p && Math.abs(p[0] - HX - 0.5) < 2 && Math.abs(p[2] - HZ - 0.5) < 2, `${await dim()} ${p}`);
    ok('...your sword and helmet are back', (await has('diamond_sword')) && (await has('iron_helmet', 'armor.head')));
    ok('...and the lounge\'s diamonds came home with you', await has('diamond'));
    const rsp = await run('data get entity TestRat respawn');
    ok('...your respawn point is your own again (overworld)', /overworld/.test(rsp) || !/gutter/.test(rsp), rsp.replace(/.*data: /, '').slice(0, 120));
  }
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
