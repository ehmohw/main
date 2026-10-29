// 2.99a: THE REX MOUNTS and THE MOUNTS PAGE (phase249) as a regular (non-op) player. rcon sets the stage (a flat yard, a test
// husk, a lava pool in the Nether, the items in hand); the bot plays:
//   rex      the Atomic Whistle used: the rex comes (23 parts, sat); right-clicked: on its back; forward: it walks, sprint: it
//            runs; the whistle used looking ahead and down at a husk: breath_0 (the plates charge), the beam - the husk is hurt;
//            sneak: off its back (it sits); sneak + use: home (host and rig gone)
//   egg      a Rex Egg dropped (Q) into Nether lava: it floats and counts; its 60 s run out (rcon moves the count to the end):
//            it bursts - the whistle is the thrower's, "THE ATOMIC REX HATCHES"
//   wheel    the whistle in the off hand, the Partner Wheel used: it goes on; the wheel's Mounts button: the Mounts page; "Call
//            your Atomic Rex": it comes - and stays out with the whistle only on the wheel; "Send ... home"; "Take it back off"
//   skiff    a Vorn Skiff Key onto the Mounts page the same way; "Call your Vorn Skiff": its ghast and hull appear, you aboard;
//            the wheel used aboard fires its laser; off it, left parked, it folds away and the page offers the call again
//   node t321.js [rex|egg|wheel|skiff]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const O = 'execute in minecraft:overworld run ', N = 'execute in minecraft:the_nether run ';
const YX = 18600, YY = 100, YZ = 16000;                 // the yard (overworld) and the pool (the Nether)
const HOST = '@e[type=minecraft:horse,tag=bm.rxh';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o, D = '') => +((await run(`${D}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async (D, sel) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const num = async (D, cmd) => +(((await run(D + cmd)).match(/(-?[\d.]+)[fdb]?$/) || [0, NaN])[1]);
  const at = async (D, x, y, z, yaw = 0, pitch = 0) => { await run(`${D}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const uuidOf = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (D, sel) => { const u = await uuidOf(D, sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const riding = async (tag) => /passed/i.test(await run(`execute as TestRat on vehicle if entity @s[tag=${tag}]`));
  const useItem = async (ms = 350) => { A.use(); await sleep(ms); A.release(); };
  const yard = async () => {
    // (the yard's chunks held first: the bot may come in far off, and a fill in a chunk nobody has loaded fails - "not loaded")
    await run(`${O}forceload add ${YX - 16} ${YZ - 16} ${YX + 16} ${YZ + 20}`); await sleep(2000);
    await run(`${O}fill ${YX - 16} ${YY} ${YZ - 16} ${YX + 16} ${YY + 12} ${YZ + 20} minecraft:air`);
    await run(`${O}fill ${YX - 16} ${YY - 1} ${YZ - 16} ${YX + 16} ${YY - 1} ${YZ + 20} minecraft:stone`);
    await run(`${O}kill @e[type=!minecraft:player,distance=..40,x=${YX},y=${YY},z=${YZ}]`);
  };
  const mine = (k) => `${HOST},tag=bm.rx${k === 'atomic' ? 'a' : 'm'},distance=..40,x=${YX},y=${YY},z=${YZ}]`;
  const parts = async () => cnt(O, `@e[type=minecraft:item_display,tag=bm.rxp,distance=..40,x=${YX},y=${YY},z=${YZ}]`);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('function bm:admin/rex/home');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players reset TestRat bm.rxrc'); await run('scoreboard players reset TestRat bm.rxcb');
  await run('time set day'); await run('weather clear');

  if (on('rex')) {
    await yard(); await at(O, YX + 0.5, YY, YZ + 0.5, 0, 0);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/atomic_whistle'); A.slot(0); await sleep(400);
    A.bars.length = 0; await useItem();
    ok('the whistle used: the Atomic Rex comes (its host, 23 parts)', await wait(4000, async () => (await cnt(O, mine('atomic'))) === 1 && (await parts()) === 23),
       `${await cnt(O, mine('atomic'))} host, ${await parts()} parts`);
    ok('...beside you, sat (nobody aboard: gait -1, stock-still)', (await sc(`${mine('atomic').slice(0, -1)},limit=1]`, 'bm.rxw')) === -1 &&
       (await num(O, `attribute ${mine('atomic').slice(0, -1)},limit=1] minecraft:movement_speed base get`)) === 0);
    ok('...never glowing (an invisible host)', (await cnt(O, `${mine('atomic').slice(0, -1)},nbt={Glowing:1b}]`)) === 0);
    const hp = await pos(O, `${mine('atomic').slice(0, -1)},limit=1]`);
    const e = await entOf(O, `${mine('atomic').slice(0, -1)},limit=1]`);
    if (e) A.interact(e.entityId); await sleep(800);
    ok('right-clicked: you climb on its back', await riding('bm.rxh'));
    A.ride(0, 0, { forward: true }); await sleep(1500);
    ok('...forward: it walks (gait 1, pace 0.33)', (await sc(`${mine('atomic').slice(0, -1)},limit=1]`, 'bm.rxw')) === 1 &&
       Math.abs((await num(O, `attribute ${mine('atomic').slice(0, -1)},limit=1] minecraft:movement_speed base get`)) - 0.33) < 0.001);
    A._in = { forward: true, sprint: true }; await sleep(1200);
    ok('...sprinting: it runs (gait 2, pace 0.45)', (await sc(`${mine('atomic').slice(0, -1)},limit=1]`, 'bm.rxw')) === 2);
    A._in = {}; await sleep(800);
    // (a husk ahead, on the ground: look 38 degrees down from the saddle - the beam leaves the mouth along your look)
    const hz = hp[2] + 3.77 + 6;
    await run(`${O}summon minecraft:husk ${hp[0]} ${YY} ${hz} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t321z"],Health:200f,attributes:[{id:"minecraft:max_health",base:200d}]}`);
    A._pitch = 38; A.pos.yaw = 0; A.pos.pitch = 38; await sleep(400);
    await useItem();
    await sleep(500);
    ok('used, riding, looking ahead: the breath charges (breath state, the tail\'s plates lit)', (await sc(`${mine('atomic').slice(0, -1)},limit=1]`, 'bm.rxs')) === 2 &&
       /_charged/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.rxp_tail4,distance=..40,x=${YX},y=${YY},z=${YZ},limit=1] item.components."minecraft:item_model"`)));
    await sleep(3200);
    const zh = await num(O, `data get entity @e[type=minecraft:husk,tag=bm.t321z,limit=1] Health`);
    ok('...the beam: the husk in front is hurt', zh < 199, `husk health ${zh}`);
    ok('...and the breath recharges (8 s on its cooldown)', (await sc('TestRat', 'bm.rxcb')) >= 4);
    A._pitch = 0; A._in = { shift: true }; await sleep(800); A._in = {}; await sleep(300); A.unride(); A.stand(); await sleep(600);
    ok('sneak: off its back - and it sits again', !(await riding('bm.rxh')) && await wait(3000, async () => (await sc(`${mine('atomic').slice(0, -1)},limit=1]`, 'bm.rxw')) === -1));
    A.input({ shift: true }); await sleep(200); await useItem(); await sleep(300); A.input({}); await sleep(800);
    ok('sneak + use: home it goes (no host, no rig)', (await cnt(O, mine('atomic'))) === 0 && (await parts()) === 0);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t321z]`);
  }

  if (on('egg')) {
    await run('clear TestRat'); await run('tag TestRat remove bm.rxhatch'); await run('advancement revoke TestRat only bm:story/rex_atomic');
    // (the pool's chunks held first, as the yard's: it used to pass only on a stray force-load left from an older run)
    await run(`${N}forceload add ${YX - 6} ${YZ - 6} ${YX + 10} ${YZ + 6}`); await sleep(2000);
    await run(`${N}fill ${YX - 6} ${YY} ${YZ - 6} ${YX + 10} ${YY + 6} ${YZ + 6} minecraft:air`);
    await run(`${N}fill ${YX - 6} ${YY - 2} ${YZ - 6} ${YX + 10} ${YY - 1} ${YZ + 6} minecraft:obsidian`);
    await run(`${N}fill ${YX + 2} ${YY - 1} ${YZ - 2} ${YX + 6} ${YY - 1} ${YZ + 3} minecraft:lava`);
    await at(N, YX + 0.5, YY, YZ + 0.5, -90, 20); await run(`${N}kill @e[type=minecraft:item,distance=..16,x=${YX},y=${YY},z=${YZ}]`);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/rex_egg'); A.slot(0); await sleep(400);
    A.drop(); await sleep(2500);
    const EGG = `@e[type=minecraft:item,distance=..12,x=${YX},y=${YY},z=${YZ}]`, EGG1 = EGG.slice(0, -1) + ',limit=1]';
    ok('the egg dropped (Q) into Nether lava: it floats there, counting', await wait(5000, async () => (await sc(EGG1, 'bm.rxl', N)) >= 1) &&
       /passed/i.test(await run(`${N}execute at ${EGG1} if block ~ ~ ~ minecraft:lava`) + (await run(`${N}execute at ${EGG1} if block ~ ~-0.3 ~ minecraft:lava`))),
       String(await sc(EGG1, 'bm.rxl', N)));
    await run(`${N}execute as ${EGG} if items entity @s contents *[minecraft:custom_data~{bm:"rex_egg"}] run scoreboard players set @s bm.rxl 58`);
    A.titles.length = 0;
    ok('...its time run out: it bursts - the whistle is yours', await wait(5000, async () => (await has('atomic_whistle')) === 1));
    ok('..."THE ATOMIC REX HATCHES", tagged, the advancement', A.titles.some(t => /ATOMIC REX HATCHES/.test(t)) &&
       /passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.rxhatch]')) && /passed|true/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/rex_atomic=true}]')),
       A.titles.join(' / '));
    await run(`${N}fill ${YX + 1} ${YY - 1} ${YZ - 2} ${YX + 5} ${YY - 1} ${YZ + 3} minecraft:obsidian`);
  }

  // (the wheel: open it, its Mounts button, a button on the Mounts page)
  const openWheel = async () => { A.slot(1); await sleep(200); return A.useWait(1500); };
  const mounts = async () => { if (!(await openWheel())) return false; const b = await A.press(/Mounts/); return !!(b && b.next); };

  if (on('wheel')) {
    await yard(); await at(O, YX + 0.5, YY, YZ + 0.5, 0, 0); await run('clear TestRat');
    await run('scoreboard players reset TestRat bm.pwrx'); await run('scoreboard players reset TestRat bm.pwsk');
    await run('loot replace entity TestRat hotbar.1 loot bm:items/partner_wheel');
    await run('loot replace entity TestRat weapon.offhand loot bm:items/atomic_whistle'); await sleep(300);
    await openWheel(); await sleep(500);
    ok('the whistle in the off hand, the wheel used: it goes on (off hand empty)', (await sc('TestRat', 'bm.pwrx')) === 1 && (await has('atomic_whistle')) === 0);
    ok('the wheel: a Mounts button; pressed - the Mounts page', await mounts() && A.buttons().some(b => /Call your Atomic Rex/.test(b.label)) &&
       A.buttons().some(b => /Take it back off/.test(b.label)) && A.buttons().some(b => /Partners/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await A.press(/Call your Atomic Rex/); await sleep(800);
    ok('"Call your Atomic Rex": it comes', await wait(4000, async () => (await cnt(O, mine('atomic'))) === 1));
    await sleep(2500);
    ok('...and stays out - the whistle only on the wheel you carry', (await cnt(O, mine('atomic'))) === 1);
    ok('the page again: "Send your Atomic Rex home"', await mounts() && A.buttons().some(b => /Send your Atomic Rex home/.test(b.label)));
    await A.press(/Send your Atomic Rex home/); await sleep(800);
    ok('...pressed: home it goes', (await cnt(O, mine('atomic'))) === 0 && (await parts()) === 0);
    ok('the page\'s « Partners button goes back to the wheel', await mounts() && !!(await A.press(/Partners/)) && A.buttons().some(b => /Mounts/.test(b.label)));
    await mounts(); await A.press(/Take it back off/); await sleep(800);
    ok('"Take it back off the wheel": the whistle is back in your pack', (await has('atomic_whistle')) === 1 && (await sc('TestRat', 'bm.pwrx')) < 1);
  }

  if (on('skiff')) {
    await yard(); await at(O, YX + 0.5, YY, YZ + 0.5, 0, 0); await run('clear TestRat');
    await run('scoreboard players reset TestRat bm.pwsk');
    await run('loot replace entity TestRat hotbar.1 loot bm:items/partner_wheel');
    await run('loot replace entity TestRat weapon.offhand loot bm:items/skiff_key'); await sleep(300);
    await openWheel(); await sleep(500);
    ok('a Vorn Skiff Key in the off hand, the wheel used: on the Mounts page', (await sc('TestRat', 'bm.pwsk')) === 1 && (await has('skiff_key')) === 0);
    ok('...the page: "Call your Vorn Skiff"', await mounts() && A.buttons().some(b => /Call your Vorn Skiff/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await A.press(/Call your Vorn Skiff/); await sleep(1200);
    const SK = `@e[type=minecraft:happy_ghast,tag=bm.skiff,distance=..20,x=${YX},y=${YY},z=${YZ}]`;
    ok('...pressed: the skiff comes - its ghast and its hull - and you are aboard', (await cnt(O, SK)) === 1 &&
       (await cnt(O, `@e[type=minecraft:item_display,tag=bm.skdisp,distance=..20,x=${YX},y=${YY},z=${YZ}]`)) === 1 && await riding('bm.skiff'));
    A.ride(0, 0, {}); await sleep(300); A.pos.yaw = 0; A.pos.pitch = 0; await run('scoreboard players set TestRat bm.skl 0');
    A.slot(1); await sleep(200); A.use();
    ok('aboard, the wheel used: the skiff\'s laser fires (as its key would)', await wait(400, async () => (await sc('TestRat', 'bm.skl')) >= 1, 30));
    await sleep(300); A.release();
    A._in = { shift: true }; await sleep(800); A._in = {}; A.unride(); A.stand(); await sleep(2000);
    // (a parked skiff folds away by itself after a few seconds with nobody aboard - phase35's watch; the page then offers the call again)
    ok('...off it, left parked: it folds away by itself, ghast and hull', await wait(8000, async () => (await cnt(O, SK)) === 0 &&
       (await cnt(O, `@e[type=minecraft:item_display,tag=bm.skdisp,distance=..20,x=${YX},y=${YY},z=${YZ}]`)) === 0, 500));
    await mounts(); await sleep(400);
    ok('...and the page offers "Call your Vorn Skiff" again', A.buttons().some(b => /Call your Vorn Skiff/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await mounts(); await A.press(/Take it back off/); await sleep(800);
    ok('"Take it back off the wheel": the key is back', (await has('skiff_key')) === 1);
  }

  await run('function bm:admin/rex/home'); await run('clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  await run('effect clear TestRat');      // (its Resistance and Fire Resistance off again - later tests must be hurt)
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
