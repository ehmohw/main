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
    // (the show is under way while the bot walks up to it: its moves are watched from the start - a short show (the Dryad's, 4 s)
    //  is mostly over by the time the bot stands beside it)
    const looks0 = new Set(); let sampling = pre.s0 >= 1;
    const sampler = (async () => { while (sampling) { looks0.add(await nbt(BODY(), 'transformation')); await sleep(150); } })();
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(hand); await sleep(250);
    const show = await entrance(ctx, eb, asks, pre);
    sampling = false; await sampler; if (show.had) show.moved = new Set([...looks0, ...(show.looksSeen || [])]).size;
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
    return { had: true, started: s0 >= 1, scale0, quiet, over, secs, peak, props, moved: looks.size, looksSeen: [...looks], whole, cleared };
  };
  // the entrance's own checks, worded for a test's ok() list (r: what meet() returned)
  const showOks = (ok, r, name, props) => {
    const s = r.show || {};
    if (props) ok(`${name}: ...${props}`, s.had && s.props >= 1, `props seen ${s.props}`);
    ok(`${name}: its entrance starts as soon as it's placed (the rig at scale 0, building itself)`, s.had && s.started && s.scale0 < 0.05, JSON.stringify({ ...s, looksSeen: undefined }));
    ok(`${name}: ...right-clicked mid-show, it doesn't talk yet`, s.had && s.quiet);
    ok(`${name}: ...the show moves (the rig's transformation changing as it goes)`, s.had && s.moved >= 3, `${s.moved} looks seen`);
    ok(`${name}: ...and ends within 10 s - the rig whole, the show's props gone`, s.had && s.over && s.whole && s.cleared, `${(s.secs || 0).toFixed(1)} s, props seen ${s.props}`);
  };
  // (3.0a) THE GEM BRINGS IT TO LIFE: the doodle born by handing a follower something - right-clicking its click box holding it.
  // The stage by rcon: the host (and the Gem, if it's wanted) summoned as TestRat's own, sitting a few blocks off. With `gem`, first
  // without the Gem: the hint, the item kept. Then handed: the item gone, the encounter there with its show - quiet till it ends -
  // and right-clicked empty-handed: it comes along (its item, the line). Then the hosts are sent home (the follower cap is 3).
  // o: { host: 'p198', hostAb: 'mz', hostTag: 'bm.mzpet', gem: true, item: 'minecraft:ink_sac', bornRe, noGemRe, joined, itemId }
  const GEM = { pfx: 'p231', ab: 'cg', tag: 'bm.cgpet' };
  const summonAs = async (pfx, dx) => run(`${O}execute as TestRat at @s rotated 0 0 positioned ~${dx} ~ ~3 run function bm:${pfx}/summon_here`);
  const sendHome = async (pfx, tag, ab) => { await run(`tag @e[type=minecraft:wolf,tag=${tag}] add bm.${ab}sel2`); await run(`${O}execute as TestRat at @s run function bm:${pfx}/dismiss`);
    await run(`tag @e[type=minecraft:wolf,tag=bm.${ab}sel2] remove bm.${ab}sel2`); };
  // (a follower called without its item in your pockets is put away after 3 s (p73/fol): the hosts' own items go in TestRat's
  //  inventory for the meeting, and come out again after)
  const HOST_ITEM = { p227: 'kettle_plane', p198: 'capshun_pencil', p231: 'creativity_gem' };
  const born = async (o, hand = 8) => {
    const { A, at, entOf, sleep, has, ENC } = ctx; const r = {};
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    const pocket = [...new Set([o.host, ...(o.gem ? [GEM.pfx] : [])])].map(h => HOST_ITEM[h]).filter(Boolean);
    for (const [i, iid] of pocket.entries()) await run(`loot replace entity TestRat inventory.${20 + i} loot bm:items/${iid}`);
    await run(`kill @e[type=minecraft:wolf,tag=${o.hostTag}]`); await run(`kill @e[type=minecraft:wolf,tag=${GEM.tag}]`); await sleep(1500);
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await summonAs(o.host, 1.5); await sleep(1500);
    await run(`data modify entity @e[type=minecraft:wolf,tag=${o.hostTag},limit=1] Sitting set value 1b`);
    const HIT = `@e[type=minecraft:interaction,tag=bm.${o.hostAb}hit,limit=1]`;
    const give = async () => { await run(`item replace entity TestRat hotbar.${hand} with ${o.item}`); A.slot(hand); await sleep(500);
      const hb = await entOf(HIT); A.bars.length = 0; A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(900); return !!hb; };
    const held = async () => +(((await run(`clear TestRat ${o.item} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
    if (o.gem) {
      r.reached0 = await give();
      r.noGem = A.bars.some(b => o.noGemRe.test(b)) && (await held()) === 1 && (await cnt(ENC)) === 0;
      r.noGemBar = A.bars.slice(-1).join('');
      await summonAs(GEM.pfx, -1.5); await sleep(1500);
      await run(`data modify entity @e[type=minecraft:wolf,tag=${GEM.tag},limit=1] Sitting set value 1b`);
    }
    r.reached = await give();
    r.placed = await wait(3000, async () => (await cnt(ENC)) === 1, 100);
    const pre = await early(ctx);
    r.spent = (await held()) === 0;
    r.bornLine = A.chats.some(c => o.bornRe.test(c)); r.chat0 = A.chats.slice(-1).join('').slice(0, 200);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250);
    await run(`item replace entity TestRat hotbar.${hand} with minecraft:air`); A.slot(hand); await sleep(250);
    r.show = await entrance(ctx, eb, null, pre, async () => (await has(o.itemId)) === 1);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    r.got = (await has(o.itemId)) === 1 && A.chats.some(c => o.joined.test(c)); r.chat = A.chats.slice(-2).join(' | ').slice(0, 200);
    await sendHome(o.host, o.hostTag, o.hostAb); if (o.gem && o.host !== GEM.pfx) await sendHome(GEM.pfx, GEM.tag, GEM.ab); await sleep(800);
    for (const iid of pocket) await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}]`);
    return r;
  };
  // ...its checks, worded for the test's ok() list
  const bornOks = (ok, r, o) => {
    if (o.gem) ok(`${o.name}: handed to ${o.hostName} without the Gem out - only a hint ("if only..."), the item kept, nothing born`, r.noGem, r.noGemBar);
    ok(`${o.name}: handed to ${o.hostName}${o.gem ? ' with the Gem out' : ''} (a right-click holding it): the item spent, the Gem brings it to life (the encounter, its line)`,
       r.reached && r.placed && r.spent && r.bornLine, r.chat0);
    showOks(ok, r, `${o.name}'s entrance`, o.props);
    ok(`${o.name}: right-clicked once the show is over - it comes along (its item, its line)`, r.got, r.chat);
  };
  return { cd, calm, fxOf, hp, home, move, meet, early, entrance, showOks, born, bornOks, sendHome, summonAs, GEM };
};
