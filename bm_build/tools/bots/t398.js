// 3.1: TALUS (phase273, the 62nd follower) as a regular (non-op) player - the owner's checklist (rigpet_t): its meeting staged in its
// three steps (rcon sets each stage; the player's own moves where they can be): the Echo (p273/enc/echo as a rider roaring in a jungle -
// staged), the seed on budding amethyst in a lush cave (rcon: the biome stands in), the drums (eight note-block beats - the advancement's
// reward run as the player) - Talus climbs out; right-clicked: the Mossback Drum. Its ways (CLIMBING LEAP, GROUND POUND, BOULDER THROW,
// WAR-DRUM); FULL SIZE and RIDE from its menu (as t397). The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'talus', NAME: 'Talus', ab: 'tl', q: 'tt', pfx: 'p273', prefix: 'tl_', item: 'mossback_drum', parts: 23, figParts: 18, hp: 60, X: 19540, Z: 16000, pron: 'it',
  lookPart: 'body', seatPart: 'head', called: /knuckle-walks back to you/, home: /sinks back into the stone/, sit: /settles on its haunches/, stand: /rises off its haunches/,
  ways: ['Climbing Leap', 'Ground Pound', 'Boulder Throw', 'War-Drum', 'Ride', 'Full Size'],
  plain: 'Mossback and amethyst', looks: ['Autumn Moss', 'Snowcap', 'Basalt Moss'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx;
    await run('tag TestRat remove bm.tlmet'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.tlenc]');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s run function bm:admin/talus_meet_here`);
    ok('Talus climbs up out of the peak (its encounter - staged)', await wait(3000, async () => (await cnt(ENC)) === 1));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Mossback Drum, and it comes along', (await has('mossback_drum')) === 1);
  },
  abilities: async (ctx) => {
    const { ok, run, num, A, sleep, PET } = ctx; const K = kit(ctx, 'tt');
    await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('CLIMBING LEAP - a foe 3 off: hurt', await K.move('mc', [[0, 3]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    ok('GROUND POUND - two foes 3 off: hurt', await K.move('k2', [[1, 3], [-1, 3]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 8000));
    ok('BOULDER THROW - a foe 8 off: hurt', await K.move('rc', [[0, 8]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300, 9000));
    const SC = async () => num(PET, 'attributes[{id:"minecraft:scale"}].base');
    await K.home(); await ctx.sneakMenu(0); await A.press(/Full Size/); await sleep(1500);
    ok('FULL SIZE: its host 3.8', Math.abs((await SC()) - 3.8) < 0.01); await ctx.sneakMenu(0); await A.press(/Full Size/); await sleep(1200);
    await ctx.sneakMenu(0); await A.press(/^Ride/); await sleep(2500);
    ok('RIDE: TestRat on its mount', /passed/i.test(await run('execute in minecraft:overworld as TestRat on vehicle if entity @s[type=minecraft:horse,tag=bm.krtl]')));
    A.input({ shift: true }); await sleep(800); A.input({}); await sleep(2500);
    ok('...off: the follower back', (await ctx.cnt(PET)) === 1);
  } });
