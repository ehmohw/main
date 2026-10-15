// 2.78a: Emma with a Wraithfire Heart blesses at level II, as a regular (non-op) player, every step a real packet: the ribbon's
// menu sets her Offense form - Strength I, the heart not given; the heart given by a right-click on her; her Wraithfire Form
// switched off in her menu (she keeps the heart) - and her Offense blessing is Strength II all the same; the heart taken back
// (her menu): Strength I again. rcon only sets the stage (the ribbon, the heart, a clean slate).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 300) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const X = 14060, Y = 121, Z = 14000;
  const uuidOf = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const has = async (iid) => /Found [1-9]/.test(await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`));
  const strength = async () => { const fx = await run('data get entity TestRat active_effects');
    const one = (fx.match(/\{[^{}]*id: "minecraft:strength"[^{}]*\}/) || [null])[0]; if (!one) return -1;
    const m = one.match(/amplifier: (\d+)b/); return m ? +m[1] : 0; };      // (the game leaves a level-I amplifier (0) out)
  const EMMA = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  for (const o of ['bm.emwf', 'bm.emst']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players reset TestRat bm.emcd'); await run('kill @e[type=minecraft:cat,tag=bm.emmapet]');
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 5} ${Z + 12} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(2000);
  // (her ribbon, used: she comes)
  await run('loot replace entity TestRat hotbar.8 loot bm:items/emma_ribbon'); A.slot(8); await sleep(300); A.use(); await sleep(400); A.release();
  ok('the ribbon used: Emma comes', await wait(4000, async () => !/No entity/.test(await run(`${O}data get entity ${EMMA} UUID`))));
  const menu = async () => { A.slot(8); await sleep(300); A.input({ shift: true }); await sleep(250); A.use(); await sleep(400); A.release(); A.input({}); await sleep(600); };
  await menu(); A.cmd('trigger bm.act set 7302'); await sleep(800);
  await run('effect clear TestRat');
  ok('her menu: Offense - she blesses you with Strength I (no heart)', await wait(8000, async () => (await strength()) === 0), `amp ${await strength()}`);
  // (the heart, given with a right-click on her)
  await run(`${O}tp ${EMMA} ${X + 0.5} ${Y} ${Z + 2.5}`); await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(900);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(300);
  const u = await uuidOf(EMMA); const ent = Object.values(A.ents).find(x => x.objectUUID === u);
  if (ent) A.interact(ent.entityId); await sleep(1500);
  ok('the heart given to her (a right-click): she keeps it', (await sc('TestRat', 'bm.emwf')) === 1 && !(await has('wraithfire_heart')), `emwf ${await sc('TestRat', 'bm.emwf')}`);
  // (her Wraithfire Form switched off - she still holds the heart)
  await menu(); A.cmd('trigger bm.act set 7307'); await sleep(2500);
  ok('her Wraithfire Form switched off in her menu (she still has the heart)', (await sc('TestRat', 'bm.emst')) === 0 && (await sc('TestRat', 'bm.emwf')) === 1);
  await run('effect clear TestRat');
  ok('...and her Offense blessing is Strength II', await wait(8000, async () => (await strength()) === 1), `amp ${await strength()}`);
  // (the heart taken back: Strength I again)
  await menu(); A.cmd('trigger bm.act set 7308'); await sleep(800);
  ok('the heart taken back (her menu): in your pack', (await sc('TestRat', 'bm.emwf')) === 0 && (await has('wraithfire_heart')));
  await run('effect clear TestRat');
  ok('...her blessing is Strength I again', await wait(8000, async () => (await strength()) === 0), `amp ${await strength()}`);
  await run('kill @e[type=minecraft:cat,tag=bm.emmapet]'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
