// 2.77: the new pairs and trios, as a regular (non-op) player - every follower called with its own item (used as an item):
// Tullius + Celi ("Frost and Brine"), Tullius + Leo ("Old Rivals"), the three of them ("The Tidewatch", and at sea); Apophiss +
// Emma ("Forgiven"), Apophiss + KillerWatt ("Venom and Volts"), Apophiss + Emma + Leo ("An Uneasy Truce"), Apophiss +
// KillerWatt + Democratus ("The Dread Court"); the hidden one, Emma + Leo + Pearlman ("The Royal Retinue") - and Pearlman
// (who doesn't count toward the three) never taking the place of a whole other trio. rcon only sets the stage (and sends the
// followers home between the scenes).
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const fx = async (sel) => (await run(`${O}data get entity ${sel} active_effects`));
  const hasFx = async (sel, id, amp = 0) => { const p = (await fx(sel)).split('}').find(q => q.includes(`"minecraft:${id}"`)); if (!p) return false;
    const m = p.match(/amplifier: (\d+)b/); return (m ? +m[1] : 0) >= amp; };   // (an amplifier of 0 isn't written at all)
  const adv = async (k) => /passed/i.test(await run(`execute if entity @a[name=TestRat,advancements={bm:story/${k}=true}]`));
  const use = async (C, slot, sneak = false) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(200); } C.use(); await sleep(400); C.release(); if (sneak) { C.input({}); await sleep(150); } };
  const PETS = { emma: ['cat', 'bm.emmapet', 'emma_ribbon'], leo: ['wolf', 'bm.leopet', 'leo_crest'], cecil: ['wolf', 'bm.cecilpet', 'cecil_gem'],
                 celi: ['wolf', 'bm.celipet', 'celi_charm'], kw: ['wolf', 'bm.kxpet', 'kw_spark'], demo: ['wolf', 'bm.dmpet', 'demo_seal'],
                 pearl: ['cat', 'bm.pmpet', 'pearl_card'], apo: ['wolf', 'bm.appet', 'apo_oath'], tul: ['wolf', 'bm.tupet', 'tul_coin'] };
  const sel = k => `@e[type=minecraft:${PETS[k][0]},tag=${PETS[k][1]},limit=1]`;
  const CDS = ['bm.emcd', 'bm.lecd', 'bm.cpcd', 'bm.cecd', 'bm.kxcd', 'bm.dmcd', 'bm.apcd', 'bm.tucd', 'bm.pmcd'];
  const A = await bot('TestRat'); await sleep(2500);
  A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const X = 13520, Y = 121, Z = 13060;
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`);
  for (let y = Y; y < Y + 12; y += 6) await run(`${O}fill ${X - 20} ${y} ${Z - 20} ${X + 20} ${y + 5} ${Z + 20} minecraft:air`);
  await run(`${O}fill ${X + 8} ${Y - 4} ${Z - 6} ${X + 16} ${Y - 1} ${Z + 6} minecraft:water`);
  const home = async () => {        // (staging: everyone sent home, every Oath/crest/charm rested, effects cleared, back to the middle)
    for (const k in PETS) await run(`${O}kill @e[tag=${PETS[k][1]}]`);
    await sleep(1500);                // (a host gone is a faint - its rest is set a few ticks later: clear it after that)
    for (const o of CDS) await run(`scoreboard players set TestRat ${o} 0`);
    await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}kill @e[type=minecraft:husk,tag=bm.t136foe]`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  };
  const call = async (keys) => {
    for (let i = 0; i < keys.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${PETS[keys[i]][2]}`);
    // (every follower item shares a use cooldown that runs down once a second: a second call within ~2 s goes unheard)
    for (let i = 0; i < keys.length; i++) { const t0 = Date.now(); await use(A, i); await wait(4000, async () => (await cnt(sel(keys[i]))) === 1);
      await sleep(Math.max(400, 2300 - (Date.now() - t0))); }
    for (const k of keys) if ((await cnt(sel(k))) !== 1) return false;
    return true;
  };
  const forget = async () => { for (const k of ['pair_frost', 'pair_rivals', 'pair_forgiven', 'pair_volts', 'trio_tide', 'trio_truce', 'trio_dread', 'trio_retinue'])
    await run(`advancement revoke TestRat only bm:story/${k}`); };
  await run('gamemode survival TestRat'); await forget(); await home();

  if (want('tul')) {
    // ================================================================== Tullius's two pairs, and the Tidewatch
    A.chats.length = 0;
    ok('Tullius and Celi, each called with their own item', await call(['tul', 'celi']));
    ok('FROST AND BRINE: the first time, its achievement and their words', await wait(4000, async () => (await adv('pair_frost')) &&
       /smells like the sea/.test(A.chats.join(' ')) && /wet dog/.test(A.chats.join(' '))), A.chats.slice(-3).join(' | ').slice(0, 240));
    ok('...you hit harder (Strength)', await wait(3000, async () => hasFx('TestRat', 'strength')));
    ok('...the pair shrug off blows (Resistance on both)', (await hasFx(sel('tul'), 'resistance')) && (await hasFx(sel('celi'), 'resistance')));
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 4.5} {Tags:["bm.t136foe"],NoAI:1b,Invulnerable:1b}`);
    ok('...and monsters near you are slowed by the frost', await wait(3000, async () => hasFx('@e[type=minecraft:husk,tag=bm.t136foe,limit=1]', 'slowness')));
    await home();
    A.chats.length = 0;
    ok('Tullius and Leo', await call(['tul', 'leo']));
    ok('OLD RIVALS: its achievement and their words', await wait(4000, async () => (await adv('pair_rivals')) && /You came back/.test(A.chats.join(' '))),
       A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('...you keep up with them (Speed, Haste II)', await wait(3000, async () => (await hasFx('TestRat', 'speed')) && (await hasFx('TestRat', 'haste', 1))));
    ok('...both hit harder (Strength on both)', (await hasFx(sel('tul'), 'strength')) && (await hasFx(sel('leo'), 'strength')));
    await home();
    A.chats.length = 0; A.bars.length = 0;
    ok('Tullius, Celi and Leo', await call(['tul', 'celi', 'leo']));
    ok('THE TIDEWATCH: "Three together", its achievement', await wait(4000, async () => (await adv('trio_tide')) && /Three together: The Tidewatch/.test(A.bars.join(' '))),
       A.bars.slice(-2).join(' / '));
    ok('...Strength and Resistance for you', await wait(3000, async () => (await hasFx('TestRat', 'strength')) && (await hasFx('TestRat', 'resistance'))));
    await run(`${O}tp TestRat ${X + 12.5} ${Y - 2.5} ${Z + 0.5}`);
    ok('...and at sea, Water Breathing and Dolphin\'s Grace', await wait(4000, async () => (await hasFx('TestRat', 'water_breathing')) && (await hasFx('TestRat', 'dolphins_grace'))));
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(500); A.stand();
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 5.5} {Tags:["bm.t136foe"],NoAI:1b,Invulnerable:1b}`);
    await run('scoreboard players set TestRat bm.p133 18');
    ok('...every 20 seconds, a frost wave: every monster round you slowed hard', await wait(5000, async () => hasFx('@e[type=minecraft:husk,tag=bm.t136foe,limit=1]', 'slowness', 2)));
    await home();
  }

  if (want('apo')) {
    // ================================================================== Apophiss's two pairs, and his two trios
    A.chats.length = 0;
    ok('Apophiss and Emma', await call(['apo', 'emma']));
    ok('FORGIVEN: its achievement and their words', await wait(4000, async () => (await adv('pair_forgiven')) && /I KNEW you were nice/.test(A.chats.join(' ')) &&
       /purely the violence/i.test(A.chats.join(' '))), A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('...you regenerate; so does he', await wait(3000, async () => (await hasFx('TestRat', 'regeneration')) && (await hasFx(sel('apo'), 'regeneration'))));
    const w0 = await sc(sel('apo'), 'bm.apch'); await sleep(2200); const w1 = await sc(sel('apo'), 'bm.apch');
    ok('...his Wrath builds faster', w1 >= w0 + 2, `${w0} -> ${w1}`);
    await run(`${O}scoreboard players set ${sel('apo')} bm.p133s 29`);
    ok('...and a shield of absorption comes back every half minute', await wait(3000, async () => hasFx('TestRat', 'absorption')));
    await home();
    A.chats.length = 0;
    ok('Apophiss and KillerWatt', await call(['apo', 'kw']));
    ok('VENOM AND VOLTS: its achievement and their words', await wait(4000, async () => (await adv('pair_volts')) && /worth talking to/.test(A.chats.join(' '))),
       A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('...you hit harder and see in the dark (Strength, Night Vision)', await wait(3000, async () => (await hasFx('TestRat', 'strength')) && (await hasFx('TestRat', 'night_vision'))));
    await home();
    A.bars.length = 0;
    ok('Apophiss, Emma and Leo', await call(['apo', 'emma', 'leo']));
    ok('AN UNEASY TRUCE: "Three together", its achievement', await wait(4000, async () => (await adv('trio_truce')) && /Three together: An Uneasy Truce/.test(A.bars.join(' '))),
       A.bars.slice(-2).join(' / '));
    ok('...two more hearts, Regeneration, Resistance', await wait(3000, async () => (await hasFx('TestRat', 'health_boost')) && (await hasFx('TestRat', 'regeneration')) &&
       (await hasFx('TestRat', 'resistance'))));
    await home();
    A.bars.length = 0;
    ok('Apophiss, KillerWatt and Democratus', await call(['apo', 'kw', 'demo']));
    ok('THE DREAD COURT: "Three together", its achievement', await wait(4000, async () => (await adv('trio_dread')) && /Three together: The Dread Court/.test(A.bars.join(' '))),
       A.bars.slice(-2).join(' / '));
    ok('...Strength II and Speed for you', await wait(3000, async () => (await hasFx('TestRat', 'strength', 1)) && (await hasFx('TestRat', 'speed'))));
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 5.5} {Tags:["bm.t136foe"],NoAI:1b,Invulnerable:1b}`);
    ok('...and monsters near you cower (Weakness, Slowness)', await wait(3000, async () => (await hasFx('@e[type=minecraft:husk,tag=bm.t136foe,limit=1]', 'weakness')) &&
       (await hasFx('@e[type=minecraft:husk,tag=bm.t136foe,limit=1]', 'slowness'))));
    await home();
  }

  if (want('retinue')) {
    // ================================================================== the hidden one
    A.bars.length = 0; A.chats.length = 0;
    ok('Emma, Leo and Pearlman', await call(['emma', 'leo', 'pearl']));
    ok('THE ROYAL RETINUE (hidden): "Three together", its achievement', await wait(4000, async () => (await adv('trio_retinue')) && /Three together: The Royal Retinue/.test(A.bars.join(' '))),
       A.bars.slice(-2).join(' / '));
    ok('...Regeneration, Luck and Hero of the Village', await wait(3000, async () => (await hasFx('TestRat', 'regeneration')) && (await hasFx('TestRat', 'luck')) &&
       (await hasFx('TestRat', 'hero_of_the_village'))));
    ok('...and Pearlman\'s appraisal pays twice as often while it lasts', (await sc('TestRat', 'bm.p133r')) >= 1);
    await home();
    // (Pearlman doesn't count toward the three: with Emma, Leo AND Cecil he is a fourth - their own trio stays)
    A.bars.length = 0;
    ok('Emma, Leo, Cecil - and Pearlman as a fourth', await call(['emma', 'leo', 'cecil', 'pearl']));
    await sleep(3500);
    // (Pearlman gives Luck himself: the Retinue's own mark is bm.p133r)
    ok('...still The Serpent\'s Bane, not the Retinue', /Three together: The Serpent's Bane/.test(A.bars.join(' ')) && !/Royal Retinue/.test(A.bars.join(' ')) &&
       !((await sc('TestRat', 'bm.p133r')) >= 1), A.bars.slice(-2).join(' / '));
    await home();
  }

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  await home();
  R.end(); A.end(); process.exit(0);
})();
