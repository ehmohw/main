// 2.77: Tullius, as a regular (non-op) player - the ghost ship found where the world made it (a cold ocean), swum up to and
// climbed aboard by its ladder (Leo along, called with his crest); the captain rising, his attacks (the harpoon hooks the bot and
// reels it in to the blunderbuss), his crew, the frost, the sea (put overboard, he swims and leaps back aboard); the bot's own
// blows through his hitbox, the win and its drops; his blunderbuss and harpoon in the bot's hands; then the Doubloon: his rig,
// sitting, his menu, his fights (the harpoon pull), the water, fainting; and his Raid Contract. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const epos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const hp = async (sel) => +(((await run(`${O}data get entity ${sel} Health`)).match(/(-?[\d.]+)f?\s*$/) || [0, NaN])[1]);
  const block = async (x, y, z) => (await run(`${O}execute if block ${x} ${y} ${z} minecraft:air`)).match(/passed/i) ? 'air' :
    ((await run(`${O}execute if block ${x} ${y} ${z} minecraft:ladder`)).match(/passed/i) ? 'ladder' : 'other');
  const use = async (C, slot, sneak = false) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(200); } C.use(); await sleep(400); C.release(); if (sneak) { C.input({}); await sleep(150); } };
  const dist = (a, b) => a && b ? Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]) : 1e9;
  const A = await bot('TestRat'); await sleep(2500);
  A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // (a real client moves itself, a small step a tick: swimming, climbing, stepping off a ladder)
  const step = (x, y, z, on) => { A.pos.x = x; A.pos.y = y; A.pos.z = z; A.write('position', { x, y, z, flags: { onGround: on, hasHorizontalCollision: false } }); A.write('tick_end', {}); };
  const glide = async (x, y, z, d = 0.15, on = false) => { A.unstand();
    for (let k = 0; k < 600; k++) { const dx = x - A.pos.x, dy = y - A.pos.y, dz = z - A.pos.z, n = Math.hypot(dx, dy, dz); if (n < 0.02) break;
      const t = Math.min(d, n); step(A.pos.x + dx / n * t, A.pos.y + dy / n * t, A.pos.z + dz / n * t, on); await sleep(50); }
    step(x, y, z, on); await sleep(50); };
  const reset = async () => {
    for (const t of ['bm.tupet', 'bm.leopet']) await run(`${O}kill @e[tag=${t}]`);
    for (const o of ['bm.tucd', 'bm.lecd', 'bm.tugc', 'bm.tucl', 'bm.tuk']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('clear TestRat'); await run('effect clear TestRat');
  };
  await reset();
  const tough = async () => { await run('attribute TestRat minecraft:max_health base set 200'); await run('effect give TestRat minecraft:instant_health 1 20 true');
    await run('effect give TestRat minecraft:resistance 900 2 true'); await run('effect give TestRat minecraft:regeneration 900 2 true'); };
  let deaths = 0; A.on('update_health', p => { if (p.health <= 0) deaths++; });
  await tough();
  const boss = '@e[type=minecraft:husk,tag=bm.tuboss,limit=1]';
  let X = null, Z = null, DY = 67;           // (the seed's column; the deck is y 67 when the sea's top is 62)

  if (want('ship') || want('fight')) {
    // ================================================================== 1. the ship: out in the cold sea, built where the world put her
    const loc = await run(`${O}locate structure bm:tul_ship`);
    const m = loc.match(/\[(-?\d+), [^,]+, (-?\d+)\]/);
    ok('a ghost ship lies out in the cold seas (locate)', !!m, loc.slice(0, 120));
    X = +m[1]; Z = +m[2];
    const biome = await run(`${O}locate biome #minecraft:is_ocean`);
    await run(`${O}tp TestRat ${X + 2.5} 63 ${Z - 14.5} 0 0`); await sleep(4000); A.stand();
    ok('...and she rides the swell when you come near (the seed builds her)', await wait(20000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.tuship]')) >= 1),
       `seed left ${await cnt('@e[type=minecraft:marker,tag=bm.tuseed]')}`);
    const shp = await epos('@e[type=minecraft:marker,tag=bm.tuship,sort=nearest,limit=1]');
    X = Math.floor(shp[0]); Z = Math.floor(shp[2]); DY = Math.floor(shp[1]) - 1;
    ok('...her deck over the sea, her captain\'s log on its lectern, a ladder down her side', (await block(X + 2, DY, Z - 5)) === 'ladder' && (await block(X + 2, DY - 5, Z - 5)) === 'ladder' &&
       /lectern/.test(await run(`${O}data get block ${X - 11} ${DY + 1} ${Z + 2} id`)) && (await block(X + 2, DY + 1, Z - 5)) === 'air',
       `ship marker ${shp}`);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.tuboss]`); await run(`${O}scoreboard players set @e[type=minecraft:marker,tag=bm.tuship] bm.tuw 0`);
    ok('the server setting "Tullius needs Leo" is on by default', (await sc('#tulleo', 'bm.cfg')) === 1);
    // (swim to her ladder, climb it, step aboard - alone)
    await run(`${O}tp TestRat ${X + 2.5} ${DY - 4.4} ${Z - 9.5} 0 0`); await sleep(1500);
    A.chats.length = 0; A.bars.length = 0;
    // (a ladder's plate is solid: a climber rests against it, mid-block)
    await glide(X + 2.5, DY - 4.4, Z - 4.5, 0.12);
    await glide(X + 2.5, DY + 1.15, Z - 4.5, 0.11);             // (up the ladder - feet just over the deck at the top)
    await glide(X + 2.5, DY + 1.15, Z - 3.5, 0.12);             // (forward, over it)
    await glide(X + 2.5, DY + 1.0, Z - 3.5, 0.1, true); A.stand();     // (and down onto it)
    ok('swim to her ladder, climb it, step aboard', dist(await epos('TestRat'), [X + 2.5, DY + 1, Z - 3.5]) < 0.8, JSON.stringify(await epos('TestRat')));
    await sleep(3500);
    ok('alone on her deck: no captain - the deck creaks ("Her captain waits for an old rival: bring Leo.")', !(await cnt(boss)) && /bring Leo/.test(A.bars.join(' ')),
       A.bars.slice(-1).join(''));
    // (Leo, called with his own crest, there on the deck)
    await run('loot replace entity TestRat hotbar.0 loot bm:items/leo_crest');
    await use(A, 0);
    ok('Leo answers his crest', await wait(4000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1));
    ok('with Leo at your side, her captain comes up out of the sea (host + 9 parts)', await wait(5000, async () => (await cnt(boss)) === 1 &&
                                                                                      (await cnt('@e[type=minecraft:item_display,tag=bm.tub]')) === 9),
       `boss ${await cnt(boss)} parts ${await cnt('@e[type=minecraft:item_display,tag=bm.tub]')}`);
    ok('...and knows Leo ("Still playing the knight?" / "I thought you went down with the ship.")', await wait(5000, async () => /Still playing the knight/.test(A.chats.join(' ')) &&
                                                                                                        /went down with the ship/.test(A.chats.join(' '))),
       A.chats.slice(-3).join(' | ').slice(0, 240));
    const bossTop = (await epos(boss)) || [0, 0, 0];
    ok('...he comes down off the quarterdeck in one bound, onto the deck in front of you', await wait(9000, async () => { const b = await epos(boss); return b && b[1] > DY + 0.5 && b[1] < DY + 2 && dist(b, await epos('TestRat')) < 6; }),
       `from ${bossTop} to ${await epos(boss)}`);
  }

  if (want('ship') || want('fight')) {
    // ================================================================== 2. the fight
    if (!(await cnt(boss))) { ok('(no captain to fight)', false); }
    ok('the intro ends: he fights (AI on, hurtable)', await wait(8000, async () => !/1b/.test(await nbt(boss, 'NoAI')) && !/1b/.test(await nbt(boss, 'Invulnerable'))));
    await run(`${O}kill @e[type=minecraft:wolf,tag=bm.leopet]`);            // (from here the thresholds are the test's own)
    await run('item replace entity TestRat hotbar.4 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]');
    await tough();
    const mx = +(((await run(`${O}attribute ${boss} minecraft:max_health get`)).match(/([\d.]+)\s*$/) || [0, 420])[1]);
    const hold = async (lo, to) => { const h = await hp(boss); if (h < mx * lo) await run(`${O}data modify entity ${boss} Health set value ${Math.round(mx * to)}f`); };
    const deck = (dx, dz) => [X + dx, DY + 1, Z + dz];
    const seen = new Set(); let lowest = 999, hooked = false, pointBlank = false;
    A.bars.length = 0; A.chats.length = 0;
    for (let k = 0; k < 160; k++) {
      await hold(0.75, 0.9);
      const a = await sc(boss, 'bm.tuatk'); if (a > 0) seen.add(a);
      if (/HOOKED/.test(A.bars.join(' '))) hooked = true;
      if (/Point\. Blank\./.test(A.chats.join(' '))) pointBlank = true;
      // (now close, now off down the deck - so he has a reason for each of his weapons)
      const b = await epos(boss);
      if (b && b[1] > DY - 1 && k % 30 === 0) {
        let p = [b[0], DY + 1, b[2] + 2];
        if ((k / 30) % 2 === 1) p = [deck(-6, -3), deck(-6, 3), deck(9, -2), deck(9, 2)].sort((u, v) => dist(v, b) - dist(u, b))[0];
        await run(`${O}tp TestRat ${p[0]} ${p[1]} ${p[2]}`); }
      lowest = Math.min(lowest, await hp('TestRat'));
      await sleep(250);
    }
    ok('phase 1: he fights with the harpoon thrust, the blunderbuss, the harpoon throw', [1, 2, 3].filter(a => seen.has(a)).length >= 2, `seen ${[...seen].join(',')}`);
    ok('...his blows land (the bot was hurt)', lowest < 190, `lowest ${lowest}`);
    ok('...the harpoon hooks the bot ("HOOKED!") and reels it in', hooked, A.bars.filter(b => /HOOK/.test(b)).slice(-1).join(''));
    ok('...to the blunderbuss, point-blank', pointBlank);
    // (the bot's own blows, on his hitbox)
    await run(`${O}data modify entity ${boss} Health set value ${Math.round(mx * 0.9)}f`);
    A.slot(4); await sleep(300);
    let dealt = 0;
    for (let k = 0; k < 4; k++) {
      const b = await epos(boss); await run(`${O}tp TestRat ${b[0]} ${b[1]} ${b[2] + 1.6} 180 0`); await sleep(250);
      const box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.bhit_tu,limit=1]');
      const h0 = await hp(boss); if (box) A.attack(box.entityId); await sleep(150); const h1 = await hp(boss); if (h1 < h0) dealt += h0 - h1;
      await sleep(650);
    }
    ok('the bot\'s sword on his hitbox hurts him (the relay)', dealt > 10, `dealt ${dealt.toFixed(1)}`);
    // (three-fifths: all hands)
    A.chats.length = 0;
    await run(`${O}data modify entity ${boss} Health set value ${Math.round(mx * 0.58)}f`);
    let crew = 0;
    ok('at three-fifths: "All hands! Repel boarders!" - his frostbitten crew', await wait(7000, async () => (crew = Math.max(crew, await cnt('@e[type=minecraft:stray,tag=bm.tucrew]'))) >= 3) &&
       /All hands/.test(A.chats.join(' ')), `crew ${crew}`);
    await sleep(1500); await run(`${O}kill @e[type=minecraft:stray,tag=bm.tucrew]`);
    // (half: the frost takes him)
    await run(`${O}data modify entity ${boss} Health set value ${Math.round(mx * 0.45)}f`);
    ok('at half: THE FROST TAKES HIM (phase 2)', await wait(9000, async () => (await sc(boss, 'bm.tuph')) === 2), `tuph ${await sc(boss, 'bm.tuph')}`);
    await wait(3000, async () => (await sc(boss, 'bm.tuatk')) !== 8);
    ok('...his harpoon ices over', await wait(3000, async () => /tu_harpoon_ice/.test(await nbt('@e[type=minecraft:item_display,tag=bm.tub,tag=bm.tup_harpoon,limit=1]', 'item'))));
    const seen2 = new Set(); let spikes = false;
    for (let k = 0; k < 160; k++) {
      await hold(0.25, 0.4);
      const a = await sc(boss, 'bm.tuatk'); if (a > 0) seen2.add(a);
      if (await cnt('@e[type=minecraft:block_display,tag=bm.tuspike]')) spikes = true;
      const b = await epos(boss), me = await epos('TestRat');
      if (b && b[1] > DY - 1 && dist(b, me) > 6) await run(`${O}tp TestRat ${b[0]} ${b[1]} ${b[2] + 2.5}`);
      await sleep(250);
    }
    ok('phase 2: the ice nova, the harpoon slam, the dive', [4, 5, 10].filter(a => seen2.has(a)).length >= 2, `seen ${[...seen2].join(',')}`);
    ok('...spikes of ice burst up round him', spikes);
    // (the sea: overboard, he swims and leaps back aboard)
    await wait(5000, async () => (await sc(boss, 'bm.tuatk')) === 0);
    await run(`${O}tp TestRat ${X + 2.5} ${DY + 1} ${Z - 3.5}`); await sleep(400);
    // (open water beside her - she can lie by an iceberg, and he won't swim in packed ice)
    let ob = [2.5, -11.5];
    for (const [dx, dz] of [[2.5, -11.5], [2.5, 11.5], [-6.5, -11.5], [8.5, -11.5], [-6.5, 11.5], [8.5, 11.5], [2.5, -14.5], [2.5, 14.5]]) {
      if (/passed/.test(await run(`${O}execute if block ${Math.floor(X + dx)} ${DY - 6} ${Math.floor(Z + dz)} minecraft:water if block ${Math.floor(X + dx)} ${DY - 5} ${Math.floor(Z + dz)} minecraft:water`))) { ob = [dx, dz]; break; }
    }
    // (watched from the moment he's in: he can be back aboard within a second and a half)
    await run(`${O}tp ${boss} ${X + ob[0]} ${DY - 6} ${Z + ob[1]}`);
    let sw = null, leapt = false;
    for (let i = 0; i < 6; i++) { const b = await epos(boss); if (b && b[1] < DY - 2) sw = b; if ((await sc(boss, 'bm.tuatk')) === 7) leapt = true; if (sw) break; await sleep(150); }
    ok('put overboard, he is in the water (swimming)', !!sw, JSON.stringify(sw || await epos(boss)) + ` at ${ob}`);
    ok('...and he leaps back aboard at you', await wait(14000, async () => { const a = await sc(boss, 'bm.tuatk'); if (a === 7) leapt = true; const b = await epos(boss);
                                                                          return leapt && b && b[1] >= DY + 0.5 && Math.abs(b[2] - Z) < 6.5; }),
       `leap ${leapt} at ${JSON.stringify(await epos(boss))} atk ${await sc(boss, 'bm.tuatk')} ph ${await sc(boss, 'bm.tuph')} tuc ${await sc(boss, 'bm.tuc')} ${await run(`${O}execute as ${boss} at @s run data get block ~ ~1.6 ~`)} ${await run(`${O}execute as ${boss} at @s if block ~ ~1.6 ~ minecraft:water`)} ${await run(`${O}data get entity ${boss} NoAI`)}`);
    // (the end: the bot lands the last blow)
    await wait(4000, async () => (await sc(boss, 'bm.tuatk')) === 0);
    await run(`${O}data modify entity ${boss} Health set value 4f`);
    A.chats.length = 0;
    for (let k = 0; k < 8 && (await cnt(boss)); k++) {
      const b = await epos(boss); await run(`${O}tp TestRat ${b[0]} ${b[1]} ${b[2] + 1.4} 180 0`); await sleep(250);
      const box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.bhit_tu,limit=1]'); if (box) A.attack(box.entityId); await sleep(700);
    }
    ok('the bot\'s blow brings him down', await wait(4000, async () => !(await cnt(boss))));
    ok('TULLIUS IS BEATEN - "Well fought... I will sail with you."', await wait(5000, async () => /Well fought/.test(A.chats.join(' ')) && /beaten on his ghost ship/.test(A.chats.join(' '))),
       A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('the drops: the Doubloon, the Frostbite Blunderbuss, his Harpoon', (await has('TestRat', 'tul_coin')) === 1 && (await has('TestRat', 'tul_blunderbuss')) === 1 && (await has('TestRat', 'tul_harpoon')) === 1);
    ok('...and the hoard (medallions)', (await has('TestRat', 'medallion')) >= 3);
    ok('his rig kneels and fades away', await wait(6000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.tub]'))));
    await run(`${O}tp TestRat ${X + 8.5} ${DY + 1} ${Z + 0.5}`); await sleep(2500);
    ok('...and he won\'t come up again today (no captain on boarding again)', !(await cnt(boss)) && (await sc('@e[type=minecraft:marker,tag=bm.tuship,limit=1]', 'bm.tuw')) === 2);
    // (the setting off - an op's choice: he rises for anyone. staging: a day has passed)
    await run('scoreboard players set #tulleo bm.cfg 0'); await run(`${O}scoreboard players set @e[type=minecraft:marker,tag=bm.tuship] bm.tuw 0`);
    await run(`${O}kill @e[type=minecraft:wolf,tag=bm.leopet]`);
    await run(`${O}tp TestRat ${X + 2.5} ${DY + 1} ${Z - 20.5}`); await sleep(1500); await run(`${O}tp TestRat ${X + 8.5} ${DY + 1} ${Z + 0.5}`);
    ok('with "Tullius needs Leo" off, he rises for anyone', await wait(5000, async () => (await cnt(boss)) === 1));
    await run(`${O}execute as @e[type=minecraft:husk,tag=bm.tuboss] at @s run function bm:p132/b/leave`); await run('scoreboard players set #tulleo bm.cfg 1');
  }

  const X2 = 13460, Y2 = 121, Z2 = 13060;
  const arena = async () => {
    await run(`${O}forceload add ${X2 - 32} ${Z2 - 32} ${X2 + 32} ${Z2 + 32}`);
    await run(`${O}fill ${X2 - 20} ${Y2 - 1} ${Z2 - 20} ${X2 + 20} ${Y2 - 1} ${Z2 + 20} minecraft:stone`);
    for (let y = Y2; y < Y2 + 12; y += 6) await run(`${O}fill ${X2 - 20} ${y} ${Z2 - 20} ${X2 + 20} ${y + 5} ${Z2 + 20} minecraft:air`);
    await run(`${O}fill ${X2 + 6} ${Y2 - 4} ${Z2 - 6} ${X2 + 14} ${Y2 - 1} ${Z2 + 6} minecraft:water`);           // (a pool, off to the east)
    await run(`${O}kill @e[type=!minecraft:player,x=${X2},y=${Y2},z=${Z2},distance=..30]`);
  };
  if (want('weapons')) {
    // ================================================================== 3. his weapons, in the bot's hands
    await reset(); await arena();
    await run(`${O}tp TestRat ${X2 + 0.5} ${Y2} ${Z2 + 0.5} 0 0`); await run('gamemode survival TestRat'); await sleep(2500); A.stand();
    await run('loot replace entity TestRat hotbar.1 loot bm:items/tul_blunderbuss');
    await run(`${O}summon minecraft:husk ${X2 + 0.5} ${Y2} ${Z2 + 3.0} {Tags:["bm.t135foe"],NoAI:1b,Health:60f,attributes:[{id:"minecraft:max_health",base:60d}]}`);
    const foe = '@e[type=minecraft:husk,tag=bm.t135foe,limit=1]';
    await sleep(400);
    let f0 = await hp(foe); A.bars.length = 0;
    await use(A, 1);
    let f1 = await hp(foe);
    ok('the Frostbite Blunderbuss: a cone of ice shards (the husk at 2.5 blocks hurt)', f1 < f0 - 10, `husk ${f0} -> ${f1}`);
    ok('...and frost slows what it hits', /slowness/.test(await nbt(foe, 'active_effects')));
    await sleep(300); A.use(); await sleep(300); A.release(); await sleep(300);      // (a new press: 3+ ticks after letting go)
    ok('...1.5 s to reload ("Reloading...")', /Reloading/.test(A.bars.join(' ')) && (await hp(foe)) === f1);
    await sleep(1600);
    await run(`${O}kill ${foe}`);
    // (the harpoon: thrown, it hooks the husk and reels it in)
    await run('loot replace entity TestRat hotbar.2 loot bm:items/tul_harpoon');
    await run(`${O}summon minecraft:husk ${X2 + 0.5} ${Y2} ${Z2 + 9.5} {Tags:["bm.t135foe"],NoAI:1b,Health:60f,attributes:[{id:"minecraft:max_health",base:60d}]}`);
    await sleep(400);
    await run(`${O}tp TestRat ${X2 + 0.5} ${Y2} ${Z2 + 0.5} 0 3`); await sleep(500);
    const d0 = dist(await epos(foe), await epos('TestRat'));
    A.slot(2); await sleep(250); A.use(); await sleep(900); A.release();
    let pulled = false;
    await wait(3000, async () => { const d = dist(await epos(foe), await epos('TestRat')); if (d < d0 - 4) pulled = true; return pulled; }, 100);
    ok('Tullius\'s Harpoon: thrown, it hooks the husk and REELS it in', pulled, `from ${d0.toFixed(1)} to ${dist(await epos(foe), await epos('TestRat')).toFixed(1)}`);
    await run(`${O}kill ${foe}`); await run(`${O}kill @e[type=minecraft:trident]`);
  }

  if (want('pet')) {
    // ================================================================== 4. the Doubloon
    await reset(); await arena(); await run('effect give TestRat minecraft:resistance 600 4 true');
    await run('time set day'); await run('weather clear');      // (a night's events toughen the mobs he's tested against)
    await run(`${O}tp TestRat ${X2 + 0.5} ${Y2} ${Z2 + 0.5} 0 0`); await run('gamemode survival TestRat'); await sleep(2500); A.stand();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/tul_coin');
    await use(A, 0);
    const pet = '@e[type=minecraft:wolf,tag=bm.tupet,limit=1]';
    ok('the Doubloon calls him (host + 9 parts)', await wait(4000, async () => (await cnt(pet)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.tup_pet]')) === 9));
    await sleep(1500);
    const r1 = await nbt('@e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_head,limit=1]', 'transformation.left_rotation'); await sleep(1600);
    const r2 = await nbt('@e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_head,limit=1]', 'transformation.left_rotation');
    ok('he breathes (the idle cycle moves him)', r1 !== r2);
    ok('one eye, a flap of flesh over the other (his head model)', /tu_head/.test(await nbt('@e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_head,limit=1]', 'item')));
    // (sit by right-clicking him)
    await run(`${O}tp ${pet} ${X2 + 0.5} ${Y2} ${Z2 + 2.0}`); await sleep(1200);
    let box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.tuhit,limit=1]');
    A.slot(5); await sleep(200); if (box) A.interact(box.entityId); await sleep(900);
    ok('right-click him: he sits', /1b/.test(await nbt(pet, 'Sitting')), `box ${box ? 'yes' : 'no'}`);
    await sleep(700); if (box) A.interact(box.entityId); await sleep(900);
    ok('again: he stands', !/1b/.test(await nbt(pet, 'Sitting')));
    // (his menu)
    A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(200); const opened = await A.useWait(); A.input({}); await sleep(200);
    ok('sneak + use the Doubloon: his menu (Sit / follow, Send him home)', opened && A.buttons().some(b => /Sit \/ follow/.test(b.label)) && A.buttons().some(b => /Send him home/.test(b.label)),
       A.buttons().map(b => b.label).join(' | '));
    const bs = await A.press(/Sit \/ follow/); await sleep(600);
    ok('"Sit / follow": he sits', bs && /1b/.test(await nbt(pet, 'Sitting')));
    A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(200); await A.useWait(); A.input({}); await sleep(200);
    await A.press(/Sit \/ follow/); await sleep(600);
    // (he fights: up close and at range - the harpoon pull)
    await run(`${O}summon minecraft:husk ${X2 - 3.5} ${Y2} ${Z2 + 2.5} {Tags:["bm.t135foe"],Health:40f,attributes:[{id:"minecraft:max_health",base:40d}]}`);
    const foe = '@e[type=minecraft:husk,tag=bm.t135foe,limit=1]';
    const f0 = await hp(foe);
    await wait(10000, async () => !(await cnt(foe)) || (await hp(foe)) < f0 - 8);
    const f1 = (await cnt(foe)) ? await hp(foe) : 0;
    ok('he fights: the harpoon thrust, the blunderbuss', f1 < f0 - 8, `husk ${f0} -> ${f1}`);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t135foe]`); await sleep(5000);
    await run(`${O}tp ${pet} ${X2 + 0.5} ${Y2} ${Z2 + 0.5}`);
    await run(`${O}summon minecraft:husk ${X2 - 11.5} ${Y2} ${Z2 + 0.5} {Tags:["bm.t135foe"],NoAI:1b,Health:60f,attributes:[{id:"minecraft:max_health",base:60d}]}`);
    await sleep(300);
    const g0 = dist(await epos(foe), await epos(pet));
    let pulled = false;
    await wait(9000, async () => { const d = dist(await epos(foe), await epos(pet)); if (d < g0 - 4) pulled = true; return pulled; }, 150);
    ok('...at range: the harpoon pull drags it in to him', pulled, `from ${g0.toFixed(1)} to ${dist(await epos(foe), await epos(pet)).toFixed(1)}`);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t135foe]`);
    // (the water: he swims; with him, you swim as he does)
    await run(`${O}tp ${pet} ${X2 + 10.5} ${Y2 - 2.5} ${Z2 + 0.5}`);
    ok('in the water he swims (the swim cycle)', await wait(3000, async () => (await sc(pet, 'bm.tus')) === 10), `state ${await sc(pet, 'bm.tus')}`);
    await run(`${O}tp TestRat ${X2 + 8.5} ${Y2 - 2} ${Z2 + 0.5}`); await sleep(2500);
    const fx = await nbt('TestRat', 'active_effects');
    ok('...and in the water beside him, you swim with him (Dolphin\'s Grace, Conduit Power)', /dolphins_grace/.test(fx) && /conduit_power/.test(fx), fx.slice(0, 160));
    await run(`${O}tp TestRat ${X2 + 0.5} ${Y2} ${Z2 + 0.5}`); await sleep(800); A.stand();
    // (send him home)
    A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(200); await A.useWait(); A.input({}); await sleep(200);
    await A.press(/Send him home/); await sleep(900);
    ok('"Send him home": he goes', !(await cnt(pet)) && await wait(3000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.tup_pet]'))));
    // (fainting)
    await use(A, 0); await wait(4000, async () => (await cnt(pet)) === 1); await sleep(1000);
    await run(`${O}kill ${pet}`);
    ok('he faints: his rig dissolves, the Doubloon rests 5 minutes', await wait(4000, async () => (await sc('TestRat', 'bm.tucd')) >= 290 && !(await cnt('@e[type=minecraft:item_display,tag=bm.tup_pet]'))),
       `cd ${await sc('TestRat', 'bm.tucd')}`);
    // (his Raid Contract)
    const fcon = await sc('TestRat', 'bm.fcon'); await run('scoreboard players set TestRat bm.fcon 0');    // (staging: no contracts signed yet)
    await run('loot replace entity TestRat hotbar.3 loot bm:items/fcontract_tul'); A.chats.length = 0;
    await use(A, 3);
    ok('Raid Contract: Tullius - "Signed!"', await wait(2000, async () => /Signed!.*Tullius/.test(A.chats.join(' '))), A.chats.slice(-1).join(''));
    if (!isNaN(fcon)) await run(`scoreboard players set TestRat bm.fcon ${fcon}`);
  }

  console.log(`(the bot died ${deaths} times)`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  await reset(); await run('attribute TestRat minecraft:max_health base set 20');
  R.end(); A.end(); process.exit(0);
})();
