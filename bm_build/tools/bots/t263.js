// 2.94c: THE NEW BONDS, as a regular (non-op) player - followers called with their own items (real uses): Emma and 8-Bit Emma
// make "Player Two Has Joined" (its hidden achievement, their intro, Speed), Leo and 8-Bit Leo "Knight of Two Worlds" (Strength),
// Cecil and 8-Bit Cecil "The Remaster" (Haste); Bender and Donado "Good Boys" (Speed), Bender and Zib "Space Dog" (Jump Boost);
// all three of those "The Space Pack" trio (its achievement, Luck - and Donado's beam lifts a monster). (rcon sets the stage.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const fx = async () => await run('data get entity TestRat active_effects');
  const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2400); };
  const X = 17820, Y = 100, Z = 16000;
  const HOSTS = ['cat,tag=bm.emmapet', 'wolf,tag=bm.xmpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.xlpet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.xcpet',
                 'wolf,tag=bm.bvpet', 'wolf,tag=bm.donado', 'wolf,tag=bm.zibpet'];
  const CDS = ['bm.emcd', 'bm.xmcd', 'bm.lecd', 'bm.xlcd', 'bm.cpcd', 'bm.xccd', 'bm.bvcd', 'bm.dncd', 'bm.zbcd'];
  const reset = async () => {
    await run('clear TestRat'); for (const t of HOSTS) await run(`kill @e[type=minecraft:${t}]`);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(3500);
    for (const o of CDS) await run(`scoreboard players set TestRat ${o} 0`);
  };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('scoreboard players reset TestRat bm.fret');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]');
  for (const a of ['pair_player_two', 'pair_two_knights', 'pair_remaster', 'pair_good_boys', 'pair_space_dog', 'trio_space_pack']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.xmmet', 'bm.xlmet', 'bm.xcmet', 'bm.leomet', 'bm.bvmet', 'bm.zbmet', 'bm.dnmet']) await run(`tag TestRat add ${t}`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await reset();

  const pair = async (name, adv_, items, hosts, effect) => {
    for (const [i, iid] of items.entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
    await sleep(500); A.chats.length = 0; A.bars.length = 0;
    for (let i = 0; i < items.length; i++) await use(i);
    const here = [];
    for (const h of hosts) here.push(await cnt(`@e[type=minecraft:${h}]`));
    ok(`${items.join(' and ')} used: ${hosts.length === 2 ? 'both' : 'all three'} come`, here.every(n => n >= 1), here.join(',') + ' || ' + A.bars.slice(-2).join(' | '));
    ok(`...together: "${name}" - its hidden achievement`, await wait(6000, async () => adv(adv_)));
    if (adv_.startsWith('pair_')) ok('...and their intro in chat', A.chats.some(c => new RegExp(name.replace(/[()]/g, '.') + '!').test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    ok(`...${effect} for you`, await wait(4000, async () => new RegExp(`minecraft:${effect}`).test(await fx())), (await fx()).slice(0, 160));
  };
  await pair('Player Two Has Joined', 'pair_player_two', ['emma_ribbon', 'cart_emma'], ['cat,tag=bm.emmapet', 'wolf,tag=bm.xmpet'], 'speed');
  await reset();
  await pair('Knight of Two Worlds', 'pair_two_knights', ['leo_crest', 'cart_leo'], ['wolf,tag=bm.leopet', 'wolf,tag=bm.xlpet'], 'strength');
  await reset();
  await pair('The Remaster', 'pair_remaster', ['cecil_gem', 'cart_cecil'], ['wolf,tag=bm.cecilpet', 'wolf,tag=bm.xcpet'], 'haste');
  await reset();
  await pair('Good Boys', 'pair_good_boys', ['bv_ball', 'donado_tag'], ['wolf,tag=bm.bvpet', 'wolf,tag=bm.donado'], 'speed');
  await reset();
  await pair('Space Dog', 'pair_space_dog', ['bv_ball', 'donadian_medal'], ['wolf,tag=bm.bvpet', 'wolf,tag=bm.zibpet'], 'jump_boost');
  await reset();
  await pair('The Space Pack', 'trio_space_pack', ['bv_ball', 'donado_tag', 'donadian_medal'], ['wolf,tag=bm.bvpet', 'wolf,tag=bm.donado', 'wolf,tag=bm.zibpet'], 'luck');
  await run(`${O}summon minecraft:husk ${X + 3} ${Y + 1} ${Z + 3} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t263z","bm.seen"]}`);
  await run('scoreboard players set TestRat bm.p188 19');
  ok('...every 20 seconds Donado\'s beam lifts the monsters round you (Levitation)', await wait(4000, async () => /levitation/.test(await run(`${O}data get entity @e[tag=bm.t263z,limit=1] active_effects`))));
  await run(`${O}kill @e[tag=bm.t263z]`);
  await reset();
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
