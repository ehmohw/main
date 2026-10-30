// 2.97: THE DOODLE DRAGON (phase235) as a regular (non-op) player - the owner's checklist (rigpet_t): Kettle's crayon drawing climbs
// off the page (rcon places him, as walking with Kettle would); asked empty-handed he wants crayons; given a dye he's yours (Kettle's
// Dragon Drawing). CLAW; CRAYON FIRE (a foe 6 off: hurt and set alight); STOMP (two foes near: slowed); BIG BLAZE (hurt, alight);
// WARM (out of a fight: Fire Resistance for you). Then the shared list.
// 3.0a: HOW HE'S MET - with Kettle and the Gem of Creativity out (rcon summons them, TestRat's own), a dye handed to Kettle (a right-
// click holding it; without the Gem only a hint, the dye kept): the Gem brings the drawing to life - his entrance, quiet till it's over - and
// right-clicked, he comes along.
// 3.0b: THE DOODLE CREEPER - his second costume, as a player: the wardrobe row locked (a hint), gunpowder handed to him (a right-click
// holding it: one taken, unlocked, he turns creeper - again: "I know that one"), his ways the creeper's, one or the other with Crayon
// Green, his creeper moves (Pop knocks back; Spark Breath pops a beat later, no fire; Fizz Stomp; KABOOM swells, flashes white, hurts
// every monster near and breaks no block; A Little Spark), kept through a send-home and a call, and off again.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'dragon', NAME: 'The Doodle Dragon', ab: 'dd', q: 'dz', pfx: 'p235d', prefix: 'dd_', item: 'doodle_drawing', parts: 12, figParts: 9, hp: 34, X: 17300, Z: 16000, pron: 'him',
  called: /scrambles back to you/, home: /folds himself back into a drawing/, sit: /curls up like a cat/, stand: /Adventure/,
  ways: ['Claw', 'Crayon Fire', 'Stomp', 'Big Blaze', 'Warm'], plain: 'Ender black', looks: ['Fire-Red Scales', 'Ocean-Blue Scales', 'Sunset-Purple Scales'],
  encounter: async (ctx) => {
    // (3.0a) THE GEM BRINGS IT TO LIFE - handed something as a regular player; its entrance; right-clicked: it comes along
    const K = kit(ctx, 'dz');
    const o = { name: 'The Doodle Dragon', host: 'p227', hostAb: 'kt', hostTag: 'bm.ktpet', hostName: 'Kettle', gem: true, item: 'minecraft:green_dye',
      noGemRe: /if only something could bring it to life/, bornRe: /scribbles in the air/, joined: /hands you his drawing/, itemId: 'doodle_drawing',
      props: 'a pencil (a prop) drawing him in the air' };
    const r = await K.born(o); K.bornOks(ctx.ok, r, o);
  },
  abilities: async (ctx) => {
    const { ok, nbt, O, run } = ctx; const K = kit(ctx, 'dz');
    ok('CLAW - a foe at his side: clawed', await K.move('mc', [[1.5, 0]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300));
    ok('CRAYON FIRE - a foe 6 off: crayon fire, hurt and alight', await K.move('rc', [[0, 6]], 'bm.trpf', async () => (await K.hp('bm.trpf')) < 300 && +((await nbt('@e[tag=bm.trpf,limit=1]', 'Fire')).match(/(-?\d+)/) || [0, -1])[1] > 0));
    ok('STOMP - two foes close: stomped, slowed', await K.move('k2', [[2, 0], [-2, 1]], 'bm.trps', async () => /slowness/.test(await K.fxOf('bm.trps')) && (await K.hp('bm.trps')) < 300));
    ok('BIG BLAZE - a foe 5 off: a long breath, hurt and alight', await K.move('gc', [[0, 5]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 290 && +((await nbt('@e[tag=bm.trpb,limit=1]', 'Fire')).match(/(-?\d+)/) || [0, -1])[1] > 0, 9000));
    await K.home(); await ctx.at(ctx.X + 0.5, ctx.Y + 1, ctx.Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await K.cd('k', 0);
    ok('WARM - out of a fight beside you: Fire Resistance for you', await ctx.wait(6000, async () => /fire_resistance/.test(await ctx.fx())));
    await K.calm();
    // ---- (3.0a) CRAYON GREEN - the Doodle ENDER Dragon's OG look, a costume row in his wardrobe (rigpet's FORM_WARDROBE, bm.ddog on the
    //      owner), chosen as a player would - sneak + use the drawing, Wardrobe, "Crayon Green": his parts wear their _og twins; and back
    const { A, sleep, cnt, score } = ctx;
    const part = (p) => `@e[type=minecraft:item_display,tag=bm.ddp_pet,tag=!bm.ddfade,tag=bm.ddp_${p},limit=1]`;
    const mdl = async (p) => (await nbt(part(p), 'item.components."minecraft:item_model"')).replace(/"/g, '');
    const row = () => A.buttons().find(b => /Crayon Green/.test(b.label));
    await run('scoreboard players set TestRat bm.ddog 0');
    await ctx.sneakMenu(0); const wd = await A.press(/Wardrobe/);
    ok('CRAYON GREEN - his wardrobe has the costume row: "Crayon Green  off"', wd && row() && /off/.test(row().label), A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/Crayon Green/); await sleep(1200);
    ok('...chosen: bm.ddog 1 - his body, head and wings wear their _og twins (dd_body_og, dd_wingr_og)', (await score('bm.ddog')) === 1 &&
       /^bm:dd_body_og(_c\d+)?$/.test(await mdl('body')) && /^bm:dd_wingr_og(_c\d+)?$/.test(await mdl('wingr')) && /_og(_c\d+)?$/.test(await mdl('head')),
       `${await mdl('body')} / ${await mdl('head')} / ${await mdl('wingr')}`);
    ok('...he scribbles himself over in green (his line)', A.bars.some(b => /scribbles himself over in green/.test(b)), A.bars.slice(-1).join(''));
    await ctx.sneakMenu(0); await A.press(/Wardrobe/); A.bars.length = 0; await A.press(/Crayon Green/); await sleep(1200);
    ok('...and back: bm.ddog 0, black crayon again (dd_body, dd_wingr)', (await score('bm.ddog')) === 0 &&
       /^bm:dd_body(_c\d+)?$/.test(await mdl('body')) && /^bm:dd_wingr(_c\d+)?$/.test(await mdl('wingr')) && A.bars.some(b => /back to black crayon/.test(b)),
       `${await mdl('body')} / ${await mdl('wingr')} | ${A.bars.slice(-1).join('')}`);
    await ctx.wait(1000, async () => (await cnt(ctx.PET)) === 1);
    // ---- (3.0b) THE DOODLE CREEPER - his second costume: locked until he's handed gunpowder (a right-click holding it: one taken, he
    //      scribbles himself into a creeper); then a wardrobe row next to Crayon Green, one or the other; his moves go creeper too
    const crRow = () => A.buttons().find(b => /Doodle Creeper/.test(b.label));
    const models = async () => `${await mdl('body')} ${await mdl('head')} ${await mdl('legr')} ${await mdl('wingr')} ${await mdl('tail')}`;
    const isCr = async () => /^bm:dd_body_cr(_c\d+)?$/.test(await mdl('body')) && /^bm:dd_head_cr(_c\d+)?$/.test(await mdl('head')) &&
      /^bm:dd_legr_cr(_c\d+)?$/.test(await mdl('legr')) && /^bm:dd_wingr_cr(_c\d+)?$/.test(await mdl('wingr')) && /^bm:dd_tail_cr(_c\d+)?$/.test(await mdl('tail'));
    const gp = async () => +(((await run('clear TestRat minecraft:gunpowder 0')).match(/Found (\d+)/) || [0, 0])[1]);
    await run('tag TestRat remove bm.ddcru'); await run('scoreboard players set TestRat bm.ddcr 0');
    await ctx.sneakMenu(0); await A.press(/Wardrobe/);
    ok('DOODLE CREEPER - his wardrobe has the row, next to Crayon Green: "Doodle Creeper  locked"', crRow() && /locked/.test(crRow().label), A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/Doodle Creeper/); await sleep(900);
    ok('...pressed while locked: a hint (hand him gunpowder), nothing on', A.bars.some(b => /gunpowder/.test(b)) && (await score('bm.ddcr')) === 0, A.bars.slice(-1).join(''));
    // handed gunpowder: right-click his click box holding it
    const HIT = '@e[type=minecraft:interaction,tag=bm.ddhit,limit=1]';
    const handGp = async () => { await run('item replace entity TestRat hotbar.8 with minecraft:gunpowder 2'); A.slot(8); await sleep(400);
      const wx = await ctx.num(ctx.PET, 'Pos[0]'), wz = await ctx.num(ctx.PET, 'Pos[2]'); await ctx.at(wx + 0.5, ctx.Y + 1, wz - 1.8, 0, 30);
      await run(`data modify entity ${ctx.PET} Sitting set value 1b`); await sleep(700);
      let hb = null; await ctx.wait(3000, async () => (hb = await ctx.entOf(HIT)) != null); A.slot(8); await sleep(300);
      A.bars.length = 0; A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1500); return !!hb; };
    await run(`data modify entity ${ctx.PET} Sitting set value 0b`);
    const reached = await handGp();
    ok('...handed gunpowder (a right-click holding it): one is taken, unlocked, and he scribbles himself into a creeper (his line)',
       reached && (await gp()) === 1 && /bm\.ddcru/.test(await ctx.tags()) && (await score('bm.ddcr')) === 1 && A.chats.some(c => /A CREEPER/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    ok('...his parts wear the creeper: dd_body_cr, dd_head_cr (its faces), dd_legr_cr - and his wings and tail an empty dd_wingr_cr / dd_tail_cr', await isCr(), await models());
    await run('clear TestRat minecraft:gunpowder'); await handGp();
    ok('...handed gunpowder again: "I know that one" - none taken', (await gp()) === 2 && A.bars.some(b => /know that one/.test(b)), A.bars.slice(-1).join(''));
    await run('clear TestRat minecraft:gunpowder'); await run(`data modify entity ${ctx.PET} Sitting set value 0b`);
    await ctx.at(ctx.X + 0.5, ctx.Y + 1, ctx.Z + 0.5, 0, 0); await sleep(2200);
    // his ways, while he's a creeper
    await ctx.sneakMenu(0); const pr = await A.press(/ways/);
    const pw = JSON.stringify(ctx.dd(A.dialogN[A.dialogN.length - 1]).body || []);
    ok("...his ways show the creeper's: Pop, Spark Breath, Fizz Stomp, KABOOM, A Little Spark", pr && ['Pop', 'Spark Breath', 'Fizz Stomp', 'KABOOM', 'A Little Spark'].every(w => pw.includes(w)), pw.slice(0, 160));
    await A.press(/« Back/); await sleep(2200);
    // one or the other: Crayon Green on takes the creeper off; the creeper on takes Crayon Green off
    await ctx.sneakMenu(0); await A.press(/Wardrobe/);
    ok('...the wardrobe row now reads "on"', crRow() && /\bon\b/.test(crRow().label), crRow() && crRow().label);
    await A.press(/Crayon Green/); await sleep(1200);
    ok('...Crayon Green turned on: the creeper comes off (bm.ddcr 0, bm.ddog 1, dd_body_og)', (await score('bm.ddcr')) === 0 && (await score('bm.ddog')) === 1 && /^bm:dd_body_og(_c\d+)?$/.test(await mdl('body')), await models());
    await ctx.sneakMenu(0); await A.press(/Wardrobe/); A.bars.length = 0; await A.press(/Doodle Creeper/); await sleep(1200);
    ok('...the Doodle Creeper turned on: Crayon Green comes off (bm.ddcr 1, bm.ddog 0), the creeper again (his line)',
       (await score('bm.ddcr')) === 1 && (await score('bm.ddog')) === 0 && await isCr() && A.bars.some(b => /crayon creeper/.test(b)), `${await models()} | ${A.bars.slice(-1).join('')}`);
    await sleep(2200);
    // his moves in the creeper's form (the stage as before: monsters set down, a cooldown cleared - he acts on his own)
    await run(`${O}fill ${ctx.X - 4} ${ctx.Y + 1} ${ctx.Z + 4} ${ctx.X + 4} ${ctx.Y + 3} ${ctx.Z + 4} minecraft:glass`);      // (blocks beside the blast)
    const hx = async (t) => ctx.num(`@e[tag=${t},limit=1]`, 'Pos[0]');
    let moved = false;
    ok('POP - a foe at his side: hurt, and blown well back', await K.move('mc', [[1.5, 0]], 'bm.trpc', async () => { if (Math.abs((await hx('bm.trpc')) - (ctx.X + 1.5)) > 1.2) moved = true;
      return moved && (await K.hp('bm.trpc')) < 300; }), `x ${await hx('bm.trpc')}`);
    ok('SPARK BREATH - a foe 6 off: sparks - a beat later it pops: hurt, and never set alight', await K.move('rc', [[0, 6]], 'bm.trpf', async () => (await K.hp('bm.trpf')) < 300 &&
       +((await nbt('@e[tag=bm.trpf,limit=1]', 'Fire')).match(/(-?\d+)/) || [0, 1])[1] <= 0));
    ok('FIZZ STOMP - two foes close: stomped, slowed', await K.move('k2', [[2, 0], [-2, 1]], 'bm.trps', async () => /slowness/.test(await K.fxOf('bm.trps')) && (await K.hp('bm.trps')) < 300));
    // KABOOM: the swell (his white flash, the whole rig bigger), the boom - every monster within 4 hurt - no block broken
    let flash = false, big = 0; const body = part('body');
    const boom = await K.move('gc', [[0, 2.5], [2, -1]], 'bm.trpb', async () => {
      if (/_crw/.test(await mdl('body'))) flash = true; big = Math.max(big, await ctx.num(body, 'transformation.scale[0]'));
      return flash && (await K.hp('bm.trpb')) < 300 && (await ctx.wait(10, async () => true)); }, 9000);
    const hurtAll = await ctx.wait(3000, async () => { const n = +((await run(`${O}execute if entity @e[tag=bm.trpb,nbt={Health:300f}]`)).match(/count: (\d+)/i) || [0, 0])[1]; return n === 0; });
    ok('KABOOM - he swells (the rig bigger) and flashes white (dd_body_crw) - then both monsters near him are hurt', boom && flash && big > 0.8 && hurtAll, `flash ${flash} scale ${big}`);
    let glassN = 0;
    for (let dx = -4; dx <= 4; dx++) for (let dy = 1; dy <= 3; dy++) if (/passed/i.test(await run(`${O}execute if block ${ctx.X + dx} ${ctx.Y + dy} ${ctx.Z + 4} minecraft:glass`))) glassN++;
    ok('...no block broken (the glass beside him all there), and back to his own size and colours after (scribbled back together)', glassN === 27 &&
       await ctx.wait(4000, async () => /^bm:dd_body_cr(_c\d+)?$/.test(await mdl('body')) && (await ctx.num(body, 'transformation.scale[0]')) < 0.8), `glass ${glassN}/27`);
    await run(`${O}fill ${ctx.X - 4} ${ctx.Y + 1} ${ctx.Z + 4} ${ctx.X + 4} ${ctx.Y + 3} ${ctx.Z + 4} minecraft:air`);
    await K.home(); await ctx.at(ctx.X + 0.5, ctx.Y + 1, ctx.Z - 1.5, 0, 10); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await K.cd('k', 0);
    ok('A LITTLE SPARK - out of a fight beside you: Absorption and Regeneration for you', await ctx.wait(6000, async () => { const f = await ctx.fx(); return /absorption/.test(f) && /regeneration/.test(f); }));
    await K.calm();
    // kept through a send-home and a call
    await ctx.sneakMenu(0); await A.press(/Send him home/); await ctx.wait(3000, async () => (await cnt(ctx.PET)) === 0);
    await run('scoreboard players set TestRat bm.ddcd 0'); await ctx.use(0); await ctx.wait(4000, async () => (await cnt(ctx.PET)) === 1); await sleep(1500);
    ok('...sent home and called again: still the Doodle Creeper', await isCr(), await models());
    // and off
    await sleep(2200); await ctx.sneakMenu(0); await A.press(/Wardrobe/); A.bars.length = 0; await A.press(/Doodle Creeper/); await sleep(1200);
    ok('...turned off in his wardrobe: the Doodle Ender Dragon again (bm.ddcr 0; dd_body, dd_wingr)', (await score('bm.ddcr')) === 0 &&
       /^bm:dd_body(_c\d+)?$/.test(await mdl('body')) && /^bm:dd_wingr(_c\d+)?$/.test(await mdl('wingr')) && A.bars.some(b => /Ender Dragon again/.test(b)), `${await models()} | ${A.bars.slice(-1).join('')}`);
    await run('tag TestRat remove bm.ddcru');
    await ctx.wait(1000, async () => (await cnt(ctx.PET)) === 1);
  } });
