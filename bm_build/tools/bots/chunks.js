// The standard every test keeps: chunks it force-loads are unloaded when it ends. The rcon helpers in lib.js and
// lib_resp.js send every command through wrap(). Before a "forceload add" goes out, the dimension's force-loaded chunks
// are asked for ("forceload query"); after it, only the chunks the test itself newly added are remembered. When the
// process exits - a clean end, a crash, a failed assertion, Ctrl+C or a sweep's timeout (SIGTERM) - exactly those are
// unloaded again, through rc.js. A chunk the pack already held stays held: the gutter's den, Lounge and Locker Hall
// chunks (force-loaded for good by bm:load), a raid instance's claimed slot, the Hollow while it's built. (t101 loads the
// den's own chunk, -256 -256: a blanket remove of what it asked for would leave the den unloaded until the next
// /reload.) A test that removes its own chunks is fine - removing them again is harmless. Only SIGKILL skips this.
// (3.1s) And a server that is down when the test ends (it was stopped mid-test): the removes that could not be sent are
// kept in .chunks_pending.json, and the next test sends them before its first command.
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const PENDING = path.join(__dirname, '.chunks_pending.json');
const readPending = () => { try { return JSON.parse(fs.readFileSync(PENDING, 'utf8')); } catch (e) { return []; } };
let flushed = false;
const held = new Map();             // "dim|cx|cz" -> [dim, cx, cz]
// (3.2a) The same for game rules: the first time a test sets one, its value as found is remembered and put back at exit (t100 and
// six more turned spawn_mobs off and never on - harmless while their old camelCase names failed, not once they were fixed).
const rules = new Map();            // name -> value as found
let hooked = false;

const dimOf = (cmd) => (cmd.match(/(?:^|\s)in\s+([a-z0-9_.-]+:[a-z0-9_/.-]+)/) || [0, 'minecraft:overworld'])[1];
const parseHeld = (out) => new Set((out.match(/\[-?\d+, -?\d+\]/g) || []).map(s => s.slice(1, -1).replace(', ', '|')));
function area(cmd) {
  const m = cmd.match(/forceload add (-?\d+) (-?\d+)(?: (-?\d+) (-?\d+))?\s*$/); if (!m) return null;
  const [x1, z1, x2, z2] = [+m[1], +m[2], m[3] !== undefined ? +m[3] : +m[1], m[4] !== undefined ? +m[4] : +m[2]];
  const cs = []; for (let cx = Math.floor(Math.min(x1, x2) / 16); cx <= Math.floor(Math.max(x1, x2) / 16); cx++)
    for (let cz = Math.floor(Math.min(z1, z2) / 16); cz <= Math.floor(Math.max(z1, z2) / 16); cz++) cs.push([cx, cz]);
  return cs;
}
function release() {
  const ruleCmds = [...rules.entries()].map(([n, v]) => `gamerule ${n} ${v}`); rules.clear();
  if (!held.size && !ruleCmds.length) return;
  // one command per run of chunks along x (same dimension, same z)
  const rows = {}; for (const [d, cx, cz] of held.values()) (rows[`${d}|${cz}`] = rows[`${d}|${cz}`] || []).push(cx);
  const cmds = [];
  for (const [k, xs] of Object.entries(rows)) {
    const [d, cz] = [k.slice(0, k.lastIndexOf('|')), +k.slice(k.lastIndexOf('|') + 1)]; xs.sort((a, b) => a - b);
    for (let i = 0; i < xs.length;) { let j = i; while (j + 1 < xs.length && xs[j + 1] === xs[j] + 1) j++;
      cmds.push(`execute in ${d} run forceload remove ${xs[i] * 16} ${cz * 16} ${xs[j] * 16} ${cz * 16}`); i = j + 1; }
  }
  held.clear(); cmds.push(...ruleCmds);
  const r = spawnSync(process.execPath, [path.join(__dirname, 'rc.js'), ...cmds], { timeout: 30000, stdio: 'ignore' });
  if (r.status !== 0) {             // (the server didn't answer: kept for the next test)
    try { fs.writeFileSync(PENDING, JSON.stringify([...new Set([...readPending(), ...cmds])])); } catch (e) {}
    console.log(`chunks.js: the server didn't answer - ${cmds.length} forceload removes kept for the next test`);
  }
}
// what an earlier test couldn't release, sent before this one's first command
async function flush(send) {
  flushed = true;
  const cmds = readPending(); if (!cmds.length) return;
  for (const c of cmds) await send(c);
  try { fs.unlinkSync(PENDING); } catch (e) {}
  console.log(`chunks.js: released ${cmds.length} forceload areas an earlier test left behind`);
}
function hook() {
  if (hooked) return; hooked = true;
  process.on('exit', release);
  for (const sig of ['SIGINT', 'SIGTERM', 'SIGHUP']) process.on(sig, () => process.exit(130));
}
// send: (command) => Promise<reply>. Returns the reply to cmd itself.
// (3.2a) rc.js is how these are put back: it only passes its commands on. Remembering them there made a chain - a game rule it put
// back was remembered and put back again at its own exit, through another rc.js, without end (hundreds of them; the server OOM-killed).
const PLAIN = path.basename((require.main && require.main.filename) || '') === 'rc.js';
async function wrap(cmd, send) {
  if (PLAIN) return send(cmd);
  if (!flushed) await flush(send);
  const g = typeof cmd === 'string' && cmd.trim().match(/^gamerule ([a-z0-9_:]+) (\S+)$/);
  if (g && !rules.has(g[1])) {
    const was = ((await send(`gamerule ${g[1]}`)).match(/currently set to:? ?(\S+)/) || [])[1];
    if (was !== undefined) { rules.set(g[1], was); hook(); }
  }
  if (typeof cmd !== 'string' || !/(^|\s)forceload add\s/.test(cmd)) return send(cmd);
  const d = dimOf(cmd), cs = area(cmd.trim());
  if (!cs) { console.log('chunks.js: a forceload add it cannot read - not released at exit: ' + cmd); return send(cmd); }
  const before = parseHeld(await send(`execute in ${d} run forceload query`));
  const r = await send(cmd);
  for (const [cx, cz] of cs) if (!before.has(`${cx}|${cz}`)) held.set(`${d}|${cx}|${cz}`, [d, cx, cz]);
  hook();
  return r;
}
module.exports = { wrap, release };
