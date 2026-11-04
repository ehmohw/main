// 3.1 smoke (the cut-back rule: summon, menu, call) - batch 3's Knight and Mimic (default), or any listed (node t395 ferro,rex), as a regular player: met (rcon,
// the stage), their item in hand; used: it comes; sneak + use: its menu (its buttons); used again: called over.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => { const R = await rcon(); const run = c => R.run(c); const res = [];
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const O = 'execute in minecraft:overworld run ', X = 19420, Y = 100, Z = 16000;
  const cnt = async (s) => +(((await run(`${O}execute if entity ${s}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  await run(`${O}forceload add ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`); await run(`${O}fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} minecraft:stone`);
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 5} ${Z + 6} minecraft:air`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const ALL = { knight: ['The Hollow Statue Knight', 'hx', 'knight_token', 'p269'], mimic: ['The Mimic', 'mx', 'mimic_key', 'p270'],
                ferro: ['The Ferro', 'fe', 'lodestone_vial', 'p271'], rex: ['The Atomic Rex', 'ry', 'atomic_whistle', 'p272'],
                talus: ['Talus', 'tl', 'mossback_drum', 'p273'], trivyrn: ['Trivyrn', 'tw', 'triune_horn', 'p274'],
                gdoodle: ['The Golden Doodle', 'gq', 'doodle_egg', 'p275'] };
  const WANT = (process.argv[2] || 'knight,mimic').split(',');
  for (const [nm, ab, iid, pfx] of WANT.map(k => ALL[k])) {
    const PET = `@e[type=minecraft:wolf,tag=bm.${ab}pet,tag=!bm.ffpet]`;
    await run(`kill ${PET}`); await run(`tag TestRat add bm.${ab}met`); await run(`scoreboard players set TestRat bm.${ab}cd 0`);
    await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); A.slot(0); await sleep(400);
    A.use(); await sleep(400); A.release(); await sleep(2500);
    ok(`${nm}: its item used - it comes`, (await cnt(PET)) === 1);
    const n0 = A.dialogN.length; A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); A.input({}); await sleep(1500);
    const labels = A.buttons().map(b => b.label);
    ok(`${nm}: sneak + use - its menu (Sit / follow, Send home, its ways, Wardrobe)`, A.dialogN.length > n0 && ['Sit / follow', 'Wardrobe'].every(l => labels.some(b => b.includes(l))), labels.join(' | '));
    await run(`${O}tp ${PET} ${X + 5} ${Y + 1} ${Z + 5}`); await sleep(500); A.bars.length = 0;
    A.use(); await sleep(400); A.release(); await sleep(1500);
    ok(`${nm}: used again - called over`, A.bars.some(b => b.includes(nm)), A.bars.slice(-1).join(''));
    await A.press(/Send .* home/).catch(() => {}); await run(`kill ${PET}`); await run('clear TestRat'); await sleep(800);
  }
  await run(`${O}forceload remove ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0); })();
