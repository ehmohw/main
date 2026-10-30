// 3.0d: A DREAD MIRE MELTS (phase246's death; phase257's sprites) - as a regular (non-op) player. rcon sets the stage (hard mode, the
// night, a Mire risen 3.5 blocks ahead of TestRat and worn to its last hits, a sword in hand); the player strikes the blow.
//   melt    its death, tick by tick (its own bm.mt): it can't be hurt once it falls (a blow lands on nothing); it sags (the trunk's
//           scale squashed, lowered); a pile of goop wells up (bm.mgoop, the dfx_goop model) and bubbles (bubble sprites, popping);
//           the trunk and tentacles gone to nothing; the goop and the puddle shrink away; then nothing left - no part, no goop, no
//           sprite - and its Shadow Remnants lie where it was
//   sweep   a Mire killed, and mid-melt swept (p246/melt - what the no-spawn sweep, the cross, the light and the Dread's fall run):
//           every part and the goop gone at once; its last bubbles gone within a second
//   node t332.js [melt|sweep]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const X = 18440, Y = 100, Z = 16040;
const O = 'execute in minecraft:overworld run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (who, o) => +((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (+v >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const vec = (s) => (s.match(/\[(-?[\d.E-]+)f, (-?[\d.E-]+)f, (-?[\d.E-]+)f\]/) || []).slice(1).map(Number);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const dfell = await sc('#dfell', 'bm.cfg'); const hard = await sc('#hard', 'bm.cfg');
  await run('scoreboard players set #dfell bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1'); await run(`${O}time set 18000`);
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(2500);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 12} minecraft:air`);
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:instant_health 1 4 true');
  await run('clear TestRat'); await run('item replace entity TestRat hotbar.8 with minecraft:netherite_sword');
  const MIRE = `@e[type=minecraft:husk,tag=bm.mire,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..4,limit=1]`;
  const near = (t, r = 10) => `@e[type=minecraft:item_display,tag=${t},x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..${r}]`;
  const clean = async () => { await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..16]`); await run(`${O}kill ${near('bm.mr', 14)}`);
    await run(`${O}execute as @e[type=minecraft:husk,tag=bm.mire,x=${X},y=${Y},z=${Z},distance=..16] run tp @s ~ -400 ~`); await sleep(400); };
  const slay = async () => {
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 10`); await sleep(800);
    await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} run function bm:p246/spawn`);
    await run(`${O}execute as ${MIRE} at @s run function bm:p246/rise0`); await sleep(2600);
    await run(`${O}data merge entity ${MIRE} {Health:104f}`); A.slot(8); await sleep(1300);
    for (let k = 0; k < 6 && (await cnt(`${MIRE.slice(0, -1)},scores={bm.ms=7}]`)) === 0; k++) { const e = await entOf(MIRE); if (e) A.attack(e.entityId); await sleep(800); }
    return await wait(3000, async () => (await cnt(`${MIRE.slice(0, -1)},scores={bm.ms=7}]`)) === 1, 100);
  };

  if (on('melt')) {
    await clean();
    ok('a Dread Mire, risen and worn down: the player\'s blow fells it - it begins to melt (ms 7)', await slay());
    const mt = async () => await sc(MIRE, 'bm.mt');
    // (a blow while it melts lands on nothing)
    await wait(3000, async () => (await mt()) >= 18, 100);
    const h0 = (await run(`${O}data get entity ${MIRE} Health`)).match(/([\d.]+)f/)?.[1];
    const e = await entOf(MIRE); if (e) A.attack(e.entityId); await sleep(600);
    const h1 = (await run(`${O}data get entity ${MIRE} Health`)).match(/([\d.]+)f/)?.[1];
    ok('...melting, it can\'t be hurt (Invulnerable; a blow changes nothing)', /1b/.test(await run(`${O}data get entity ${MIRE} Invulnerable`)) && h0 === h1, `${h0} -> ${h1}`);
    ok('...and it doesn\'t fight (no grab, no stab: bm.ms stays 7)', (await sc(MIRE, 'bm.ms')) === 7);
    // (it sags: the trunk squashed - its height scale below its width - and lowered)
    let sag = null;
    await wait(4000, async () => { if ((await mt()) < 50) return false;
      const s = vec(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.mr_seg2,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..6,limit=1] transformation.scale`)); sag = s; return s.length === 3 && s[1] < s[0] * 0.75; }, 100);
    ok('...it sags and slumps: its trunk squashed flat (scale y well under x)', sag && sag[1] < sag[0] * 0.75, JSON.stringify(sag));
    ok('...a pile of goop wells up where it was (dfx_goop)', await wait(3000, async () => (await cnt(near('bm.mgoop', 4))) === 1 &&
       /dfx_goop/.test(await run(`${O}data get entity ${near('bm.mgoop', 4).slice(0, -1)},limit=1] item`)), 100));
    ok('...and bubbles (bubble sprites on it, popping)', await wait(3000, async () => (await cnt(near('bm.dfx_bubble', 4))) >= 1, 100));
    ok('...the goop at its full size', await wait(3000, async () => { const s = vec(await run(`${O}data get entity ${near('bm.mgoop', 4).slice(0, -1)},limit=1] transformation.scale`)); return s[0] > 2; }, 150));
    let last = null;
    ok('...its trunk and tentacles gone to nothing (scale 0)', await wait(4000, async () => {
      const a = vec(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.mr_head,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..10,limit=1] transformation.scale`));
      const b = vec(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.mr_t1c,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..12,limit=1] transformation.scale`));
      last = [a, b]; return a[0] === 0 && b[0] === 0; }, 150), JSON.stringify(last));
    await wait(3000, async () => (await mt()) >= 88, 100); const m1 = await mt(); ok('...still bubbling, a few seconds', m1 >= 80 && (await cnt(near('bm.mgoop', 4))) === 1, `mt ${m1}`);
    ok('...the goop and the puddle shrink away', await wait(4000, async () => { const s = vec(await run(`${O}data get entity ${near('bm.mgoop', 4).slice(0, -1)},limit=1] transformation.scale`)); return s.length === 3 && s[0] === 0; }, 150));
    ok('...then it is gone: the host', await wait(4000, async () => (await cnt(`@e[type=minecraft:husk,tag=bm.mire,x=${X},y=${Y},z=${Z},distance=..16]`)) === 0, 150));
    ok('...no part, no goop left (bm.mr)', (await cnt(near('bm.mr', 14))) === 0);
    ok('...no sprite left within 2 s (bm.dfx)', await wait(2500, async () => (await cnt(near('bm.dfx', 14))) === 0, 200));
    ok('...and its Shadow Remnants lie where it was', await wait(2000, async () => (await cnt(`@e[type=minecraft:item,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..4,nbt={Item:{components:{"minecraft:custom_data":{bm:"shadow_remnant"}}}}]`)) >= 1, 200));
  }

  if (on('sweep')) {
    await clean();
    ok('a second Mire felled: it melts', await slay());
    await wait(5000, async () => (await sc(MIRE, 'bm.mt')) >= 60, 100);
    ok('...mid-melt: the goop and its bubbles out', (await cnt(near('bm.mgoop', 4))) === 1);
    await run(`${O}execute as ${MIRE} at @s run function bm:p246/melt`);
    ok('swept (p246/melt, as the sweeps run it): the host, every part and the goop gone at once', (await cnt(`@e[type=minecraft:husk,tag=bm.mire,x=${X},y=${Y},z=${Z},distance=..16]`)) === 0 && (await cnt(near('bm.mr', 14))) === 0);
    ok('...its last bubbles gone within a second', await wait(1500, async () => (await cnt(near('bm.dfx', 14))) === 0, 100));
  }

  await clean();
  await run(`scoreboard players set #dfell bm.cfg ${dfell === -99 ? 0 : dfell}`); await run(`scoreboard players set #hard bm.cfg ${hard === -99 ? 0 : hard}`);
  await run('clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  await R.end(); process.exit(0);
})();
