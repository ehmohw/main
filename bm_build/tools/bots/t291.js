// 2.96: RUFUS GNAW, rat for hire - for keeps, as a regular (non-op) player - the owner's checklist (rigpet_t). An old world's
// carrot-on-a-stick contract (rcon: as an older version left it) becomes the new Mercenary Contract; its first use signs him on
// (a week in the purse) and he comes. His ways: the BLADE (a slash), the CROSSBOW (a bolt), the DIRTY TRICK (three foes: smoke -
// blinded, slowed, weakened), the PAYDAY VOLLEY (paid today: two foes, bolts), SCAVENGE (out of a fight: something handed over).
// The PAY: a new day takes a day's wage from his purse (paid: Luck for you, Resistance for him); the purse empty, he stays -
// unpaid, no extras; "Pay a week's wages" pressed in his menu: 4 Tokens, 7 days, paid today; "His pay book"; a Veteran at 7
// days paid (40 health). Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'rufus', NAME: 'Rufus Gnaw', ab: 'ru', q: 'rg', pfx: 'p228', prefix: 'rf_', item: 'merc_contract', parts: 14, figParts: 13, hp: 30, X: 17300, Z: 16000, pron: 'him',
  called: /Right behind you|Who are we hitting/, home: /Counting/, sit: /Wake me if it's money/, stand: /Break's over/,
  ways: ['Payday', 'Ranks', 'Crossbow', 'Blade', 'Dirty Trick', 'Payday Volley', 'Scavenge'],
  plain: 'His red bandana', looks: ['Black Bandana', 'Royal Blue Bandana', 'Forest Bandana'],
  encounter: async ({ A, run, ok, wait, O, cnt, has, X, Y, Z, at, sleep, use, PET }) => {
    // (the stage: an older world - his old contract, a carrot on a stick, and his old wages; nothing signed on yet)
    for (const o of ['bm.mpurse', 'bm.mdays', 'bm.mpaid', 'bm.mday', 'bm.mstate']) await run(`scoreboard players reset TestRat ${o}`);
    await run('clear TestRat'); await run('item replace entity TestRat hotbar.0 with minecraft:carrot_on_a_stick[minecraft:custom_data={bm:"merc_contract"}]');
    A.chats.length = 0;
    ok('an old Mercenary Contract (a carrot on a stick, from before) becomes the new one in your pocket - "same rat, for keeps now"',
       await wait(4000, async () => (await has('merc_contract')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:carrot_on_a_stick 0'))) &&
       A.chats.some(c => /for keeps now/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/merc_contract'); await sleep(400);
    A.chats.length = 0; await use(0); await sleep(1500);
    ok('the contract used the first time: he signs on, for keeps - a week\'s wages in the purse', A.chats.some(c => /For keeps, boss/.test(c)) &&
       +((await run('scoreboard players get TestRat bm.mpurse')).match(/has (\d+)/) || [0, 0])[1] === 7, A.chats.slice(-1).join('').slice(0, 160));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.rg${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    const fxOf = async (t) => nbt(`@e[tag=${t},limit=1]`, 'active_effects');
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    const day = async () => +((await run('scoreboard players get #day bm.bm')).match(/has (-?\d+)/) || [0, 0])[1];
    await calm();
    // ---- BLADE and CROSSBOW
    await zom(2.0, 0, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~1.4 ~ ~`); await cd('mc', 0);
    ok('BLADE - a foe beside him: slashed', await wait(5000, async () => (await hp('bm.trps')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(9, 0, 'bm.trpb'); await cd('rc', 0);
    ok('CROSSBOW - a foe 9 off: a bolt hits it', await wait(7000, async () => (await hp('bm.trpb')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    // ---- DIRTY TRICK: three foes close - a smoke bomb
    for (const [dx, dz] of [[2, 1], [2, -1], [-2, 1]]) await zom(dx, dz, 'bm.trpd');
    await run(`${O}execute at ${PET} run tp @e[tag=bm.trpd] ~2 ~ ~1`); await cd('k2', 0);
    ok('DIRTY TRICK - three foes close: smoke - blinded, slowed and weakened', await wait(6000, async () => (await cnt('@e[tag=bm.trpd,nbt={active_effects:[{id:"minecraft:blindness"}]}]')) >= 2 &&
       /weakness/.test(await fxOf('bm.trpd'))), `${await cnt('@e[tag=bm.trpd,nbt={active_effects:[{id:"minecraft:blindness"}]}]')} blinded`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    // ---- PAYDAY: a new day takes a day's wage; paid - Luck for you, Resistance for him
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    const p0 = await score('bm.mpurse'), d0 = await score('bm.mdays');
    A.chats.length = 0; A.bars.length = 0; await run('scoreboard players set TestRat bm.mday -1');           // (the stage: a new day comes round)
    ok('a new day: a day\'s wage out of his purse, a day served, paid today', await wait(4000, async () => (await score('bm.mpurse')) === p0 - 1) &&
       (await score('bm.mdays')) === d0 + 1 && (await score('bm.mpaid')) === await day(), `purse ${await score('bm.mpurse')} days ${await score('bm.mdays')}`);
    ok('...paid: Luck for you, Resistance for him', await wait(4000, async () => /luck/.test(await fx()) && /resistance/.test(await nbt(PET, 'active_effects'))));
    // ---- PAYDAY VOLLEY (paid today): two foes - bolts
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(8, 2, 'bm.trpv'); await zom(8, -2, 'bm.trpv'); await cd('gc', 0);
    ok('PAYDAY VOLLEY - paid, two foes off: bolts into both', await wait(9000, async () => (await cnt('@e[tag=bm.trpv,nbt={Health:300.0f}]')) === 0),
       `untouched ${await cnt('@e[tag=bm.trpv,nbt={Health:300.0f}]')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    // ---- SCAVENGE: out of a fight, beside you - something handed over
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    A.bars.length = 0; await cd('k', 0);
    ok('SCAVENGE - out of a fight beside you: he hands you something he found', await wait(7000, async () => A.bars.some(b => /Yours\. Don't ask|A Token\. Fell out/.test(b))),
       A.bars.slice(-1).join(''));
    // ---- unpaid: the purse empty, a new day - he stays, without the extras
    await run('scoreboard players set TestRat bm.mpurse 0'); await run('scoreboard players set TestRat bm.mpaid -1');   // (the stage: yesterday's wage, and a new day)
    A.chats.length = 0; await run('scoreboard players set TestRat bm.mday -1');
    ok('the purse empty, a new day: he stays - "a contract\'s a contract" - unpaid (no extras)', await wait(4000, async () => A.chats.some(c => /a contract's a contract/.test(c))) &&
       (await cnt(PET)) === 1 && (await score('bm.mpaid')) !== await day() && await wait(3000, async () => (await cnt(`${PET.replace(',limit=1]', '')},tag=!bm.rupaid]`)) === 1));
    // ---- PAY A WEEK, pressed in his menu: 4 Tokens, 7 days - paid for today too
    await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]'); for (let i = 0; i < 4; i++) await run('loot give TestRat loot bm:items/token');
    ok('his menu: "Pay a week\'s wages" and "His pay book"', await sneakMenu(0) && A.buttons().some(b => /Pay a week's wages/.test(b.label)) && A.buttons().some(b => /His pay book/.test(b.label)),
       A.buttons().map(b => b.label).join(' | ').slice(0, 200));
    A.chats.length = 0; await A.press(/Pay a week's wages/); await sleep(1200);
    ok('...pressed: 4 Tokens go, 7 days into the purse (one taken for today) - paid today', (await score('bm.mpurse')) === 6 && (await score('bm.mpaid')) === await day() &&
       !/Found [1-9]/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"token"}] 0')), `purse ${await score('bm.mpurse')}`);
    await sneakMenu(0); A.chats.length = 0; await A.press(/His pay book/); await sleep(1000);
    ok('...his pay book: rank, days served, the purse, and paid today', A.chats.some(c => /Rank:/.test(c) && /In the purse/.test(c)) && A.chats.some(c => /Paid today: yes/.test(c)),
       A.chats.slice(-3).join(' | ').slice(0, 220));
    // ---- RANKS: seven days paid - a Veteran (40 health)
    await run('scoreboard players set TestRat bm.mdays 7');
    ok('seven days paid: a Veteran - 40 health', await wait(4000, async () => (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 40));
    await run('scoreboard players set TestRat bm.mdays 0'); await sleep(1500);
    await calm();
  } });
