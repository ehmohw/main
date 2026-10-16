// 2.74: checkpoint respawn + kept pockets, kit 32/4, Lights Out / Glass Cannon only out on the heist, den names + carpet,
// Sanctuary glow, Skiff parts, bank pieces, temple glow fade, Sky Isles steadiness, chatter toggle
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, qs, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500);
  const want = k => !ONLY || ONLY.test(k);
  const cntIn = async (sel) => +(((await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/) || [0, 0])[1]);
  const items = async (pred) => { const s = await run(`clear TestRat ${pred} 0`); const m = s.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const pos = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const fx = async (id) => new RegExp(`id: "minecraft:${id}"`).test(await run('data get entity TestRat active_effects'));
  const maxhp = async () => +(((await run('attribute TestRat minecraft:max_health get')).match(/is (-?[\d.]+)/) || [0, -1])[1]);
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');

  // ================================================================== THE DEN: no carpet on the floor, one name each
  if (want('den')) {
    for (const t of [4, 3]) {
      await heist('levers', 'a', t); await sleep(1500);
      const GI = await num('scoreboard players get TestRat bm.gvi');
      const L = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},limit=1]`;
      const o = await run(`execute in bm:gutter as ${L} at @s if entity @e[type=minecraft:item,distance=..30]`); const n = /passed/.test(o) ? +((o.match(/Count: (\d+)/) || [0, 1])[1]) : 0;
      ok(`Tier ${t} den built: no loose carpet (or anything) on the floor`, n === 0, `items ${n}`);
    }
    const nv = [];
    for (const tg of ['bm.gvgt', 'bm.gvrec', 'bm.gvtail']) nv.push((await run(`execute in bm:gutter run data get entity @e[type=minecraft:villager,tag=${tg},limit=1] CustomNameVisible`)).replace(/.*data: /, ''));
    ok('Goldtooth, the Recruiter and the Tailor: no always-on name tag (the short-range nameplate shows it)', nv.every(v => v === '0b' || /no elements/.test(v)), nv.join(' '));
    const pl = await cntIn('@e[type=minecraft:text_display,tag=bm.plate,distance=0..]');
    ok('...and their nameplates are there', pl >= 3, `${pl}`);
  }

  // ================================================================== THE KIT: 32 food, 4 paperweights
  if (want('kit')) {
    await run('clear TestRat'); await run('scoreboard players set TestRat bm.kr2 1'); await run('execute as TestRat at @s run function bm:p72/kit/give_2');
    await sleep(300);
    const beef = await items('minecraft:cooked_beef'), pw = await items('*[minecraft:custom_data~{bm:"paperweight"}]');
    ok(`A kit: ${beef} food and ${pw} paperweights`, beef === 32 && pw === 4);
    await run('clear TestRat'); await run('execute as TestRat at @s run function bm:p104/resupply'); await sleep(200);
    ok('Another job tops them back up to 32 and 4', (await items('minecraft:cooked_beef')) === 32 && (await items('*[minecraft:custom_data~{bm:"paperweight"}]')) === 4);
  }

  // ================================================================== KNOCKED OUT: the checkpoint, pockets as they were
  if (want('ko')) {
    await heist('levers', 'a', 2); await begin(); await sleep(1500);
    const GI = await num('scoreboard players get TestRat bm.gvi');
    const I = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
    const q1 = (await qs('levers'))[0];
    await run(`scoreboard players set #gi bm.rng ${GI}`); await at('levers', q1, 'function bm:p70/ctx'); await at('levers', q1, 'function bm:p70/solved'); await sleep(1500);
    const cp = (await run(`execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.gvcp,scores={bm.gvi=${GI}},limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
    const sp = await run('data get entity TestRat respawn');
    const spm = sp.match(/pos: \[I; (-?\d+), (-?\d+), (-?\d+)\]/);
    ok('Room cleared: your spawn moves to its exit door', spm && +spm[1] === Math.floor(cp[0]) && +spm[3] === Math.floor(cp[2]) && /gutter/.test(sp), `${spm && spm.slice(1)} vs ${cp}`);
    // pockets: a kit, some used; armour, off hand, an odd slot, XP
    await run('clear TestRat'); await run('scoreboard players set TestRat bm.gvrole 2'); await run('scoreboard players set TestRat bm.kr2 1');
    await run('execute as TestRat at @s run function bm:p72/kit/give_2'); await sleep(200);
    await run('clear TestRat minecraft:cooked_beef 22');                           // (ate some: 10 left)
    await run('item replace entity TestRat container.20 with minecraft:apple 3');
    await run('item replace entity TestRat armor.head with minecraft:iron_helmet');
    await run('item replace entity TestRat weapon.offhand with minecraft:shield');
    await run('xp set TestRat 5 levels'); await sleep(600);
    const inv0 = (await run('data get entity TestRat Inventory')).match(/Slot:/g).length;
    const lv0 = await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvlv`);
    await run(`execute in bm:gutter as ${room('levers', q1)} at @s run tp TestRat ~ ~ ~`); await sleep(500);
    const dp = await pos();
    A.chats.length = 0;
    await run('kill TestRat'); await sleep(3500);
    const p = await pos();
    const near = p && Math.abs(p[0] - cp[0]) < 1.5 && Math.abs(p[2] - cp[2]) < 1.5;
    ok('Knocked out: you come to at the checkpoint (not the den)', near, `${p} vs ${cp}`);
    const inv1 = ((await run('data get entity TestRat Inventory')).match(/Slot:/g) || []).length;
    ok(`...every slot as it was (${inv1} of ${inv0})`, inv1 === inv0);
    ok('...the apples still in slot 20', /apple/.test(await run('data get entity TestRat Inventory[{Slot:20b}]')));
    ok('...helmet on, shield in the off hand', /passed/.test(await run('execute if items entity TestRat armor.head minecraft:iron_helmet')) && /passed/.test(await run('execute if items entity TestRat weapon.offhand minecraft:shield')));
    ok('...the food you ate stays eaten (10, no fresh kit)', (await items('minecraft:cooked_beef')) === 10, `${await items('minecraft:cooked_beef')}`);
    ok('...XP kept', (await num('xp query TestRat levels')) === 5);
    const fo = await run(`execute in bm:gutter positioned ${dp[0]} ${dp[1]} ${dp[2]} if entity @e[type=minecraft:item,distance=..6]`); const fl = /passed/.test(fo) ? 1 : 0;
    ok('...nothing left lying where you fell', fl === 0, `${fl}`);
    ok('...a try is still lost', (await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvlv`)) === lv0 - 1);
    ok('...and the message says so', A.chats.some(c => /where your crew last cleared the way/.test(c)), A.chats.slice(-3).join(' | ').slice(0, 200));
    // the void: same spot, nothing touched
    await run(`execute in bm:gutter as ${room('levers', q1)} at @s run tp TestRat ~ ~ ~`); await sleep(300);
    await run('execute as TestRat at @s run function bm:p112/void_ko'); await sleep(500);
    const p2 = await pos();
    ok('The void hauls you to the checkpoint too, pockets untouched', p2 && Math.abs(p2[0] - cp[0]) < 1.5 && (await items('minecraft:cooked_beef')) === 10);
    // ================================================================== LIGHTS OUT / GLASS CANNON
    await run('effect clear TestRat');
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvmod 17`);           // (Lights Out + Glass Cannon)
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvst 1`);
    await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(2500);
    const m1 = await maxhp();
    ok('Lights Out + Glass Cannon, before BEGIN, in the den: no darkness, full health', !(await fx('darkness')) && m1 >= 20, `max ${m1}`);
    A.chats.length = 0;
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvst 2`); await sleep(2500);
    ok('BEGIN: Glass Cannon halves your health - and says so (not the difficulty)', (await maxhp()) <= m1 / 2 + 0.5 && A.chats.some(c => /Glass Cannon/.test(c) && /not the difficulty/.test(c)), `max ${await maxhp()}`);
    ok('Heist on, but you\'re in the den: still no darkness', !(await fx('darkness')));
    await run(`execute in bm:gutter as ${room('levers', q1)} at @s run tp TestRat ~ ~ ~`); await sleep(2500);
    ok('Out on the heist: Lights Out\'s darkness', await fx('darkness'));
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvst 4`); await sleep(4500);
    ok('The vault pays out: health back, the darkness lifts', (await maxhp()) >= 20 && !(await fx('darkness')), `max ${await maxhp()}`);
  }

  // ================================================================== THE SANCTUARY
  if (want('sanct')) {
    await heist('levers', 'a', 2); await begin(); await sleep(1000);
    const q = (await qs('levers'))[1];
    await at('levers', q, 'function bm:p90/sanctum/init'); await at('levers', q, 'tag @s add bm.gvr_sanctum'); await at('levers', q, 'tag @s remove bm.gvr_levers');
    const S = `@e[type=minecraft:marker,tag=bm.gvr_sanctum,scores={bm.gvq=${q}},limit=1]`;
    const glow = async () => { const o = (await run(`execute in bm:gutter as ${S} at @s run data get entity @e[type=minecraft:item_display,tag=bm.gvshd,limit=1,sort=nearest] Glowing`)); return (/no elements|nothing/i.test(o) || o.trim() === '') ? '0b' : o.replace(/.*data: /, ''); };
    const vr = (await run(`execute in bm:gutter as ${S} at @s run data get entity @e[type=minecraft:item_display,tag=bm.gvshd,limit=1,sort=nearest] view_range`)).replace(/.*data: /, '');
    ok('The shrines: no glow while nobody\'s there, and a short view range', (await glow()) === '0b' && /0\.4/.test(vr), `${await glow()} ${vr}`);
    await run(`execute in bm:gutter as ${S} at @s run tp TestRat ~ ~ ~`); await sleep(2500);
    ok('Walk in: they glow', (await glow()) === '1b');
    await run(`execute in bm:gutter as ${S} at @s run tp TestRat ~-18 ~ ~`); await sleep(2500);
    ok('Walk off: the glow goes', (await glow()) === '0b');
  }

  // ================================================================== SKIFF PARTS
  if (want('skiff')) {
    await run('execute in bm:gutter run data modify block -200 64 -197 Items set value []');
    await run('execute as TestRat at @s run function bm:admin/skiff_haul');
    const it = await run('execute in bm:gutter run data get block -200 64 -197 Items');
    ok('An alien heist\'s 5%: a Vorn Skiff part goes into the haul', /skiff_(hull|dome|coil|core|emitter|reactor)/.test(it), it.slice(0, 160));
    await run('execute in bm:gutter run data modify block -200 64 -197 Items set value []');
    const hl = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p70/haul.mcfunction', 'utf8');
    ok('...rolled in every won heist\'s haul, only for an alien heist, at 5%', /if score #gn bm.rng matches 3 store result score #r bm.rng run random value 1\.\.100/.test(hl) && /if score #r bm.rng matches \.\.5 run function bm:p120\/skiff/.test(hl));
  }

  // ================================================================== THE GUTTER BANK
  if (want('bank')) {
    await run('clear TestRat'); for (const o of ['bm.gbc', 'bm.gbm', 'bm.gbt']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('loot give TestRat loot bm:items/gutter_medallion'); await run('loot give TestRat loot bm:items/gutter_medallion'); await run('loot give TestRat loot bm:items/gutter_trophy');
    await run('give TestRat minecraft:stone 1');
    for (let i = 0; i < 5; i++) await run('loot give TestRat loot bm:items/gutter_coin');
    await run('scoreboard players set TestRat bm.menu 7802'); await run('execute as TestRat at @s run function bm:p80/bank_deposit'); await sleep(300);
    const c = await num('scoreboard players get TestRat bm.gbc'), m = await num('scoreboard players get TestRat bm.gbm'), t = await num('scoreboard players get TestRat bm.gbt');
    ok(`Deposit: 2 Medallions and a Trophy kept as pieces (${m}, ${t}); all told ${c} coins`, m === 2 && t === 1 && c === 165);
    const ui = await run('data get storage bm:ui bk2');
    ok('...the account page shows them, and 5 loose coins', /gm: 2/.test(ui) && /gt: 1/.test(ui) && /c: 5[,}]/.test(ui), ui.slice(0, 200));
    // (taking pieces out, one currency at a time: t154)
    await run('scoreboard players remove TestRat bm.gbc 40'); await run('execute as TestRat run function bm:p80/init_me');
    const c2 = await num('scoreboard players get TestRat bm.gbc'), m2 = await num('scoreboard players get TestRat bm.gbm'), t2 = await num('scoreboard players get TestRat bm.gbt');
    ok(`Spend 40 from the bank (165 = a Trophy, 2 Medallions + 5): broken into change only as far as needed (${c2} = ${t2} T, ${m2} M + ${c2 - 128 * t2 - 16 * m2})`, c2 === 125 && t2 === 0 && m2 === 7);
  }

  // ================================================================== THE TEMPLE'S STONES
  if (want('temple')) {
    await run('execute in bm:gutter run summon minecraft:block_display 0 70 0 {Tags:["bm.gvtb","bm.t120"],block_state:{Name:"minecraft:mossy_cobblestone"},Glowing:1b}');
    await sleep(2000);
    ok('A solved temple\'s stones glow for now...', /1b/.test(await run('execute in bm:gutter run data get entity @e[type=minecraft:block_display,tag=bm.t120,limit=1] Glowing')));
    await sleep(10500);
    ok('...and 10 seconds on, the glow is gone', !/1b/.test(await run('execute in bm:gutter run data get entity @e[type=minecraft:block_display,tag=bm.t120,limit=1] Glowing')));
    await run('execute in bm:gutter run kill @e[type=minecraft:block_display,tag=bm.t120]');
  }

  // ================================================================== THE SKY ISLES
  if (want('isles')) {
    await heist('isles', 'a', 3); await begin(); await sleep(1000);
    const q = (await qs('isles'))[0];
    await at('isles', q, `tp TestRat ${rel(12, 5, 12)}`); await sleep(3000);
    const kr = +(((await run('attribute TestRat minecraft:explosion_knockback_resistance get')).match(/is (-?[\d.]+)/) || [0, -1])[1]);
    ok(`On the islands with the guards out: steadier against gusts (${kr})`, kr >= 0.6);
    await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5'); await sleep(1000);
    const kr2 = +(((await run('attribute TestRat minecraft:explosion_knockback_resistance get')).match(/is (-?[\d.]+)/) || [0, -1])[1]);
    ok('...and back to normal off them', kr2 === 0, `${kr2}`);
  }

  // ================================================================== CHATTER
  if (want('chat')) {
    await run('tag TestRat add bm.leown'); await run('scoreboard players set TestRat bm.menu 7950');
    await run('execute as TestRat run function bm:p119/hush'); A.chats.length = 0;
    await run('execute as TestRat at @s run function bm:p96/banter_1'); await sleep(500);
    ok('Chatter off: Celi and Leo\'s banter doesn\'t reach you', !A.chats.some(c => /Try to keep up, sir knight/.test(c)));
    await run('execute as TestRat run function bm:p119/hush'); A.chats.length = 0;
    await run('execute as TestRat at @s run function bm:p96/banter_1'); await sleep(500);
    ok('Chatter on: it does', A.chats.some(c => /Try to keep up, sir knight/.test(c)));
    await run('tag TestRat remove bm.leown');
  }

  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  // (leave it as found: off every heist, with what it carried - p70/home is the way out a heist's own exits take)
  await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home');
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
