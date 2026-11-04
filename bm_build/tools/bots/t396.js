// 3.1: THE FERRO (phase271, the 60th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t394:
// its encounter staged (admin/ferro_meet_here - rcon: the deep, dark deepslate and KillerWatt and the Ink Blot are the stage): a second
// Ink Blot falls in behind TestRat (its form display, the rig hidden); TestRat WALKS up to it: it bristles - "...that's not mine." -
// and melts out of it; right-clicked: the Lodestone Vial, and it comes along. Its ways: LASH, SPIKE BURST, MAGNETIC PULL (pulled in),
// ENGULF (hidden, then spat - hurt). MIMICRY: Bender (met, out - rcon) within 6 for 3 s: learned (bm:ferro/learned/bender); its
// menu -> Forms: "Bender" pressed - it morphs (the form display fm_bv_ball, the rig hidden, bm.fexf); "Its own shape": back. The
// shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'ferro', NAME: 'The Ferro', ab: 'fe', q: 'fq', pfx: 'p271', prefix: 'fe_', item: 'lodestone_vial', parts: 16, figParts: 5, hp: 32, X: 19460, Z: 16000, pron: 'it',
  lookPart: 'body', seatPart: 'body', called: /pours itself back to you/, home: /the puddle into a bead/, sit: /little goo armchair/, stand: /The goo is up/,
  ways: ['Lash', 'Spike Burst', 'Magnetic Pull', 'Engulf', 'Mimicry'],
  plain: 'Mirror black', looks: ['Quicksilver', 'Gold Leaf', 'Deep Violet'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx;
    await run('tag TestRat remove bm.femet'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.feenc]');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s run function bm:admin/ferro_meet_here`);
    ok('the Ink Blot that isn\'t falls in behind TestRat (its encounter, wearing the Ink Blot\'s form)', await wait(3000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.feencf]')) === 1);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    A.chats.length = 0; await A.walkTo(ex + 0.5, ez - 2.0); await sleep(1500);
    ok('...TestRat walks up to it: it bristles - "...that\'s not mine." - and melts out of the disguise', A.chats.some(c => /not mine/.test(c)) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.feencf]')) === 0, A.chats.slice(-1).join('').slice(0, 160));
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Lodestone Vial in TestRat\'s hands, and it comes along', (await has('lodestone_vial')) === 1, A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, cnt, A, sleep, PET, X, Y, Z, O, at, entOf, score } = ctx; const K = kit(ctx, 'fq');
    await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('LASH - a foe 2 off: hurt', await K.move('mc', [[0, 2]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    ok('SPIKE BURST - a foe 1.5 off: hurt', await K.move('k2', [[0, 1.5]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 8000));
    let z0 = 0;
    ok('MAGNETIC PULL - a foe 6 off: pulled in, hurt', await K.move('rc', [[0, 6]], 'bm.trpc', async () => { z0 = await num('@e[tag=bm.trpc,limit=1]', 'Pos[2]');
      return (await K.hp('bm.trpc')) < 300 && Math.abs(z0 - Z) < 5; }, 8000), `z ${z0 - Z}`);
    let gone = false;
    ok('ENGULF - a foe 2 off: engulfed (hidden, bm.fein) - and spat out, hurt', await K.move('gc', [[0, 2]], 'bm.trpd', async () => {
      if ((await cnt('@e[tag=bm.trpd,tag=bm.fein]')) === 1) gone = true; return gone && (await cnt('@e[tag=bm.trpd,tag=bm.fein]')) === 0 && (await K.hp('bm.trpd')) < 300; }, 9000));
    // MIMICRY: Bender met and out beside it for 3 s - learned; then Forms -> Bender, and back
    await K.home(); await run('advancement revoke TestRat only bm:ferro/learned/bender'); await run('advancement grant TestRat only bm:met/bender');
    await run('loot replace entity TestRat inventory.20 loot bm:items/bv_ball'); await K.summonAs('p195', 1.0); await sleep(1500);
    await run(`${O}tp @e[type=minecraft:wolf,tag=bm.bvpet] ${X + 1.5} ${Y + 1} ${Z}`); await run('data modify entity @e[type=minecraft:wolf,tag=bm.bvpet,limit=1] Sitting set value 1b');
    ok('MIMICRY - Bender (met) within 6 for 3 s: learned for good', await wait(7000, async () => /true/.test(await run('execute if entity TestRat[advancements={bm:ferro/learned/bender=true}] run say true')) ||
       /passed/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:ferro/learned/bender=true}]')), 300));
    await ctx.sneakMenu(0); await A.press(/Forms/);
    ok('...its menu -> Forms: Bender is there', A.buttons().some(b => /Bender/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await A.press(/Bender/); await sleep(2500);
    ok('...pressed: it morphs - a goo Bender (fm_bv_ball), the rig hidden (bm.fexf)', /bm\.fexf/.test(await nbt(PET, 'Tags')) &&
       /fm_bv_ball/.test(await nbt('@e[type=minecraft:item_display,tag=bm.fep_form,limit=1]', 'item.components."minecraft:item_model"')), await nbt(PET, 'Tags'));
    await ctx.sneakMenu(0); await A.press(/Forms/); await A.press(/Its own shape/); await sleep(2000);
    ok('..."Its own shape": back (no form display, bm.fexf gone)', !/bm\.fexf/.test(await nbt(PET, 'Tags')) && (await cnt('@e[type=minecraft:item_display,tag=bm.fep_form]')) === 0);
    await K.sendHome('p195', 'bm.bvpet', 'bv'); await run('clear TestRat *[minecraft:custom_data~{bm:"bv_ball"}]');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
