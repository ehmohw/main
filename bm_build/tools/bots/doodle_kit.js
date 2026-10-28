// 2.97: what the seven 2.97 followers' tests share (t304-t310): an ability fired by clearing its cooldown, as rigpet_t's own
// tests do (the stage: rcon; the follower acts on its own), and an encounter met as a player - right-clicked empty-handed, then
// with the thing it wants in hand.
module.exports = (ctx, q) => {
  const { run, wait, O, nbt, num, cnt, PET, X, Y, Z, zom } = ctx;
  const cd = async (o, v) => run(`scoreboard players set ${PET} bm.${q}${o} ${v}`);
  const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2', 'x']) await cd(o, o === 'x' ? 0 : 900); };
  const fxOf = async (t) => nbt(`@e[tag=${t},limit=1]`, 'active_effects');
  const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
  const home = async () => { await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await ctx.sleep(400); };
  // one move: foes set down at [dx, dz] (from the follower, at X Z), its cooldown cleared, then the test
  const move = async (o, foes, tag, test, ms = 7000) => {
    await home(); for (const [dx, dz] of foes) await zom(dx, dz, tag);
    await cd(o, 0); return wait(ms, test);
  };
  // the encounter: placed by rcon (as it would place itself), met as a player
  const meet = async ({ A, at, entOf, sleep, has, ENC }, place, asks, wantItem, joined, itemId, hand = 8) => {
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s rotated 0 0 positioned ^ ^ ^5 run function bm:${place}`);
    const placed = await wait(5000, async () => (await cnt(ENC)) === 1);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(hand); await sleep(250);
    A.bars.length = 0; if (eb && asks) { A.interact(eb.entityId); await sleep(900); }
    const asked = !asks || A.bars.some(b => asks.test(b));
    const lastBar = A.bars.slice(-1).join('');
    if (wantItem) await run(`item replace entity TestRat hotbar.${hand} with ${wantItem}`); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    const got = (await has(itemId)) === 1 && A.chats.some(c => joined.test(c));
    return { placed, asked, got, lastBar, chat: A.chats.slice(-2).join(' | ').slice(0, 200) };
  };
  return { cd, calm, fxOf, hp, home, move, meet };
};
