// 2.78a: Apophiss's forms, as a regular (non-op) player: the Oath calls him (his own scales, no wings); right-clicked holding the
// Ethereal Gem (a real interact packet on his click box) he takes it - the ethereal king's scales and his wings out, the gem
// gone from the hand; the Wraithfire Heart: soul-blue scales and wings, the gem back in the bot's pack; his poses still turn the
// wings; a picked colour gives way to the form; sneak + right-click empty-handed: the heart back, his own scales, no wings.
// rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const use = async (C, slot) => { C.slot(slot); await sleep(250); C.use(); await sleep(400); C.release(); };
  const part = p => `@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_${p},limit=1]`;
  const model = async p => ((await nbt(part(p), 'item.components')).match(/"minecraft:item_model": "([^"]+)"/) || [0, ''])[1];
  const wscale = async () => +(((await nbt(part('wingr'), 'transformation.scale[0]')).match(/([\d.]+)f/) || [0, NaN])[1]);
  const X = 16460, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  for (const t of ['bm.appet', 'bm.emmapet', 'bm.leopet', 'bm.cecilpet', 'bm.kxpet', 'bm.wilfrey']) await run(`kill @e[tag=${t}]`);
  for (const o of ['bm.apcd', 'bm.apel', 'bm.cosap']) await run(`scoreboard players set TestRat ${o} 0`);
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y} ${Z + 16} minecraft:stone`); await run(`${O}fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 12} ${Z + 16} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2000);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_oath');
  await use(A, 0);
  const pet = '@e[type=minecraft:wolf,tag=bm.appet,limit=1]';
  ok('the Oath calls him', await wait(5000, async () => (await cnt(pet)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.app_pet]')) === 14));
  await sleep(2500);
  ok('his own scales, his wings away', (await model('body')) === 'bm:apo_body' && (await wscale()) === 0, `${await model('body')} wing ${await wscale()}`);
  await run(`${O}tp ${pet} ${X + 0.5} ${Y + 1} ${Z + 3.5}`); await run(`${O}data modify entity ${pet} Sitting set value 1b`); await sleep(1200);
  const click = async (slot, sneak = false) => {
    const box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.aphit,limit=1]'); if (!box) return false;
    A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.interact(box.entityId, sneak); await sleep(900); if (sneak) { A.input({}); await sleep(200); } return true;
  };
  // ---- the Ethereal Gem
  await run('loot replace entity TestRat hotbar.1 loot bm:items/ethereal_gem'); A.bars.length = 0;
  const c1 = await click(1);
  ok('right-click him holding the Ethereal Gem: he takes it (out of the hand)', c1 && (await has('ethereal_gem')) === 0, A.bars.slice(-1).join(''));
  ok('...the ethereal king\'s scales', /_eth$/.test(await model('body')) && /_eth$/.test(await model('head')) && /_eth$/.test(await model('coil')),
     `${await model('body')} ${await model('head')}`);
  ok('...and his wings out', await wait(2000, async () => (await wscale()) > 1), `wing ${await wscale()}`);
  ok('...the player is told', A.bars.some(b => /ETHEREAL FORM/.test(b)), A.bars.slice(-1).join(''));
  // (his poses still turn the wings: stand him up and watch a wing move)
  await run(`${O}data modify entity ${pet} Sitting set value 0b`); const w0 = await nbt(part('wingr'), 'transformation.left_rotation'); await sleep(2500);
  const w1 = await nbt(part('wingr'), 'transformation.left_rotation');
  ok('...his wings move with his poses (up from his seat)', w0 !== w1 && (await wscale()) > 1, `${w0.slice(0, 40)} -> ${w1.slice(0, 40)}`);
  await run(`${O}tp ${pet} ${X + 0.5} ${Y + 1} ${Z + 3.5}`); await run(`${O}data modify entity ${pet} Sitting set value 1b`); await sleep(1500);
  // ---- the Wraithfire Heart (the gem comes back)
  await run('loot replace entity TestRat hotbar.2 loot bm:items/wraithfire_heart'); A.bars.length = 0;
  await click(2);
  ok('the Wraithfire Heart: he takes it, and gives the Ethereal Gem back', (await has('wraithfire_heart')) === 0 && (await has('ethereal_gem')) === 1);
  ok('...WRAITHFIRE FORM: soul-blue scales, wings still out', /_wf$/.test(await model('body')) && /_wf$/.test(await model('tail1')) && (await wscale()) > 1,
     `${await model('body')} wing ${await wscale()}`);
  ok('...fire won\'t touch him', await wait(2500, async () => /fire_resistance/.test(await nbt(pet, 'active_effects'))));
  // ---- a colour picked while he burns: the form keeps his hide
  await run('scoreboard players set TestRat bm.cosap 1'); await run('execute as TestRat run function bm:p99/apo_now'); await sleep(600);
  ok('a colour picked meanwhile: the form keeps his hide (no "_c1" under it)', /_wf$/.test(await model('body')), await model('body'));
  // ---- sneak + right-click empty-handed: the heart back
  await run('clear TestRat *[minecraft:custom_data~{bm:"ethereal_gem"}]'); A.bars.length = 0;
  await click(5, true);
  ok('sneak + right-click empty-handed: the Wraithfire Heart comes back out', (await has('wraithfire_heart')) === 1);
  ok('...his scales again (in the colour picked), wings away', (await model('body')) === 'bm:apo_body_c1' && await wait(1500, async () => (await wscale()) === 0),
     `${await model('body')} wing ${await wscale()}`);
  await run('scoreboard players set TestRat bm.cosap 0');
  await run(`kill @e[tag=bm.appet]`); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
