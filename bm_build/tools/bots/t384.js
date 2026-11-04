// 3.0k: THE RAT KING (phase262) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t163/t324: his
// audience in the Counting House under the Loom Sanctuary. The stage (rcon): TestRat given the Compass's mark (bm.kbcomp - every
// other follower met) - the King's Coin comes by itself; a stone floor in the island's column; the hall's chunks held. TestRat
// holds the coin there and SNEAKS (a real input) - down the rat-run into the hall. The King on his throne (his full size);
// spoken to: the tribute dialog - 32 Gold Ingots pressed (the button the client was shown); the Shell of Rats - five rats on the
// table, a wrong one poked first ("Pfah. Again."), then the thief (rcon only reads which cup it is) - the Royal Marker, and he
// joins. The mouse hole carries TestRat back up where it came down. Then his ways (the Sceptre Slam, the Court, the Loan,
// the King's Cut), COMPANION SIZE from his menu (host scale and click box both shrink, kept across a send-home and a call, and
// back), and the shared list (menu, sitting, wardrobe, aura, contract, frame, display case, Cecil's doll, fainting).
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
const CX = -2587, CZ = 2617, FY = -56;                                 // (phase262: the Counting House)
const LAND = [CX + 0.5, FY, CZ + 5.5], THRONE = [CX + 0.5, FY + 1, CZ - 4.5], HOLE = [CX + 7.5, FY, CZ + 0.5];
const COLX = -2586.5, COLZ = 2623.5, COLY = 120;                        // (phase253: the island's landing column - where you sneak to go down)
const ROOM = `x=${CX - 7},y=${FY},z=${CZ - 7},dx=14,dy=6,dz=14`;
runT({ W: 'ratking', NAME: 'The Rat King', ab: 'rw', q: 'qw', pfx: 'p262', prefix: 'rkf_', item: 'royal_marker', parts: 14, figParts: 13, hp: 44, X: 19060, Z: 16000, pron: 'him',
  lookPart: 'cape', called: /proceeds, briskly, back to your side/, home: /sweeps his cape round himself/, sit: /settles on his haunches/, stand: /hoard won't count itself/,
  ways: ['Sceptre Swat', 'Sceptre Slam', 'The Court', 'A Loan, With Interest', "The King's Cut", 'Bonds and Debts', 'Companion Size'],
  plain: 'Crimson and royal blue', looks: ['Midnight Cape', 'Emerald Court', 'Royal Purple'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, score, num, PET } = ctx;
    const ENC = `@e[type=minecraft:interaction,tag=bm.rwenc,${ROOM},limit=1]`;
    const PARTS = `@e[type=minecraft:item_display,tag=bm.rwencp,${ROOM}]`;
    const cup = (i) => `@e[type=minecraft:interaction,tag=bm.rwcup,${ROOM},scores={bm.qwsl=${i}},limit=1]`;
    // ---- the stage: the hall's chunks held, a floor in the island's column, TestRat with the Compass's mark - no coin yet
    await run(`${O}forceload add ${CX - 12} ${CZ - 12} ${CX + 12} ${CZ + 12}`);
    await run(`${O}forceload add ${COLX - 4} ${COLZ - 4} ${COLX + 4} ${COLZ + 4}`);
    await run('tag TestRat remove bm.rwmet'); await run('tag TestRat remove bm.rwpaid'); await run('tag TestRat remove bm.rwcoin'); await run('clear TestRat');
    await run(`${O}fill ${COLX - 2} ${COLY - 1} ${COLZ - 2} ${COLX + 2} ${COLY - 1} ${COLZ + 2} minecraft:stone`);
    await run(`${O}fill ${COLX - 2} ${COLY} ${COLZ - 2} ${COLX + 2} ${COLY + 3} ${COLZ + 2} minecraft:air`);
    await run('tag TestRat add bm.kbcomp');
    ok("the Compass's mark (every other follower met): the King's Coin comes by itself", await wait(4000, async () => (await has('kings_coin')) === 1));
    ok('...and the Counting House is built under the island (#rwver)', await wait(20000, async () => (await score('bm.p2', '#rwver')) >= 1, 500));
    // ---- the way down: the coin held in the column, sneaking for three seconds
    await at(COLX, COLY, COLZ, 0, 0);
    await run('clear TestRat *[minecraft:custom_data~{bm:"kings_coin"}]'); await run('loot replace entity TestRat hotbar.7 loot bm:items/kings_coin');
    A.slot(7); await sleep(400); A.bars.length = 0; A.input({ shift: true });
    const down = await wait(7000, async () => A.pos && A.pos.y < -50, 200); A.input({}); await sleep(800);
    ok('the coin held, sneaking: "something is gnawing at it" - and down the rat-run into the hall', down && A.bars.some(b => /gnawing/.test(b)), A.bars.slice(-2).join(' | '));
    ok('...in the hall: Adventure mode', await wait(3000, async () => (await cnt('@a[name=TestRat,gamemode=adventure]')) === 1));
    ok('...and the Rat King on his throne, his rig (13 parts shown - the coin unseen)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       Math.abs((await num(ENC, 'Pos[2]')) - THRONE[2]) < 0.8, `enc ${await cnt(ENC)} parts ${await cnt(PARTS)}`);
    ok('...at his own size: his click box 2.9 tall', (await num(ENC, 'height')) > 2.5, `${await num(ENC, 'height')}`);
    // ---- spoken to: the tribute
    await at(THRONE[0], FY, THRONE[2] + 3, 180, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250);
    const n0 = A.dialogN.length; A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId);
    ok('spoken to: "Fifty DEBTS, I call it" - and his tribute dialog', await wait(3000, async () => A.dialogN.length > n0) && A.chats.some(c => /Fifty DEBTS/.test(c)),
       A.chats.slice(-1).join('').slice(0, 160));
    ok('...32 Gold Ingots, 16 Gutter Coins, a Golden Cheese Wheel', ['32 Gold Ingots', '16 Gutter Coins', 'A Golden Cheese Wheel'].every(l => A.buttons().some(b => b.label.includes(l))),
       A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/32 Gold Ingots/); await sleep(800);
    ok('...pressed with no gold: "You haven\'t got" - nothing taken', A.bars.some(b => /haven't got/.test(b)) && !/bm\.rwpaid/.test(await ctx.tags()), A.bars.slice(-1).join(''));
    await run('give TestRat minecraft:gold_ingot 40');
    eb = await entOf(ENC); const n1 = A.dialogN.length; if (eb) A.interact(eb.entityId); await wait(3000, async () => A.dialogN.length > n1);
    A.chats.length = 0; await A.press(/32 Gold Ingots/); await sleep(1200);
    ok('...pressed with 40 ingots: 32 taken (paid, bm.rwpaid) - "Gold. Good, honest, heavy gold."', /bm\.rwpaid/.test(await ctx.tags()) &&
       /Found 8/.test(await run('clear TestRat minecraft:gold_ingot 0')) && A.chats.some(c => /honest, heavy gold/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    // ---- the Shell of Rats: five on the table; a wrong one poked, then the thief
    ok('the Shell of Rats: five court rats and their five cups on the table', await wait(3000, async () => (await cnt(`@e[tag=bm.rwsr,${ROOM}]`)) === 5 && (await cnt(`@e[tag=bm.rwcup,${ROOM}]`)) === 5));
    ok('...the shuffle runs, then it\'s your pick (stage 4: "Which one?")', await wait(8000, async () => (await score('bm.qwg', ENC)) === 4, 200));
    await at(CX - 3 + 0.5, FY, CZ + 2.2, 180, 30);
    let th = await score('bm.qwth', ENC); const wrong = (th + 2) % 5;
    let cb = null; await wait(3000, async () => (cb = await entOf(cup(wrong))) != null, 200);
    A.chats.length = 0; if (cb) A.attack(cb.entityId); await sleep(900);
    ok('a wrong rat poked: "Pfah. Again." - a new thief, a new shuffle', A.chats.some(c => /Pfah\. Again/.test(c)) && (await score('bm.qwg', ENC)) >= 2 && (await has('royal_marker')) === 0,
       A.chats.slice(-1).join('').slice(0, 160));
    ok('...your pick again', await wait(8000, async () => (await score('bm.qwg', ENC)) === 4, 200));
    th = await score('bm.qwth', ENC); cb = null; await wait(3000, async () => (cb = await entOf(cup(th))) != null, 200);
    A.chats.length = 0; if (cb) A.attack(cb.entityId); await sleep(900);
    ok('the thief poked: "Sharp eyes. I like sharp eyes."', A.chats.some(c => /Sharp eyes/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    ok('...the Royal Marker in TestRat\'s hands, and he joins you', await wait(5000, async () => (await has('royal_marker')) === 1) && A.chats.some(c => /joins you/.test(c)),
       A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('...the throne empty, the table cleared; once (bm.rwmet)', await wait(4000, async () => (await cnt(ENC)) === 0 && (await cnt(`@e[tag=bm.rwshell,${ROOM}]`)) === 0) &&
       /bm\.rwmet/.test(await ctx.tags()) && await wait(4000, async () => (await cnt(PET)) === 1));
    // ---- the mouse hole: back up where TestRat came down
    await at(HOLE[0] - 1.5, FY, HOLE[2], -90, 0); A.input({ forward: true }); await wait(4000, async () => A.pos && A.pos.y > 100, 100); A.input({}); await sleep(800);
    ok('the mouse hole: back up the rat-run, where TestRat came down', A.pos && Math.abs(A.pos.y - COLY) < 2 && Math.abs(A.pos.x - COLX) < 2, A.pos && `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    ok('...and survival again', await wait(4000, async () => (await cnt('@a[name=TestRat,gamemode=survival]')) === 1));
    // (home together: the stage)
    await run('tag TestRat add bm.rwtp'); await run(`${O}tag ${PET} add bm.rwtp`);
    await run(`${O}tp @e[tag=bm.rwtp] ${ctx.X + 0.5} ${ctx.Y + 1} ${ctx.Z + 0.5}`); await run(`${O}tag @e[tag=bm.rwtp] remove bm.rwtp`);
    await run('clear TestRat *[minecraft:custom_data~{bm:"kings_coin"}]'); await run('clear TestRat minecraft:gold_ingot');
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait, O, cnt, num, nbt, A, sleep, PET, use } = ctx; const K = kit(ctx, 'qw');
    ok('SCEPTRE SLAM - two foes near: hurt and slowed', await K.move('k2', [[2, 2], [-2, 2]], 'bm.trps', async () => (await K.hp('bm.trps')) < 300 &&
       /slowness/.test(await K.fxOf('bm.trps')), 7000));
    ok('THE COURT - a foe 6 off: his rats about it, bitten, weakened', await K.move('gc', [[0, 6]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300 &&
       /weakness/.test(await K.fxOf('bm.trpc')), 9000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); A.bars.length = 0; await K.cd('k', 0);
    ok('A LOAN, WITH INTEREST - out of a fight beside you: a coin\'s worth of something', await wait(6000, async () => A.bars.some(b => /The Rat King:/.test(b))), A.bars.slice(-1).join(''));
    await K.calm();
    // ---- THE KING'S CUT: kills of yours with him near pay a tithe now and then (twenty, by rcon - the stage; at least one pays)
    await run('clear TestRat minecraft:gold_nugget'); await run('clear TestRat minecraft:emerald');
    for (let i = 0; i < 4; i++) { await run('scoreboard players add TestRat bm.rwmk 5'); await sleep(1100); }
    const got = +(((await run('clear TestRat minecraft:gold_nugget 0')).match(/Found (\d+)/) || [0, 0])[1]) + +(((await run('clear TestRat minecraft:emerald 0')).match(/Found (\d+)/) || [0, 0])[1]);
    ok("THE KING'S CUT - twenty kills with him near: a tithe paid (gold nuggets, an emerald...)", got > 0, `${got}`);
    // ---- COMPANION SIZE, from his menu: the host's scale and his click box shrink with the rig; kept across a send-home; and back
    const HIT = '@e[type=minecraft:interaction,tag=bm.rwhit,limit=1]';
    await run('scoreboard players set TestRat bm.rwcs 0'); await sleep(800);
    ok('COMPANION SIZE - off: his own size (host 1.6, click box 2.9 tall)', Math.abs((await num(PET, 'attributes[{id:"minecraft:scale"}].base')) - 1.6) < 0.01 &&
       (await num(HIT, 'height')) > 2.5, `${await num(PET, 'attributes[{id:"minecraft:scale"}].base')} / ${await num(HIT, 'height')}`);
    await ctx.sneakMenu(0); A.bars.length = 0; await A.press(/Companion Size/); await sleep(1500);
    ok('...pressed on his menu: on (bm.rwcs 1) - "FUN-SIZED"', (await ctx.score('bm.rwcs')) === 1 && A.bars.some(b => /FUN-SIZED/.test(b)), A.bars.slice(-1).join(''));
    ok('...his host shrinks (0.85) and his click box with it (1.6 tall, 0.85 wide)', Math.abs((await num(PET, 'attributes[{id:"minecraft:scale"}].base')) - 0.85) < 0.01 &&
       Math.abs((await num(HIT, 'height')) - 1.6) < 0.05 && Math.abs((await num(HIT, 'width')) - 0.85) < 0.05, `${await num(PET, 'attributes[{id:"minecraft:scale"}].base')} / ${await num(HIT, 'width')} x ${await num(HIT, 'height')}`);
    const sc = await num('@e[type=minecraft:item_display,tag=bm.rwp_pet,tag=bm.rwp_body,tag=!bm.rwfade,limit=1]', 'transformation.scale[0]');
    ok('...and the rig itself at companion size (its body shown at 0.48)', Math.abs(sc - 0.48) < 0.02, `${sc}`);
    await ctx.sneakMenu(0); await A.click(/Send .* home/); await sleep(1500);
    await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2500);
    ok('...sent home and called again: still companion-sized (host 0.85, box 1.6)', Math.abs((await num(PET, 'attributes[{id:"minecraft:scale"}].base')) - 0.85) < 0.01 &&
       Math.abs((await num(HIT, 'height')) - 1.6) < 0.05, `${await num(PET, 'attributes[{id:"minecraft:scale"}].base')} / ${await num(HIT, 'height')}`);
    await ctx.sneakMenu(0); A.bars.length = 0; await A.press(/Companion Size/); await sleep(1500);
    ok('...and off again: "A king should LOOM" - host 1.6, click box 2.9', (await ctx.score('bm.rwcs')) === 0 && A.bars.some(b => /LOOM/.test(b)) &&
       Math.abs((await num(PET, 'attributes[{id:"minecraft:scale"}].base')) - 1.6) < 0.01 && (await num(HIT, 'height')) > 2.5, A.bars.slice(-1).join(''));
  } });
