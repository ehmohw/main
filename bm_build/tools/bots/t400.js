// 3.1: THE GOLDEN DOODLE (phase275, the 64th follower - the last) as a regular (non-op) player - the owner's checklist (rigpet_t), copied from
// t399: her meeting staged (her fight won: rcon tags TestRat bm.gdwin and stands her up - admin/gdoodle_meet); right-clicked: the Doodle Egg;
// her goose ways (HONK, the NECK-WHIP SLAP, the WADDLE CHARGE); the FORM button (her menu's Settings page): goose -> the Gilded Eldritch (host 1.6, the
// bm.gqf1 tag, the gk_ models) -> her Lightbringer form (bm.gqf2, gh_) -> goose (0.8); COMPANION SIZE in a big form (host 1.0); the form kept
// across a recall; her doll set down and sneak + right-clicked: goose -> Eldritch -> Lightbringer form. The shared list.
const runT = require('./rigpet_t'); const kit = require('./doodle_kit');
runT({ W: 'gdoodle', NAME: 'The Golden Doodle', ab: 'gq', q: 'gu', pfx: 'p275', prefix: 'gq_', item: 'doodle_egg', parts: 35, figParts: 11, hp: 48, X: 19620, Z: 16000, pron: 'her',
  lookPart: 'body', seatPart: 'head', called: /waddles back to you/, home: /tucks herself into a golden egg/, sit: /plops down/, stand: /shakes out her feathers/,
  ways: ['The Goose', 'The Gilded Eldritch', 'Her Lightbringer form', 'Form', 'Companion Size', 'Lucky'],
  plain: 'Gold leaf', looks: ['Rose Gold', 'Platinum', 'Midnight Gold'],
  encounter: async (ctx) => {
    const { ok, run, has, A, sleep, wait, O, cnt, entOf, at, num, ENC, X, Y, Z } = ctx;
    await run('tag TestRat remove bm.gqmet'); await run('tag TestRat add bm.gdwin'); await run('clear TestRat'); await run('kill @e[type=minecraft:interaction,tag=bm.gqenc]');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s rotated 0 0 run function bm:admin/gdoodle_meet`);
    ok('her fight won: the cured goose stands by the pond (staged)', await wait(3000, async () => (await cnt(ENC)) === 1));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 20);
    let eb = null; await wait(4000, async () => (eb = await entOf(ENC)) != null, 250);
    A.slot(8); await sleep(250); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked: the Doodle Egg, and she comes along', (await has('doodle_egg')) === 1);
  },
  abilities: async (ctx) => {
    const { ok, run, num, nbt, A, sleep, PET, cnt, O } = ctx; const K = kit(ctx, 'gu');
    await run('scoreboard players set TestRat bm.gqform 0'); await run(`data modify entity ${PET} Sitting set value 0b`);
    ok('HONK - a foe 3 off: hurt', await K.move('mc', [[0, 3]], 'bm.trpa', async () => (await K.hp('bm.trpa')) < 300, 8000));
    ok('the NECK-WHIP SLAP - two foes 2 off: hurt', await K.move('k2', [[1, 2], [-1, 2]], 'bm.trpb', async () => (await K.hp('bm.trpb')) < 300, 8000));
    ok('the WADDLE CHARGE - a foe 7 off: she runs at it, and it is hurt', await K.move('rc', [[0, 7]], 'bm.trpc', async () => (await K.hp('bm.trpc')) < 300, 9000));
    const SC = async () => num(PET, 'attributes[{id:"minecraft:scale"}].base');
    const HEAD = '@e[type=minecraft:item_display,tag=bm.gqp_pet,tag=bm.gqp_head,limit=1]';
    const mdl = async () => (await nbt(HEAD, 'item.components."minecraft:item_model"')).replace(/"/g, '');
    const form = async () => { await ctx.sneakMenu(0); await A.press(/Settings/); await sleep(800); await A.press(/Form/); await sleep(1500); };   // (phase260: Form is on her Settings page)
    await K.home();
    await form();
    ok('FORM: the Gilded Eldritch - host 1.6, its models', Math.abs((await SC()) - 1.6) < 0.01 && (await cnt(`${PET.slice(0, -1)},tag=bm.gqf1]`)) === 1 && /gk_head/.test(await mdl()), await mdl());
    await ctx.sneakMenu(0); await A.press(/Companion Size/); await sleep(1500);
    ok('COMPANION SIZE in a big form: host 1.0', Math.abs((await SC()) - 1.0) < 0.01);
    await ctx.sneakMenu(0); await A.press(/Companion Size/); await sleep(1200);
    await form();
    ok('FORM: her Lightbringer form - bm.gqf2, the gh_ models', (await cnt(`${PET.slice(0, -1)},tag=bm.gqf2]`)) === 1 && /gh_head/.test(await mdl()), await mdl());
    await A.press(/Send .* home/).catch(() => {}); await sleep(1500); await ctx.use(0); await sleep(2500);
    ok('...recalled: still her Lightbringer form', (await cnt(`${PET.slice(0, -1)},tag=bm.gqf2]`)) === 1);
    await form();
    ok('FORM: the goose again - host 0.8, the gq_ models', Math.abs((await SC()) - 0.8) < 0.01 && /gq_head/.test(await mdl()), await mdl());
    // (her doll: set down, then sneak + right-clicked - the three forms, round again)
    await run('loot replace entity TestRat hotbar.7 loot bm:items/doll_gdoodle'); await ctx.use(7); await sleep(1200);
    const DOLL = '@e[type=minecraft:item_display,tag=bm.doll_gdoodled,limit=1]', DHIT = '@e[type=minecraft:interaction,tag=bm.doll_gdoodlehit,limit=1]';
    const dm = async () => (await nbt(DOLL, 'item.components."minecraft:item_model"')).replace(/"/g, '');
    let db = null; await ctx.wait(3000, async () => (db = await ctx.entOf(DHIT)) != null, 250);
    const seen = [await dm()];
    for (let i = 0; i < 3; i++) { A.input({ shift: true }); await sleep(200); if (db) A.interact(db.entityId); await sleep(600); A.input({}); await sleep(400); seen.push(await dm()); }
    ok('her doll, sneak + right-clicked: goose -> Eldritch -> Lightbringer form -> goose', seen.join(',') === 'bm:doll_gdoodle,bm:doll_gdoodle_k,bm:doll_gdoodle_h,bm:doll_gdoodle', seen.join(','));
    await run(`${O}kill ${DOLL}`); await run(`${O}kill ${DHIT}`);
  } });
