// 2.80d: DENNIS AND PISTACHIO, THE TRADERS - as a regular (non-op) player, every step a real packet (rcon sets the stage: a
// Black Market placed fresh - their rooms built by the market itself - the ore and the mob parts, a new day, favour one
// trade from full, 49 trades): into Dennis's Assay Office - he greets you, right-clicked: his page (the record, the favour,
// a button per lot with today's count); 32 coal handed over - a Token; five a day, the sixth refused; a lot short - "count
// again"; a new day - the counts back to nought. Pistachio's Pantry the same - his common lots, his RARE PARTS page (a wither
// skeleton skull: 5 Tokens), nothing carried (no arrows, no gold). Favour full: Dennis's Prospector's Rune, Pistachio's Tithe
// Seal - and again, earned again. The rune onto a pickaxe in the other hand (not twice), the seal onto a sword; out in the
// world the pickaxe mines its hundredth block - a Token (not with a plain pick, not past the day's 8); the sword slays a
// zombie - a Token. Then the fiftieth trade with each: he joins you - his horn, his cloche; lost, and he gives you another.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const plain = async (iid) => +(((await run(`clear TestRat minecraft:${iid} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); };
  const dd = (d) => d && (d.data || d);
  const press = async (re) => { await sleep(1100); return A.press(re); };       // (a button is a chat command: too many too fast and the server kicks for spam)
  const labels = () => A.buttons().map(b => b.label.replace(/\s+/g, ' ').trim());
  const title = () => JSON.stringify(dd(A.dialogN[A.dialogN.length - 1] || {}).title || '');
  const body = () => JSON.stringify(dd(A.dialogN[A.dialogN.length - 1] || {}).body || '');
  // (a market of its own, as t162's: template (x, y, z) is the world's (CX + x, CY + y, CZ + z); their rooms at template x 31-45, z 75-80, floor y 9)
  const CX = 24000, CY = 30, CZ = 24000;
  const SPOT = { dw: [CX + 34.5, CY + 10, CZ + 79], ps: [CX + 42.5, CY + 10, CZ + 79] };
  const near = k => `x=${SPOT[k][0]},y=${SPOT[k][1]},z=${SPOT[k][2]},distance=..3`;
  const HIT = k => `@e[type=minecraft:interaction,tag=bm.${k}nhit,${near(k)},limit=1]`;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat'); await run('effect clear TestRat minecraft:haste');
  // (a stranger to them both: no trades, no favour, never greeted, neither one walking with you)
  const zero = ['bm.dwt', 'bm.pst', 'bm.dwf', 'bm.psf', 'bm.dwr', 'bm.psr', 'bm.dwmb', 'bm.dwpk', 'bm.pssw', 'bm.dwcl'];
  for (let i = 0; i < 10; i++) zero.push(`bm.dwq${i}`);
  for (let i = 0; i < 22; i++) zero.push(`bm.psq${i}`);
  for (const o of zero) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players operation TestRat bm.dwday = #day bm.bm'); await run('scoreboard players operation TestRat bm.psday = #day bm.bm');
  for (const t of ['bm.dwhi', 'bm.pshi', 'bm.dwmet', 'bm.pimet', 'bm.dwseen', 'bm.psseen']) await run(`tag TestRat remove ${t}`);
  for (const a of ['story/dw_prize', 'story/ps_prize', 'story/dw_join', 'story/pi_join']) await run(`advancement revoke TestRat only bm:${a}`);
  await run('kill @e[type=minecraft:wolf,tag=bm.dwpet]'); await run('kill @e[type=minecraft:wolf,tag=bm.pipet]');
  await run('scoreboard players reset #p162r bm.p162');

  // ================================================================== the stage: a market placed fresh, their rooms built by it
  await run(`${O}forceload add ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (await passes(`${O}execute if entity ${MK}`)) await run(`${O}tag ${MK} remove bm.dp280`);
  else { let pl = ''; for (let t = 0; t < 30; t++) { pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); } console.log('   placed: ' + pl.slice(0, 60)); }
  await at(CX + 38.5, CY + 10, CZ + 72.5, 0, 0);                         // (the alcove between the twin stairs, under the balcony)
  const built = await wait(30000, async () => passes(`${O}execute if entity ${MK.replace(',limit=1', ',tag=bm.dp280,limit=1')}`), 500);
  await sleep(1500);
  ok('a Black Market placed: it digs out their two rooms itself', built);
  ok('Dennis at his counter: his rig (nine parts), his click box', (await cnt(`@e[type=minecraft:item_display,tag=bm.dwn,${near('dw')}]`)) === 9 && (await cnt(HIT('dw'))) === 1,
     `${await cnt(`@e[type=minecraft:item_display,tag=bm.dwn,${near('dw')}]`)} parts, ${await cnt(HIT('dw'))} box`);
  ok('Pistachio in his pantry: his rig (eight parts), his click box', (await cnt(`@e[type=minecraft:item_display,tag=bm.psn,${near('ps')}]`)) === 8 && (await cnt(HIT('ps'))) === 1,
     `${await cnt(`@e[type=minecraft:item_display,tag=bm.psn,${near('ps')}]`)} parts, ${await cnt(HIT('ps'))} box`);
  ok('...the signs over their doors', /ASSAY OFFICE/.test(await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.p162prop,x=${CX + 32.9},y=${CY + 12.6},z=${CZ + 73.96},distance=..0.5,limit=1] text`)) &&
     /PANTRY/.test(await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.p162prop,x=${CX + 42.9},y=${CY + 12.6},z=${CZ + 73.96},distance=..0.5,limit=1] text`)));
  ok('...the doors open, the rooms dug', await passes(`${O}execute if block ${CX + 32} ${CY + 10} ${CZ + 74} minecraft:air`) &&
     await passes(`${O}execute if block ${CX + 34} ${CY + 11} ${CZ + 77} minecraft:air`) && await passes(`${O}execute if block ${CX + 34} ${CY + 9} ${CZ + 77} minecraft:polished_deepslate`));

  const enter = async (k) => { await at(SPOT[k][0], SPOT[k][1], SPOT[k][2] - 2.6, 0, 10); await sleep(1200); };
  const click = async (k) => { const n0 = A.dialogN.length; const h = await entOf(HIT(k)); if (!h) return false; A.slot(7); await sleep(200);
    A.interact(h.entityId); await wait(3000, async () => A.dialogN.length > n0, 100); await sleep(200); return A.dialogN.length > n0; };
  const tokens = () => has('token');

  // ================================================================== Dennis's Assay Office
  A.chats.length = 0; await enter('dw');
  ok('into his office: he greets you (his hello, once)', await wait(3000, async () => /bm\.dwseen/.test(await run('tag TestRat list'))));
  ok('right-clicked: his first words, then his page', (await click('dw')) && A.chats.some(c => /Dennis is the name - ore is the game/.test(c)) && /ASSAY OFFICE/.test(title()),
     A.chats.slice(-2).join(' | ').slice(0, 160));
  ok('...the record (0 of 50) and his favour (0 of 30)', /Trades with Dennis/.test(body()) && /of 50/.test(body()) && /of 30/.test(body()), body().slice(0, 200));
  console.log('   [dennis] ' + labels().join(' | '));
  const DW = ['32 Coal', '32 Raw Copper', '24 Raw Iron', '16 Raw Gold', '48 Redstone Dust', '32 Lapis Lazuli', '32 Nether Quartz', '32 Amethyst Shards', 'Diamond', '2 Ancient Debris'];
  ok('...a button per lot, each with its Tokens and today\'s count', DW.every(l => labels().some(x => x.startsWith(l) && /Token/.test(x) && /0\/\d/.test(x))), labels().join(' | ').slice(0, 300));
  await run('give TestRat minecraft:coal 200'); await sleep(300);
  let t0 = await tokens();
  let pr = await press(/^32 Coal/);
  ok('32 coal handed over: a Token, the coal gone', pr && pr.next && (await tokens()) === t0 + 1 && (await plain('coal')) === 168, `tokens ${await tokens()}, coal ${await plain('coal')}`);
  ok('...his page again: Coal 1/5, a trade on the record, a point of favour', labels().some(l => /^32 Coal.*1\/5/.test(l)) && (await score('bm.dwt')) === 1 && (await score('bm.dwf')) === 1,
     labels().find(l => /Coal/.test(l)));
  for (let i = 0; i < 4; i++) await press(/^32 Coal/);
  ok('...five lots in a day: 5 Tokens', (await tokens()) === t0 + 5 && labels().some(l => /^32 Coal.*5\/5/.test(l)), `${await tokens()}`);
  A.chats.length = 0; await press(/^32 Coal/); await sleep(300);
  ok('...the sixth refused: "That\'s enough Coal for today" - nothing taken', (await tokens()) === t0 + 5 && (await plain('coal')) === 40 && A.chats.some(c => /enough Coal for today/.test(c)),
     A.chats.slice(-1).join(''));
  A.bars.length = 0; await press(/^16 Raw Gold/); await sleep(300);
  ok('a lot short (no raw gold): "That takes 16 Raw Gold, lad - count again"', A.bars.some(b => /That takes 16 Raw Gold/.test(b)) && (await tokens()) === t0 + 5, A.bars.slice(-1).join(''));
  await run('give TestRat minecraft:diamond 3'); await press(/^Diamond/);
  ok('a diamond: 2 Tokens (the Fence\'s rate)', (await tokens()) === t0 + 7 && (await plain('diamond')) === 2);
  await run('scoreboard players set TestRat bm.dwday -1');                  // (a new day)
  await press(/^32 Coal/);
  ok('a new day: the counts back to nought - coal again (1/5)', (await tokens()) === t0 + 8 && labels().some(l => /^32 Coal.*1\/5/.test(l)), labels().find(l => /Coal/.test(l)));
  await run('clear TestRat minecraft:coal'); await run('clear TestRat minecraft:diamond');

  // ================================================================== Pistachio's Pantry
  A.chats.length = 0; await enter('ps');
  ok('into the pantry: right-clicked - his first words, then his page', (await click('ps')) && A.chats.some(c => /Pistachio, at your service/.test(c)) && /PISTACHIO'S PANTRY/.test(title()),
     A.chats.slice(-2).join(' | ').slice(0, 160));
  console.log('   [pistachio] ' + labels().join(' | '));
  ok('...his common lots: flesh, bones, string by the 32', ['32 Rotten Flesh', '32 Bones', '32 String', '16 Spider Eyes', '24 Gunpowder', '8 Ender Pearls'].every(l => labels().some(x => x.startsWith(l))),
     labels().join(' | ').slice(0, 300));
  ok('...nothing a mob carries: no arrows, weapons, gold or nuggets', !labels().some(l => /Arrow|Sword|Bow|Gold|Nugget|Trident/i.test(l)));
  await run('give TestRat minecraft:rotten_flesh 64'); await sleep(300);
  t0 = await tokens();
  await press(/^32 Rotten Flesh/);
  ok('32 rotten flesh: a Token (and a trade, and favour)', (await tokens()) === t0 + 1 && (await plain('rotten_flesh')) === 32 && (await score('bm.pst')) === 1 && (await score('bm.psf')) === 1,
     `${await tokens()} ${await plain('rotten_flesh')}`);
  pr = await press(/Rare parts/);
  ok('"Rare parts »": his rare page - skulls and heads, shells and tears', pr && pr.next && /rare parts/.test(title()) &&
     ['Wither Skeleton Skull', 'Zombie Head', 'Skeleton Skull', 'Creeper Head', 'Shulker Shell', "2 Rabbit's Feet", '2 Ghast Tears'].every(l => labels().some(x => x.startsWith(l))),
     labels().join(' | ').slice(0, 300));
  ok('...a wither skeleton skull: 5 Tokens, 3 a day', labels().some(l => /^Wither Skeleton Skull.*5 Tokens.*0\/3/.test(l)), labels().find(l => /Wither/.test(l)));
  await run('give TestRat minecraft:wither_skeleton_skull 4'); await sleep(200);
  for (let i = 0; i < 3; i++) await press(/^Wither Skeleton Skull/);
  ok('...three skulls: 15 Tokens', (await tokens()) === t0 + 16 && (await plain('wither_skeleton_skull')) === 1, `${await tokens()}`);
  A.chats.length = 0; await press(/^Wither Skeleton Skull/); await sleep(300);
  ok('...the fourth: "The pantry is quite full" - the skull kept', (await plain('wither_skeleton_skull')) === 1 && A.chats.some(c => /quite full of Wither Skeleton Skull/.test(c)), A.chats.slice(-1).join(''));
  pr = await press(/Common lots/);
  ok('"« Common lots": back to the front page', pr && pr.next && /PISTACHIO'S PANTRY"/.test(title()) || (pr && pr.next && !/rare parts/.test(title())));
  await run('clear TestRat minecraft:rotten_flesh'); await run('clear TestRat minecraft:wither_skeleton_skull');

  // ================================================================== favour full: the rune and the seal - earned, then earned again
  await run('execute as TestRat run function bm:admin/favour_full');
  await enter('dw'); await click('dw');
  await run('give TestRat minecraft:raw_iron 48'); A.chats.length = 0;
  await press(/^24 Raw Iron/); await sleep(500);
  ok('Dennis\'s favour full: his Prospector\'s Rune', (await has('prospector_rune')) === 1 && A.chats.some(c => /Take my rune/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 160));
  ok('...the favour starts again (0), a rune on his record, its achievement', (await score('bm.dwf')) === 0 && (await score('bm.dwr')) === 1 &&
     await passes('execute if entity @a[name=TestRat,advancements={bm:story/dw_prize=true}]'));
  ok('...the page says so (favour 0 of 30)', /"0"/.test(body()) || /0.{0,40}of 30/.test(body()));
  await run('scoreboard players set TestRat bm.dwf 29'); await press(/^24 Raw Iron/); await sleep(300);
  ok('...and earned again the same way: a second rune (renewable, never free)', (await has('prospector_rune')) === 2 && (await score('bm.dwr')) === 2);
  await enter('ps'); await click('ps');
  await run('give TestRat minecraft:bone 32'); A.chats.length = 0;
  await press(/^32 Bones/); await sleep(500);
  ok('Pistachio\'s favour full: his Tithe Seal', (await has('tithe_seal')) === 1 && (await score('bm.psf')) === 0 && A.chats.some(c => /Tithe Seal/.test(c)),
     A.chats.slice(-2).join(' | ').slice(0, 160));
  await run('clear TestRat minecraft:raw_iron'); await run('clear TestRat minecraft:bone');

  // ================================================================== out in the world: the rune on a pickaxe, the seal on a sword
  const X = 16700, Y = 100, Z = 16000;
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 30);
  // (the runes and the seal earned above are put away first: each step below counts from none)
  await run('clear TestRat *[minecraft:custom_data~{bm:"prospector_rune"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"tithe_seal"}]');
  await run('item replace entity TestRat hotbar.0 with minecraft:air');
  await run('loot replace entity TestRat hotbar.1 loot bm:items/prospector_rune');
  A.bars.length = 0; await use(1);
  ok('the rune used with nothing in the other hand: "Hold the pickaxe to upgrade in your other hand"', A.bars.some(b => /Hold the pickaxe/.test(b)) && (await has('prospector_rune')) === 1, A.bars.slice(-1).join(''));
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond_pickaxe[minecraft:enchantments={"minecraft:efficiency":5}]');
  await sleep(2200); A.bars.length = 0; await use(1);
  const off = await run('data get entity TestRat equipment.offhand');
  ok('...with a pickaxe in the other hand: the pickaxe takes it (its lore), the rune used up', /bm_pros: 1b/.test(off) && /Prospector's Rune/.test(off) && (await has('prospector_rune')) === 0,
     off.replace(/.*data: /, '').slice(0, 200));
  await run('loot replace entity TestRat hotbar.1 loot bm:items/prospector_rune'); await sleep(2200); A.bars.length = 0; await use(1);
  ok('...a second rune on the same pickaxe: "That pickaxe has one already" - kept', A.bars.some(b => /has one already/.test(b)) && (await has('prospector_rune')) === 1, A.bars.slice(-1).join(''));
  await run('clear TestRat *[minecraft:custom_data~{bm:"prospector_rune"}]');
  A.slot(0); await sleep(200); A.swap(); await sleep(500);                 // (F: the pickaxe into the main hand)
  ok('F: the upgraded pickaxe in hand', /bm_pros/.test(await run('data get entity TestRat SelectedItem')));
  await run('effect give TestRat minecraft:haste 600 1 true');
  const dig = async (x, y, z) => { await A.mine(x, y, z, 120); await sleep(700); };
  await run('scoreboard players set TestRat bm.dwmb 99'); await run('scoreboard players set #p162r bm.p162 1');
  t0 = await tokens(); A.bars.length = 0;
  await dig(X + 1, Y, Z + 1); await sleep(800);
  ok('its hundredth block mined: "Your Prospector\'s Rune turns up a Token!" - a Token', await passes(`${O}execute if block ${X + 1} ${Y} ${Z + 1} minecraft:air`) &&
     (await tokens()) === t0 + 1 && A.bars.some(b => /Rune turns up a Token/.test(b)), `tokens ${await tokens()} (was ${t0}), count ${await score('bm.dwmb')}`);
  ok('...the count starts its next hundred', (await score('bm.dwmb')) === 0, `${await score('bm.dwmb')}`);
  await run('scoreboard players set TestRat bm.dwmb 99'); await run('scoreboard players set TestRat bm.dwpk 8'); await run('scoreboard players operation TestRat bm.dwpkd = #day bm.bm');
  t0 = await tokens(); await dig(X + 2, Y, Z + 1); await sleep(800);
  ok('...but not past the day\'s 8 (a cobblestone generator makes no mint)', (await tokens()) === t0 && (await score('bm.dwmb')) === 0, `${await tokens()} ${await score('bm.dwmb')}`);
  await run('item replace entity TestRat weapon.mainhand with minecraft:diamond_pickaxe[minecraft:enchantments={"minecraft:efficiency":5}]');
  await run('scoreboard players set TestRat bm.dwmb 99'); await run('scoreboard players set TestRat bm.dwpk 0');
  t0 = await tokens(); await dig(X + 3, Y, Z + 1); await sleep(800);
  ok('a plain pickaxe: no count, no Token', (await tokens()) === t0 && (await score('bm.dwmb')) === 99, `${await tokens()} ${await score('bm.dwmb')}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..10]`);
  // (the seal)
  await run('item replace entity TestRat weapon.mainhand with minecraft:air');
  await run('item replace entity TestRat weapon.offhand with minecraft:iron_sword');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/tithe_seal'); await sleep(2200);
  A.bars.length = 0; await use(2);
  const off2 = await run('data get entity TestRat equipment.offhand');
  ok('the Tithe Seal with a sword in the other hand: pressed into it (its lore), the seal used up', /bm_tithe: 1b/.test(off2) && /Tithe Seal/.test(off2) && (await has('tithe_seal')) === 0,
     off2.replace(/.*data: /, '').slice(0, 200));
  A.slot(2); await sleep(200); A.swap(); await sleep(500);
  await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y + 1} ${Z + 2.2} {NoAI:1b,Health:1f,PersistenceRequired:1b,Tags:["bm.t182z","bm.seen"],equipment:{head:{id:"minecraft:leather_helmet",count:1}},drop_chances:{head:0f}}`); await sleep(800);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 20);
  t0 = await tokens(); A.bars.length = 0;
  const zs = '@e[type=minecraft:zombie,tag=bm.t182z,limit=1]'; let z = null; await wait(3000, async () => (z = await entOf(zs)) != null);
  if (z) A.attack(z.entityId); await sleep(1500);
  ok('the sealed sword slays a zombie: "the departed leave a Token!" - a Token', (await cnt(zs)) === 0 && (await tokens()) === t0 + 1 && A.bars.some(b => /departed leave a Token/.test(b)),
     `zombie ${await cnt(zs)}, tokens ${await tokens()} (was ${t0})`);
  await run('scoreboard players reset #p162r bm.p162'); await run('effect clear TestRat minecraft:haste');
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..10]`); await run(`${O}kill @e[tag=bm.t182z]`);

  // ================================================================== the fiftieth trade: he joins you
  await run('execute as TestRat run function bm:admin/trades_50');
  for (let i = 0; i < 10; i++) await run(`scoreboard players set TestRat bm.dwq${i} 0`);
  for (let i = 0; i < 22; i++) await run(`scoreboard players set TestRat bm.psq${i} 0`);
  await enter('dw'); await click('dw');
  ok('49 trades with Dennis: "49 of 50 - and he joins you"', /49/.test(body()) && /joins you/.test(body()), body().slice(0, 160));
  await run('give TestRat minecraft:raw_copper 32'); A.chats.length = 0;
  await press(/^32 Raw Copper/); await sleep(800);
  ok('the fiftieth: Dennis joins you - his Horn', (await has('dw_horn')) === 1 && /bm\.dwmet/.test(await run('tag TestRat list')) && A.chats.some(c => /Fifty trades/.test(c)),
     A.chats.slice(-3).join(' | ').slice(0, 200));
  ok('...his achievement (Thick as Thieves); his page says he walks with you', await passes('execute if entity @a[name=TestRat,advancements={bm:story/dw_join=true}]') &&
     /walks with you now/.test(body()), body().slice(0, 160));
  // (2.82t: a lost horn is no longer handed out for a click - fifty trades without it earn another)
  await run('clear TestRat *[minecraft:custom_data~{bm:"dw_horn"}]'); A.chats.length = 0; await sleep(600);
  await click('dw'); await sleep(300);
  ok('the horn lost: right-clicked, no free horn (2.82t)', (await has('dw_horn')) === 0 && !A.chats.some(c => /Good thing I've two/.test(c)));
  await run('scoreboard players set TestRat bm.dwlost 48');                // (48 trades already made without it)
  for (let i = 0; i < 10; i++) await run(`scoreboard players set TestRat bm.dwq${i} 0`);
  await run('give TestRat minecraft:raw_copper 64'); A.bars.length = 0;
  await press(/^32 Raw Copper/); await sleep(800);
  ok('...a trade without it: "1 more trades and Dennis trusts you with another"', (await has('dw_horn')) === 0 && A.bars.some(b => /1 more trades and Dennis/.test(b)), A.bars.slice(-1).join(''));
  A.chats.length = 0; await press(/^32 Raw Copper/); await sleep(800);
  ok('...the fiftieth trade without it: another horn ("Good thing I\'ve two")', (await has('dw_horn')) === 1 && A.chats.some(c => /Good thing I've two/.test(c)), A.chats.slice(-1).join(''));
  await enter('ps'); await click('ps');
  await run('give TestRat minecraft:string 32'); A.chats.length = 0;
  await press(/^32 String/); await sleep(800);
  ok('the fiftieth with Pistachio: he joins you - his Little Cloche', (await has('pi_cloche')) === 1 && /bm\.pimet/.test(await run('tag TestRat list')) && A.chats.some(c => /Fifty transactions/.test(c)),
     A.chats.slice(-3).join(' | ').slice(0, 200));
  ok('...his achievement (Service Included)', await passes('execute if entity @a[name=TestRat,advancements={bm:story/pi_join=true}]'));

  // ---------------------------------------------------------------- clean up
  await run('clear TestRat'); await run('effect clear TestRat');
  for (const o of zero) await run(`scoreboard players set TestRat ${o} 0`);
  await at(CX + 38.5, CY + 10, CZ + 72.5, 0, 0);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
