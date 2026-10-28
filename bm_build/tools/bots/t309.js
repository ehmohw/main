// 2.97: THE LIGHTBRINGER (phase236) as a regular (non-op) player - the owner's checklist (rigpet_t). HARD MODE ONLY, before the
// final reckoning: a herald comes down (rcon places her, as the open sky by day would); empty-handed and wearing nothing holy she
// asks you to wear the light; once you've faced the Dread's master (bm.dfin) she won't come; wearing a holy helmet she gives you her
// feather. SMITE (a foe 6 off: a pillar of light); BLESS (you hurt in a fight: Regeneration II, Absorption); WARD (Resistance II,
// Absorption for you); PRAY (out of a fight); HOLY FAVOUR (wearing something holy beside her: Regeneration). Then the shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
const HOLY = 'minecraft:golden_helmet[custom_data={bm_angel:1b}]';
runT({ W: 'lightbringer', NAME: 'The Lightbringer', ab: 'lh', q: 'lz', pfx: 'p236l', prefix: 'lb_', item: 'herald_feather', parts: 16, figParts: 15, hp: 40, X: 17800, Z: 16000, pron: 'her',
  called: /glides back to your side/, home: /rises into the light/, sit: /kneels and folds her wings/, stand: /Shall we go on/,
  ways: ['Smite', 'Bless', 'Ward', 'Pray', 'Holy Favour'], plain: 'Pearl and gold', looks: ['Royal Vestments', 'Amethyst Vestments', 'Dawn Vestments'],
  encounter: async (ctx) => {
    const { A, run, ok, wait, cnt, at, entOf, has, num, X, Y, Z, ENC, sleep, O } = ctx;
    await run('time set noon'); await run('scoreboard players set #hard bm.cfg 1');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s rotated 0 0 positioned ^ ^ ^5 run function bm:p236l/enc/place`);
    ok('hard mode, by day, in the open: a herald comes down in a pillar of light', await wait(5000, async () => (await cnt(ENC)) === 1) && A.chats.some(c => /herald of the Divine One/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    const talk = async () => { const eb = await entOf(ENC); A.bars.length = 0; A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1200); };
    A.slot(8); await sleep(300); await talk();
    ok('right-clicked wearing nothing holy: "Wear the light"', A.bars.some(b => /Wear the light/.test(b)) && (await has('herald_feather')) === 0, A.bars.slice(-1).join(''));
    await run(`item replace entity TestRat armor.head with ${HOLY}`); await run('tag TestRat add bm.dfin'); await sleep(600); await talk();
    ok('...having faced the Dread\'s master already: she won\'t come ("My work here is finished")', A.bars.some(b => /work here is finished/.test(b)) && (await has('herald_feather')) === 0, A.bars.slice(-1).join(''));
    await run('tag TestRat remove bm.dfin'); await run('scoreboard players set #hard bm.cfg 0'); await sleep(400); await talk();
    ok('...not in hard mode: "Not yet"', A.bars.some(b => /Not yet/.test(b)) && (await has('herald_feather')) === 0, A.bars.slice(-1).join(''));
    await run('scoreboard players set #hard bm.cfg 1'); await sleep(400); await talk();
    ok('...hard mode, wearing something holy: her feather given', (await has('herald_feather')) === 1 && A.chats.some(c => /plucks a feather/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    await run('item replace entity TestRat armor.head with minecraft:air');
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z, fx, wait, sleep } = ctx; const K = kit(ctx, 'lz');
    ok('SMITE - a foe 6 off: a pillar of light (the undead hurt hard)', await K.move('rc', [[0, 6]], 'bm.trps', async () => (await K.hp('bm.trps')) <= 286));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat');
    await run('damage TestRat 6 minecraft:generic'); await ctx.zom(0, 8, 'bm.trpb'); await K.cd('sc', 0);
    ok('BLESS - you hurt, a foe about: Regeneration II and Absorption', await wait(6000, async () => /regeneration[^}]*amplifier: ?1b|amplifier: ?1b[^}]*regeneration/.test(await fx()) && /absorption/.test(await fx())), await fx());
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    ok('WARD - a foe near: Resistance II and Absorption II for you', await K.move('gc', [[3, 1]], 'bm.trpw', async () => /absorption[^}]*amplifier: ?1b|amplifier: ?1b[^}]*absorption/.test(await fx())));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await K.cd('k', 0);
    ok('PRAY - out of a fight beside you: Regeneration', await wait(6000, async () => /regeneration/.test(await fx())));
    await K.calm(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run('tag TestRat remove bm.lhseen'); await run('effect clear TestRat'); await run(`item replace entity TestRat armor.head with ${HOLY}`); ctx.A.chats.length = 0;
    ok('HOLY FAVOUR - wearing something holy beside her: Regeneration, and she notices', await wait(5000, async () => /regeneration/.test(await fx())) && ctx.A.chats.some(c => /you wear the light/.test(c)), ctx.A.chats.slice(-1).join(''));
    await run('item replace entity TestRat armor.head with minecraft:air'); await run('tag TestRat remove bm.lhseen');
  } });
