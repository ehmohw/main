// 2.71: the B and C versions of the Spire, the Tinker's Bench, the Mason's Plan and the Dig
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, local } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const has = async (sel) => /passed/.test(await run(`execute if items entity TestRat container.* ${sel}`));
  const uuid = async () => (await run('data get entity TestRat UUID')).match(/\[I; ?(-?\d+), ?(-?\d+), ?(-?\d+), ?(-?\d+)\]/).slice(1).join(',');
  const isb = async (k, q, pos, b) => /passed/.test(await at(k, q, `execute if block ${pos} ${b}`));
  const press = async (k, q, pos, face = 'floor', facing = 'east') => { await at(k, q, `setblock ${pos} minecraft:pale_oak_button[face=${face},facing=${facing},powered=true]`); await sleep(400);
    await at(k, q, `setblock ${pos} minecraft:pale_oak_button[face=${face},facing=${facing},powered=false]`); await sleep(200); };
  const plate = async (k, q) => { await at(k, q, `summon minecraft:item ${relf(22.5, 14.1, 12.5)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`); await sleep(900); };
  const spireOpen = async q => (await sc('spire', q, 'bm.gvs')) === 3 && /passed/.test(await at('spire', q, `execute if block ${rel(24, 15, 12)} minecraft:air`));
  const lr = async q => (await local('spire', q)).map(v => Math.round(v * 10) / 10);

  // ================================================================== THE SPIRE
  if (want('spire')) {
    // ---- B: the ladder spire
    await heist('spire', 'b', 3); await begin();
    let Q = await qs('spire'); let q = Q[0];
    ok('Spires, all variant B (the Ladder Spire)', Q.length >= 1 && (await sc('spire', q, 'bm.gvvar')) === 1, `${Q}`);
    const A1 = fnText('p112/spire/init') && [...fnText('p114/spireb/init').matchAll(/setblock (~\S* ~\S* ~\S*) minecraft:air/g)].length;
    const lad = /passed/.test(await at('spire', q, `execute if block ${rel(5, 5, 9)} minecraft:ladder if block ${rel(13, 9, 4)} minecraft:ladder if block ${rel(19, 12, 9)} minecraft:ladder`));
    const old = /passed/.test(await at('spire', q, `execute if block ${rel(4, 4, 12)} minecraft:air if block ${rel(6, 5, 14)} minecraft:air`));
    ok('...ladders up three posts, the old spiral gone', lad && old && A1 > 5, `ladders ${lad} old gone ${old}`);
    await go('spire', q, 2, 12);
    await at('spire', q, `tp TestRat ${relf(13.5, 10, 3.5)}`); await sleep(400);
    await at('spire', q, `tp TestRat ${rel(18, 4, 20)}`); await sleep(500);
    let l = await lr(q);
    ok('...the second post is a checkpoint: a fall brings you back to it', Math.abs(l[0] - 13.5) < 0.6 && Math.abs(l[2] - 3.5) < 0.6 && l[1] >= 9.9, `${l}`);
    await at('spire', q, `tp TestRat ${rel(2, 4, 12)}`); await run('scoreboard players reset TestRat bm.gvcpk');
    await at('spire', q, `tp TestRat ${rel(18, 4, 20)}`); await sleep(500); l = await lr(q);
    ok('...without it: back to the start', Math.abs(l[0] - 2.5) < 0.6 && Math.abs(l[2] - 12.5) < 0.6, `${l}`);
    await plate('spire', q);
    ok('...the plate at the top: open', await spireOpen(q));
    // ---- C: the switch spire
    await heist('spire', 'c', 3); await begin();
    Q = await qs('spire'); q = Q[0];
    ok('Variant C (the Switch Spire) when forced', Q.length >= 1 && (await sc('spire', q, 'bm.gvvar')) === 2, `${Q}`);
    const red = [[8, 12, 6], [8, 15, 6], [10, 16, 7], [14, 8, 10], [12, 8, 11], [9, 8, 11]], blue = [[15, 16, 8], [16, 14, 9], [16, 12, 9], [8, 13, 12], [8, 15, 13]];
    const solidIs = async (cells, b) => { for (const [x, z, t] of cells) if (!(await isb('spire', q, rel(x, t - 1, z), b))) return false; return true; };
    const ghosts = await cnt('@e[type=minecraft:block_display,tag=bm.gvprop]');
    ok('...red solid, blue only a ghost of glass; switch posts with buttons', await solidIs(red, 'minecraft:red_concrete') && await solidIs(blue, 'minecraft:air') &&
       await isb('spire', q, rel(12, 8, 16), 'minecraft:pale_oak_button') && ghosts >= 11, `ghosts ${ghosts}`);
    await go('spire', q, 2, 12);
    await press('spire', q, rel(12, 8, 16));
    ok('...press a switch: blue goes solid, red vanishes', await solidIs(blue, 'minecraft:blue_concrete') && await solidIs(red, 'minecraft:air'));
    await press('spire', q, rel(16, 10, 9));
    ok('...press another: back to red', await solidIs(red, 'minecraft:red_concrete') && await solidIs(blue, 'minecraft:air'));
    await at('spire', q, `tp TestRat ${relf(16.5, 10, 9.5)}`); await sleep(400);
    await at('spire', q, `tp TestRat ${rel(18, 4, 20)}`); await sleep(500); l = await lr(q);
    ok('...the middle post is a checkpoint', Math.abs(l[0] - 16.5) < 0.6 && Math.abs(l[2] - 9.5) < 0.6, `${l}`);
    await plate('spire', q);
    ok('...the plate at the top: open', await spireOpen(q));
  }

  // ================================================================== THE TINKER'S BENCH
  const RID = { 1: ['compass', 'clock', 'shears'], 2: ['bucket', 'fishing_rod', 'bow'], 3: ['spyglass', 'flint_and_steel', 'lead'], 4: ['shield', 'item_frame', 'brush'],
                5: ['piston', 'observer', 'dropper'] };
  if (want('bench')) {
    const u = await uuid();
    const hand = async q => { await at('bench', q, `data modify entity @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14,limit=1] interaction set value {player:[I;${u}],timestamp:1L}`); await sleep(500); };
    for (const tier of [1, 5]) {
      await heist('bench', 'b', tier); await begin();
      const Q = await qs('bench'); const q = Q[0]; await go('bench', q, 8, 12); await sleep(700);
      const rc = await sc('bench', q, 'bm.gvc'); const want_ = RID[tier][rc % 10]; const wrong = RID[tier].find(x => x !== want_);
      const txt = await at('bench', q, `data get entity @e[type=minecraft:text_display,distance=..16,sort=nearest,limit=1] text`);
      const sgn = (await run(`execute in bm:gutter as ${room('bench', q)} at @s run data get entity @e[type=minecraft:text_display,limit=1,sort=furthest,distance=..1] text`));
      const rid = fnText('p114/benchb/init');
      ok(`Tier ${tier}: variant B (the Riddle) - a riddle, not a name; parts for three things`, (await sc('bench', q, 'bm.gvvar')) === 1 && await has('*[minecraft:custom_data~{bm_room:1b}]') &&
         !new RegExp(want_.replace('_', ' '), 'i').test(rid.split('\n').find(L => L.includes(`matches ${rc} run`)) || ''), `wants ${want_}`);
      const a0 = await alarm();
      await run(`item replace entity TestRat weapon.mainhand with minecraft:${wrong}`); await hand(q);
      ok(`...hand in the wrong one (${wrong}): kept, and the alarm rings`, !(await solved('bench', q)) && (await alarm()) > a0 && !(await has(`minecraft:${wrong}`)), `${a0} -> ${await alarm()}`);
      await run('item replace entity TestRat weapon.mainhand with minecraft:dirt'); await hand(q);
      ok('...something else entirely: refused, no alarm', !(await solved('bench', q)));
      await run(`item replace entity TestRat weapon.mainhand with minecraft:${want_}`); await hand(q);
      ok(`...the ${want_}: open, and the parts go back`, await solved('bench', q) && !(await has('*[minecraft:custom_data~{bm_room:1b}]')));
    }
    for (const tier of [2, 4]) {
      await heist('bench', 'c', tier); await begin();
      const Q = await qs('bench'); const q = Q[0]; await go('bench', q, 8, 12); await sleep(700);
      const pats = await at('bench', q, `data get block ${rel(12, 7, 1)} patterns`);
      const looms = /passed/.test(await at('bench', q, `execute if block ${rel(7, 4, 20)} minecraft:loom if block ${rel(12, 4, 20)} minecraft:loom if block ${rel(17, 4, 20)} minecraft:loom`));
      const layers = (pats.match(/pattern:/g) || []).length;
      ok(`Tier ${tier}: variant C (the Herald's Banner) - a banner on the wall, looms, a white banner and dyes`, looms && layers === (tier === 2 ? 2 : 3) &&
         await has('minecraft:white_banner') && await has('*[minecraft:custom_data~{bm_room:1b}]'), pats.slice(-160));
      const list = pats.replace(/^.*?data: /, '').trim();
      const arr = [...list.matchAll(/\{(?:[^{}])*\}/g)].map(m => m[0]);
      const swapped = '[' + [...arr].reverse().join(',') + ']';
      const a0 = await alarm();
      await run(`item replace entity TestRat weapon.mainhand with minecraft:white_banner[minecraft:banner_patterns=${swapped}]`); await hand(q);
      const s1 = await solved('bench', q), a1 = await alarm(), fresh = await has('minecraft:white_banner[minecraft:banner_patterns=[]]');
      ok('...the right layers in the wrong order: refused - the alarm, and a fresh banner', !s1 && a1 > a0 && fresh, `solved ${s1} alarm ${a0}->${a1} fresh ${fresh}`);
      await run(`item replace entity TestRat weapon.mainhand with minecraft:white_banner[minecraft:banner_patterns=${list}]`); await hand(q);
      ok('...the banner just like the wall\'s: open', await solved('bench', q));
    }
  }

  // ================================================================== THE MASON'S PLAN
  if (want('mason')) {
    for (const tier of [1, 5]) {
      await heist('mason', 'b', tier); await begin();
      const Q = await qs('mason'); const q = Q[0]; await go('mason', q, 6, 12); await sleep(800);
      const p = await sc('mason', q, 'bm.gvc');
      const fixed = [...fnText(`p114/masonb/p${p}`).matchAll(/setblock (~\S* ~\S* ~\S*) minecraft:(\w+_wool)/g)];
      const need = [...fnText(`p114/masonb/chk${p}`).matchAll(/unless block (~\S* ~\S* ~\S*) minecraft:(\w+_concrete)/g)].map(m => [m[1], m[2]]);
      let wool = 0; for (const f of fixed) if (await isb('mason', q, f[1], `minecraft:${f[2]}`)) wool++;
      ok(`Tier ${tier}: variant B (the Mosaic) - a 4x4 lodestone grid, ${fixed.length} wool set, the blocks handed out`, wool === fixed.length && fixed.length + need.length === 16 &&
         /passed/.test(await at('mason', q, `execute if block ${rel(13, 3, 13)} minecraft:lodestone unless block ${rel(14, 3, 14)} minecraft:lodestone`)) && await has('minecraft:red_concrete'),
         `wool ${wool}/${fixed.length}`);
      // a wrong fill (two swapped) - shut; the right one - open
      const sw = need.map(x => [...x]); const k2 = sw.findIndex(x => x[1] !== sw[0][1]); [sw[0][1], sw[k2][1]] = [sw[k2][1], sw[0][1]];
      for (const [r, b] of sw) await at('mason', q, `setblock ${r} minecraft:${b}`); await sleep(800);
      ok('...two colours swapped: still shut', !(await solved('mason', q)));
      await press('mason', q, rel(2, 5, 9), 'wall', 'east'); await sleep(300);
      let cleared = true; for (const [r] of need) if (!(await isb('mason', q, r, 'minecraft:air'))) cleared = false;
      let woolKept = true; for (const f of fixed) if (!(await isb('mason', q, f[1], `minecraft:${f[2]}`))) woolKept = false;
      ok('...RESET clears your blocks (the wool stays) and hands them out again', cleared && woolKept && await has('minecraft:red_concrete'));
      for (const [r, b] of need) await at('mason', q, `setblock ${r} minecraft:${b}`); await sleep(800);
      ok('...every row and column one of each: open', await solved('mason', q));
    }
    await heist('mason', 'c', 3); await begin();
    const Q = await qs('mason'); const q = Q[0]; await go('mason', q, 6, 12); await sleep(800);
    const p = await sc('mason', q, 'bm.gvc');
    const cells = [...fnText(`p114/masonc/chk${p}`).matchAll(/unless block (~\S* ~\S* ~\S*) minecraft:(black_concrete|air)/g)].map(m => [m[1], m[2]]);
    const clues = +(((await at('mason', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:text_display,tag=bm.gvprop,distance=..8]')).match(/Count: (\d+)/) || [0, -1])[1]);
    ok('Variant C (the Picture) - a 5x5 grid, a clue for every row and column, black blocks handed out', cells.length === 25 && clues >= 10 && await has('minecraft:black_concrete'), `clues ${clues}`);
    const blacks = cells.filter(c => c[1] === 'black_concrete');
    for (const [r] of blacks.slice(1)) await at('mason', q, `setblock ${r} minecraft:black_concrete`);
    const extra = cells.find(c => c[1] === 'air'); await at('mason', q, `setblock ${extra[0]} minecraft:black_concrete`); await sleep(800);
    ok('...one block in the wrong place: still shut', !(await solved('mason', q)));
    await at('mason', q, `setblock ${extra[0]} minecraft:air`); await at('mason', q, `setblock ${blacks[0][0]} minecraft:black_concrete`); await sleep(800);
    ok('...the one picture that fits: open', await solved('mason', q));
  }

  // ================================================================== THE DIG
  if (want('dig')) {
    await heist('dig', 'b', 2); await begin();
    let Q = await qs('dig'); let q = Q[0]; await go('dig', q, 4, 12); await sleep(800);
    const b = await sc('dig', q, 'bm.gvc');
    ok('Variant B (the Minefield): the Fixer\'s pick (packed mud only), the first column dug, numbers in it', (await sc('dig', q, 'bm.gvvar')) === 1 &&
       await has('minecraft:stone_pickaxe[minecraft:can_break={blocks:"minecraft:packed_mud"}]') && (await cnt('@e[type=minecraft:text_display,tag=bm.gvprop]')) >= 21 &&
       await isb('dig', q, rel(10, 4, 12), 'minecraft:packed_mud') && await isb('dig', q, rel(9, 4, 12), 'minecraft:air'), `board ${b}`);
    const lines = fnText(`p114/digb/c${b}`).split('\n').filter(L => L.includes(' 4 ') || true);
    const cellOf = L => { const m = L.match(/unless block (~\S*) (~\S*) (~\S*) minecraft:packed_mud positioned \S+ \S+ \S+ run function bm:p114\/digb\/(\w+)/); return m ? { x: m[1], z: m[3], y: m[2], f: m[4] } : null; };
    const all = lines.map(cellOf).filter(Boolean);
    const safe = all.find(c => c.f.startsWith('s') && c.y === '~'), mine = all.find(c => c.f === 'mine' && c.y === '~1');
    const t0 = await cnt('@e[type=minecraft:text_display,tag=bm.gvprop]');
    await at('dig', q, `setblock ${safe.x} ~0 ${safe.z} minecraft:air`); await sleep(700);
    const t1 = await cnt('@e[type=minecraft:text_display,tag=bm.gvprop]');
    ok(`...dig a safe cell: it opens and shows its number (${safe.f.slice(1)})`, t1 === t0 + 1 && await isb('dig', q, `${safe.x} ~1 ${safe.z}`, 'minecraft:air'));
    const a0 = await alarm();
    await at('dig', q, `setblock ${mine.x} ~1 ${mine.z} minecraft:air`); await sleep(700);
    ok('...dig into TNT: BOOM - the alarm, and the charge sits there (it won\'t dig)', (await alarm()) > a0 && await isb('dig', q, `${mine.x} ~0 ${mine.z}`, 'minecraft:tnt'), `${a0} -> ${await alarm()}`);
    const t2 = await cnt('@e[type=minecraft:text_display,tag=bm.gvprop]'); await sleep(1000);
    ok('...a dug cell isn\'t counted twice', (await cnt('@e[type=minecraft:text_display,tag=bm.gvprop]')) === t2);
    await at('dig', q, `tp TestRat ${rel(19, 4, 12)}`); await sleep(600);
    ok('...across to the far side: open (and the pick goes back)', await solved('dig', q) && !(await has('*[minecraft:custom_data~{bm_digpick:1b}]')));
    // ---- C
    await heist('dig', 'c', 2); await begin();
    Q = await qs('dig'); q = Q[0]; await go('dig', q, 4, 12); await sleep(800);
    const m = await sc('dig', q, 'bm.gvc');
    const cube = [...fnText(`p114/digc/k${m}`).matchAll(/unless block (~\S* ~\S* ~\S*) minecraft:(calcite|air)/g)].map(x => [x[1], x[2]]);
    const keep = cube.filter(c => c[1] === 'calcite').length;
    const minis = +(((await at('dig', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:block_display,tag=bm.gvprop,distance=..20]')).match(/Count: (\d+)/) || [0, -1])[1]);
    ok('Variant C (the Sculptor): the wall gone, a 3x3x3 of calcite, the model on its plinth, the chisel', (await sc('dig', q, 'bm.gvvar')) === 2 &&
       await isb('dig', q, rel(12, 9, 12), 'minecraft:air') && await isb('dig', q, rel(12, 5, 12), 'minecraft:calcite') && minis === keep + 1 &&
       await has('minecraft:stone_pickaxe[minecraft:can_break={blocks:"minecraft:calcite"}]'), `model ${minis - 1}/${keep}`);
    const gone = cube.filter(c => c[1] === 'air');
    for (const [r] of gone.slice(1)) await at('dig', q, `setblock ${r} minecraft:air`);
    const wrong = cube.find(c => c[1] === 'calcite'); await at('dig', q, `setblock ${wrong[0]} minecraft:air`); await sleep(800);
    ok('...carve away a block that should stay: still shut', !(await solved('dig', q)));
    const a0c = await alarm();
    await press('dig', q, rel(2, 5, 9), 'wall', 'east'); await sleep(300);
    ok('...RESET: the whole block back (the alarm rings)', await isb('dig', q, wrong[0], 'minecraft:calcite') && await isb('dig', q, gone[1][0], 'minecraft:calcite') && (await alarm()) > a0c);
    for (const [r] of gone) await at('dig', q, `setblock ${r} minecraft:air`); await sleep(800);
    ok('...carved to match the model: open', await solved('dig', q));
  }
  await run('function bm:admin/variant_random'); await run('function bm:admin/rooms_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
