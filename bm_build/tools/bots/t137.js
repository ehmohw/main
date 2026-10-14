// 2.77b: the Wraithfire Heart forged on the ground, as a regular (non-op) player: an Ethereal Gem set down, a Scorching Heart
// set down beside it (and, the second time, the other way round) - both with the items themselves. They rise, glide together,
// circle closer and closer and merge: a Wraithfire Heart drops, the bot picks it up, Burning Blue is earned. Pearlman doesn't
// offer the fusion any more. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const epos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const use = async (C, slot, sneak = false) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(200); } C.use(); await sleep(400); C.release(); if (sneak) { C.input({}); await sleep(150); } };
  const dist = (a, b) => a && b ? Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]) : 1e9;
  const X = 16080, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  const HT = '@e[type=minecraft:item_display,tag=bm.wfh2,limit=1]', GM = '@e[type=minecraft:item_display,tag=bm.wfg,limit=1]';

  // (the bot stands at the middle; first it faces south and looks down at the floor in front, then west)
  const face = async (yaw) => { await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} ${yaw} 60`); await wait(2000, async () => A.pos && Math.abs(A.pos.y - (Y + 1)) < 0.1, 100); await sleep(300); };
  for (const order of [['gem', 'heart'], ['heart', 'gem']]) {
    const tag = order.join(' then ');
    await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run('clear TestRat');
    await run('advancement revoke TestRat only bm:story/wraithfire');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/ethereal_gem'); await run('loot replace entity TestRat hotbar.1 loot bm:items/scorching_heart');
    A.chats.length = 0; A.bars.length = 0;
    for (const [k, what] of order.entries()) {
      await face(k === 0 ? 0 : 90);
      await use(A, what === 'gem' ? 0 : 1, true);
      await sleep(400);
      if (k === 0) ok(`[${tag}] the ${what} is set down`, what === 'gem' ? (await cnt(`@e[type=minecraft:item_display,tag=bm.eshr,x=${X},y=${Y},z=${Z},distance=..6]`)) === 1
                                                                     : (await cnt(`@e[type=minecraft:interaction,tag=bm.hearth,x=${X},y=${Y},z=${Z},distance=..6]`)) === 1,
                      A.bars.slice(-2).join(' / ').slice(0, 160));
    }
    // (the forging: no one says so - it simply begins)
    ok(`[${tag}] ...and beside it, the other: the forging begins`, await wait(2500, async () => (await cnt('@e[type=minecraft:marker,tag=bm.wfm]')) === 1),
       A.bars.slice(-2).join(' / ').slice(0, 160));
    ok(`[${tag}] "The heart's fire leans toward the gem's cold light..."`, /leans toward the gem/.test(A.chats.join(' ')));
    ok(`[${tag}] both are taken into it (no shrine, no Hearthfire left to pick up)`, (await cnt('@e[type=minecraft:item_display,tag=bm.eshr]')) === 0 &&
       (await cnt('@e[type=minecraft:interaction,tag=bm.hearth]')) === 0 && (await cnt('@e[type=minecraft:interaction,tag=bm.eshr_hit]')) === 0);
    // (the circling runs from about 1.6 s to 4.6 s after the forging starts: sample inside it)
    await sleep(1700);
    const h1 = await epos(HT), g1 = await epos(GM);
    ok(`[${tag}] they rise and glide together`, h1 && g1 && h1[1] > Y + 2 && g1[1] > Y + 2, `heart ${JSON.stringify(h1)} gem ${JSON.stringify(g1)}`);
    await sleep(400);
    const h2 = await epos(HT), g2 = await epos(GM);
    await sleep(1100);
    const h3 = await epos(HT), g3 = await epos(GM);
    ok(`[${tag}] ...circling one another, closer and closer`, h2 && h3 && dist(h2, h3) > 0.05 && dist(h2, g2) > dist(h3, g3),
       `apart ${dist(h2, g2).toFixed(2)} -> ${dist(h3, g3).toFixed(2)}`);
    ok(`[${tag}] "...and drinks it. The flame is turning blue."`, /turning blue/.test(A.chats.join(' ')));
    // (the merge: the heart drops; the bot is a block away and picks it up)
    ok(`[${tag}] they merge - a Wraithfire Heart, and the bot picks it up`, await wait(6000, async () => (await has('TestRat', 'wraithfire_heart')) === 1), A.chats.slice(-2).join(' | ').slice(0, 200));
    ok(`[${tag}] "...burns blue. A Wraithfire Heart."`, /burns blue/.test(A.chats.join(' ')));
    ok(`[${tag}] Burning Blue is earned`, /passed/i.test(await run(`${O}execute if entity @a[name=TestRat,advancements={bm:story/wraithfire=true}]`)));
    ok(`[${tag}] nothing is left behind (no marker, no gem, no heart, no light block)`, (await cnt('@e[type=minecraft:marker,tag=bm.wfm]')) === 0 &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.wfh2]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.wfg]')) === 0 &&
       !/passed/i.test(await run(`${O}execute if block ${X} ${Y + 1} ${Z} minecraft:light`)) && !/passed/i.test(await run(`${O}execute if block ${X + 1} ${Y + 1} ${Z} minecraft:light`)) &&
       !/passed/i.test(await run(`${O}execute if block ${X - 1} ${Y + 1} ${Z} minecraft:light`)) && !/passed/i.test(await run(`${O}execute if block ${X} ${Y + 1} ${Z + 1} minecraft:light`)));
    ok(`[${tag}] ...and both ingredients are used up`, (await has('TestRat', 'ethereal_gem')) === 0 && (await has('TestRat', 'scorching_heart')) === 0);
  }

  // ---- far apart, they don't fuse; and the heart's lore says how
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/ethereal_gem'); await run('loot replace entity TestRat hotbar.1 loot bm:items/scorching_heart');
  ok('the Scorching Heart\'s lore: "Set down beside an Ethereal Gem, they fuse."', /Set down beside an Ethereal Gem/.test(await run('data get entity TestRat Inventory[{Slot:1b}].components')));
  await face(0); await use(A, 0, true); await sleep(300);
  await run(`${O}tp TestRat ${X + 6.5} ${Y + 1} ${Z + 0.5} 90 60`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - (X + 6.5)) < 0.1, 100); await sleep(300);
  await use(A, 1, true); await sleep(1500);
  ok('six blocks apart: no forging (the gem sings, the Hearthfire burns)', (await cnt('@e[type=minecraft:marker,tag=bm.wfm]')) === 0 &&
     (await cnt('@e[type=minecraft:item_display,tag=bm.eshr]')) === 1 && (await cnt('@e[type=minecraft:interaction,tag=bm.hearth]')) === 1);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);

  // ---- Pearlman: the fusion is gone from his trades
  await run(`${O}execute positioned ${X + 3.5} ${Y + 1} ${Z + 3.5} run function bm:p60/pm/spawn`); await sleep(800);
  const offers = await run(`${O}data get entity @e[type=minecraft:villager,limit=1,sort=nearest,x=${X + 3.5},y=${Y + 1},z=${Z + 3.5}] Offers`);
  ok('Pearlman still trades (he came)', /Recipes/.test(offers), offers.slice(0, 120));
  ok('...but no longer fuses a Scorching Heart and an Ethereal Gem', !/wraithfire_heart/.test(offers));
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
