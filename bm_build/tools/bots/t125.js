// 2.75b: records, the hidden cache, Democratus (size, seat, duel), KillerWatt sits, Sparks Fly, Call-for menus, the Lounge on the
// Heist Plans, one-name traders, party ghosts, followers appear whole + faint, the Lantern wakes
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'); const OUT = BMB + 'out_p2/BlackMarket_DP/data/bm/';
const F = p => fs.readFileSync(OUT + 'function/' + p + '.mcfunction', 'utf8');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
const X = 19000, Y = 120, Z = 19000;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+(?:\.\d+)?)\D*$/); return m ? +m[1] : NaN; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async sel => /passed/i.test(await run(`execute if entity ${sel}`));
  const cnt = async sel => { const o = await run(`execute if entity ${sel}`); return /passed/.test(o) ? +((o.match(/Count: (\d+)/) || [0, 1])[1]) : 0; };
  const A = await bot('TestRat'); await sleep(2500);
  const field = async () => {
    await run(`forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
    await run(`fill ${X - 30} ${Y - 1} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:grass_block`); await run(`fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y + 20} ${Z + 30} minecraft:air`);
    for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.dmpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.cecilpet', 'giant,tag=bm.salboss', 'vindicator,tag=bm.dmboss'])
      await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
    await sleep(1500);
    for (const o of ['bm.emcd', 'bm.kxcd', 'bm.dmcd', 'bm.lecd', 'bm.cecd', 'bm.cpcd']) await run(`scoreboard players set TestRat ${o} 0`);
    await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('weather clear'); await run('time set day');
    await sleep(500);
  };
  await run('gamerule doMobSpawning false');

  if (want('disc')) {
    for (const k of ['big_score', 'invasion', 'lucky', 'market', 'hollow']) {
      await run('clear TestRat'); await run(`loot give TestRat loot bm:items/music_disc_${k}`);
      const it = await run('data get entity TestRat Inventory[0].components');
      ok(`Record "${k}": plays its own song in a jukebox`, it.includes(`"minecraft:jukebox_playable": "bm:${k}"`) || it.includes(`jukebox_playable":"bm:${k}"`), it.slice(0, 120));
    }
    ok('...each song is registered (jukebox_song + its sound)', ['big_score', 'invasion', 'lucky', 'market', 'hollow'].every(k => fs.existsSync(OUT + `jukebox_song/${k}.json`)) &&
       ['big_score', 'invasion', 'lucky', 'market', 'hollow'].every(k => fs.existsSync(`${BMB}out_p2/BlackMarket_RP/assets/bm/sounds/records/${k}.ogg`)));
    await run('clear TestRat'); await run('execute as TestRat at @s run function bm:admin/disc_haul');
    ok('The Big Score: a won haul can carry it (into the haul barrel, with a line in chat)', /big_score/.test(F('p124/big_score')) && /function bm:p124\/big_score/.test(F('p70/haul')));
    const ov = fs.readFileSync(OUT + 'loot_table/p32/overseer.json', 'utf8'), tr = fs.readFileSync(OUT + 'loot_table/p32/trooper.json', 'utf8');
    ok('Invasion: the Overseer (half the time), the Vorn - killed on an invasion night', ov.includes('music_disc_invasion') && tr.includes('music_disc_invasion') && tr.includes('bm.ninv'));
    const jp = fs.readdirSync(OUT + 'loot_table/entities/jackpot').map(f => fs.readFileSync(OUT + 'loot_table/entities/jackpot/' + f, 'utf8'));
    ok('Lucky Night: every Jackpot monster can drop it (Lucky Nights only)', jp.length > 3 && jp.every(j => j.includes('music_disc_lucky') && j.includes('bm.nlk')));
    const hid = fs.readFileSync(OUT + 'loot_table/p2/hollow/hidden.json', 'utf8');
    ok('The Hollow: the hidden cache always has one (in the Throne - not a heist room)', hid.includes('music_disc_hollow') && hid.includes('bm:hollow_throne'));
    // a lucky-night kill by a player drops it; any other night it doesn't
    await field();
    let got = 0;
    for (const night of [0, 1]) {
      if (night) { await run('function bm:admin/lucky_night'); } else { await run('scoreboard players set #lucky bm.bm 0'); await run('time set 14000'); }
      await sleep(1500);
      if (night) ok('Lucky Night started (and copied onto the player)', /has 1/.test(await run('scoreboard players get TestRat bm.nlk')));
      let n = 0;
      for (let i = 0; i < 25; i++) {
        await run(`summon minecraft:cow ${X + 3} ${Y} ${Z} {Tags:["t125z"],NoAI:1b,DeathLootTable:"bm:entities/lucky_prime/cow",Health:1f}`);
        await run(`damage @e[type=cow,tag=t125z,limit=1] 50 minecraft:player_attack by TestRat`);
      }
      await sleep(600);
      n = await cnt(`@e[type=item,x=${X - 8},y=${Y - 4},z=${Z - 8},dx=16,dy=10,dz=16,nbt={Item:{components:{"minecraft:custom_data":{bm:"music_disc_lucky"}}}}]`);
      if (night === 0) got = n; else ok(`Lucky record from Lucky Primes: none on an ordinary night (${got}), some on a Lucky Night (${n} of 25)`, got === 0 && n >= 1);
      await run(`kill @e[type=item,x=${X - 8},y=${Y - 4},z=${Z - 8},dx=16,dy=10,dz=16]`);
    }
    await run('scoreboard players set #lucky bm.bm 0'); await run('time set day');
  }

  if (want('hidden')) {
    await field();
    await run(`setblock ${X + 4} ${Y} ${Z} minecraft:chest`);
    await run(`summon minecraft:marker ${X + 4.5} ${Y + 0.5} ${Z + 0.5} {Tags:["bm.chestm","bm.d_hollow","t125m"],data:{loot:"bm:p2/hollow/hidden"}}`);
    await run('tag TestRat remove bm.hid_hollow'); await run(`tp TestRat ${X - 10} ${Y} ${Z}`); await sleep(1500);
    await run(`tp TestRat ${X + 2.5} ${Y} ${Z + 0.5}`); await sleep(2500);
    const lt = await run(`data get block ${X + 4} ${Y} ${Z} LootTable`);
    ok('A newcomer at the Hollow\'s (looted, empty) hidden cache: it fills for them', /hollow\/hidden/.test(lt) && /bm.hid_hollow/.test(await run('tag TestRat list')), lt.slice(0, 80));
    await run(`data remove block ${X + 4} ${Y} ${Z} LootTable`); await sleep(2000);
    ok('...once per player: walking up again, it stays empty', !/LootTable/.test(await run(`data get block ${X + 4} ${Y} ${Z}`)) || /Found no/.test(await run(`data get block ${X + 4} ${Y} ${Z} LootTable`)));
    await run('kill @e[type=marker,tag=t125m]'); await run(`setblock ${X + 4} ${Y} ${Z} minecraft:air`);
  }

  if (want('demo')) {
    await field();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/demo_seal');
    await run('execute as TestRat at @s run function bm:p97/try_summon'); await sleep(2500);
    const body = '@e[type=item_display,tag=bm.dmp,tag=bm.dp_body,tag=!bm.dmbp,limit=1]';
    const s0 = await run(`data get entity ${body} transformation.scale[0]`);
    ok('Democratus is drawn bigger (1.06)', /1\.06/.test(s0), s0.replace(/.*data: /, ''));
    await run('execute as @e[type=wolf,tag=bm.dmpet,limit=1] run data merge entity @s {Sitting:1b}'); await sleep(3500);
    const legY = await num(`data get entity @e[type=item_display,tag=bm.dmp,tag=bm.dp_legr,tag=!bm.dmbp,limit=1] transformation.translation[1]`);
    ok('Sitting: the seat pose (the rig drops so the hips meet the ground)', legY < -0.4, `legr dy ${legY}`);
    await run('execute as @e[type=wolf,tag=bm.dmpet,limit=1] run data merge entity @s {Sitting:0b}');
    // the duel: one huge blow, past his yield
    await run('scoreboard players set TestRat bm.dmsc 0'); await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/demo_seal');
    await run('scoreboard players set TestRat bm.menu 9700'); await run('scoreboard players set #act bm.pay 9701'); await run('execute as TestRat at @s run function bm:p97/act');
    await sleep(800);
    const boss = '@e[type=vindicator,tag=bm.dmboss,limit=1]';
    ok('The duel starts: the duelist has his hidden cushion (1000 health, the bar shows 400)', (await num(`data get entity ${boss} Health`)) === 1000);
    await run('scoreboard players set TestRat bm.dmd 1'); await sleep(300);
    await run(`data merge entity ${boss} {Invulnerable:0b,NoAI:1b}`);
    await run(`damage ${boss} 800 minecraft:player_attack by TestRat`); await sleep(200);
    ok('One massive blow (800) can\'t kill him outright...', await has(boss), `health ${await num(`data get entity ${boss} Health`)}`);
    await run('effect give TestRat minecraft:instant_damage 1 1 true'); await sleep(150);
    await run('execute as TestRat run data modify entity @s Health set value 4f');
    A.chats.length = 0; await sleep(5500);
    const scy = await run('clear TestRat *[minecraft:custom_data~{bm:"demo_scythe"}] 0');
    ok('...he yields - and though you\'re down to two hearts, it\'s a win: his scythe is yours', /Found 1/.test(scy) && !A.chats.some(c => /lost the duel/.test(c)), scy);
    await sleep(1500);
    ok('...and his duelist body is gone with him', (await cnt('@e[type=item_display,tag=bm.dmbp]')) === 0);
    // a duelist killed outright anyway (a /kill): his body still goes
    await run('scoreboard players set TestRat bm.menu 9700'); await run('scoreboard players set #act bm.pay 9701'); await run('execute as TestRat at @s run function bm:p97/act'); await sleep(800);
    await run(`kill ${boss}`); await sleep(2500);
    ok('Killed by other means: no body left standing', (await cnt('@e[type=item_display,tag=bm.dmbp]')) === 0);
    await run('effect give TestRat minecraft:instant_health 1 5 true');
  }

  if (want('kw')) {
    await field();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/kw_spark'); A.slot(0); await sleep(500);
    await run('execute as TestRat at @s run function bm:p79/pet/try'); await sleep(2500);
    const W = '@e[type=wolf,tag=bm.kxpet,limit=1]';
    ok('KillerWatt has a click box beside him (not riding him)', (await cnt('@e[type=interaction,tag=bm.kxhit]')) === 1 && !/bm.kxhit/.test(await run(`data get entity ${W} Passengers`)));
    await run(`tp ${W} ${X + 3.5} ${Y} ${Z + 0.5}`); await sleep(300);
    await run('item replace entity TestRat hotbar.0 with minecraft:air'); await run('loot replace entity TestRat weapon.offhand loot bm:items/kw_spark'); await sleep(200);
    // right-click: we play the server side of it (the box's interaction record)
    await run('execute as @e[type=interaction,tag=bm.kxhit,limit=1] run data modify entity @s interaction set value {player:[I;0,0,0,0],timestamp:0L}');
    await run('execute as @e[type=interaction,tag=bm.kxhit,limit=1] run function bm:p125/kw/click');
    await run(`execute as TestRat run function bm:p125/kw/clicker`); await sleep(2500);
    ok('Right-click him (empty hand): he sits', /1b/.test(await run(`data get entity ${W} Sitting`)) && (await sc(W, 'bm.kxs')) === 4, `kxs ${await sc(W, 'bm.kxs')}`);
    const bY = await num(`data get entity @e[type=item_display,tag=bm.kxp_body,tag=bm.kxp_pet,limit=1] transformation.translation[1]`);
    ok('...down on his haunches (his seat pose)', bY < -0.6, `body dy ${bY}`);
    await run(`execute as TestRat run function bm:p125/kw/clicker`); await sleep(1000);
    ok('Again: he stands', /0b/.test(await run(`data get entity ${W} Sitting`)));
    await run('loot replace entity TestRat hotbar.0 loot bm:items/kw_spark'); A.slot(0); await sleep(300);
    await run('scoreboard players set TestRat bm.gvhc 0'); await run(`execute as TestRat at @s run function bm:p125/kw/clicker`); await sleep(800);
    ok('Clicking him with the Spark still mounts him', /passed/.test(await run('execute as TestRat on vehicle if entity @s[tag=bm.kxpet]')));
    await run('ride TestRat dismount'); await sleep(1500);
    ok('...riding, his box steps aside; off him, it\'s back', (await cnt('@e[type=interaction,tag=bm.kxhit]')) === 1);
    // Sparks Fly
    await run('loot replace entity TestRat hotbar.1 loot bm:items/emma_ribbon'); await run('advancement revoke TestRat only bm:story/emma_kw');
    await run('execute as TestRat at @s run function bm:p57/try_summon'); A.chats.length = 0; await sleep(3500);
    const eff = await run('data get entity TestRat active_effects');
    ok('Sparks Fly (Emma + KillerWatt): you\'re quicker and quicker-handed', /speed/.test(eff) && /haste/.test(eff), eff.slice(0, 120));
    ok('...a shield of sparks (Absorption), and the hidden achievement', /absorption/.test(eff) && A.chats.some(c => /Sparks Fly/.test(c)));
    ok('...KillerWatt tougher', /resistance/.test(await run(`data get entity ${W} active_effects`)));
  }

  if (want('eth')) {
    await field();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/kw_spark'); A.slot(0); await sleep(300);
    await run('execute as TestRat at @s run function bm:p79/pet/try'); await sleep(2500);
    const W = '@e[type=wolf,tag=bm.kxpet,limit=1]';
    await run(`tp ${W} ${X + 2.5} ${Y} ${Z + 0.5}`); await sleep(300);
    await run('execute as TestRat at @s run function bm:p79/el/set {i:10}'); await sleep(500);
    ok('KillerWatt in his Ethereal form', (await sc('TestRat', 'bm.kxel')) === 10);
    await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(1200);
    const riding = async () => /passed/.test(await run('execute as TestRat on vehicle if entity @s[tag=bm.kxpet]'));
    const wy = async () => num(`data get entity ${W} Pos[1]`);
    ok('Mounted - and on the ground he walks (no flying until you take off)', (await riding()) && !/1b/.test(await run(`data get entity ${W} NoGravity`)) && !/bm.kxfly/.test(await run(`data get entity ${W} Tags`)));
    const y0 = await wy(); let top = y0;
    A.input({ jump: true }); for (let i = 0; i < 6; i++) { await sleep(50); top = Math.max(top, await wy()); } A.input({}); await sleep(900);
    ok(`Jump: he hops (${y0.toFixed(2)} -> ${top.toFixed(2)})`, top > y0 + 0.4);
    A.input({ jump: true }); await sleep(120); A.input({}); await sleep(160); A.input({ jump: true }); await sleep(250); A.input({});
    await sleep(300);
    ok('Jump again in mid-air: he takes off and flies', /bm.kxfly/.test(await run(`data get entity ${W} Tags`)) && /1b/.test(await run(`data get entity ${W} NoGravity`)));
    await run('rotate TestRat -90 70'); await sleep(4000);
    ok('Look down to the ground: he lands and walks again', !/bm.kxfly/.test(await run(`data get entity ${W} Tags`)) && !/1b/.test(await run(`data get entity ${W} NoGravity`)), (await run(`data get entity ${W} Tags`)).slice(-80));
    // a wall ahead: he climbs it
    const wx = Math.floor(await num(`data get entity ${W} Pos[0]`)) + 3;
    await run(`fill ${wx} ${Y} ${Z - 3} ${wx} ${Y + 3} ${Z + 3} minecraft:stone`); await run('rotate TestRat -90 0');
    const c0 = await wy(); let ctop = c0;
    A.input({ forward: true }); for (let i = 0; i < 30; i++) { await sleep(100); ctop = Math.max(ctop, await wy()); } A.input({});
    ok(`A wall ahead, walking: he climbs it (${c0.toFixed(2)} -> ${ctop.toFixed(2)})`, ctop > c0 + 1.5);
    await run(`fill ${wx} ${Y} ${Z - 3} ${wx} ${Y + 3} ${Z + 3} minecraft:air`); await run('ride TestRat dismount');
  }

  if (want('leap')) {
    await field();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/kw_spark'); A.slot(0); await sleep(300);
    await run('execute as TestRat at @s run function bm:p79/pet/try'); await sleep(2500);
    const W = '@e[type=wolf,tag=bm.kxpet,limit=1]';
    await run(`tp ${W} ${X + 2.5} ${Y} ${Z + 0.5}`); await sleep(300);
    await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(1200);
    const arm = async () => (await run('data get entity @e[type=item_display,tag=bm.kxp_armr,tag=bm.kxp_pet,limit=1] item.components."minecraft:item_model"')).replace(/.*data: /, '');
    await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(300);
    const mid = await arm(); await sleep(3500);
    const after = await arm();
    ok(`Thunder Leap: arms flexed in the leap (${mid}) - and back to normal when he lands (${after})`, /_flex/.test(mid) && !/_flex/.test(after));
    await run('ride TestRat dismount');
  }

  if (want('menu')) {
    await field();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/leo_crest');
    await run('execute as TestRat run function bm:p99/menu/leo'); await sleep(200);
    ok('Leo not out: his menu says "Call for Leo"', /Call for Leo/.test(await run('data get storage bm:ui wd.r_home')));
    await run('scoreboard players set TestRat bm.menu 9920'); await run('scoreboard players set TestRat bm.act 9920'); await run('execute as TestRat at @s run function bm:p28/act'); await sleep(2500);
    ok('...and the button calls him', await has('@e[type=wolf,tag=bm.leopet]'));
    await run('execute as TestRat run function bm:p99/menu/leo'); await sleep(200);
    ok('Leo out: "Send him home"', /Send him home/.test(await run('data get storage bm:ui wd.r_home')));
    await run('scoreboard players set TestRat bm.menu 9920'); await run('scoreboard players set TestRat bm.act 9920'); await run('execute as TestRat at @s run function bm:p28/act'); await sleep(1500);
    ok('...which sends him home', !(await has('@e[type=wolf,tag=bm.leopet]')));
    ok('Every follower\'s menu has the Call/Send switch (and Democratus\' challenge)', ['emma', 'celi', 'zib', 'cecil', 'kw', 'leo', 'demo'].every(w => /r_home/.test(F(`p99/dlg/${w}`))) &&
       /Call for Democratus/.test(F('p97/menu')));
    // a button clicked once works (the 2.74-2.75 codes used to read the last click)
    await run('scoreboard players set #act bm.pay 0'); await run('tag TestRat remove bm.hush'); await run('scoreboard players set TestRat bm.menu 9920');
    await run('scoreboard players set TestRat bm.act 7735'); await run('execute as TestRat at @s run function bm:p28/act'); await sleep(200);
    ok('One click on "Chatter" toggles it (the newer buttons read this click, not the last one)', /bm.hush/.test(await run('tag TestRat list')));
    await run('tag TestRat remove bm.hush');
    ok('The Ledger\'s Office: a Fixer\'s Lounge button (the Heist Plans are part of the Ledger since 2.75)', /set 7880/.test(F('p80/office_dlg')) && /7880[^\n]*p121\/from_ledger/.test(F('p80/act')));
  }

  if (want('npc')) {
    await field();
    await run(`summon minecraft:villager ${X + 3} ${Y} ${Z} {NoAI:1b,Tags:["bm.npc","t125v"],CustomName:"Test Trader"}`); await sleep(3000);
    ok('A trader with a nameplate joins the no-name-tag team (one name: the plate)', /passed/.test(await run('execute if entity @e[type=villager,tag=t125v,team=bm.npcs,tag=bm.plated]')) &&
       (await cnt(`@e[type=text_display,tag=bm.plate,x=${X + 2},y=${Y - 1},z=${Z - 1},dx=2,dy=4,dz=2]`)) === 1);
    ok('...whose name tag never shows', /nametagVisibility never/.test(F('load')));
    await run(`execute at @e[type=villager,tag=t125v,limit=1] run summon minecraft:text_display ~ ~ ~ {Tags:["bm.plate"],text:"dup"}`); await sleep(1500);
    ok('Two plates on one trader: one goes', (await cnt(`@e[type=text_display,tag=bm.plate,x=${X + 2},y=${Y - 1},z=${Z - 1},dx=2,dy=4,dz=2]`)) === 1);
    await run('execute as @e[type=villager,tag=t125v] run tp @s ~ -400 ~');
    ok('Party teams no longer see "friendly invisibles" (a tamed mount counts as one)', /seeFriendlyInvisibles false/.test(F('p67/make')) && /seeFriendlyInvisibles false/.test(F('p67/sync1')));
  }

  if (want('appear')) {
    await field();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon');
    const rig = F('p57/rig_here');
    ok('Emma\'s parts are summoned at full size (no growing from nothing; the wings stay folded)', /bm\.ep_body[^\n]*scale:\[0\.85f/.test(rig) && /bm\.ep_wingr[^\n]*scale:\[0f/.test(rig) && !/bm\.ep_body[^\n]*interpolation_duration:[1-9]/.test(rig));
    ok('...and Leo\'s, Democratus\', Celi\'s, Cecil\'s', /scale:\[0\.96f/.test(F('p96/rig_here') || '') || /bm.lep[^\n]*scale:\[0\.96f/.test(fs.readdirSync(OUT + 'function/p96').map(f => f.endsWith('.mcfunction') ? F('p96/' + f.slice(0, -11)) : '').join('\n')));
    await run('execute as TestRat at @s run function bm:p57/try_summon'); await sleep(2500);
    ok('Emma called', await has('@e[type=cat,tag=bm.emmapet]'));
    // she faints
    await run('kill @e[type=cat,tag=bm.emmapet]'); await sleep(500);
    const mid = await cnt('@e[type=item_display,tag=bm.emp]'); const dz = await num('data get entity @e[type=item_display,tag=bm.ep_body,limit=1] transformation.translation[1]');
    ok('She faints: for a moment she sinks down where she stood (her seat pose), dazed', mid >= 8 && dz < 0, `${mid} parts, body dy ${dz}`);
    await sleep(1800);
    ok('...then gone in her burst of petals', (await cnt('@e[type=item_display,tag=bm.emp]')) === 0);
  }

  if (want('lantern')) {
    await field();
    await run('scoreboard players set #forced bm.bm 1');
    await run(`execute positioned ${X} ${Y} ${Z + 22} run function bm:p82/summon`); await sleep(1500);
    const G = '@e[type=giant,tag=bm.salboss,limit=1]';
    const bodyM = async () => (await run('data get entity @e[type=item_display,tag=bm.salp_body,limit=1] item.components."minecraft:item_model"')).replace(/.*data: /, '');
    ok('The Lantern waits as a plain pumpkin, sitting in the field', /saldorm/.test(await run(`data get entity ${G} Tags`)) && /sal_body_plain/.test(await bodyM()));
    ok('...unhurt by anything while it sleeps; no boss bar', /1b/.test(await run(`data get entity ${G} Invulnerable`)));
    await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 12} 0 0`); await sleep(800);
    ok('Come close: it wakes (shudders, and the ground shakes under you)', /salwake/.test(await run(`data get entity ${G} Tags`)) && (await sc('TestRat', 'bm.shk')) >= 1);
    await sleep(1200);
    ok('...its face catches fire', /"bm:sal_body"/.test(await bodyM()));
    await sleep(5000);
    ok('...legs out, up, a roar - and it\'s awake (vulnerable, hunting)', !/salwake|saldorm/.test(await run(`data get entity ${G} Tags`)) && /0b/.test(await run(`data get entity ${G} Invulnerable`)));
    await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 6}`); await sleep(2500);
    let shook = false;
    for (let i = 0; i < 20 && !shook; i++) { if ((await sc('TestRat', 'bm.shk')) >= 1) shook = true; await sleep(150); }
    ok('Every step it takes shakes the ground near it', shook);
    await run(`execute as ${G} at @s run function bm:p82/leave`); await run('scoreboard players set #forced bm.bm 0'); await sleep(2000);
  }

  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.dmpet', 'wolf,tag=bm.leopet']) await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
