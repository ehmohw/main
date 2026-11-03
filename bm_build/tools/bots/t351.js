// 3.0g: A FOLLOWER'S KILL IS ITS OWNER'S (phase201's OWN: a blow of a follower's own move that may kill is dealt "by" the follower
// "from" its owner), as a regular (non-op) player: Emma called with her ribbon; rcon sets the stage (a floor, a NoAI zombie at
// low health 4 blocks off, Emma's ethereal form started, a statistics objective for the bot) and reads the results.
//   Emma's Crescent Dive kills it: the bot's "killed: zombie" statistic counts it (a player kill), experience orbs drop where it
//   fell (no XP without a player kill), and the zombie turned on nobody first; a zombie left at full health and struck by her keeps
//   its last attacker Emma (on attacker - the follower, not the bot), so a monster she hits turns on her, not on you.
//   node t351.js
const { bot, rcon, sleep } = require('./lib_resp');
const O = 'execute in minecraft:overworld run ';
const X = 21460, Y = 100, Z = 16400;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)[a-z]?$/) || [0, NaN])[1]);
  const sc = async (who, o) => +((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, 0])[1];
  const EMMA = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]';
  const ZOM = '@e[type=minecraft:zombie,tag=t351,limit=1]';
  const zombie = async (hp) => { await run(`${O}kill @e[type=minecraft:zombie,tag=t351]`); await run(`${O}kill @e[type=minecraft:experience_orb,x=${X},y=${Y},z=${Z},distance=..20]`);
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 4.5} {Tags:["t351","bm.seen"],NoAI:1b,PersistenceRequired:1b,IsBaby:0b,Health:${hp}f}`); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('time set noon');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`); await sleep(1500);
  await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}fill ${X - 12} ${Y + 9} ${Z - 12} ${X + 12} ${Y + 9} ${Z + 12} minecraft:glass`);          // (a roof: no daylight burning)
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30,type=!minecraft:item_display]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z - 3.5} 0 0`); await sleep(1200); A.stand();
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p62/emma_go`); await run('scoreboard players set TestRat bm.emcd 0'); await sleep(1500);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon'); await run('scoreboard players set TestRat bm.emwf 0'); await sleep(500);
  A.slot(0); await sleep(250); A.use(); await sleep(400); A.release();
  ok('Emma called with her ribbon', await wait(6000, async () => (await cnt(EMMA)) === 1));
  await run('scoreboard objectives remove t351k'); await run('scoreboard objectives add t351k minecraft.killed:minecraft.zombie');
  await run('scoreboard players set TestRat t351k 0');

  // ---- a zombie she can finish: her move's killing blow is yours
  await zombie(3);
  await run(`${O}execute as ${EMMA} at @s run function bm:p57/ascend`);
  let orbs = 0;
  const dead = await wait(20000, async () => { await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 30`);
    const o = await cnt(`@e[type=minecraft:experience_orb,x=${X},y=${Y},z=${Z},distance=..14]`); orbs = Math.max(orbs, o); return (await cnt(ZOM)) === 0; }, 200);
  await sleep(600); orbs = Math.max(orbs, await cnt(`@e[type=minecraft:experience_orb,x=${X},y=${Y},z=${Z},distance=..14]`));
  ok('Emma\'s Crescent Dive fells the zombie', dead);
  ok('...a player kill: the bot\'s "killed: zombie" statistic counts it', (await sc('TestRat', 't351k')) >= 1, `killed ${await sc('TestRat', 't351k')}`);
  ok('...and it drops experience (only a player kill does)', orbs >= 1, `orbs ${orbs}`);

  // ---- a zombie at full health she only hurts: her blow stays hers (it turns on her, not on you)
  await zombie(20); await sleep(300);
  let by = '';
  await wait(15000, async () => { await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 30`);
    const h = await num(`${O}data get entity ${ZOM} Health`);
    if (h < 20 && h > 0) { by = await run(`${O}execute as ${ZOM} on attacker run data get entity @s Tags`); return true; } return false; }, 200);
  ok('a zombie she only wounds: its attacker is Emma (on attacker - the follower), not you', /bm\.emmapet/.test(by), by.slice(0, 160));

  await run(`${O}kill @e[type=minecraft:zombie,tag=t351]`); await run(`${O}execute as ${EMMA} run scoreboard players set @s bm.eme 1`); await sleep(1500);
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p62/emma_go`); await run('scoreboard objectives remove t351k');
  await run(`${O}fill ${X - 12} ${Y + 9} ${Z - 12} ${X + 12} ${Y + 9} ${Z + 12} minecraft:air`); await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
