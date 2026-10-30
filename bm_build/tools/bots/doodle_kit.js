// 2.97: what the seven 2.97 followers' tests share (t304-t310): an ability fired by clearing its cooldown, as rigpet_t's own
// tests do (the stage: rcon; the follower acts on its own), and an encounter met as a player - right-clicked empty-handed, then
// with the thing it wants in hand. (3.0a: an encounter with an entrance - rigpet's ENC_SHOW - is watched through it first: quiet
// while it runs, whole and clickable once it's over; `showOks` words its checks.)
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
    const placed = await wait(5000, async () => (await cnt(ENC)) === 1, 100);
    const pre = await early(ctx);
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(hand); await sleep(250);
    const show = await entrance(ctx, eb, asks, pre);
    if (show.had) { eb = await entOf(ENC); A.slot(hand); await sleep(250); }
    A.bars.length = 0; if (eb && asks) { A.interact(eb.entityId); await sleep(900); }
    const asked = !asks || A.bars.some(b => asks.test(b));
    const lastBar = A.bars.slice(-1).join('');
    if (wantItem) await run(`item replace entity TestRat hotbar.${hand} with ${wantItem}`); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    const got = (await has(itemId)) === 1 && A.chats.some(c => joined.test(c));
    return { placed, asked, got, lastBar, chat: A.chats.slice(-2).join(' | ').slice(0, 200), show };
  };
  // (3.0a) THE ENTRANCE (rigpet's Cfg.ENC_SHOW): while bm.<q>sh runs the rig builds itself (it starts at scale 0) and the box
  // won't talk - a right-click then gets nothing; once it's over (well within 10 s) the rig is whole and the show's props gone.
  // { had: false } when the encounter has no show.
  const BODY = () => `@e[type=minecraft:item_display,tag=bm.${ctx.C.ab}encp,tag=bm.${ctx.C.ab}p_body,limit=1]`;
  // (read the moment it's placed: is a show running, and how big is the rig)
  const early = async ({ ENC }) => ({ s0: await ctx.score(`bm.${q}sh`, ENC), scale0: await num(BODY(), 'transformation.scale[1]') });
  // (asks: the actionbar it answers an empty hand with; talked: or an async test of its own - the Cursor's click recruits outright)
  const entrance = async ({ A, sleep, C, ENC }, eb, asks, pre, talked) => {
    const sh = async () => ctx.score(`bm.${q}sh`, ENC);
    const PROPS = `@e[tag=bm.${C.ab}shp]`;
    const { s0, scale0 } = pre || await early(ctx);
    if (!(s0 >= 1) || !((await sh()) >= 1)) return { had: false };
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(700);
    const quiet = !A.bars.some(b => asks && asks.test(b)) && !(talked && await talked());
    let props = 0, peak = 0; const looks = new Set();
    const t0 = Date.now();
    const over = await wait(10000, async () => { props = Math.max(props, await cnt(PROPS)); const v = await sh(); peak = Math.max(peak, v);
      looks.add(await nbt(BODY(), 'transformation')); return v === 0; }, 150);
    const secs = (Date.now() - t0) / 1000 + 0.7;
    await sleep(400);
    const whole = (await num(BODY(), 'transformation.scale[1]')) > 0.3;
    const cleared = (await cnt(PROPS)) === 0;
    return { had: true, started: s0 >= 1, scale0, quiet, over, secs, peak, props, moved: looks.size, whole, cleared };
  };
  // the entrance's own checks, worded for a test's ok() list (r: what meet() returned)
  const showOks = (ok, r, name, props) => {
    const s = r.show || {};
    if (props) ok(`${name}: ...${props}`, s.had && s.props >= 1, `props seen ${s.props}`);
    ok(`${name}: its entrance starts as soon as it's placed (the rig at scale 0, building itself)`, s.had && s.started && s.scale0 < 0.05, JSON.stringify(s));
    ok(`${name}: ...right-clicked mid-show, it doesn't talk yet`, s.had && s.quiet);
    ok(`${name}: ...the show moves (the rig's transformation changing as it goes)`, s.had && s.moved >= 3, `${s.moved} looks seen`);
    ok(`${name}: ...and ends within 10 s - the rig whole, the show's props gone`, s.had && s.over && s.whole && s.cleared, `${(s.secs || 0).toFixed(1)} s, props seen ${s.props}`);
  };
  return { cd, calm, fxOf, hp, home, move, meet, early, entrance, showOks };
};
