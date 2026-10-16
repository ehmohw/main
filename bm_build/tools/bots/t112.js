// 2.69 new rooms: the Sky Isles, the Spire, the Tinker's Bench, the Mason's Plan, the Dig; Block Party, Red Light Green Light, Memory Match
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, local, pos } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const waitFor = async (f, ms) => { const t = Date.now(); while (Date.now() - t < ms) { if (await f()) return true; await sleep(200); } return false; };
  const has = async (sel) => /passed/.test(await run(`execute if items entity TestRat container.* ${sel}`));
  const uuid = async () => (await run('data get entity TestRat UUID')).match(/\[I; ?(-?\d+), ?(-?\d+), ?(-?\d+), ?(-?\d+)\]/).slice(1).join(',');

  // ================================================================== THE SKY ISLES
  if (want('isles')) {
    await heist('isles', 'a', 3); await begin();
    let Q = await qs('isles'); ok('A heist of Sky Isles (Tier III)', Q.length >= 2, `${Q}`);
    let q = Q[0];
    ok('...islands over open air: no floor between them, nothing below', /passed/.test(await at('isles', q, `execute if block ${rel(8, 3, 4)} minecraft:air if block ${rel(8, 0, 4)} minecraft:air if block ${rel(8, -3, 4)} minecraft:air unless block ${rel(12, 3, 12)} minecraft:air`)));
    await go('isles', q, 4, 12); await sleep(1500);
    const g1 = await cnt('@e[tag=bm.gvg]');
    ok('...step onto the bridge: guards on the islands', g1 >= 3, `${g1}`);
    await run('execute in bm:gutter as @e[tag=bm.gvg,limit=1,sort=random] at @s run tag @s add t112g');
    await at('isles', q, `tp @e[tag=t112g,limit=1] ${rel(8, 0, 4)}`); await sleep(400);
    ok('...knock one off the edge: it\'s gone', (await cnt('@e[tag=t112g]')) === 0);
    const ko0 = await num('execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,limit=1] bm.gvko');
    await at('isles', q, `tp TestRat ${relf(8.5, 0.5, 4.5)}`); await sleep(800);
    const ko1 = await num('execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,limit=1] bm.gvko');
    const inDen = /passed/.test(await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s if entity @a[name=TestRat,distance=..14]'));
    ok('...fall into the void (Tier III): knocked out - back in the den, a try gone', ko1 > ko0 && inDen, `ko ${ko0} -> ${ko1}, den ${inDen}`);
    await go('isles', q, 4, 12); await sleep(300);
    await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(2500);
    const br = await cnt('@e[type=minecraft:breeze,tag=bm.gvg]'); const cap = await cnt('@e[tag=bm.gvcap]');
    ok('...the second wave: a captain, and breezes on the wind', br >= 1 && cap === 1, `breezes ${br} captain ${cap}`);
    await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(2500);
    ok('...cleared: the way on opens', await solved('isles', q));
    await heist('isles', 'a', 2); await begin();
    Q = await qs('isles'); q = Q[0]; await go('isles', q, 4, 12); await sleep(500);
    ok('Tier II: hay at the bottom', /passed/.test(await at('isles', q, `execute if block ${rel(8, 0, 4)} minecraft:hay_block`)));
    const ko2 = await num('execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,limit=1] bm.gvko');
    await at('isles', q, `tp TestRat ${relf(8.5, 1, 4.5)}`); await sleep(500); const l = await local('isles', q);
    ok('...a fall there: back to the start, no knock-out', l && l[0] < 3 && Math.abs(l[1] - 4) < 0.1 && (await num('execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,limit=1] bm.gvko')) === ko2, `${l}`);
  }

  // ================================================================== THE SPIRE
  if (want('spire')) {
    await heist('spire', 'a', 3); await begin();
    const Q = await qs('spire'); ok('A heist of Spires (Tier III)', Q.length >= 2, `${Q}`);
    const q = Q[0]; await go('spire', q, 2, 12);
    const fell = fnText('p112/spire/fell'); const cp = fell.match(/run tp @s (~\S* ~\S* ~\S*)\n/)[1];
    await at('spire', q, `tp TestRat ${cp}`); await sleep(400);
    ok('...touch the gold checkpoint: it\'s yours', (await num('scoreboard players get TestRat bm.gvcpk')) === q);
    await at('spire', q, `tp TestRat ${rel(18, 4, 20)}`); await sleep(400); const l1 = await local('spire', q);
    ok('...fall into the hay: back at the checkpoint', l1 && l1[1] > 6, `${l1}`);
    await at('spire', q, `tp TestRat ${rel(2, 4, 12)}`); await sleep(300); await run('scoreboard players reset TestRat bm.gvcpk'); await at('spire', q, `tp TestRat ${rel(18, 4, 20)}`); await sleep(400); const l2 = await local('spire', q);
    ok('...without it: back to the start', l2 && l2[0] < 3 && l2[1] < 4.5, `${l2}`);
    await at('spire', q, `summon minecraft:item ${relf(22.5, 14.1, 12.5)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`); await sleep(800);
    ok('...the plate at the top: open (the high door unbarred)', (await sc('spire', q, 'bm.gvs')) === 3 && /passed/.test(await at('spire', q, `execute if block ${rel(24, 15, 12)} minecraft:air`)));
  }

  // ================================================================== THE TINKER'S BENCH
  if (want('bench')) {
    for (const tier of [1, 4]) {
      await heist('bench', 'a', tier); await begin();
      const Q = await qs('bench'); const q = Q[0]; await go('bench', q, 8, 12); await sleep(600);
      const rc = await sc('bench', q, 'bm.gvc'); const t = Math.floor(rc / 10), j = rc % 10;
      const TG = { 10: 'compass', 11: 'clock', 40: 'hopper', 41: 'piston' }[rc];
      const parts = await has('*[minecraft:custom_data~{bm_room:1b}]');
      ok(`Tier ${tier}: walk in - the Fixer wants a ${TG}, and hands over the parts (and some extras)`, parts && !!TG, `recipe ${rc}`);
      const u = await uuid();
      const hand = async () => { await at('bench', q, `data modify entity @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14,limit=1] interaction set value {player:[I;${u}],timestamp:1L}`); await sleep(400); };
      await run('item replace entity TestRat weapon.mainhand with minecraft:dirt'); await hand();
      ok('...hand in the wrong thing: refused', !(await solved('bench', q)));
      await run(`item replace entity TestRat weapon.mainhand with minecraft:${TG}`); await run('give TestRat minecraft:stick 3'); await hand();
      const left = await has('*[minecraft:custom_data~{bm_room:1b}]') || await has('minecraft:stick');
      ok(`...hand in the ${TG}: open - and the leftover parts go back`, await solved('bench', q) && !left, `left ${left}`);
    }
  }

  // ================================================================== THE MASON'S PLAN
  if (want('mason')) {
    await heist('mason', 'a', 1); await begin();
    let Q = await qs('mason'); let q = Q[0]; await go('mason', q, 8, 12); await sleep(600);
    const inv = await run('data get entity TestRat Inventory');
    ok('Walk in: coloured blocks that only go down on lodestone', /concrete/.test(inv) && /can_place_on/.test(inv), inv.slice(0, 200));
    const p = await sc('mason', q, 'bm.gvc');
    const want_ = [...fnText(`p112/mason/chk${p}`).matchAll(/unless block (~\S* ~\S* ~\S*) minecraft:(\w+_concrete)/g)].map(m => [m[1], m[2]]);
    // place one with the bot: on the lodestone - yes; on the floor - no
    await run('item replace entity TestRat hotbar.0 with minecraft:red_concrete[minecraft:custom_data={bm_room:1b},minecraft:can_place_on={blocks:"minecraft:lodestone"}] 2');
    A.slot(0); await sleep(200);
    const mp = await H.mpos('mason', q); const gx = Math.floor(mp[0] - 12.5 + 11), gy = Math.floor(mp[1] - 1), gz = Math.floor(mp[2] - 12.5 + 11);
    await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${gx + 0.5} ${gy + 1} ${gz - 2.5} 0 40`); await sleep(400);
    A.useOn(gx, gy, gz, 1); await sleep(500);
    const placed = /passed/.test(await run(`execute in bm:gutter unless block ${gx} ${gy + 1} ${gz} minecraft:air`));
    A.useOn(gx - 1, gy, gz, 1); await sleep(500);
    const floorPlaced = /passed/.test(await run(`execute in bm:gutter unless block ${gx - 1} ${gy + 1} ${gz} minecraft:air`));
    ok('...a block placed on the lodestone stays; on the floor it won\'t go down', placed && !floorPlaced, `lode ${placed} floor ${floorPlaced}`);
    await at('mason', q, `fill ${rel(11, 4, 11)} ${rel(13, 4, 13)} minecraft:air`); for (const [r, b] of want_) await at('mason', q, `setblock ${r} minecraft:${b}`);
    await sleep(800);
    ok('...the grid matches the plan: open', await solved('mason', q) && want_.length === 9);
    await heist('mason', 'a', 3); await begin();
    Q = await qs('mason'); q = Q[0]; await go('mason', q, 8, 12); await sleep(600);
    const p2 = await sc('mason', q, 'bm.gvc');
    ok('Tier III: the plan is drawn turned round (a later plan)', p2 >= 6);
    await at('mason', q, `setblock ${rel(12, 4, 12)} minecraft:red_concrete`);
    await at('mason', q, `setblock ${rel(2, 5, 9)} minecraft:pale_oak_button[face=wall,facing=east,powered=true]`); await sleep(400);
    ok('...RESET clears the grid and hands the blocks out again', /passed/.test(await at('mason', q, `execute if block ${rel(12, 4, 12)} minecraft:air`)) && await has('*[minecraft:custom_data~{bm_room:1b}]'));
  }

  // ================================================================== THE DIG
  if (want('dig')) {
    await heist('dig', 'a', 1); await begin();
    const Q = await qs('dig'); const q = Q[0]; await go('dig', q, 4, 12); await sleep(600);
    ok('Walk in: the Fixer\'s pick', await has('*[minecraft:custom_data~{bm_digpick:1b}]'));
    let mud = null; for (let z = 2; z <= 22 && !mud; z++) if (/passed/.test(await at('dig', q, `execute if block ${rel(9, 4, z)} minecraft:mud_bricks`))) mud = z;
    let rock = null; for (let z = 2; z <= 22 && rock === null; z++) if (/passed/.test(await at('dig', q, `execute if block ${rel(9, 4, z)} minecraft:deepslate_bricks`))) rock = z;
    const pk = await run('data get entity TestRat Inventory[{id:"minecraft:stone_pickaxe"}].components');
    ok('...it bites the mud bricks and nothing else (the rest of the wall is rock)', /can_break": \{blocks: "minecraft:mud_bricks"\}/.test(pk) && mud !== null && rock !== null, pk.slice(-120));
    await at('dig', q, `setblock ${rel(9, 4, mud)} minecraft:air destroy`); await sleep(1200);
    ok('...mined mud doesn\'t lie about', !/passed/.test(await at('dig', q, 'execute positioned ~-12.5 ~-4 ~-12.5 if entity @e[type=minecraft:item,dx=24,dy=15,dz=24]')));
    await at('dig', q, `tp TestRat ${rel(19, 4, 12)}`); await sleep(500);
    ok('...through to the far side: open (and the pick goes back)', await solved('dig', q) && !(await has('*[minecraft:custom_data~{bm_digpick:1b}]')));
    // (every maze: one vein reaches the far face)
    let through = true; for (const f of ['m0', 'm1', 'm2', 'm3', 'm4', 'm5']) { const t = fnText(`p112/dig/${f}`); if (((t.match(/fill ~3 /g) || []).length) !== 1) through = false; }
    ok('...in every layout exactly one vein reaches the far face', through);
  }

  // ================================================================== BLOCK PARTY
  if (want('party')) {
    await run('function bm:admin/room_party'); await heist('levers', 'a', 1); await begin();
    const Q = await qs('party'); ok('Block Party is laid when forced', Q.length === 1, `${Q}`);
    const q = Q[0]; await go('party', q, 2, 12); await sleep(800);
    ok('...walk in: a colour is called', (await sc('party', q, 'bm.gvs')) === 1);
    const ch = await sc('party', q, 'bm.gvk');
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvbt,scores={bm.gvy1=${ch}},limit=1] at @s run tp TestRat ~ ~ ~`);
    await waitFor(async () => (await sc('party', q, 'bm.gvs')) === 2, 6000); await sleep(200);
    const under = /passed/.test(await run('execute at TestRat unless block ~ ~-1 ~ minecraft:air'));
    let other = 0; for (let i = 0; i < 36; i++) { }
    const wrongGone = /passed/.test(await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvbt,limit=1] unless score @s bm.gvy1 matches ${ch} at @s if block ~ ~-1 ~ minecraft:air`)) ||
                      !/passed/.test(await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvbt] unless score @s bm.gvy1 matches ${ch} at @s unless block ~ ~-1 ~ minecraft:air`));
    ok('...the rest of the floor drops; the called colour holds you', under && wrongGone);
    await waitFor(async () => (await sc('party', q, 'bm.gvc')) >= 2, 6000);
    ok('...survived: a round to the crew', (await sc('party', q, 'bm.gvw')) >= 1);
    const ch2 = await sc('party', q, 'bm.gvk'); const a0 = await alarm();
    await waitFor(async () => (await sc('party', q, 'bm.gvs')) === 2, 6000);
    await at('party', q, `tp TestRat ${rel(12, 1, 12)}`); await sleep(400);
    ok('...caught off it - into the pit: a miss (the alarm)', (await alarm()) > a0);
    await run(`execute in bm:gutter run scoreboard players set ${room('party', q)} bm.gvc 99`);
    await waitFor(async () => (await sc('party', q, 'bm.gvs')) === 3, 8000);
    ok('...after the last round the floor comes back and the way opens', await solved('party', q) && /passed/.test(await at('party', q, `execute if block ${rel(22, 3, 12)} minecraft:white_concrete`)));
  }

  // ================================================================== RED LIGHT, GREEN LIGHT
  if (want('redlight')) {
    await run('function bm:admin/room_redlight'); await heist('levers', 'a', 1); await begin();
    const Q = await qs('redlight'); ok('Red Light, Green Light is laid when forced', Q.length === 1, `${Q}`);
    const q = Q[0]; await go('redlight', q, 2, 12); await sleep(600);
    ok('...walk in: GREEN LIGHT', (await sc('redlight', q, 'bm.gvs')) === 1);
    await at('redlight', q, `tp TestRat ${rel(8, 4, 12)}`);
    const red = await waitFor(async () => (await sc('redlight', q, 'bm.gvs')) === 2 && (await sc('redlight', q, 'bm.gvw')) === -1, 8000);
    const a0 = await alarm(); await sleep(200);
    await at('redlight', q, `tp TestRat ${rel(10, 4, 12)}`); await sleep(400); const l = await local('redlight', q);
    ok('...move while the watcher looks: back to the line (the alarm)', red && l && l[0] < 3.5 && (await alarm()) > a0, `${l}`);
    await waitFor(async () => (await sc('redlight', q, 'bm.gvs')) === 1, 8000);
    await at('redlight', q, `tp TestRat ${rel(22, 4, 12)}`); await sleep(500);
    ok('...over the gold line on a green: everyone\'s across - open', await solved('redlight', q));
  }

  // ================================================================== MEMORY MATCH
  if (want('memory')) {
    await run('function bm:admin/room_memory'); await heist('levers', 'a', 1); await begin();
    const Q = await qs('memory'); ok('Memory Match is laid when forced', Q.length === 1, `${Q}`);
    const q = Q[0]; await go('memory', q, 3, 12); await sleep(500);
    const sym = []; for (let i = 0; i < 16; i++) sym.push(await num(`execute in bm:gutter run scoreboard players get @e[type=minecraft:interaction,tag=bm.gvmm${i},limit=1] bm.gvy1`));
    const click = async i => { await run(`execute in bm:gutter run data modify entity @e[type=minecraft:interaction,tag=bm.gvmm${i},limit=1] interaction set value {player:[I;1,2,3,4],timestamp:1L}`); await sleep(150); };
    ok('...sixteen cards, eight pairs', [0, 1, 2, 3, 4, 5, 6, 7].every(s => sym.filter(x => x === s).length === 2), `${sym}`);
    const a = 0, b = sym.findIndex((s, i) => i > 0 && s !== sym[0]);
    const m0 = await sc('memory', q, 'bm.gvy3');
    await click(a); const shown = await run(`execute in bm:gutter as @e[type=minecraft:interaction,tag=bm.gvmm${a},limit=1] at @s run data get entity @e[type=minecraft:item_display,tag=bm.gvmmd,distance=..1.2,limit=1] item.id`);
    await click(b); await sleep(1200);
    ok('...turn two that differ: shown, then face down again - a miss', !/paper/.test(shown) && (await sc('memory', q, 'bm.gvy3')) === m0 - 1, shown.slice(-40));
    for (let s = 0; s < 8; s++) { const [i, j] = sym.map((x, k) => x === s ? k : -1).filter(k => k >= 0); await click(i); await click(j); await sleep(1100); }
    ok('...all eight pairs: open', await solved('memory', q));
  }
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('function bm:admin/variant_random');
  await run('tag @a remove bm.gvok');   // (the operator's pass that staged the vault)
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
