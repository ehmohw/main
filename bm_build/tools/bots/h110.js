// 2.69 test helpers: a heist of nothing but one kind of room, in one variant; rooms addressed by their number (bm.gvq)
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const fs = require('fs');
const OUT = BMB + 'out_p2/BlackMarket_DP/data/bm/function/';
const rel = (x, y, z) => `~${x - 12} ~${y - 4} ~${z - 12}`;
const relf = (x, y, z) => `~${+(x - 12.5).toFixed(3)} ~${+(y - 4).toFixed(3)} ~${+(z - 12.5).toFixed(3)}`;
function mk(run) {
  const num = async c => +(((await run(c)).match(/(?:Count: |has |data: |Found )(-?\d+)/) || [0, -1])[1]);
  const cnt = async (sel) => +(((await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/) || [0, 0])[1]);
  let GI = 1;
  const room = (k, q) => `@e[type=minecraft:marker,tag=bm.gvr_${k},scores={bm.gvq=${q},bm.gvi=${GI}},limit=1]`;
  const at = (k, q, cmd) => run(`execute in bm:gutter as ${room(k, q)} at @s run ${cmd}`);
  const sc = (k, q, o) => num(`execute in bm:gutter run scoreboard players get ${room(k, q)} ${o}`);
  const alarm = () => num('execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,limit=1] bm.gva');
  const solved = async (k, q) => (await sc(k, q, 'bm.gvs')) === 3 && /passed/.test(await at(k, q, `execute if block ${rel(24, 5, 12)} minecraft:air`));
  const go = async (k, q, x = 3, z = 12) => { await at(k, q, `tp TestRat ${rel(x, 4, z)} -90 0`); await new Promise(r => setTimeout(r, 400)); };
  const qs = async (k) => { const out = []; for (let q = 1; q <= 12; q++) if ((await cnt(room(k, q))) === 1) out.push(q); return out; };
  async function heist(kind, v, tier = 1, toks = 8) {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never');
    await run(`function bm:admin/rooms_only_${kind}`); await run(`function bm:admin/variant_${v}`);
    await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
    await run('tag TestRat remove bm.gvzap'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone');
    await new Promise(r => setTimeout(r, 2500));
    for (let i = 0; i < toks; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
    await new Promise(r => setTimeout(r, 7000));
    GI = await num('scoreboard players get TestRat bm.gvi');
  }
  async function begin() {
    await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ~ ~ ~');
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s run setblock ${rel(23, 5, 15)} minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
    await new Promise(r => setTimeout(r, 600));
  }
  const pos = async (who = 'TestRat') => { const m = (await run(`data get entity ${who} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? [+m[1], +m[2], +m[3]] : null; };
  const mpos = async (k, q) => { const m = (await run(`execute in bm:gutter run data get entity ${room(k, q)} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? [+m[1], +m[2], +m[3]] : null; };
  const local = async (k, q) => { const p = await pos(); const m = await mpos(k, q); return p && m ? [p[0] - m[0] + 12.5, p[1] - m[1] + 4, p[2] - m[2] + 12.5] : null; };
  async function mouse(B) {   // TestMouse joins TestRat's heist (as crew)
    await run('scoreboard players operation TestMouse bm.gvi = TestRat bm.gvi'); await run('scoreboard players operation TestMouse bm.gvrun = TestRat bm.gvrun');
    await run('tag TestMouse add bm.gvp'); await run('gamemode adventure TestMouse'); await run('effect give TestMouse resistance 900 4 true');
  }
  return { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, rel, relf, pos, mpos, local, mouse };
}
function fnText(path) { return fs.readFileSync(OUT + path + '.mcfunction', 'utf8'); }
module.exports = { mk, rel, relf, fnText };
