// 3.1: TRIVYRN (phase274, the 63rd follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t398: its meeting
// staged (admin/trivyrn_meet_here - the three scales, the portal and the three cracks are the stage); right-clicked: the Triune Horn; its ways
// (THE LASH, WING GUST, TRI-BREATH); FULL SIZE and RIDE from its menu. The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'trivyrn', NAME: 'Trivyrn', ab: 'tw', q: 'tv', pfx: 'p274', prefix: 'tw_', item: 'triune_horn', parts: 43, figParts: 34, hp: 56, X: 19580, Z: 16000, pron: 'it',
  lookPart: 'body', seatPart: 'head', called: /lopes back to you/, home: /which way home is/, sit: /crouches low/, stand: /Up! Up!/,
  ways: ['The Lash', 'Wing Gust', 'Tri-Breath', 'Ride', 'Full size', 'The Kaiju Trio'],
  plain: 'Three-world maroon', looks: ['Dawnscale', 'Abyssal', 'Storm Grey'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx;
    await run('tag TestRat remove bm.twmet'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.twenc]');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s run function bm:admin/trivyrn_meet_here`);
    ok('the egg hatches: Trivyrn (its encounter - staged)', await wait(3000, async () => (await cnt(ENC)) === 1));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Triune Horn, and it comes along', (await has('triune_horn')) === 1);
  },
  abilities: async (ctx) => {
    const { ok, run, num, A, sleep, PET } = ctx; const K = kit(ctx, 'tv');
    await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('THE LASH - a foe 4 off: hurt', await K.move('mc', [[0, 4]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    ok('WING GUST - two foes 3 off: hurt', await K.move('k2', [[1, 3], [-1, 3]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 8000));
    ok('TRI-BREATH - a foe 8 off: hurt', await K.move('rc', [[0, 8]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300, 9000));
    const SC = async () => num(PET, 'attributes[{id:"minecraft:scale"}].base');
    await K.home(); await ctx.sneakMenu(0); await A.press(/Full size/); await sleep(1500);
    ok('FULL SIZE: its host 3.6', Math.abs((await SC()) - 3.6) < 0.01); await ctx.sneakMenu(0); await A.press(/Full size/); await sleep(1200);
    await ctx.sneakMenu(0); await A.press(/^Ride/); await sleep(2500);
    ok('RIDE: TestRat on its mount', /passed/i.test(await run('execute in minecraft:overworld as TestRat on vehicle if entity @s[type=minecraft:horse,tag=bm.krtw]')));
    A.input({ shift: true }); await sleep(800); A.input({}); await sleep(2500);
    ok('...off: the follower back', (await ctx.cnt(PET)) === 1);
  } });
