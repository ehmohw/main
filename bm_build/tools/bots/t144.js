// 2.78: "never used up" items really aren't, as a regular (non-op) player. (In 26.3 a used consumable is taken from the hand
// AFTER its advancement runs, so the old hand-it-straight-back saw it still there, gave nothing - and the item was gone.) The
// Tome of Blinking blinks you 7 blocks and stays in your hand; a Jackpot card's play leaves the next card (one fewer play) in
// your hand; a lucky map piece, read, stays - and the ninth makes the map with no piece left over. (The Warpstone and Wilfrey's
// locket: t143; the raid kit's abilities, which only live in the vault: t80.) rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const inHand = async (iid) => new RegExp(`"${iid}"`).test(await nbt('TestRat', 'SelectedItem.components."minecraft:custom_data".bm'));
  const X = 16600, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2500, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const useSlot = async (s, ms) => { A.slot(s); await sleep(300); A.use(); await sleep(ms); A.release(); await sleep(600); };

  // ---------------------------------------------------------------- the Tome of Blinking
  await at(X + 0.5, Y + 1, Z - 6.5, 0, 0);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/blink_tome');
  await useSlot(0, 900);
  ok('the Tome of Blinking blinks you 7 blocks ahead', await wait(2000, async () => A.pos && Math.abs(A.pos.z - (Z + 0.5)) < 0.3), A.pos ? `z ${A.pos.z.toFixed(2)}` : '');
  ok('...and stays in your hand (not used up)', await wait(1500, async () => await inHand('blink_tome')) && (await has('TestRat', 'blink_tome')) === 1);
  await sleep(8200);                                                 // (its 8-second cooldown)
  await useSlot(0, 900);
  ok('...and blinks again, after its cooldown', await wait(2000, async () => A.pos && Math.abs(A.pos.z - (Z + 7.5)) < 0.3) && (await has('TestRat', 'blink_tome')) === 1, A.pos ? `z ${A.pos.z.toFixed(2)}` : '');

  // ---------------------------------------------------------------- a Jackpot scratch card: the next card, in the same hand
  await run('clear TestRat'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await run('loot replace entity TestRat hotbar.2 loot bm:items/jackpot_card_5');
  A.bars.length = 0; await useSlot(2, 1400);
  ok('a play on a fresh Jackpot card: the card in your hand now shows four plays', await wait(1500, async () => await inHand('jackpot_card_4')) &&
     (await has('TestRat', 'jackpot_card_5')) === 0 && (await has('TestRat', 'jackpot_card_4')) === 1, A.bars.slice(-1).join('').slice(0, 80));
  await sleep(1500);                                                 // (the scratch reveals itself half a second later)
  await useSlot(2, 1400);
  ok('...another: three', await wait(1500, async () => await inHand('jackpot_card_3')) && (await has('TestRat', 'jackpot_card_4')) === 0);

  // ---------------------------------------------------------------- lucky map pieces: read, they stay; the ninth makes the map, none over
  await run('clear TestRat');
  for (let k = 1; k <= 8; k++) await run(`loot give TestRat loot bm:items/lucky_fragment_${k}`);     // (hotbar 0..7)
  A.bars.length = 0; await useSlot(0, 1100);
  ok('a lucky map piece, read: "8 / 9" - and the piece stays', await wait(1500, async () => (await has('TestRat', 'lucky_fragment_1')) === 1) && /8/.test(A.bars.join(' ')),
     `${A.bars.slice(-1).join('').slice(0, 80)} pieces ${await has('TestRat', 'lucky_fragment_1')}`);
  await run('loot give TestRat loot bm:items/lucky_fragment_9');                                        // (hotbar 8)
  A.titles.length = 0; await useSlot(8, 1100);
  await sleep(600);
  let left = 0; for (let k = 1; k <= 9; k++) left += await has('TestRat', `lucky_fragment_${k}`);
  ok('the ninth piece read: the nine fit together (THE GILDED ROOST) - none left over', A.titles.some(t => /GILDED ROOST/.test(t)) && left === 0, `${left} pieces left`);

  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
