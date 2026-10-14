// v2.67b: Democratus in rain and thunder, Leo's water breathing, the follower trios, followers swimming, one rest room a heist
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 19300, Y = 120, Z = 19000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const hpOf = async sel => { const m = (await run(`data get entity ${sel} Health`)).match(/([\d.]+)f/); return m ? +m[1] : NaN; };
  const eff = async (sel, e) => new RegExp(`minecraft:${e}`).test(await run(`data get entity ${sel} active_effects`));
  const effAmp = async (sel, e) => { const o = await run(`data get entity ${sel} active_effects[{id:"minecraft:${e}"}].amplifier`); const m = o.match(/data: (\d+)b/);
    return m ? +m[1] : (/Found no|No /.test(o) ? -1 : 0); };
  const ty = async sel => { const m = (await run(`data get entity ${sel} transformation.translation[1]`)).match(/(-?[\d.]+)f/); return m ? +m[1] : NaN; };
  const until = async (f, ms = 4000) => { for (let t = 0; t < ms; t += 200) { if (await f()) return true; await sleep(200); } return !!(await f()); };
  const W = { emma: '@e[type=cat,tag=bm.emmapet,limit=1]', leo: '@e[type=wolf,tag=bm.leopet,limit=1]', cecil: '@e[type=wolf,tag=bm.cecilpet,limit=1]',
              celi: '@e[type=wolf,tag=bm.celipet,limit=1]', demo: '@e[type=wolf,tag=bm.dmpet,limit=1]', kw: '@e[type=wolf,tag=bm.kxpet,limit=1]', zib: '@e[type=wolf,tag=bm.zibpet,limit=1]' };
  const ITEM = { emma: ['emma_ribbon', 'p57/use'], leo: ['leo_crest', 'p96/use'], cecil: ['cecil_gem', 'p46/pet/use'], celi: ['celi_charm', 'p66/use'],
                 demo: ['demo_seal', 'p97/use'], kw: ['kw_spark', 'p79/spark'], zib: ['donadian_medal', 'p72/zb/use'] };
  const HOME = { emma: 'emma', leo: 'leo', cecil: 'cecil', celi: 'celi', demo: 'demo', kw: 'killerwatt', zib: 'zib' };
  const call = async who => { await run('item replace entity TestRat weapon.mainhand with air'); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${ITEM[who][0]}`);
    await run('scoreboard players set TestRat bm.gvhc 0'); await run(`execute as TestRat at @s run function bm:${ITEM[who][1]}`); await sleep(1500);
    await run('item replace entity TestRat weapon.mainhand with air'); };
  const home = async who => { await run('scoreboard players operation #me bm.pid = TestRat bm.pid'); await run(`execute as TestRat at @s run function bm:p98/home/${HOME[who]}`); await sleep(900); };
  const homeAll = async () => { for (const w of Object.keys(W)) await home(w); };
  await run(`forceload add ${X - 32} ${Z - 32} ${X + 48} ${Z + 32}`); await sleep(1500);
  await run(`fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`); await run(`fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y + 16} ${Z + 20} minecraft:air`);
  // the pool: 11 x 11, four deep, a pillar in the middle to stand on
  const PX = X + 32;
  await run(`fill ${PX - 6} ${Y - 6} ${Z - 6} ${PX + 6} ${Y - 1} ${Z + 6} minecraft:stone`); await run(`fill ${PX - 5} ${Y - 5} ${Z - 5} ${PX + 5} ${Y - 1} ${Z + 5} minecraft:water`);
  await run(`fill ${PX - 6} ${Y} ${Z - 6} ${PX + 6} ${Y + 8} ${Z + 6} minecraft:air`); await run(`fill ${PX} ${Y - 5} ${Z} ${PX} ${Y - 1} ${Z} minecraft:stone`);
  await run('time set day'); await run('weather clear'); await run('gamerule doMobSpawning false'); await run('gamerule advance_weather false');
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.dmpet', 'vindicator,tag=bm.dmboss'])
    await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  for (const o of ['bm.lecd', 'bm.dmcd', 'bm.cpcd', 'bm.kxcd', 'bm.emcd', 'bm.cecd', 'bm.zbcd', 'bm.cpel', 'bm.kxel', 'bm.trio', 'bm.triob', 'bm.trioc'])
    await run(`scoreboard players set TestRat ${o} 0`);
  for (const t of ['bane', 'storm', 'guard', 'odd']) await run(`advancement revoke TestRat only bm:story/trio_${t}`);
  // (their own items in the pack, or they head home)
  for (const [n, w] of Object.keys(ITEM).entries()) await run(`loot replace entity TestRat container.${9 + n} loot bm:items/${ITEM[w][0]}`);
  await sleep(1000);

  // ---- Leo: water breathing, always
  await call('leo');
  ok('Leo out: you breathe underwater (no water needed)', await until(() => eff('TestRat', 'water_breathing')));

  // ---- the Serpent's Bane: Emma, Leo, Cecil
  await call('emma'); await call('cecil');
  ok("Emma, Leo and Cecil: the Serpent's Bane", await until(async () => (await sc('TestRat', 'bm.trio')) === 1), `trio ${await sc('TestRat', 'bm.trio')}`);
  ok('...its hidden achievement', /true|passed/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/trio_bane=true}]')));
  ok('...you regenerate and shrug off blows', (await eff('TestRat', 'regeneration')) && (await eff('TestRat', 'resistance')));
  ok('...and the three hit harder', (await eff(W.leo, 'strength')) && (await eff(W.emma, 'strength')) && (await eff(W.cecil, 'strength')));

  // ---- swimming: Emma, Leo, Cecil in deep water
  await run(`tp TestRat ${PX + 0.5} ${Y} ${Z + 0.5}`); await sleep(300);
  await run(`tp ${W.emma} ${PX + 2.5} ${Y - 2} ${Z + 0.5}`); await run(`tp ${W.leo} ${PX - 1.5} ${Y - 2} ${Z + 2.5}`); await run(`tp ${W.cecil} ${PX + 0.5} ${Y - 2} ${Z - 2.5}`);
  ok('Emma swims in deep water', await until(async () => (await sc(W.emma, 'bm.ems')) === 10, 5000), `state ${await sc(W.emma, 'bm.ems')}`);
  ok('Leo swims', await until(async () => (await sc(W.leo, 'bm.les')) === 10, 3000), `state ${await sc(W.leo, 'bm.les')}`);
  ok('Cecil swims (sunk to the chest, paddling)', await until(async () => (await ty('@e[type=item_display,tag=bm.cpet,tag=bm.cp_body,limit=1]')) < 0.3, 3000),
     `${await ty('@e[type=item_display,tag=bm.cpet,tag=bm.cp_body,limit=1]')}`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); for (const w of ['emma', 'leo', 'cecil']) await run(`tp ${W[w]} ${X + 2.5} ${Y} ${Z + 0.5}`);
  ok('...and walks again on dry land', await until(async () => (await sc(W.leo, 'bm.les')) !== 10, 3000));

  // ---- the Princess's Guard: Emma, Leo, Celi
  await home('cecil'); await call('celi');
  ok("Emma, Leo and Celi: the Princess's Guard", await until(async () => (await sc('TestRat', 'bm.trio')) === 3), `trio ${await sc('TestRat', 'bm.trio')}`);
  ok('...two more hearts for you', await until(() => eff('TestRat', 'health_boost'), 2000));
  ok('...and the three are tougher', await eff(W.celi, 'resistance'));

  // ---- the Storm Court: Cecil, Democratus, KillerWatt
  await home('emma'); await home('leo'); await home('celi'); await run('effect clear TestRat');
  await call('cecil'); await call('demo'); await call('kw');
  ok('Cecil, Democratus and KillerWatt: the Storm Court', await until(async () => (await sc('TestRat', 'bm.trio')) === 2), `trio ${await sc('TestRat', 'bm.trio')}`);
  ok('...Strength II and Speed for you', await until(async () => (await effAmp('TestRat', 'strength')) === 1 && (await eff('TestRat', 'speed')), 2000));
  await run(`scoreboard players set ${W.kw} bm.kxch 0`); await run(`scoreboard players set ${W.demo} bm.dmch 0`); await sleep(4600);
  ok('...and their charged attacks build by themselves', (await sc(W.kw, 'bm.kxch')) >= 1 && (await sc(W.demo, 'bm.dmch')) >= 1, `kw ${await sc(W.kw, 'bm.kxch')} demo ${await sc(W.demo, 'bm.dmch')}`);
  // swimming: Democratus, KillerWatt
  await run(`tp TestRat ${PX + 0.5} ${Y} ${Z + 0.5}`); await sleep(300);
  await run(`tp ${W.demo} ${PX + 2.5} ${Y - 2} ${Z + 0.5}`); await run(`tp ${W.kw} ${PX - 2.5} ${Y - 2} ${Z - 2.5}`); await run(`tp ${W.cecil} ${PX + 0.5} ${Y - 2} ${Z + 2.5}`);
  ok('Democratus swims', await until(async () => (await sc(W.demo, 'bm.dms')) === 10, 5000), `state ${await sc(W.demo, 'bm.dms')}`);
  ok('KillerWatt swims (his breaststroke, not the hover)', await until(async () => (await sc(W.kw, 'bm.kxs')) === 3, 3000), `state ${await sc(W.kw, 'bm.kxs')}`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); for (const w of ['demo', 'kw', 'cecil']) await run(`tp ${W[w]} ${X + 2.5} ${Y} ${Z + 0.5}`);

  // ---- the Odd Ones: Emma, Cecil, KillerWatt
  await home('demo'); await run('effect clear TestRat'); await call('emma');
  ok('Emma, Cecil and KillerWatt: the Odd Ones', await until(async () => (await sc('TestRat', 'bm.trio')) === 4), `trio ${await sc('TestRat', 'bm.trio')}`);
  ok('...Speed II, Jump Boost and Haste for you', await until(async () => (await effAmp('TestRat', 'speed')) === 1 && (await eff('TestRat', 'jump_boost')) && (await eff('TestRat', 'haste')), 2000));
  await home('kw');
  ok('One of them leaves: the trio breaks', await until(async () => (await sc('TestRat', 'bm.trio')) === 0, 3000), `trio ${await sc('TestRat', 'bm.trio')}`);

  // ---- swimming: Celi and Zib
  await home('emma'); await home('cecil'); await call('celi'); await call('zib');
  await run(`tp TestRat ${PX + 0.5} ${Y} ${Z + 0.5}`); await sleep(300);
  await run(`tp ${W.celi} ${PX + 2.5} ${Y - 2} ${Z + 0.5}`); await run(`tp ${W.zib} ${PX - 2.5} ${Y - 2} ${Z + 0.5}`);
  ok('Celi swims', await until(async () => (await sc(W.celi, 'bm.ces')) === 10, 5000), `state ${await sc(W.celi, 'bm.ces')}`);
  ok('Zib swims', await until(async () => (await sc(W.zib, 'bm.zbs')) === 10, 3000), `state ${await sc(W.zib, 'bm.zbs')}`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await homeAll(); await run('effect clear TestRat');

  // ---- Democratus: the rain, the thunder
  await call('demo'); await sleep(500);
  ok('Clear skies: Democratus is himself', (await sc(W.demo, 'bm.dmwx')) === 0);
  await run('weather rain');
  ok('Rain: he grows stronger', await until(async () => (await sc(W.demo, 'bm.dmwx')) === 1, 3000), `wx ${await sc(W.demo, 'bm.dmwx')}`);
  ok('...Resistance', await eff(W.demo, 'resistance'));
  const swing = async () => {
    await run('kill @e[type=husk,tag=bm.t103h]'); await run(`tp ${W.demo} ${X + 3.5} ${Y} ${Z + 0.5}`); await run(`scoreboard players set ${W.demo} bm.dmch 0`);
    await run(`summon minecraft:husk ${X + 5.5} ${Y} ${Z + 0.5} {Tags:["bm.t103h","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:80f,attributes:[{id:"minecraft:max_health",base:80d},{id:"minecraft:armor",base:0d}]}`);
    await until(async () => (await hpOf('@e[type=husk,tag=bm.t103h,limit=1]')) < 80, 5000); await sleep(300);
    return 80 - (await hpOf('@e[type=husk,tag=bm.t103h,limit=1]')); };
  const d1 = await swing();
  ok('...his sweep: 20 in the rain', d1 >= 19.5 && d1 < 25, `dealt ${d1}`);
  await run('weather thunder'); await sleep(5600);
  ok('A thunderstorm: stronger still', (await sc(W.demo, 'bm.dmwx')) === 2, `wx ${await sc(W.demo, 'bm.dmwx')}`);
  ok('...Resistance II and Regeneration', (await effAmp(W.demo, 'resistance')) === 1 && (await eff(W.demo, 'regeneration')));
  const d2 = await swing();
  ok('...his sweep: 26 in a thunderstorm', d2 >= 25.5, `dealt ${d2}`);
  ok('...and each blow charges him twice', (await sc(W.demo, 'bm.dmch')) >= 2, `charge ${await sc(W.demo, 'bm.dmch')}`);
  await run('kill @e[type=husk,tag=bm.t103h]'); await run('weather clear');
  ok('Clear again: back to himself (once the rain has passed)', await until(async () => (await sc(W.demo, 'bm.dmwx')) === 0, 9000));
  await home('demo');

  // ---- one rest room a heist
  const rested = async () => /returned 1/.test(await run('execute store result score #x bm.rng run function bm:p90/lay/rested'));
  await run('scoreboard players set #endl bm.rng 0'); await run('scoreboard players set #epool bm.rng 0');
  ok('No rest room yet: one may be drawn', !(await rested()));
  const rf = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p90/lay/rested.mcfunction', 'utf8');
  const bits = [...rf.matchAll(/#bit bm\.rng (\d+)/g)].map(m => +m[1]);
  ok('Both rest rooms are checked (the Rats\' Rest and the Sanctuary)', bits.length === 2, rf);
  for (const [k, b] of bits.map((b, i) => [i ? 'Sanctuary' : 'Rats\' Rest', b])) {
    await run(`scoreboard players set #epool bm.rng ${b}`);
    ok(`...a ${k} already laid: no second rest room`, await rested());
  }
  await run('scoreboard players set #epool bm.rng 0'); await run('scoreboard players set #endl bm.rng 1');
  ok('The Endless Vault draws neither (it has its own Rests)', await rested());
  await run('scoreboard players set #endl bm.rng 0');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log('ERR', e); process.exit(1); });
