// 2.78: the Recruiter only deals in names you know - as a regular (non-op) player, every step a real packet: into the Lounge
// with the Ledger (its own buttons), a click on the Recruiter - his book. Before you've met anyone: no follower's contract
// on it, only the hirelings' and the vault gems' pages (and nothing free - no Cecil). Celi met (her Moon Charm held): her
// contract on his book, bought from the wallet, then "IN YOUR PACK"; used - signed; "SIGNED" on his book. A contract for a
// follower you haven't met won't sign, and keeps. A hireling's contract and a vault gem bought from their pages. His
// villager has no trades left. (rcon sets the stage only: a platform, coins in the bank, the charm, a stray contract.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const labels = () => A.buttons().map(b => b.label.replace(/[^\x20-\x7e]/g, '').replace(/\s+/g, ' ').trim());
  const shown = () => JSON.stringify(A.dialogN[A.dialogN.length - 1] || {});
  const uuidStr = async (sel) => { const m = (await run(`execute in bm:gutter run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const O = 'execute in minecraft:overworld run ';
  const HX = 13000, HY = 121, HZ = 13000;
  const KINDS = ['cecil', 'emma', 'celi', 'zib', 'killerwatt', 'leo', 'demo', 'escort', 'apo', 'tul', 'frog', 'donado', 'fishy', 'dennis', 'pistachio', 'omega', 'ashur', 'chef', 'neighbor', 'ava', 'pearlq', 'bloo', 'stalker', 'lantern', 'bender', 'bones'];
  const A = await bot('TestRat'); await sleep(2500);
  // ---- the stage: a newcomer to the vault who has met no one
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvwaitd', 'bm.lgch', 'bm.lkch']) await run(`tag TestRat remove ${t}`);
  for (const k of KINDS) await run(`advancement revoke TestRat only bm:met/${k}`);
  await run('scoreboard players set TestRat bm.fcon 0'); await run('scoreboard players set TestRat bm.crew 0'); await run('scoreboard players set TestRat bm.gvhr 0'); await run('scoreboard players set TestRat bm.gbc 3000');
  await run('loot give TestRat loot bm:items/fixers_ledger');
  await sleep(1500); A.stand(); await sleep(500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player (no operator commands)', /unknown|incomplete|permission/i.test(A.chats.join(' ')), A.chats.slice(-1).join('').slice(0, 120));

  // ---- into the Lounge the way a player goes: the Ledger, the Office, "The Fixer's Lounge", stand still
  A.slot(0); await sleep(300); await A.useWait();
  A.click(/Fixer's Lounge/); await wait(8000, async () => /gutter/.test(await dim())); await sleep(2500); A.stand();
  ok('Into the Fixer\'s Lounge with the Ledger', /gutter/.test(await dim()));
  const hit = '@e[type=minecraft:interaction,tag=bm.rechit,x=-321,y=60,z=-257,dx=26,dy=20,dz=26,limit=1]';
  ok('The Recruiter has a counter to click (his old trades replaced by his book)', await wait(3000, async () => /passed/.test(await run(`execute in bm:gutter if entity ${hit}`))));
  const trades = await run('execute in bm:gutter run data get entity @e[type=minecraft:villager,tag=bm.gvrec,x=-321,y=60,z=-257,dx=26,dy=20,dz=26,limit=1] Offers.Recipes');
  ok('...and his villager sells nothing any more', /\[\]|Found no elements/.test(trades), trades.replace(/.*data: /, '').slice(0, 80));
  await run(`execute in bm:gutter at ${hit} rotated 0 0 positioned ^ ^ ^-1.6 run tp TestRat ~ ~ ~ 0 0`); await sleep(1500);
  const eu = await uuidStr(hit); const ent = Object.values(A.ents).find(e => e.objectUUID === eu);
  const open = async () => { const n0 = A.dialogN.length; A.interact(ent.entityId); await wait(2500, async () => A.dialogN.length > n0, 100); await sleep(200); };
  ok('(the bot sees his counter)', !!ent);

  // ---- 1. met no one: no follower's contract on his book, nothing free
  await open();
  console.log('   [book] ' + labels().join(' | '));
  ok('Click the Recruiter: his book opens', /THE RECRUITER/.test(shown()));
  ok('...no follower\'s contract on it (not even Cecil\'s) - met no one yet', !labels().some(l => /Cecil|Emma|Celi|Zib|KillerWatt|Leo|Democratus|Skiff|Apophiss|Tullius|Frog|Donado/.test(l)), labels().join(' | '));
  ok('...it says so ("No names on his books yet"), and counts "0 of N" (the full roster, 2.87: Ava, Pearl, Bloo)', /No names on his books yet/.test(shown()) && /"0"/.test(shown()) && /of [12]\d/.test(shown()));
  ok('...the hirelings\' and the vault gems\' pages are there', labels().some(l => /Hirelings/.test(l)) && labels().some(l => /Vault gems/.test(l)));

  // ---- 2. a contract for someone you haven't met won't sign - and keeps
  await run('loot replace entity TestRat hotbar.3 loot bm:items/fcontract_leo');
  A.chats.length = 0; A.slot(3); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(900);
  ok('A Raid Contract for Leo, whom you haven\'t met, won\'t sign: "find them out in the world first"', /haven't met them yet/i.test(A.chats.join(' ')) && (await sc('TestRat', 'bm.fcon')) === 0,
     A.chats.slice(-1).join('').slice(0, 140));
  ok('...and the contract keeps', (await has('fcontract_leo')) === 1);
  await run('clear TestRat *[minecraft:custom_data~{bm:"fcontract_leo"}]');

  // ---- 3. Celi met (her Moon Charm in your pocket): her contract is on his book
  await run('loot replace entity TestRat hotbar.4 loot bm:items/celi_charm');
  ok('Holding Celi\'s Moon Charm: you\'ve met her (bm:met/celi)', await wait(3000, async () => /passed/.test(await run('execute if entity @a[name=TestRat,advancements={bm:met/celi=true}]'))));
  await open();
  console.log('   [book] ' + labels().join(' | '));
  const celi = labels().find(l => /^Celi /.test(l));
  ok('His book now has Celi\'s contract, priced in coins', !!celi && /\d+ coins/.test(celi) && /"1"/.test(shown()), celi);
  ok('...and still no one else\'s', labels().filter(l => /Cecil|Emma|Zib|KillerWatt|Leo|Democratus|Skiff|Apophiss|Tullius|Frog|Donado/.test(l)).length === 0);
  const price = +((celi || '').match(/(\d+) coins/) || [0, 0])[1];
  const bank0 = await sc('TestRat', 'bm.gbc');
  const pr = await A.press(/^Celi /);
  ok('Press it: you pay, and the Recruiter hands you Raid Contract: Celi', (await has('fcontract_celi')) === 1 && (await sc('TestRat', 'bm.gbc')) === bank0 - price, `${bank0} -> ${await sc('TestRat', 'bm.gbc')} (price ${price})`);
  ok('...his book again: Celi "IN YOUR PACK"', !!pr && pr.next && labels().some(l => /^Celi IN YOUR PACK/.test(l)), labels().join(' | '));
  A.chats.length = 0; await A.press(/^Celi /);
  ok('...pressed again: "use it to sign Celi on" - no second sale', /use it to sign Celi on/.test(A.chats.join(' ')) && (await has('fcontract_celi')) === 1);
  // (use it, as an item)
  const cs = +(((await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"fcontract_celi"}}}].Slot')).match(/(\d+)b?\s*$/) || [0, -1])[1]);
  if (cs !== 5) await run(`item replace entity TestRat hotbar.5 from entity TestRat container.${cs}`), await run(`item replace entity TestRat container.${cs} with minecraft:air`);
  A.chats.length = 0; A.slot(5); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(900);
  ok('Use the contract: Celi is signed for the vault', ((await sc('TestRat', 'bm.fcon')) & 4) === 4 && (await has('fcontract_celi')) === 0, `${A.chats.slice(-1).join('').slice(0, 120)}`);
  await open();
  ok('...his book: Celi "SIGNED"', labels().some(l => /^Celi SIGNED/.test(l)), labels().join(' | '));

  // ---- 4. the hirelings' page and the vault gems' page
  let p = await A.press(/Hirelings/);
  console.log('   [hirelings] ' + labels().join(' | '));
  ok('"Hirelings": five contracts and a way back', !!p && p.next && labels().filter(l => /coins/.test(l)).length === 5 && labels().some(l => /The Recruiter/.test(l)));
  const h = labels().find(l => /coins/.test(l)); const hp = +h.match(/(\d+) coins/)[1]; const hb = await sc('TestRat', 'bm.gbc');
  await A.press(new RegExp('^' + h.split(' ')[0]));
  ok(`...buy ${h.split(' ')[0]}'s: paid, and the contract is yours`, (await sc('TestRat', 'bm.gbc')) === hb - hp && (await run('clear TestRat *[minecraft:custom_data~{bm:"contract_brawler"}] 0')).includes('Found 1'),
     `${hb} -> ${await sc('TestRat', 'bm.gbc')}`);
  p = await A.press(/The Recruiter/);
  ok('..."« The Recruiter" goes back to his book', !!p && p.next && /THE RECRUITER/.test(shown()));
  p = await A.press(/Vault gems/);
  console.log('   [gems] ' + labels().join(' | '));
  ok('"Vault gems": the nine and a way back', !!p && p.next && labels().filter(l => /coins/.test(l)).length === 9);
  const g = labels().find(l => /Fire Gem/.test(l)); const gp = +g.match(/(\d+) coins/)[1]; const gb = await sc('TestRat', 'bm.gbc');
  await A.press(/Fire Gem/);
  const gem = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"gem_fire"}}}].components."minecraft:custom_data"');
  ok('...buy the Fire Gem: paid, and it\'s the vault\'s own (it stays in the vault)', (await sc('TestRat', 'bm.gbc')) === gb - gp && /bm_vault: 1b/.test(gem), gem.replace(/.*data: /, ''));

  // ---- the stage put back
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.fcon 0'); await run('scoreboard players set TestRat bm.crew 0'); await run('scoreboard players set TestRat bm.gbc 0');
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(2000);
  await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
