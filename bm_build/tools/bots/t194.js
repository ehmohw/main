// 2.81: THE BLACK MARKET, REBUILT - an old market (the 1.13-2.80 layout, turned a quarter) becomes the new town in place, and
// everything it had still works - as a regular (non-op) player, every step a real packet. rcon sets the stage: the old market
// placed from its 2.80 template (a test fixture, written into the world's generated structures), its traders spawned, a
// follower (a tagged wolf) and a dropped diamond inside, a ladder-shaft marker and a block of its shaft past the tunnel's end.
//   The player walks in: the market is rebuilt - one new marker (bm.m289b), the old one gone; the player moved up to the Lookout,
//   the diamond with them; the follower still there; the shaft untouched (no second one). The new town's blocks, turned like
//   the old market (the clock tower's bell). The traders back - one of each; the installs run again: the gate and back-room
//   ledgers, the Dark Auction's podium, the Gilded Gutter's Teller and Concierge, Fishy's Cabinet, Dennis's and Pistachio's
//   rooms, the slot machines, the Bounty Board, the lectern, the Scrap Bin, the lift button, the ambience emitters.
//   Then as the player: Old Barnaby's trades; his back room (a Regular); /trigger bm.standing; the Bounty Board (no bounty
//   tonight); the Dark Auction's gate (Silver Key) lets you into the hall; the Gilded Gutter's gate (Gold Key) - in, and the
//   Rat Bank's Teller; the Captain's front door (the Rat King's Key) into Rat Gang HQ.
const { bot, rcon, sleep } = require('./lib_resp');
const path = require('path'); const { execSync } = require('child_process');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 300) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';      // (a spot 555 blocks from the nearest natural market)
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  // the old market, turned clockwise once: template block (x, z) lands at world (CX - x?) - read through its marker instead
  const CX = 20000, CY = 30, CZ = -18000;
  const BOX = `x=${CX - 99},y=${CY - 2},z=${CZ - 2},dx=101,dy=36,dz=80`;
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,${BOX}]`;
  const rel = (x, y, z) => `^${+(x - 38.5).toFixed(3)} ^${+(y - 12).toFixed(3)} ^${+(z - 46.5).toFixed(3)}`;
  const at = (cmd) => run(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s run ${cmd}`);
  const atIf = (cond) => passes(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s if ${cond}`);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const click = async (sel, ms = 900) => { const e = await entOf(sel); if (!e) return false; A.interact(e.entityId); await sleep(ms); return true; };
  const ledger = (id) => `@e[type=minecraft:interaction,tag=bm.ledger,scores={bm.lgid=${id}},${BOX},limit=1]`;
  const posOf = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await wait(4000, async () => /unknown|incomplete/i.test(A.chats.join(' ')), 200);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run('tp TestRat 0 120 0'); await sleep(1000);
  await run('scoreboard players set #state bm.auc 0');

  // ---- the stage: the 2.80 market written out as a fixture, placed turned a quarter clockwise
  const SRV = process.env.BM_SRV || path.join(require('os').homedir(), 'bm_srv');
  const fx = path.join(SRV, 'world', 'datapacks', 'BlackMarket_DP', 'data', 'bm', 'structure', 'market_v2.nbt');     // (the test server's copy only: dev.sh puts a clean pack back)
  execSync(`python3 -c "import sys; sys.path.insert(0, '.'); import market2; market2.build().export(sys.argv[1])" "${fx}"`, { cwd: path.join(__dirname, '..', '..') });
  await run('reload'); await sleep(6000);
  await run(`${O}forceload add ${CX - 112} ${CZ - 8} ${CX + 100} ${CZ + 104}`); await sleep(4000);
  await run(`${O}kill @e[type=!minecraft:player,${BOX}]`);
  let pl = ''; for (let t = 0; t < 30; t++) { pl = await run(`${O}place template bm:market_v2 ${CX} ${CY} ${CZ} clockwise_90`); if (!/not loaded/.test(pl)) break; await sleep(2000); }
  ok('the stage: an old (2.80) market placed, turned a quarter', /placed|loaded template/i.test(pl) && (await cnt(MK)) === 1 && !(await passes(`${O}execute if entity ${MK.replace(']', ',tag=bm.m289b]')}`)), pl.slice(0, 80));
  // (the traders spawn from their markers by themselves; only if they haven't yet, spawn them now)
  await wait(8000, async () => (await cnt(`@e[tag=bm.npc_fence,${BOX}]`)) > 0, 500);
  if (!(await cnt(`@e[tag=bm.npc_fence,${BOX}]`))) { await run(`${O}execute as @e[type=minecraft:marker,tag=bm.npc_spawn,${BOX}] at @s run function bm:npc/spawn`); await sleep(800); }
  const oldFence = await cnt(`@e[tag=bm.npc_fence,${BOX}]`);            // (the Fence is a wandering trader)
  // (a player's dog: a tamed wolf owned by TestRat - a bare follower tag without its owner and id would set its rig respawning)
  await at(`summon minecraft:wolf ${rel(38.5, 10, 40.5)} {Tags:["t194pet"],PersistenceRequired:1b,NoAI:1b}`);
  await run(`${O}data modify entity @e[tag=t194pet,limit=1] Owner set from entity TestRat UUID`);
  await at(`summon minecraft:item ${rel(37.5, 10.5, 39.5)} {Item:{id:"minecraft:diamond",count:3},Tags:["t194dia"],PickupDelay:32767s}`);
  await at(`summon minecraft:marker ${rel(38.5, 18, 99.5)} {Tags:["bm.mshaft","bm.msdone","bm.ms74","t194shaft"]}`);
  await at(`setblock ${rel(38.5, 20.5, 100.5)} minecraft:chiseled_stone_bricks`);
  ok('...its traders spawned (the old Fence among them), a follower and a dropped diamond inside, a shaft past the tunnel', oldFence === 1 &&
     (await cnt(`@e[tag=t194pet,${BOX}]`)) === 1 && (await cnt(`@e[tag=t194dia]`)) === 1 && (await cnt('@e[tag=t194shaft]')) === 1, `fence ${oldFence}`);

  // ---- the player walks in: the market is rebuilt
  await run('loot give TestRat loot bm:items/market_key');                 // (a player inside came through the vault door - with the Market Key)
  await run(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s run tp TestRat ${rel(38.5, 10, 40.5)}`); await sleep(500);
  const rebuilt = await wait(30000, async () => passes(`${O}execute if entity ${MK.replace(']', ',tag=bm.m289b]')}`), 500);
  await sleep(2500);
  ok('walked in: the market is rebuilt - one marker, the new one (bm.m289b)', rebuilt && (await cnt(MK)) === 1);
  const p = await posOf(); const lookout = await passes(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s positioned ${rel(38.5, 18, 78.5)} if entity @a[name=TestRat,distance=..3]`);
  ok('the player was moved up to the Lookout, by the vault door', lookout, p && p.map(v => v.toFixed(1)).join(' '));
  ok('...the diamond with them; the follower still where it was', (await passes(`${O}execute as @e[tag=t194dia] at @s if entity @a[name=TestRat,distance=..3]`)) && (await cnt(`@e[tag=t194pet,${BOX}]`)) === 1);
  ok('the ladder shaft untouched: its marker and its block, no second shaft', (await cnt('@e[tag=t194shaft]')) === 1 && (await cnt('@e[type=minecraft:marker,tag=bm.mshaft]')) >= 1 &&
     (await atIf(`block ${rel(38.5, 20.5, 100.5)} minecraft:chiseled_stone_bricks`)) && (await cnt(`@e[type=minecraft:marker,tag=bm.mshaft,${BOX.replace('dx=101', 'dx=104').replace(`x=${CX - 99}`, `x=${CX - 102}`)}]`)) === 1);
  ok('the new town, turned like the old market: the clock tower\'s bell, the Lookout\'s terrace', (await atIf(`block ${rel(46.5, 23.5, 33.5)} minecraft:bell`)) &&
     (await atIf(`block ${rel(38.5, 17.5, 76.5)} #bm:market_floor`)));
  // ---- the traders come back, one of each; the installs run again
  const kinds = ['fence', 'pawn', 'outfitter', 'arms', 'armory', 'chef', 'professor', 'lucky', 'blood', 'captain', 'wizard', 'dock'];
  await wait(20000, async () => { for (const k of kinds) if ((await cnt(`@e[type=minecraft:villager,tag=bm.npc_${k},${BOX}]`)) !== 1) return false; return true; }, 1000);
  const tally = []; for (const k of kinds) tally.push(`${k} ${await cnt(`@e[tag=bm.npc_${k},type=!minecraft:item_display,${BOX}]`)}`);
  ok('the traders are back - one of each (Cecil, Salty Sal and the Captain too)', tally.every(t => / 1$/.test(t)), tally.join(', '));
  await wait(15000, async () => (await cnt(`@e[type=minecraft:interaction,tag=bm.ledger,${BOX}]`)) >= 16, 1000);
  const L = await cnt(`@e[type=minecraft:interaction,tag=bm.ledger,${BOX}]`);
  const lids = []; for (const id of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25, 26]) lids.push(await cnt(ledger(id).replace(',limit=1', '')));
  ok('the ledgers: ten back rooms and six gates, each once (and the Gutter\'s and the podium\'s)', lids.every(n => n === 1), `${L} in all; ${lids.join(' ')}`);
  // (2.81a) every back-room book lies on its trader's counter - a book, not a lectern; on a whole block, nothing on top; the trader beside it
  const onCounter = [];
  const TRADERS = ['fence', 'pawn', 'outfitter', 'arms', 'armory', 'chef', 'professor', 'lucky', 'captain', 'blood'];     // (phase28's TRADER_ORDER: ledger 1..10)
  for (let id = 1; id <= 10; id++) {
    if (!(await passes(`${O}execute as ${ledger(id)} at @s if entity @e[type=minecraft:item_display,tag=bm.lg_book,distance=..0.3] unless block ~ ~-0.5 ~ minecraft:lectern ` +
                       `unless block ~ ~-0.5 ~ #minecraft:slabs unless block ~ ~-0.5 ~ #minecraft:air if block ~ ~ ~ #minecraft:air if block ~ ~1 ~ #minecraft:air ` +
                       `if entity @e[type=!minecraft:item_display,tag=bm.npc_${TRADERS[id - 1]},distance=..3.5]`))) onCounter.push(TRADERS[id - 1]);
  }
  ok('...every back-room book on its trader\'s counter: no lecterns, no slabs, nothing on top, the trader beside it', onCounter.length === 0, `off: ${onCounter.join(' ')}`);
  ok('the Gilded Gutter\'s Teller and Concierge, the Auctioneer', (await cnt(`@e[tag=bm.g_teller,type=minecraft:interaction,${BOX}]`)) + (await cnt(`@e[tag=bm.g_teller,${BOX}]`)) >= 1 &&
     (await cnt(`@e[tag=bm.g_concierge,${BOX}]`)) >= 1 && (await cnt(`@e[tag=bm.auctioneer,${BOX}]`)) >= 1);
  await wait(15000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.cabhall,${BOX}]`)) === 1, 1000);
  ok('Fishy\'s Cabinet (its hall, Fishy at his desk); Dennis and Pistachio in their rooms', (await cnt(`@e[type=minecraft:marker,tag=bm.cabhall,${BOX}]`)) === 1 &&
     (await cnt(`@e[type=minecraft:interaction,tag=bm.fynhit,${BOX}]`)) === 1 && (await cnt(`@e[type=minecraft:marker,tag=bm.dwspot,${BOX}]`)) === 1 && (await cnt(`@e[type=minecraft:marker,tag=bm.psspot,${BOX}]`)) === 1);
  await wait(15000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.slot,${BOX}]`)) === 3, 1000);
  ok('the riverboat\'s three slot machines, the jackpot sign', (await cnt(`@e[type=minecraft:marker,tag=bm.slot,${BOX}]`)) === 3 && (await cnt(`@e[tag=bm.slotd,${BOX}]`)) === 3 && (await cnt(`@e[tag=bm.potd,${BOX}]`)) === 1);
  await wait(15000, async () => (await cnt(`@e[type=minecraft:interaction,tag=bm.bbhit,${BOX}]`)) === 1, 1000);
  ok('the Bounty Board (its notice and hitbox, once), the lectern with the newcomers\' book, the Scrap Bin, the lift button',
     (await cnt(`@e[type=minecraft:interaction,tag=bm.bbhit,${BOX}]`)) === 1 && (await cnt(`@e[tag=bm.bboard,${BOX}]`)) === 1 &&
     (await atIf(`block ${rel(34.5, 18.5, 80.5)} minecraft:lectern[has_book=true]`)) && (await atIf(`block ${rel(33.5, 10.5, 23.5)} minecraft:barrel`)) &&
     (await atIf(`block ${rel(43.5, 18.5, 86.5)} #minecraft:buttons`)));
  ok('the special-night ambience emitters, all seven districts', (await cnt(`@e[type=minecraft:marker,tag=bm.amb,${BOX}]`)) === 7);
  ok('nothing of the old market left over: no stray traders\' models or old neon', (await cnt(`@e[type=minecraft:item_display,tag=bm.rat_sprite,${BOX}]`)) <= 40 &&
     (await cnt(`@e[tag=bm.neon_docks,type=minecraft:text_display,${BOX}]`)) <= 1);

  // ---- as the player: a trader, his back room, standing, the board
  await run('scoreboard players set TestRat bm.stand 4000'); await run('scoreboard players set TestRat bm.tier 4');
  const near = async (x, y, z, yaw = 0) => { await at(`tp TestRat ${rel(x, y, z)} ~${yaw} 0`); await sleep(1200); };
  await near(33.5, 10, 20.5, 90);
  const w0 = A.windows.length;
  await click(`@e[type=minecraft:villager,tag=bm.npc_pawn,${BOX},limit=1]`, 1500);
  ok('Old Barnaby: right-clicked, his trades open', A.windows.length > w0, `${A.windows.length - w0} windows`);
  for (const w of A.windows.slice(w0)) A.close(w.windowId || w.id || 1); await sleep(400);
  const n0 = A.dialogN.length;
  await click(ledger(2), 1200);
  // (the back rooms are registry dialogs: the client is sent the dialog's id, {"dialog": n}, not its text)
  ok('...his back room: the ledger on his counter opens it', A.dialogN.length > n0 && /"dialog":\d+|Back Room/i.test(JSON.stringify(A.dialogN.slice(-1)[0] || '')),
     JSON.stringify(A.dialogN.slice(-1)[0] || '').slice(0, 120));
  const n1 = A.dialogN.length; A.cmd('trigger bm.standing'); await wait(3000, async () => A.dialogN.length > n1, 100);
  ok('/trigger bm.standing: your standing (Family)', A.dialogN.length > n1 && /Family/.test(JSON.stringify(A.dialogN.slice(-1)[0] || '')));
  await near(34.5, 10, 38.5, 180); A.titles.length = 0; A.chats.length = 0; A.bars.length = 0;
  await click(`@e[type=minecraft:interaction,tag=bm.bbhit,${BOX},limit=1]`, 1200);
  ok('the Bounty Board, right-clicked: no bounty tonight', [...A.bars, ...A.titles, ...A.chats].some(t => /No bounties tonight/.test(t)), [...A.bars, ...A.titles, ...A.chats].slice(-2).join(' | ').slice(0, 120));
  // ---- the gates: the Dark Auction (Silver Key), the Gilded Gutter (Gold Key) and its Teller, Rat Gang HQ (the Rat King's Key)
  await run('loot give TestRat loot bm:items/rat_king_key');
  await near(39.5, 10, 17.5, 180);
  await click(ledger(21), 1500);
  const inHall = await passes(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s positioned ${rel(37.5, 10, 12.5)} if entity @a[name=TestRat,distance=..2.5]`);
  ok('the Dark Auction\'s gate ledger: the key lets you into the hall', inHall, (await posOf() || []).map(v => v.toFixed(1)).join(' '));
  await near(47.5, 18, 17.5, 180);
  await click(ledger(23), 1500);
  const inGutter = await passes(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s positioned ${rel(46.5, 18, 12.5)} if entity @a[name=TestRat,distance=..2.5]`);
  ok('the Gilded Gutter\'s gate, off the Fence\'s terrace: in', inGutter, (await posOf() || []).map(v => v.toFixed(1)).join(' '));
  const tl = ledger(42);
  await run(`${O}execute as ${tl} at @s run tp TestRat ^ ^ ^1.5 facing entity @s`); await sleep(1200);
  const n2 = A.dialogN.length; await click(tl, 1500);
  ok('...the Rat Bank\'s Teller: the bank opens', A.dialogN.length > n2 && /Bank|BANK|Teller/i.test(JSON.stringify(A.dialogN.slice(-1)[0] || '')), JSON.stringify(A.dialogN.slice(-1)[0] || '').slice(0, 100));
  await near(5.5, 10, 25.5, 180);
  await click(ledger(25), 1500);
  const inDen = await passes(`${O}execute as ${MK.replace(']', ',limit=1]')} at @s rotated as @s positioned ${rel(4.5, 10, 16.5)} if entity @a[name=TestRat,distance=..2.5]`);
  ok('the dock house\'s ledger (the Rat King\'s Key): through to Rat Gang HQ, the Captain there', inDen && (await cnt(`@e[type=minecraft:villager,tag=bm.npc_captain,${BOX}]`)) === 1,
     (await posOf() || []).map(v => v.toFixed(1)).join(' '));

  // ---- tidy up: the stage's leftovers; the chunks are let go
  await run(`${O}kill @e[tag=t194pet]`); await run(`${O}kill @e[tag=t194dia]`); await run(`${O}kill @e[tag=t194shaft]`);
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.stand 0'); await run('scoreboard players set TestRat bm.tier 0'); await run('tp TestRat 0 120 0');
  await run(`${O}forceload remove ${CX - 112} ${CZ - 8} ${CX + 100} ${CZ + 104}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
