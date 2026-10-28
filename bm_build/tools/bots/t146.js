// 2.78: every follower in a frame - as a regular (non-op) player, every step a real packet: Zib's Donadian Medal,
// KillerWatt's Spark and Pearlman's card (and, 2.78a, Wilfrey's locket; 2.79, Fishy's Pocket Bowl; 2.80h, Dennis's horn and Pistachio's cloche; 2.82, Omega's Monocle) each hung in an item frame with a right-click: the follower climbs out (and says
// so), stays by the frame (nobody's - not the player's), still there ten seconds on; the item punched out of the frame:
// the follower goes with it. rcon only sets the stage (a wall, the frames, the three items).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const X = 16420, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 14} ${Y} ${Z - 8} ${X + 14} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 14} ${Y + 1} ${Z - 8} ${X + 14} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`${O}fill ${X - 14} ${Y + 1} ${Z + 5} ${X + 14} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 2.5} 0 -10`);
  await wait(2000, async () => A.pos && Math.abs(A.pos.z - (Z + 2.5)) < 0.05, 100); await sleep(400);

  const KINDS = [['Zib', 'donadian_medal', 'wolf', 'bm.zibpet', -4], ['KillerWatt', 'kw_spark', 'wolf', 'bm.kxpet', 0], ['Pearlman', 'pearl_card', 'cat', 'bm.pmpet', 4],
                 ['Wilfrey', 'wilfrey_locket', 'wolf', 'bm.wilfrey', -2], ['Fishy', 'fy_bowl', 'wolf', 'bm.fypet', 2],
                 ['Dennis', 'dw_horn', 'wolf', 'bm.dwpet', -6], ['Pistachio', 'pi_cloche', 'wolf', 'bm.pipet', 6],
                 ['Omega', 'om_monocle', 'wolf', 'bm.ompet', 8], ['Ashur', 'ashur_cinder', 'wolf', 'bm.aspet', -8], ['The Chef', 'chef_ladle', 'wolf', 'bm.kkpet', 10], ['The Neighbor', 'neighbor_baton', 'wolf', 'bm.nbpet', -10],
                 ['Queen Ava', 'av_locket', 'wolf', 'bm.avpet', 1], ['Queen Pearl', 'pq_pearls', 'wolf', 'bm.pqpet', -1], ['Bloo', 'bo_claw', 'wolf', 'bm.bopet', 3],
                 ['The Stalker', 'st_hook', 'wolf', 'bm.svpet', -3], ['The Arachno-Lantern', 'ln_gourd', 'wolf', 'bm.lnpet', -5], ['Bender', 'bv_ball', 'wolf', 'bm.bvpet', -7], ['Bones', 'bn_whistle', 'wolf', 'bm.bjpet', -9], ['Mr. Capshun', 'capshun_pencil', 'wolf', 'bm.mzpet', 9], ['Kettle', 'kettle_plane', 'wolf', 'bm.ktpet', 12], ['Rufus Gnaw', 'merc_contract', 'wolf', 'bm.rupet', -12], ['Henry', 'henry_tag', 'wolf', 'bm.hypet', 13], ['Nia', 'nia_bell', 'wolf', 'bm.nipet', -13], ['The Gem of Creativity', 'creativity_gem', 'wolf', 'bm.cgpet', 14], ['Batty', 'gentry_batty', 'wolf', 'bm.ytpet', -14], ['Eggbert', 'gentry_eggbert', 'wolf', 'bm.ebpet', 11], ['The Count', 'gentry_count', 'wolf', 'bm.knpet', -11], ['The Doodle Dragon', 'doodle_drawing', 'wolf', 'bm.ddpet', -2], ['The Eraser', 'eraser_crumb', 'wolf', 'bm.ezpet', 2], ['The Cursor', 'cursor_mouse', 'wolf', 'bm.uxpet', -4], ['The Ink Blot', 'ink_pot', 'wolf', 'bm.ibpet', 4], ['The Speech Bubble', 'caption_card', 'wolf', 'bm.wbpet', -8], ['The Lightbringer', 'herald_feather', 'wolf', 'bm.lhpet', 8], ['The Pale Dryad', 'dryad_cap', 'wolf', 'bm.pypet', -6], ['The Bound Sovereign', 'sov_eye', 'wolf', 'bm.xvpet', 15], ['The Sky Buddies', 'sky_mobile', 'wolf', 'bm.ybpet', 5], ['8-Bit Emma', 'cart_emma', 'wolf', 'bm.xmpet', 7], ['8-Bit Leo', 'cart_leo', 'wolf', 'bm.xlpet', 11], ['8-Bit Cecil', 'cart_cecil', 'wolf', 'bm.xcpet', -11]];
  const ONLY = process.argv.slice(2);   // (node t146.js [name...]: just those)
  for (const [name, iid, host, tag, dx] of KINDS.filter(k => !ONLY.length || ONLY.includes(k[0]))) {
    await run('time set noon');                  // (2.97: a long test - night falls, and on a Dread Night nobody comes out of a frame)
    await run(`${O}summon minecraft:item_frame ${X + dx} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t146f"]}`); await sleep(400);
    await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(300);
    await run(`${O}tp TestRat ${X + dx + 0.5} ${Y + 1} ${Z + 2.5} 0 -10`); await sleep(800);
    const frSel = `@e[type=minecraft:item_frame,tag=bm.t146f,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..2,limit=1]`;
    let fr = null; await wait(4000, async () => (fr = await entOf(A, frSel)) != null, 250);
    ok(`${name}: a frame on the wall`, fr != null);
    if (!fr) continue;
    A.slot(0); await sleep(300); A.bars.length = 0;
    if (fr) A.interact(fr.entityId); await sleep(2800);
    const pet = `@e[type=minecraft:${host},tag=${tag},tag=bm.ffpet,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..10]`;
    ok(`${name}'s item in a frame: ${name} climbs out`, (await cnt(pet)) === 1, `out ${await cnt(pet)}`);
    ok('...and says so', A.bars.some(b => new RegExp(`${name} climbs? out of the frame`).test(b)), A.bars.slice(-1).join(''));
    if (name === 'Wilfrey') ok('...in his bones (his body comes with him)', (await cnt(`@e[type=minecraft:wither_skeleton,tag=bm.wil_body,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..10]`)) === 1);
    ok('...nobody\'s - not the player\'s', (await cnt(`${pet.slice(0, -1)},scores={bm.pid=${+((await run('scoreboard players get TestRat bm.pid')).match(/has (-?\d+)/) || [0, -9])[1]}}]`)) === 0);
    await sleep(10000);
    ok('...still there by the frame ten seconds on (within 20 blocks: Wilfrey roams fast)', (await cnt(pet.replace('distance=..10', 'distance=..20'))) === 1,
       `${await cnt(pet.replace('distance=..10', 'distance=..20'))} near; ${(await run(`${O}data get entity @e[type=minecraft:${host},tag=${tag},tag=bm.ffpet,limit=1] Pos`)).replace(/^.*data: /, '')}`);
    A.attack(fr.entityId); await sleep(500);
    ok('the item punched out of the frame: out it drops', await wait(1500, async () => (await cnt(`@e[type=minecraft:item,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..3]`)) >= 1));
    ok(`...and ${name} goes with it`, await wait(3000, async () => (await cnt(pet)) === 0));
    if (name === 'Wilfrey') ok('...his bones too', await wait(3000, async () => (await cnt(`@e[type=minecraft:wither_skeleton,tag=bm.wil_body,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..12]`)) === 0));
    await run(`${O}kill @e[type=minecraft:item,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..4]`);
    await run(`${O}kill @e[type=minecraft:item_frame,tag=bm.t146f,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..1]`);   // (2.98: its spot free for the next)
  }
  await run(`${O}kill @e[type=minecraft:item_frame,tag=bm.t146f]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
