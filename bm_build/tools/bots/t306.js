// 2.97: THE CURSOR (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): a Glitched Cartridge USED WITH
// NOBODY BESIDE YOU - and the screen's own pointer slips out; right-clicked, it's yours (The Cursor's Mouse). CLICK; SELECT (a
// foe 6 off: glowing, weakened); DRAG (two foes: dragged in, slowed); LOADING... (frozen, then hurt); UNDO (Regeneration for you).
// 3.0a: HOW IT'S MET - the cartridge used with nobody beside you only buzzes now (kept); with the Gem of Creativity beside you (rcon
// summons it) the Gem brings the screen's pointer to life - its entrance, a click mid-show doesn't select you - and right-clicked, it's yours.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'cursor', NAME: 'The Cursor', ab: 'ux', q: 'uq', pfx: 'p235c', prefix: 'cu_', item: 'cursor_mouse', parts: 3, figParts: 2, hp: 28, X: 17500, Z: 16000, pron: 'it',
  seatPart: 'body', called: /glides back beside you/, home: /clicks itself shut/, sit: /blinking slowly/, stand: /Point me at something/,
  ways: ['Click', 'Select', 'Drag', 'Loading...', 'Undo'], plain: 'Classic white', looks: ['Ocean Theme', 'Rose Theme', 'Lime Theme'],
  encounter: async (ctx) => {
    const { A, run, ok, wait, cnt, at, entOf, has, X, Y, Z, ENC, sleep, use, O } = ctx;
    const K = kit(ctx, 'uq');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`kill @e[type=minecraft:wolf,tag=${K.GEM.tag}]`); await sleep(1000);
    await run('loot replace entity TestRat hotbar.4 loot bm:items/glitch_cart'); await sleep(2200);
    A.bars.length = 0; await use(4); await sleep(600);
    ok('a Glitched Cartridge used with nobody beside you: it only buzzes (kept), no pointer', (await cnt(ENC)) === 0 && (await has('glitch_cart')) === 1 &&
       A.bars.some(b => /buzzes/.test(b)), A.bars.slice(-1).join(''));
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await K.summonAs(K.GEM.pfx, -1.5); await sleep(1500);
    await run(`data modify entity @e[type=minecraft:wolf,tag=${K.GEM.tag},limit=1] Sitting set value 1b`);
    await run('scoreboard players set TestRat bm.gvhc 0'); A.chats.length = 0;
    await use(4);
    const out = await wait(5000, async () => (await cnt(ENC)) === 1, 100); const pre = await K.early(ctx);
    ok('...used with the Gem of Creativity beside you: the Gem brings the pointer to life (its rig and a click box), the cartridge spent', out &&
       A.chats.some(c => /Gem of Creativity's light catches/.test(c)) && (await has('glitch_cart')) === 0, A.chats.slice(-1).join('').slice(0, 160));
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(300);
    // (its entrance - a glitch, a blinking I-beam, *click* into its arrow: a click mid-show doesn't select you yet)
    const show = await K.entrance(ctx, eb, null, pre, async () => (await has('cursor_mouse')) === 1);
    K.showOks(ok, { show }, 'The Cursor\'s entrance', null);
    eb = await entOf(ENC); A.slot(8); await sleep(300);
    A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: selected - its mouse given', (await has('cursor_mouse')) === 1 && A.chats.some(c => /Selected/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    await K.sendHome(K.GEM.pfx, K.GEM.tag, K.GEM.ab); await sleep(800);
  },
  abilities: async (ctx) => {
    const { ok, run, X, Y, Z } = ctx; const K = kit(ctx, 'uq');
    ok('CLICK - a foe at its side: clicked', await K.move('mc', [[1.5, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300));
    ok('SELECT - a foe 6 off: selected - glowing and weakened', await K.move('rc', [[0, 6]], 'bm.trps', async () => /glowing/.test(await K.fxOf('bm.trps')) && /weakness/.test(await K.fxOf('bm.trps'))));
    ok('DRAG - two foes near: dragged in, slowed', await K.move('k2', [[3.5, 0], [-3, 2]], 'bm.trpd', async () => /slowness/.test(await K.fxOf('bm.trpd')) && (await K.hp('bm.trpd')) < 300));
    let frozen = false;
    ok('LOADING... - a foe near: frozen (an hourglass), then hurt as it finishes', await K.move('gc', [[3, 0]], 'bm.trpw', async () => {
      if (/slowness[^}]*amplifier: ?9b|amplifier: ?9b[^}]*slowness/.test(await K.fxOf('bm.trpw'))) frozen = true; return frozen && (await K.hp('bm.trpw')) < 300; }, 10000), `frozen ${frozen}`);
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await K.cd('k', 0);
    ok('UNDO - out of a fight beside you: Regeneration for you', await ctx.wait(6000, async () => /regeneration/.test(await ctx.fx())));
    await K.calm();
  } });
