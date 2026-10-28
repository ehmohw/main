// 2.98: the shared as-a-player test of a Gutter Gentry follower (t297 Batty, t298 Eggbert, t299 the Count) - rigpet_t's owner's list,
// with the Gentry's own way in: each win over the Gutter Gentry (rcon: the stage - that lair won, the earlier wins' tokens already
// given) leaves the next one's Calling Token (Batty's, then Eggbert's, then the Count's); used (a real use), it signs him on and
// calls him. His chibi costume is his second form.
const runT = require('./rigpet_t');
module.exports = (G) => runT(Object.assign({
  form: { button: /Gentry \/ chibi/, suffix: '_c', score: `bm.${G.ab}form` }, prefix: `${G.pre}`, pron: 'him',
  encounter: async ({ A, run, ok, wait, O, has, X, Y, Z, sleep, use }) => {
    for (let n = 1; n <= 3; n++) await run(`tag TestRat ${n < G.n ? 'add' : 'remove'} bm.gtk${n}`);
    A.chats.length = 0;
    await run(`${O}execute as TestRat at @s run function bm:p232/won`);       // (the stage: the Gentry beaten, once more)
    ok(`the Gutter Gentry beaten (win ${G.n}): ${G.NAME}'s Calling Token, slipped to you`, await wait(4000, async () => (await has(G.item)) === 1 &&
       A.chats.some(c => new RegExp(`${G.NAME} slips you a calling token`).test(c))), A.chats.slice(-1).join('').slice(0, 160));
    ok('...and only his', (await Promise.all(G.others.map(has))).every(n => n === 0));
    await run(`clear TestRat *[minecraft:custom_data~{bm:"${G.item}"}]`); await run(`loot replace entity TestRat hotbar.7 loot bm:items/${G.item}`);
    A.chats.length = 0; await use(7);
    ok('the token used: he answers it - a second chance', await wait(4000, async () => A.chats.some(c => new RegExp(`${G.NAME} answers the token`).test(c))), A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async ({ run, ok, wait, O, nbt, num, fx, PET, zom, X, Y, Z, sleep, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.${G.q}${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    const fxOf = async (t) => nbt(`@e[tag=${t},limit=1]`, 'active_effects');
    await run(`${O}time set noon`); await calm();
    await zom(2.0, 0, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~1.4 ~ ~`); await cd('mc', 0);
    ok(`${G.ways[0].toUpperCase()} - a foe beside him`, await wait(5000, async () => (await hp('bm.trps')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    if (G.ranged) {
      await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(8, 0, 'bm.trpr'); await cd('rc', 0);
      ok(`${G.ranged} - a foe 8 off: struck from range, slowed`, await wait(7000, async () => (await hp('bm.trpr')) < 300 && /slowness/.test(await fxOf('bm.trpr'))));
      await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    }
    if (G.crowd) {
      await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); for (const [dx, dz] of [[1.5, 1], [1.5, -1]]) await zom(dx, dz, 'bm.trph'); await cd('k2', 0);
      ok(`${G.crowd[0]} - two foes close: ${G.crowd[1]}`, await wait(6000, async () => new RegExp(G.crowd[1]).test(await fxOf('bm.trph'))));
      await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    }
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(2, 0, 'bm.trpc'); await cd('gc', 0);
    ok(`${G.charge[0]} - charged: ${G.charge[1] || 'struck'}`, await wait(8000, async () => (await hp('bm.trpc')) < 295 && (!G.charge[1] || new RegExp(G.charge[1]).test(await fxOf('bm.trpc')))));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(3000);
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await cd('k', 0);
    ok(`${G.kind[0]} - out of a fight beside you: ${G.kind.slice(1).join(' and ')}`, await wait(7000, async () => { const f = await fx(); return G.kind.slice(1).every(e => f.includes(e)); }));
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await calm();
  } }, G));
