// 3.1: THE MIMIC (phase270, the 59th follower) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from t393:
// a Tier III heist of nothing but Three Coffers rooms (h110's stage, as t111's); this room the one in forty (admin/mimic_vault -
// rcon); TestRat right-clicks a WRONG coffer (a real click on its box): not the vault's Mimic - THE Mimic (its encounter), in a
// TANTRUM - right-clicked empty-handed: SNAP (no key); a Gutter Coin in hand: it eats it, calms; right-clicked: the Mimic's Key,
// and it comes along. Out of the vault, its ways: SNAP LUNGE (hurt); DISGUISE (still 5 s: just a chest, eyes shut) and the AMBUSH
// (a monster walked up to it: the snap at double); SWALLOW AND SPIT (a foe swallowed - unseen - and spat out, hurt); THE STASH
// (sneak + right-click: it opens wide - a stash cart under its mouth; TestRat right-clicks into it: the stash's screen opens; what's
// in it is kept when it shuts, and there when it opens again). Right-click sit (it settles). The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit'); const { mk, rel } = require('./h110');
runT({ W: 'mimic', NAME: 'The Mimic', ab: 'mx', q: 'wx', pfx: 'p270', prefix: 'mm_', item: 'mimic_key', parts: 13, figParts: 7, hp: 34, X: 19380, Z: 16000, pron: 'it',
  lookPart: 'body', seatPart: 'lid', called: /clatters back to you/, home: /is just a chest/, sit: /settles, feet tucked/, stand: /There's loot somewhere/,
  ways: ['Snap Lunge', 'Disguise', 'Swallow and Spit', 'The Stash', 'Finders Keepers'],
  plain: 'Oak chest', looks: ['Trapped Chest', 'Christmas Chest', 'Black Tongue'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, X, Y, Z } = ctx;
    const H = mk(run); const { room, at: atR, sc, qs, heist, begin, go } = H;
    const G = 'execute in bm:gutter run ';
    const cntG = async (sel) => +(((await run(`${G}execute if entity ${sel}`)).match(/count: (\d+)/i) || [0, 0])[1]);
    const uuidG = async (sel) => { const m = (await run(`${G}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
      const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
    const entG = async (sel) => { const u = await uuidG(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
    await run('tag TestRat remove bm.mxmet'); await run('tag TestRat remove bm.wxheard'); await run('kill @e[type=minecraft:interaction,tag=bm.mxenc]');
    await heist('coffers', 'a', 3); await begin();
    const Q = await qs('coffers'); const q = Q[0];
    ok('a Tier III heist, its Three Coffers rooms (the stage: h110)', Q.length > 0, `${Q}`);
    await atR('coffers', q, 'function bm:admin/mimic_vault');
    const h = await sc('coffers', q, 'bm.gvc'); const wrong = (h + 1) % 4; const CZ = [6, 10, 14, 18];
    await go('coffers', q, 17.5, CZ[wrong] + 0.5); await sleep(1500);
    const COF = `@e[type=minecraft:interaction,tag=bm.gvcof${wrong},limit=1]`;
    let cb = null; await wait(4000, async () => (cb = await entG(COF)) != null, 250);
    A.slot(8); await run('item replace entity TestRat hotbar.8 with minecraft:air'); await sleep(250); A.chats.length = 0;
    if (cb) A.interact(cb.entityId); await sleep(1200);
    const ENC = '@e[type=minecraft:interaction,tag=bm.mxenc,limit=1]';
    ok('a wrong coffer opened, in that room: it LOOKS BACK - THE Mimic, in a tantrum (its encounter; no vault Mimic)', (await cntG(ENC)) === 1 &&
       A.chats.some(c => /LOOKS BACK/.test(c)) && (await cntG('@e[type=minecraft:rabbit,tag=bm.gvmimic]')) === 0, A.chats.slice(-1).join('').slice(0, 160));
    ok('...it hops about in its tantrum (bm.wxtt running)', /has [1-9]/.test(await run(`${G}scoreboard players get ${ENC} bm.wxtt`)));
    let eb = null; await wait(4000, async () => (eb = await entG(ENC)) != null, 250);
    A.chats.length = 0; A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(1000);
    ok('right-clicked mid-tantrum, empty-handed: SNAP - no key', (await has('mimic_key')) === 0 && A.bars.some(b => /SNAP/.test(b)), A.bars.slice(-1).join(''));
    await run('loot replace entity TestRat hotbar.8 loot bm:items/gutter_coin'); A.slot(8); await sleep(400);
    eb = await entG(ENC); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1200);
    ok('...a Gutter Coin handed to it: eaten, DELIGHTED - it calms (licks you)', A.chats.some(c => /DELIGHTED/.test(c)) && A.chats.some(c => /LICKS/.test(c)) &&
       +(((await run('clear TestRat *[minecraft:custom_data~{bm:"gutter_coin"}] 0')).match(/Found (\d+)/) || [0, 0])[1]) === 0, A.chats.slice(-2).join(' | ').slice(0, 200));
    eb = await entG(ENC); A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked, calm: the Mimic\'s Key in TestRat\'s hands, and it comes along', (await has('mimic_key')) === 1, A.chats.slice(-2).join(' | ').slice(0, 200));
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('execute in bm:gutter run kill @e[type=minecraft:interaction,tag=bm.mxenc]'); await run('execute in bm:gutter run kill @e[type=minecraft:item_display,tag=bm.mxencp]');
    await run('effect give TestRat minecraft:resistance 900 4 true');
    await ctx.at(X + 0.5, Y + 1, Z + 0.5, 0, 10); await sleep(1500);
  },
  abilities: async (ctx) => {
    const { ok, run, wait, num, nbt, cnt, A, sleep, PET, X, Y, Z, O, at, entOf, score } = ctx; const K = kit(ctx, 'wx');
    const HIT = '@e[type=minecraft:interaction,tag=bm.mxhit,limit=1]';
    const LID = '@e[type=minecraft:item_display,tag=bm.mxp_pet,tag=bm.mxp_lid,tag=!bm.mxfade,limit=1]';
    await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('SNAP LUNGE - a foe 2 off: hurt', await K.move('mc', [[0, 2]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    let gone = false;
    ok('SWALLOW AND SPIT - a foe 2 off: swallowed (unseen, bm.wxin) - and spat out, hurt', await K.move('gc', [[0, 2]], 'bm.trpb', async () => {
      if ((await cnt('@e[tag=bm.trpb,tag=bm.wxin]')) === 1) gone = true; return gone && (await cnt('@e[tag=bm.trpb,tag=bm.wxin]')) === 0 && (await K.hp('bm.trpb')) < 300; }, 9000), `swallowed ${gone}`);
    ok('...spat out as it was (its NoAI kept, visible again)', /1b/.test(await nbt('@e[tag=bm.trpb,limit=1]', 'NoAI')) && !/invisibility/.test(await K.fxOf('bm.trpb')));
    // DISGUISE, and the ambush
    await K.home(); await run(`scoreboard players set ${PET} bm.wxds 0`);
    ok('DISGUISE - still 5 s, no foe near: just a chest (bm.mxdis), its eyes shut', await wait(9000, async () => /bm\.mxdis/.test(await nbt(PET, 'Tags'))), await nbt(PET, 'Tags'));
    await run(`scoreboard players set ${PET} bm.wxmc 0`); await ctx.zom(0, 1.6, 'bm.trpc');
    ok('...a monster walks up to it: AMBUSHED - the snap at double', await wait(5000, async () => (await K.hp('bm.trpc')) < 294.5) && !/bm\.mxdis/.test(await nbt(PET, 'Tags')),
       `${await K.hp('bm.trpc')}`);
    // THE STASH
    await K.home(); await sleep(800);
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.6, 0, 40); A.slot(7); await run('item replace entity TestRat hotbar.7 with minecraft:air'); await sleep(300);
    let hb = await entOf(HIT); A.bars.length = 0; if (hb) A.interact(hb.entityId, true); await sleep(1200);
    const CART = '@e[type=minecraft:chest_minecart,tag=bm.mxcart,limit=1]';
    ok('THE STASH - sneak + right-click: it opens wide (bm.mxst), a stash cart under its mouth', /bm\.mxst/.test(await nbt(PET, 'Tags')) && (await cnt(CART)) === 1 &&
       A.bars.some(b => /welcome mat/.test(b)), A.bars.slice(-1).join(''));
    const w0 = A.windows.length; let cart = await entOf(CART); if (cart) A.interact(cart.entityId); await sleep(1000);
    ok('...TestRat right-clicks into its mouth: the stash\'s screen opens', A.windows.length > w0, `${A.windows.length - w0}`);
    // (an item put in its first slot - by rcon: the bot library has no container clicks - then the screen shut, and TestRat walks off)
    await run(`${O}item replace entity ${CART} container.0 with minecraft:diamond 3`);
    if (A.windows.length > w0) A.close(A.windows[A.windows.length - 1].windowId); await sleep(400);
    await at(wx + 0.5, Y + 1, wz - 8.5, 0, 10);
    ok('...walked off: it shuts (the cart gone, not dropped)', await wait(4000, async () => !/bm\.mxst/.test(await nbt(PET, 'Tags')) && (await cnt(CART)) === 0) &&
       (await cnt(`@e[type=minecraft:item,x=${wx},y=${Y},z=${wz},distance=..4]`)) === 0);
    await at(wx + 0.5, Y + 1, wz - 1.6, 0, 40);
    hb = await entOf(HIT); if (hb) A.interact(hb.entityId, true); await sleep(1200);
    ok('...opened again: the three diamonds still in it (kept on TestRat)', /diamond/.test(await nbt(CART, 'Items')) && /count: 3/.test(await nbt(CART, 'Items')), await nbt(CART, 'Items'));
    await at(wx + 0.5, Y + 1, wz - 8.5, 0, 10);
    ok('...and shut again as TestRat goes', await wait(4000, async () => !/bm\.mxst/.test(await nbt(PET, 'Tags')) && (await cnt(CART)) === 0));
    await run('data remove storage bm:mxst p' + (await score('bm.pid')));
    // ---- THE TREASURE CHEST (look 8, an outfit): unlocked (rcon - as if bought), chosen in its wardrobe: every swapped part's model the
    //      outfit's (its body's item definition the strongbox's, mmt_body); kept across a send-home
    const BODY8 = '@e[type=minecraft:item_display,tag=bm.mxp_pet,tag=bm.mxp_body,tag=!bm.mxfade,limit=1]';
    await run('execute as TestRat run function bm:p99/unlock/mimic8'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
    await ctx.sneakMenu(0); await A.press(/Wardrobe/); const tc = await A.press(/Treasure Chest/); await sleep(1500);
    const def = JSON.stringify(JSON.parse(require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_RP/assets/bm/items/mm_body_c8.json', 'utf8')));
    ok('THE TREASURE CHEST - chosen in its wardrobe: its body mm_body_c8, the strongbox\'s model (mmt_body)', !!tc && (await score('bm.cosmx')) === 8 &&
       /mm_body_c8/.test(await nbt(BODY8, 'item.components."minecraft:item_model"')) && /mmt_body/.test(def), `${await nbt(BODY8, 'item.components."minecraft:item_model"')} | ${def.slice(0, 80)}`);
    await ctx.sneakMenu(0); await A.press(/Send .* home/); await sleep(1500); await ctx.use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2500);
    ok('...sent home and called again: still the Treasure Chest', /mm_body_c8/.test(await nbt(BODY8, 'item.components."minecraft:item_model"')));
    await run('scoreboard players set TestRat bm.cosmx 0'); await run(`${O}execute as TestRat run function bm:p99/mimic_now`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  } });
