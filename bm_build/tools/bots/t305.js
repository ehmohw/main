// 2.97: THE ERASER (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): found hiding near the Gem (rcon
// places it); asked empty-handed it can only erase; given paper (a fresh start) it's yours (The Eraser's Lucky Crumb). RUB OUT -
// and PINK CRUMBS LEFT BEHIND on the ground; BOUNCE (two foes near: slowed); UNMAKE (hurt, weakened); TIDY UP (your poison
// rubbed out). Then the shared list.
// 3.0a: HOW IT'S MET - paper handed to the Gem of Creativity (rcon summons it, TestRat's own; a right-click holding it): its old mistake
// rubs itself out of the air - its entrance, quiet till it's over - and right-clicked, it comes along.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'eraser', NAME: 'The Eraser', ab: 'ez', q: 'ea', pfx: 'p235e', prefix: 'er_', item: 'eraser_crumb', parts: 9, figParts: 7, hp: 30, X: 17400, Z: 16000, pron: 'it',
  seatPart: 'body', called: /hurries back to you/, home: /rubs itself out of sight/, sit: /so as not to erase anything/, stand: /I'm ready/,
  ways: ['Rub Out', 'Bounce', 'Unmake', 'Tidy Up'], plain: 'Classic pink', looks: ['Blue Rubber', 'Mint Rubber', 'Lemon Rubber'],
  encounter: async (ctx) => {
    // (3.0a) THE GEM BRINGS IT TO LIFE - handed something as a regular player; its entrance; right-clicked: it comes along
    const K = kit(ctx, 'ea');
    const o = { name: 'The Eraser', host: 'p231', hostAb: 'cg', hostTag: 'bm.cgpet', hostName: 'the Gem of Creativity', gem: false, item: 'minecraft:paper',
      bornRe: /rubs itself out of the air/, joined: /doesn't erase a thing/, itemId: 'eraser_crumb' };
    const r = await K.born(o); K.bornOks(ctx.ok, r, o);
  },
  abilities: async (ctx) => {
    const { ok, run, cnt, O, X, Y, Z } = ctx; const K = kit(ctx, 'ea');
    await run(`${O}kill @e[type=minecraft:item_display,tag=bm.ezcrumb]`);
    ok('RUB OUT - a foe at its side: rubbed', await K.move('mc', [[1.5, 0]], 'bm.trpr', async () => (await K.hp('bm.trpr')) < 300));
    ok('...and it leaves PINK CRUMBS behind on the ground', await ctx.wait(3000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.ezcrumb,x=${X},y=${Y},z=${Z},distance=..6]`)) >= 1));
    await run(`${O}kill @e[tag=bm.trpz]`); await K.calm();
    ok('...the crumbs swept up after a few seconds', await ctx.wait(9000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.ezcrumb]')) === 0));
    ok('BOUNCE - two foes close: a belly-flop, slowed', await K.move('k2', [[2, 0], [-1.5, 1]], 'bm.trpb', async () => /slowness/.test(await K.fxOf('bm.trpb')) && (await K.hp('bm.trpb')) < 300));
    ok('UNMAKE - a foe at its side: scrubbed (hurt twice), weakened', await K.move('gc', [[1.5, 1]], 'bm.trpu', async () => (await K.hp('bm.trpu')) < 290 && /weakness/.test(await K.fxOf('bm.trpu')), 9000));
    await K.home(); await ctx.at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run('effect give TestRat minecraft:poison 60 0'); await run('effect give TestRat minecraft:slowness 60 0'); await K.cd('k', 0);
    ok('TIDY UP - out of a fight beside you: your poison and slowness rubbed out, Regeneration', await ctx.wait(6000, async () => { const f = await ctx.fx(); return !/poison|slowness/.test(f) && /regeneration/.test(f); }));
    await K.calm();
  } });
