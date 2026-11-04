// 3.0k: THE MENUS, TIDIED (phase261), as a regular (non-op) player pressing what the client was sent - every screen's buttons are
// routed in BUTTON_CODES.md, and every page is walked:
//   wheel     12 partners on it: page 1 has 8 "Call" rows, "Page 1 of 2" and Next ›; Next: the other 4 and ‹ Previous; Previous:
//             page 1 again. No Chatter / Keep up rows; "⚙ Your settings": its page (Keep up, chatter), « Back: the wheel.
//   bank      the Banker's Card: the account page - the four balances in its text, Currencies › and the account's own buttons, no
//             currency rows; Currencies ›: the 13, « Your account; Tokens: its page (Deposit all); « back: the account.
//   crew      the Fixer's Ledger -> Raid Crew: "N on" in the title, "? How the crew works" (its tooltip the rules), pressed: the page.
//   outfits   Raid Crew -> Outfits (every follower met: 51 wardrobes): page 1 of 5, Next to page 3, Previous to 2; a wardrobe
//             from page 2 opens; the page is remembered when you come back.
//   recruiter his book (opened as his NPC does - he stands in the den): 51 names, paged; Hirelings › on every page and back.
//   tailor    the same for the Tailor's followers.
//   node t386.js [wheel|bank|crew|outfits|recruiter|tailor]
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '../..');
const ONLY = process.argv.slice(2);
const on = (s) => !ONLY.length || ONLY.includes(s);
const legend = fs.readFileSync(path.join(ROOT, 'BUTTON_CODES.md'), 'utf8');
const routed = new Set(); for (const l of legend.split('\n')) { const m = l.match(/^\| (\d+)(?: \(link\))? \|.*\| ([^|]*) \|$/); if (m && !/not routed/.test(m[2])) routed.add(+m[1]); }
const MET = fs.readdirSync(path.join(ROOT, 'out_p2/BlackMarket_DP/data/bm/advancement/met')).map(f => f.replace('.json', ''));

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const X = 16880, Y = 100, Z = 16180;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  { const p0 = A.press.bind(A); A.press = async (re, ms) => { await sleep(700); return p0(re, ms); }; }
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true');
  await run(`${O}forceload add ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`);
  await run(`${O}fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} minecraft:grass_block`); await run(`${O}fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 5} ${Z + 6} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
  const shown = () => { const d = A.dialogN[A.dialogN.length - 1] || {}; return d.data || d; };
  const title = () => JSON.stringify(shown().title || '');
  const body = () => JSON.stringify(shown().body || '');
  const labels = () => A.buttons().map(b => b.label);
  const acts = () => JSON.stringify(shown().actions || '');      // (a page number or a greyed arrow has no action: not a button the client can press)
  const unrouted = () => A.buttons().filter(b => /bm\.act set \d+/.test(b.command) && !routed.has(+b.command.match(/set (\d+)/)[1])).map(b => b.label);
  const R0 = (n) => ok(`${n}: every button on it routed`, !unrouted().length, unrouted().join(', '));
  const use = async (slot, sneak = false) => { await run('scoreboard players set TestRat bm.gvhc 0'); const n0 = A.dialogN.length; A.slot(slot); await sleep(200);
    if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(350); A.release(); A.input({}); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const allMet = async (yes) => { for (const m of MET) await run(`advancement ${yes ? 'grant' : 'revoke'} TestRat only bm:met/${m}`); };

  if (on('wheel')) {
    const pid = +((await run('scoreboard players get TestRat bm.pid')).match(/has (-?\d+)/) || [0, 0])[1];
    for (let i = 0; i < 60; i++) await run(`scoreboard players set TestRat bm.pw${i} ${i < 12 ? 1 : 0}`);
    await run('tag TestRat remove bm.pwfo'); await run('tag TestRat remove bm.pwaz'); await run('scoreboard players set TestRat bm.pg_wh 0');
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel');
    await use(0);
    const calls = () => labels().filter(l => /^\W*\s*(Call|Send) /.test(l) && !/Send all|Bring them|Team/.test(l));
    ok('the wheel, 12 partners on it: page 1 - 8 partner rows, "Page 1 of 2", Next ›, no ‹ Previous to press', calls().length === 8 && acts().includes('Page 1 of 2') &&
       A.buttons().some(b => /^Next/.test(b.label) && b.command), labels().join(' | ').slice(0, 300));
    ok('...no Chatter or Keep up rows (they\'re on Your settings), and ⚙ Your settings', !labels().some(l => /^Chatter|^Keep up/.test(l)) && labels().some(l => /Your settings/.test(l)));
    R0('...page 1');
    const first = calls()[0];
    let p = await A.press(/^Next/);
    ok('...Next ›: page 2 of 2 - the other 4, ‹ Previous', p && p.next && calls().length === 4 && acts().includes('Page 2 of 2') && !calls().includes(first), calls().join(' | '));
    R0('...page 2');
    p = await A.press(/Previous/);
    ok('...‹ Previous: page 1 again', p && p.next && calls().length === 8 && calls()[0] === first);
    await use(0);
    ok('...used again: the page you were on (1)', acts().includes('Page 1 of 2'));
    await A.press(/^Next/); await use(0);
    ok('...on page 2, used again: still page 2 (remembered)', acts().includes('Page 2 of 2'));
    p = await A.press(/Your settings/);
    ok('...⚙ Your settings: its page, with Keep up and chatter', p && p.next && /YOUR SETTINGS/.test(title()) && labels().some(l => /^Keep up/.test(l)) && labels().some(l => /chatter/.test(l)));
    R0('...Your settings');
    p = await A.press(/« Back/);
    ok('...« Back: the wheel', p && p.next && /Page \d of 2/.test(acts()));
    for (let i = 0; i < 60; i++) await run(`scoreboard players set TestRat bm.pw${i} 0`);
    await run(`data remove storage bm:pw p${pid}`); await run('clear TestRat');
  }

  if (on('bank')) {
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/bankers_card');
    await run('scoreboard players set TestRat bm.bk_tok 7'); await run('scoreboard players set TestRat bm.bk_med 3');
    await use(0);
    ok('the Banker\'s Card: the account - its text shows Tokens 7 and Medallions 3', /Rat Bank/.test(title()) && /"7"/.test(body()) && /"3"/.test(body()) && /Medallions/.test(body()), body().slice(0, 200));
    ok('...Currencies ›, Deposit everything, Savings, Exchange, Auto-deposit, Community Pots, Send to a player - and no currency rows',
       ['Currencies', 'Deposit everything', 'Savings', 'Exchange', 'Auto-deposit', 'Community Pots', 'Send to a player'].every(w => labels().some(l => l.includes(w))) &&
       !labels().some(l => /^Tokens|^Royal Pearls/.test(l)) && labels().length <= 10, labels().join(' | '));
    R0('...the account page');
    let p = await A.press(/^Currencies/);
    const cur = labels().filter(l => !/«/.test(l));
    ok('...Currencies ›: all 13, and « Your account', p && p.next && /currencies/.test(title()) && cur.length === 13 && labels().some(l => /« Your account/.test(l)), labels().join(' | '));
    R0('...the currencies page');
    p = await A.press(/^Tokens/);
    ok('...Tokens: its own page (deposit and take out)', p && p.next && labels().some(l => /Deposit all Tokens/.test(l)), labels().join(' | ').slice(0, 200));
    R0('...the Tokens page');
    p = await A.press(/« Back to your account|« Your account/);
    ok('...« back: the account page', p && p.next && labels().some(l => /^Currencies/.test(l)));
    await A.press(/^Currencies/); p = await A.press(/« Your account/);
    ok('...and from Currencies, « Your account: the account page', p && p.next && labels().some(l => /^Currencies/.test(l)));
    await run('clear TestRat');
  }

  if (on('crew') || on('outfits')) {
    await allMet(true);
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
    await use(0); let p = await A.press(/Raid Crew/);
    if (on('crew')) {
      const how = A.buttons().find(b => /How the crew works/.test(b.label));
      ok('the Fixer\'s Ledger -> Raid Crew: "N on" in the title, and "? How the crew works"', p && p.next && /\d+ on/.test(title()) && !!how, title().slice(0, 200));
      const tip = JSON.stringify(((shown().actions || []).find(a => /How the crew works/.test(JSON.stringify(a.label))) || {}).tooltip || '');
      ok('...its tooltip has the rules (switch on, who comes first, hirelings)', /switch/.test(tip) && /Hirelings|hirelings/.test(tip), tip.slice(0, 160));
      R0('...the crew page');
      p = await A.press(/How the crew works/);
      ok('...pressed: the crew page again', p && p.next && /RAID CREW/.test(title()));
    }
    if (on('outfits')) {
      await run('scoreboard players set TestRat bm.pg_ow 0');
      p = await A.press(/^Outfits/);
      const wd = () => labels().filter(l => /'s wardrobe$/.test(l));
      ok('Raid Crew -> Outfits, every follower met: page 1 - 12 wardrobes, Next ›', p && p.next && wd().length === 12 && labels().some(l => /^Next.*1\/5/.test(l)), labels().join(' | ').slice(0, 300));
      R0('...Outfits page 1');
      const w1 = wd()[0];
      await A.press(/^Next/); p = await A.press(/^Next/);
      ok('...Next twice: page 3 of 5, other wardrobes', p && p.next && labels().some(l => /^Next.*3\/5/.test(l)) && !wd().includes(w1), labels().join(' | ').slice(0, 200));
      p = await A.press(/Previous/);
      const w2 = wd()[0];
      ok('...‹ Previous: page 2', p && p.next && labels().some(l => /^Next.*2\/5/.test(l)));
      R0('...Outfits page 2');
      p = await A.press(new RegExp('^' + w2.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$'));
      ok(`...${w2}: their wardrobe`, p && p.next && /wardrobe/.test(title()), title().slice(0, 100));
      p = await A.press(/« Outfits/);
      ok('...« Outfits & buffs: back on page 2 (remembered)', p && p.next && labels().some(l => /^Next.*2\/5/.test(l)), labels().join(' | ').slice(0, 200));
      // the last page: whatever's left, no Next to press, the buffs and « Raid Crew still there
      await A.press(/^Next/); await A.press(/^Next/); p = await A.press(/^Next/);
      ok('...the last page (5 of 5): the rest, Next greyed, « Raid Crew still there', p && p.next && wd().length === 51 - 48 &&
         !A.buttons().some(b => /^Next/.test(b.label) && b.command) && labels().some(l => /« Raid Crew/.test(l)), labels().join(' | ').slice(0, 300));
      R0('...Outfits page 5');
    }
  }

  if (on('recruiter')) {
    await allMet(true);
    await run('scoreboard players set TestRat bm.pg_rc 0');
    await run('execute as TestRat at @s run function bm:p137/rc/main'); await sleep(800);     // (the stage: as his NPC's click does - he's in the den)
    const names = () => labels().filter(l => / coins$|SIGNED|FILED|IN YOUR PACK/.test(l));
    ok('the Recruiter, 51 met: page 1 - 12 names, Hirelings ›, Next ›', names().length === 12 && labels().some(l => /^Hirelings/.test(l)) && labels().some(l => /^Next.*1\/5/.test(l)),
       labels().join(' | ').slice(0, 300));
    R0('...his page 1');
    let p = await A.press(/^Next/);
    ok('...Next: page 2, Hirelings › still there', p && p.next && labels().some(l => /^Next.*2\/5/.test(l)) && labels().some(l => /^Hirelings/.test(l)));
    p = await A.press(/^Hirelings/);
    ok('...Hirelings ›: their page', p && p.next && /HIRELINGS/.test(title()));
    R0('...the hirelings\' page');
    p = await A.press(/« The Recruiter/);
    ok('...« The Recruiter: back on page 2', p && p.next && labels().some(l => /^Next.*2\/5/.test(l)));
  }

  if (on('tailor')) {
    await allMet(true);
    await run('scoreboard players set TestRat bm.pg_tl 0');
    await run('execute as TestRat at @s run function bm:p103/tl/main'); await sleep(800);     // (the stage: the Tailor stands in the den)
    ok('the Tailor, 51 met: page 1 - Next ›, Display cases', labels().some(l => /^Next.*1\/5/.test(l)) && labels().some(l => /Display cases/.test(l)), labels().join(' | ').slice(0, 300));
    R0('...his page 1');
    let p = await A.press(/^Next/);
    const f = labels().find(l => !/Next|Previous|Display cases|Auras|«/.test(l));
    ok('...Next: page 2', p && p.next && labels().some(l => /^Next.*2\/5/.test(l)));
    p = await A.press(new RegExp('^' + f.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$'));
    ok(`...${f}: their stock`, p && p.next && /the Tailor/.test(title()), title().slice(0, 100));
    R0('...their stock');
    p = await A.press(/« The Tailor/);
    ok('...« The Tailor: back on page 2', p && p.next && labels().some(l => /^Next.*2\/5/.test(l)));
  }
  await allMet(false); await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
