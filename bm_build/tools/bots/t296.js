// 2.98: THE GEM OF CREATIVITY, as a regular (non-op) player - the owner's checklist (rigpet_t). It comes to you when the Creative
// Spark forms: Mr. Capshun, Kettle and Emma called with their own items (real uses) - and down out of the sky, once, comes the Gem.
// Its ways: CONJURE (a foe within 14: one of its 3D Buddies pops out of a sparkle at it, its own attack), PRISM (a foe close: a flash
// off its facets), INSPIRATION (out of a fight: Haste and Luck for you), MASTERPIECE (three foes: three Buddies at once). It feels in
// text - an emoticon riding over it (:) c: :o :3 o3o ^-^ ;( ...): >:( in a fight. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'gem', NAME: 'The Gem of Creativity', ab: 'cg', q: 'cq', pfx: 'p231', prefix: 'cg_', item: 'creativity_gem', parts: 3, figParts: 3, hp: 40, X: 17400, Z: 17600, pron: 'it',
  called: /floats down to you/, home: /twinkles goodbye/, sit: /settles low and dims/, stand: /lifts and brightens/,
  ways: ['Conjure', 'Prism', 'Inspiration', 'Masterpiece', 'Creative Forms'],
  plain: 'Its own colours', looks: ['Ruby Facets', 'Sapphire Facets', 'Amethyst Facets'], lookPart: 'body',
  encounter: async ({ A, run, ok, wait, O, cnt, has, X, Y, Z, sleep, use }) => {
    for (const t of ['bm.mzmet', 'bm.ktmet', 'bm.emmet']) await run(`tag TestRat add ${t}`);
    for (const o of ['bm.mzcd', 'bm.ktcd', 'bm.emcd']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('advancement revoke TestRat only bm:story/trio_creative_spark');
    const items = ['capshun_pencil', 'kettle_plane', 'emma_ribbon'];
    for (const [i, iid] of items.entries()) await run(`loot replace entity TestRat hotbar.${i + 5} loot bm:items/${iid}`);
    A.chats.length = 0;
    for (let i = 0; i < 3; i++) { await use(i + 5); await sleep(2200); }
    const here = [await cnt('@e[type=minecraft:wolf,tag=bm.mzpet]'), await cnt('@e[type=minecraft:wolf,tag=bm.ktpet]'), await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')];
    ok('Mr. Capshun, Kettle and Emma called with their own items', here.every(n => n >= 1), here.join(','));
    ok('...together, the Creative Spark: down out of the sky comes the Gem - yours', await wait(8000, async () => (await has('creativity_gem')) === 1) &&
       A.chats.some(c => /A swirl of every colour comes down out of the sky/.test(c)), A.chats.slice(-3).join(' | ').slice(0, 200));
    for (const w of ['capshun', 'kettle', 'emma']) await run(`${O}execute as TestRat at @s run function bm:p98/home/${w}`);
    for (let i = 5; i < 8; i++) await run(`item replace entity TestRat hotbar.${i} with minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
    await run('clear TestRat *[minecraft:custom_data~{bm:"creativity_gem"}]'); await run('loot replace entity TestRat hotbar.7 loot bm:items/creativity_gem');
    await use(7); await sleep(1500);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, X, Y, Z, sleep, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.cq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'rc', 'mc', 'k']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    const EMO = '@e[type=minecraft:text_display,tag=bm.cgemo,limit=1]';
    await run(`${O}time set noon`); await calm();
    ok('an emoticon rides over it (how it feels, in text)', await wait(4000, async () => (await cnt(EMO)) === 1));
    await zom(2.0, 0, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~1.4 ~ ~`); await cd('mc', 0);
    ok('PRISM - a foe beside it: a flash off its facets', await wait(5000, async () => (await hp('bm.trps')) < 300));
    ok('...and in a fight its face says so (>:( >:o :|)', await wait(4000, async () => /(>:\(|>:o|:\|)/.test(await nbt(EMO, 'text'))), await nbt(EMO, 'text'));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(9, 0, 'bm.trpp'); await cd('rc', 0);
    ok('CONJURE - a foe 9 off: one of its Buddies pops out of a sparkle at it', await wait(6000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgbdm]')) >= 1));
    ok('...the Buddy strikes', await wait(5000, async () => (await hp('bm.trpp')) < 300));
    ok('...and goes', await wait(8000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgbdm]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.cgbdp]')) === 0));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); for (const [dx, dz] of [[4, 0], [4, 2], [4, -2]]) await zom(dx, dz, 'bm.trpm'); await cd('gc', 0);
    ok('MASTERPIECE - three foes: three Buddies at once', await wait(8000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgbdm]')) >= 2));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(4000);
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await cd('k', 0);
    ok('INSPIRATION - out of a fight beside you: Haste and Luck', await wait(7000, async () => /haste/.test(await fx()) && /luck/.test(await fx())));
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await calm();
  } });
