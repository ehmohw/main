// 2.74: outfits and Emma's buff from the Ledger; Emma remembers her buff
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500);
  const asRat = c => run(`execute as TestRat at TestRat run ${c}`);
  const click = async (code, via = 'p28/act') => { if (via === 'p28/act') await run(`scoreboard players set TestRat bm.act ${code}`); else await run(`scoreboard players set #act bm.pay ${code}`); return asRat(`function bm:${via}`); };
  const menu = () => num('scoreboard players get TestRat bm.menu');
  const tagged = async t => /passed/.test(await run(`execute if entity @a[name=TestRat,tag=${t}]`));
  // ---- in the vault
  await heist('levers', 'a', 2); await begin();
  await asRat('function bm:admin/wardrobe_all');
  await asRat('function bm:p80/office'); await click(7807, 'p80/act'); ok('Raid Crew page (on a heist) shows the new button', (await menu()) === 7807 && fnText('p98/crew').includes('Outfits'));
  await click(7950, 'p80/act'); ok('...Outfits & Emma\'s buff opens', (await menu()) === 7950);
  await click(7951, 'p80/act'); ok('...Emma\'s wardrobe opens from it, in the vault', (await menu()) === 9800 && await tagged('bm.wdled'));
  await asRat('scoreboard players set @s bm.emr 0');
  const ribbonObj = (fnText('p99/pick/ribbon2').match(/scoreboard players set @s (\S+) 2/) || [])[1];
  await click(9804); ok(`...pick an outfit: it's on (${ribbonObj} = 2) and the wardrobe stays open`, (await num(`scoreboard players get TestRat ${ribbonObj}`)) === 2 && (await menu()) === 9800);
  await click(9800); ok('...its first button goes back to the page (nobody is sent home)', (await menu()) === 7950);
  for (const [code, w, b] of [[7952, 'celi', 9840], [7953, 'zib', 9860], [7954, 'cecil', 9880], [7955, 'kw', 9900], [7956, 'leo', 9920], [7957, 'demo', 9940]]) {
    await click(code, 'p80/act');
    const opened = (await menu()) === b; await click(b);
    ok(`...${w}'s wardrobe opens too, and its back button returns to the page`, opened && (await menu()) === 7950);
  }
  await click(7962, 'p80/act');
  ok('Emma\'s buff from the Ledger (she isn\'t out): Offense, remembered', (await num('scoreboard players get TestRat bm.emode')) === 2 && (await menu()) === 7950);
  await asRat('function bm:p119/plain/emma');
  ok('Sneak + use (the ordinary way in): the ordinary wardrobe, with Send home', !(await tagged('bm.wdled')) && (await menu()) === 9800);
  // ---- outside: Emma comes with the remembered buff; the Ledger changes her while she's out
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.gvi');
  await sleep(1500); await run('clear TestRat'); await run('scoreboard players set TestRat bm.emcd 0');
  await asRat('function bm:p57/try_summon'); await sleep(500);
  const E = '@e[type=minecraft:cat,tag=bm.emmapet,distance=..8,limit=1,sort=nearest]';
  ok('Emma called: she arrives on the remembered buff (Offense), not Healing', (await num(`execute positioned 13000.5 120 13000.5 run scoreboard players get ${E} bm.emm`)) === 2);
  await asRat('function bm:p80/give_ledger').catch(() => {});
  const lg = fnText('admin/tier_finds'); // (any give line) - give the ledger
  await run('give TestRat ' + (fnText('p80/first_ledger').split('\n').find(l => l.startsWith('give @s')) || '').replace(/^give @s /, ''));
  await asRat('function bm:p80/office'); await click(7950, 'p80/act'); await click(7963, 'p80/act');
  ok('...the Ledger switches her to Defense while she\'s out, and it\'s remembered', (await num(`execute positioned 13000.5 120 13000.5 run scoreboard players get ${E} bm.emm`)) === 3 && (await num('scoreboard players get TestRat bm.emode')) === 3);
  await asRat('function bm:p98/home/emma'); await sleep(800); await run('scoreboard players set TestRat bm.emcd 0');
  await asRat('function bm:p57/try_summon'); await sleep(500);
  ok('...sent home and called again: still Defense', (await num(`execute positioned 13000.5 120 13000.5 run scoreboard players get ${E} bm.emm`)) === 3);
  await asRat('function bm:p98/home/emma'); await run('scoreboard players reset TestRat bm.emode'); await run('clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
