// 3.1: THE ATOMIC REX (phase272, the 61st follower - phase249's mount, a follower now) as a regular (non-op) player - the owner's
// checklist (rigpet_t): the hatching staged (rcon: the egg's own gift, p249/egg/gift, as its 60 s in the lava would): the whistle,
// and it's a follower met; its ways (TAIL SWIPE, STOMP, ATOMIC BREATH - set alight - ROAR); FULL SIZE from its menu (host 1.4 -> 3.6,
// click box 2.6 -> 7.6, the rig x3) and back; RIDE from its menu: the follower goes, the mount (phase249's) comes with TestRat on
// it; got off (sneak): the mount gone, the follower back. THE MECHA: the hangar's dormant machine with its four pieces (rcon gives
// them) - a non-pilot (not met) is told it needs a pilot, pieces kept; met: the costume earned (look 1) and worn (rx_atomic_body_c1).
// The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'rex', NAME: 'The Atomic Rex', ab: 'ry', q: 'rq', pfx: 'p272', prefix: 'rx_atomic_', item: 'atomic_whistle', parts: 23, figParts: 23, hp: 60, X: 19500, Z: 16000, pron: 'it',
  lookPart: 'body', lookModel: 'rx_atomic_body', seatPart: 'head', called: /stomps back to you/, home: /lumbers off home/, sit: /settles down on its haunches/, stand: /up it gets/,
  ways: ['Tail Swipe', 'Stomp', 'Atomic Breath', 'Roar', 'Ride', 'Full size'],
  plain: 'Charcoal and nuclear blue', looks: ['Ember Rex', 'Glacier Rex'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep } = ctx;
    await run('tag TestRat remove bm.rymet'); await run('tag TestRat remove bm.rxhatch'); await run('clear TestRat');
    A.chats.length = 0; await run('execute as TestRat at @s run function bm:p249/egg/gift'); await sleep(1500);
    ok('hatched (the egg\'s gift): the Atomic Whistle, and it\'s a follower met', (await has('atomic_whistle')) === 1 && /bm\.rymet/.test(await run('tag TestRat list')) &&
       A.chats.some(c => /is your follower/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, cnt, A, sleep, PET, X, Y, Z, O, at, entOf, score } = ctx; const K = kit(ctx, 'rq');
    await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('TAIL SWIPE - a foe 2 off: hurt', await K.move('mc', [[0, 2]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    ok('STOMP - two foes 2 off: hurt', await K.move('k2', [[1, 2], [-1, 2]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 8000));
    ok('ATOMIC BREATH - a foe 6 off: hurt, set alight', await K.move('rc', [[0, 6]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300, 9000));
    ok('ROAR - a foe 5 off: slowed', await K.move('gc', [[0, 5]], 'bm.trpd', async () => /slowness/.test(await K.fxOf('bm.trpd')), 8000));
    // FULL SIZE
    const SC = async () => num(PET, 'attributes[{id:"minecraft:scale"}].base'); const HIT = '@e[type=minecraft:interaction,tag=bm.ryhit,limit=1]';
    await K.home(); await run('scoreboard players set TestRat bm.rqcs 0'); await sleep(800);
    await ctx.sneakMenu(0); A.bars.length = 0; await A.press(/Full size/); await sleep(1500);
    ok('FULL SIZE - pressed on its menu: its host 3.6, its click box 7.6 tall', Math.abs((await SC()) - 3.6) < 0.01 && (await num(HIT, 'height')) > 7, `${await SC()} / ${await num(HIT, 'height')}`);
    await ctx.sneakMenu(0); await A.press(/Full size/); await sleep(1500);
    ok('...and off: 1.4, 2.6', Math.abs((await SC()) - 1.4) < 0.01 && Math.abs((await num(HIT, 'height')) - 2.6) < 0.05);
    // RIDE
    await ctx.sneakMenu(0); await A.press(/^Ride/); await sleep(2500);
    ok('RIDE - pressed: the follower gone, phase249\'s mount here with TestRat on it', (await cnt(PET)) === 0 &&
       /passed/i.test(await run(`${O}execute as TestRat on vehicle if entity @s[type=minecraft:horse]`)), await run(`${O}execute if entity @e[type=minecraft:horse,tag=bm.ryride]`));
    A.input({ shift: true }); await sleep(800); A.input({}); await sleep(2500);
    ok('...off it (sneak): the mount gone, the follower back', (await cnt('@e[type=minecraft:horse,tag=bm.ryride]')) === 0 && (await cnt(PET)) === 1);
    // THE MECHA
    for (const i of ['mecha_blueprint_1', 'mecha_blueprint_2', 'mecha_blueprint_3', 'mecha_core']) await run(`loot give TestRat loot bm:items/${i}`);
    await run('tag TestRat remove bm.rymet'); A.chats.length = 0; await run('execute as TestRat at @s run function bm:p249/hang/try'); await sleep(600);
    ok('THE MECHA - a non-pilot at the hangar: "it needs a pilot", the pieces kept', A.chats.some(c => /needs a pilot/.test(c)) &&
       +(((await run('clear TestRat *[minecraft:custom_data~{bm:"mecha_core"}] 0')).match(/Found (\d+)/) || [0, 0])[1]) === 1);
    await run('tag TestRat add bm.rymet'); A.chats.length = 0; await run('execute as TestRat at @s run function bm:p249/hang/try'); await sleep(800);
    ok('...its pilot: the costume earned (look 1)', ((await score('bm.wurex')) & 2) === 2, `${await score('bm.wurex')}`);
    await run('scoreboard players set TestRat bm.cosry 1'); await run(`${O}execute as TestRat run function bm:p99/rex_now`); await sleep(800);
    ok('...worn: its body the Mecha\'s (rx_atomic_body_c1)', /rx_atomic_body_c1/.test(await nbt('@e[type=minecraft:item_display,tag=bm.ryp_pet,tag=bm.ryp_body,limit=1]', 'item.components."minecraft:item_model"')));
    await run('scoreboard players set TestRat bm.cosry 0'); await run(`${O}execute as TestRat run function bm:p99/rex_now`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
