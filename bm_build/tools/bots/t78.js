// v2.65: follower cosmetics - Emma's ribbons and dresses, Celi's outfits, Zib's uniforms; the Tailor's stock (raid exclusives - not Velour's, 2.82); the hidden ones
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const fs = require('fs'); const path = require('path');
const res = []; const X = 17000, Y = 120, Z = 17000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const press = async (sneak) => { await run('scoreboard players set TestRat bm.gvhc 0'); if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.use(); await sleep(300); A.release(); if (sneak) A.input({}); await sleep(600); };
  const hold = async iid => { await run('item replace entity TestRat weapon.mainhand with air'); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${iid}`); await sleep(150); };
  const models = async tag => { const o = await run(`execute as @e[type=item_display,tag=${tag}] run data get entity @s item.components."minecraft:item_model"`); return o; };
  const allModels = async (tag) => { const out = []; for (let i = 0; i < 16; i++) { const o = await run(`data get entity @e[type=item_display,tag=${tag},limit=1,tag=!bm.t78seen] item.components."minecraft:item_model"`);
    if (/No entity/.test(o)) break; out.push((o.match(/"([^"]+)"/) || [0, o])[1]); await run(`tag @e[type=item_display,tag=${tag},limit=1,tag=!bm.t78seen] add bm.t78seen`); }
    await run('tag @e[tag=bm.t78seen] remove bm.t78seen'); return out; };
  await run(`forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`); await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run('weather clear'); await run('time set day');
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.dmpet', 'wolf,tag=bm.cecilpet']) await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run('kill @e[type=item_display,tag=bm.emp]'); await run('kill @e[type=item_display,tag=bm.cep]'); await run('kill @e[type=item_display,tag=bm.zbr]');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  for (const o of ['bm.cosr', 'bm.cosd', 'bm.cosc', 'bm.cosz', 'bm.emcd', 'bm.zbcd', 'bm.wur', 'bm.wud', 'bm.wuc', 'bm.wuz', 'bm.coso']) await run(`scoreboard players reset TestRat ${o}`);
  // (their own items in the pack, or they go home after three seconds)
  for (const [n, i] of ['emma_ribbon', 'celi_charm', 'donadian_medal'].entries()) await run(`loot replace entity TestRat container.${9 + n} loot bm:items/${i}`);
  await sleep(1000);

  // ---- EMMA
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(1500);
  const base = await allModels('bm.emp');
  ok('Emma comes in her own clothes (no dress, pink ribbon)', base.length >= 8 && !base.some(m => /_d\d_m\d|em_head_r/.test(m)), base.join(' '));
  await hold('cos_dress_3'); await press(false);
  const d3 = await allModels('bm.emp');
  ok('Sakura dress: her dress re-dyed (the scarf still shows her buff)', d3.some(m => /_d3_m\d/.test(m)) && (await num('scoreboard players get TestRat bm.cosd')) === 3, d3.filter(m => /_d/.test(m)).join(' '));
  ok('...and the dress is used up - unlocked for good in her wardrobe (2.67)', /No items|^[^\d]*0\b|: 0$/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"cos_dress_3"}] 0')) &&
     ((await num('scoreboard players get TestRat bm.wud')) & 8) === 8);
  await hold('cos_ribbon_2'); await press(false);
  const r2 = await allModels('bm.emp');
  ok('Midnight ribbon: tied in her hair', r2.includes('bm:em_head_r2') && r2.some(m => /_d3_m\d/.test(m)), r2.filter(m => /head|_d/.test(m)).join(' '));
  // she keeps them on the next call
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(1500);
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(1800);
  const again = await allModels('bm.emp');
  ok('Called again: still in Sakura with the Midnight ribbon', again.includes('bm:em_head_r2') && again.some(m => /_d3_m\d/.test(m)), again.filter(m => /head|_d/.test(m)).join(' '));
  await hold('cos_dress_3'); await press(true);
  const back = await allModels('bm.emp');
  ok('Sneak + use the dress: back in her own blue', !back.some(m => /_d\d_m\d/.test(m)) && back.includes('bm:em_head_r2') && !((await num('scoreboard players get TestRat bm.cosd')) > 0), back.join(' ') + ' cosd=' + (await run('scoreboard players get TestRat bm.cosd')) + ' bars=' + A.bars.slice(-2).join('|'));
  await hold('cos_ribbon_2'); await press(true);
  ok('Sneak + use the ribbon: her pink one again', !(await allModels('bm.emp')).some(m => /em_head_r/.test(m)));
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(600);
  await hold('cos_ribbon_5'); await press(false);
  ok('With Emma away, a ribbon is remembered for next time', (await num('scoreboard players get TestRat bm.cosr')) === 5 && /next time/.test(A.bars.join(' ')), A.bars.slice(-1)[0]);
  await run('scoreboard players set TestRat bm.cosr 0');

  // ---- CELI
  await run('execute as TestRat at @s run function bm:p66/summon_here'); await sleep(2500);
  const c0 = await allModels('bm.cep');
  await hold('cos_celi_2'); await press(false);
  const c2 = await allModels('bm.cep');
  ok('Celi in Rosehip: tunic and skirt in the new colours', c0.length > 4 && !c0.some(m => /_o\d$/.test(m)) && c2.some(m => /_o2$/.test(m)), c2.filter(m => /_o/.test(m)).join(' '));
  await hold('celi_charm'); await press(true);
  ok('...sneak + use her charm: her wardrobe (2.67)', (await num('scoreboard players get TestRat bm.menu')) === 9840);
  await run('scoreboard players set TestRat bm.act 9842'); await sleep(600);
  ok('...her own clothes from it', !(await allModels('bm.cep')).some(m => /_o\d$/.test(m)));
  await run('execute as @e[type=wolf,tag=bm.celipet] at @s run function bm:p66/go'); await sleep(800);

  // ---- ZIB
  await run('scoreboard players set TestRat bm.zbcd 0'); await run('execute as TestRat at @s run function bm:p72/zb/summon'); await sleep(1500);
  await hold('cos_zib_1'); await press(false);
  const z1 = await allModels('bm.zbr');
  ok('Zib in the Crimson Guard uniform', z1.some(m => /_u1$/.test(m)) && (await num('scoreboard players get TestRat bm.cosz')) === 1, z1.filter(m => /_u/.test(m)).join(' '));
  await run('execute as @e[type=wolf,tag=bm.zibpet] at @s run function bm:p72/zb/beamup'); await sleep(800);
  await run('execute as TestRat at @s run function bm:p72/zb/summon'); await sleep(1500);
  ok('...and still wearing it when he beams back down', (await allModels('bm.zbr')).some(m => /_u1$/.test(m)));
  await hold('cos_zib_1'); await press(true);
  ok('...sneak + use: his navy again', !(await allModels('bm.zbr')).some(m => /_u\d$/.test(m)));
  await run('execute as @e[type=wolf,tag=bm.zibpet] at @s run function bm:p72/zb/beamup'); await sleep(500);

  // ---- where they come from
  const root = BMB + 'out_p2/BlackMarket_DP/data/bm';
  const all = []; const walk = d => { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : all.push(p); } }; walk(path.join(root, 'function'));
  const vel = all.filter(p => /outfitter/.test(p)).map(p => fs.readFileSync(p, 'utf8')).join('\n');
  const tl = all.filter(p => /p103[\/]tl[\/]/.test(p)).map(p => fs.readFileSync(p, 'utf8')).join('\n');
  ok('Follower cosmetics are raid exclusives (2.82): Madame Velour sells none', !/bm:"cos_/.test(vel));
  ok('...the Tailor in the den sells the ribbons, dresses and outfits', ['cos_ribbon_1', 'cos_ribbon_5', 'cos_dress_1', 'cos_dress_4', 'cos_celi_3', 'cos_zib_2'].every(i => tl.includes(`bm:"${i}"`)));
  const lt = ['shiny', 'secret', 'champion', 'ratking'].map(t => fs.readFileSync(path.join(root, 'loot_table/p76', t + '.json'), 'utf8')).join('\n');
  ok('The hidden four drop from the vault\'s rare foes and secrets', ['cos_ribbon_6', 'cos_dress_5', 'cos_celi_4', 'cos_zib_3'].every(i => lt.includes(i)));
  await run(`forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
