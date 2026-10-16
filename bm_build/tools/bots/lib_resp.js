// Minimal 26.3 test bot (26.1.2 protocol data patched to 26.3's packet table) + RCON.
process.env.PV = '777';
const mc = require('minecraft-protocol');
const net = require('net');
const chunks = require('./chunks');

function text(nbt) {   // flatten an anonymous-NBT text component to a plain string
  const walk = (n) => {
    if (n == null) return '';
    if (typeof n !== 'object') return String(n);
    if (n.type && 'value' in n) return walk(n.value);
    if (Array.isArray(n)) return n.map(walk).join('');
    let s = '';
    if (n.text) s += walk(n.text);
    if (n['']) s += walk(n['']);
    if (n.translate) s += '[' + walk(n.translate) + ']';
    if (n.score) s += '#';
    if (n.extra) s += walk(n.extra);
    return s;
  };
  return walk(nbt);
}

// typed NBT (as the protocol library hands it over) -> plain values
function plain(n) {
  if (n == null || typeof n !== 'object') return n;
  if (Array.isArray(n)) return n.map(plain);
  if ('type' in n && 'value' in n && Object.keys(n).length <= 2) {
    if (n.type === 'compound') { const o = {}; for (const k in n.value) o[k] = plain(n.value[k]); return o; }
    if (n.type === 'list') return (n.value && n.value.value ? n.value.value : []).map(v => plain(n.value.type === 'compound' ? { type: 'compound', value: v } : { type: n.value.type, value: v }));
    return plain(n.value);
  }
  const o = {}; for (const k in n) o[k] = plain(n[k]); return o;
}
function flat(t) {       // a text component -> its words
  if (t == null) return ''; if (typeof t !== 'object') return String(t); if (Array.isArray(t)) return t.map(flat).join('');
  return (t.text != null ? String(t.text) : '') + (t[''] != null ? flat(t['']) : '') + (t.translate ? '[' + t.translate + ']' : '') + (t.extra ? flat(t.extra) : '');
}
function buttonsOf(d) {  // every button a dialog shows: its label and the command it runs
  const out = [];
  const walk = (x) => { if (!x || typeof x !== 'object') return; if (Array.isArray(x)) return x.forEach(walk);
    if (x.label != null && x.action && typeof x.action === 'object') out.push({ label: flat(x.label).trim(), command: x.action.command || '', type: x.action.type || '' });
    for (const k in x) if (k !== 'label') walk(x[k]); };
  walk(d); return out;
}
function bot(name) {
  return new Promise((res, rej) => {
    const c = mc.createClient({ host: '127.0.0.1', port: 25565, username: name, version: '26.1.2', auth: 'offline', hideErrors: true });
    c.seq = 1; c.bars = []; c.chats = []; c.ents = {}; c.pos = null; c.windows = [];
    c.on('error', () => {});
    // sounds heard (name + channel: 0 master, 1 music, 2 record, ...) and sounds stopped, as the client got them (2.80)
    c.sounds = []; c.stops = [];
    c.on('sound_effect', (p) => { try { const b = Buffer.from(p.data && p.data.data ? p.data.data : p.data); let i = 0;
      const vi = () => { let v = 0, sh = 0, x; do { x = b[i++]; v |= (x & 0x7f) << sh; sh += 7; } while (x & 0x80); return v; };
      const id = vi(); let name = '#' + (id - 1);
      if (id === 0) { const n = vi(); name = b.slice(i, i + n).toString('utf8'); i += n; if (b[i++]) i += 4; }
      c.sounds.push({ name, cat: vi(), t: Date.now() }); } catch (e) {} });
    c.on('stop_sound', (p) => c.stops.push(Object.assign({ t: Date.now() }, p)));
    c.on('position', (p) => { c.write('teleport_confirm', { teleportId: p.teleportId, x: p.x, y: p.y, z: p.z, yaw: p.yaw, pitch: p.pitch }); c.pos = p; });
    c.on('action_bar', (p) => c.bars.push(text(p.text)));
    c.titles = [];          // (titles and subtitles, as shown)
    c.on('set_title_text', (p) => c.titles.push(text(p.text)));
    c.on('set_title_subtitle', (p) => c.titles.push(text(p.text)));
    c.on('system_chat', (p) => (p.isActionBar ? c.bars : c.chats).push(text(p.content)));
    c.on('spawn_entity', (p) => { c.ents[p.entityId] = p; });
    c.on('entity_destroy', (p) => { for (const id of p.entityIds) delete c.ents[id]; });
    c.on('open_window', (p) => c.windows.push(p));
    c.dialogs = [];
    c.dialogN = [];
    c.on('show_dialog', (p) => { try { c.dialogs.push(JSON.stringify(p.dialog)); c.dialogN.push(plain(p.dialog)); } catch (e) { c.dialogs.push(String(p.dialog)); } });   // (what's on screen: every button's text and command)
    c.on('clear_dialog', () => { c.dialogClosed = (c.dialogClosed || 0) + 1; });
    c.on('chunk_batch_finished', () => { try { c.write('chunk_batch_received', { chunksPerTick: 25 }); } catch (e) {} });   // (or the server stops sending chunks - and their entities)
    c.on('update_health', (p) => { c.health = p.health; if (p.health <= 0) setTimeout(() => { try { c.write('client_command', { actionId: 0 }); } catch (e) {} }, 300); });
    c.on('respawn', () => { setTimeout(() => { try { c.write('player_loaded', {}); } catch (e) {} }, 300); });   // (a real client reports it's loaded after each respawn / dimension change)
    c.on('login', (p) => {
      c.eid = p.entityId;
      setTimeout(() => { try { c.write('player_loaded', {}); c.write('client_command', { actionId: 0 }); } catch (e) {} res(c); }, 1500);
    });
    c.on('kick_disconnect', (p) => console.log('KICKED', name, JSON.stringify(p).slice(0, 300)));
    setTimeout(() => rej(new Error('login timeout')), 20000);
    c.slot = (i) => c.write('held_item_slot', { slotId: i });
    c.use = (hand = 'main_hand') => c.write('use_item', { hand, sequence: c.seq++, rotation: { x: c.pos ? c.pos.yaw : 0, y: c.pos ? c.pos.pitch : 0 } });
    c.release = () => c.write('block_dig', { status: 6, location: { x: 0, y: 0, z: 0 }, face: 0, sequence: c.seq++ });
    // (26.3's player actions: 1 is CHANGE_DESTROY_DIRECTION, so 6 is RELEASE_USE_ITEM and 7 is SWAP_ITEM_WITH_OFFHAND - the F key)
    c.swap = () => c.write('block_dig', { status: 7, location: { x: 0, y: 0, z: 0 }, face: 0, sequence: c.seq++ });
    c.drop = (stack = false) => c.write('block_dig', { status: stack ? 4 : 5, location: { x: 0, y: 0, z: 0 }, face: 0, sequence: c.seq++ });   // Q (ctrl+Q: the stack)
    // (mining: 26.3's actions are 0 START_DESTROY, 1 CHANGE_DESTROY_DIRECTION, 2 ABORT_DESTROY, 3 STOP_DESTROY - "2" gives up the block)
    c.mine = async (x, y, z, ms = 200, face = 1) => { c.write('block_dig', { status: 0, location: { x, y, z }, face, sequence: c.seq++ }); await new Promise(r => setTimeout(r, ms));
      c.write('block_dig', { status: 3, location: { x, y, z }, face, sequence: c.seq++ }); };
    c.input = (flags) => c.write('player_input', { inputs: flags });
    c.interact = (eid, sneaking = false) => c.write('use_entity', { target: eid, hand: 'main_hand', location: { x: 0, y: 0.5, z: 0 }, sneaking });
    c.attack = (eid) => c.write('attack', { entityId: eid });
    c.useOn = (x, y, z, face = 1) => c.write('block_place', { hand: 'main_hand', location: { x, y, z }, direction: face, cursorX: 0.5, cursorY: 0.5, cursorZ: 0.5,
                                                            insideBlock: false, worldBorderHit: false, sequence: c.seq++ });
    c.close = (id) => c.write('close_window', { windowId: id });
    c.cmd = (s) => c.write('chat_command', { command: s });
    // (a real client tells the server where it stands every tick or so - on the ground, still - and walks in small steps)
    // (one move per client tick, each tick closed with tick_end - the server kicks a client that moves twice in one tick)
    c.ground = (on = true) => { if (!c.pos) return; c.write('position', { x: c.pos.x, y: c.pos.y, z: c.pos.z, flags: { onGround: on, hasHorizontalCollision: false } }); c.write('tick_end', {}); };
    c.stand = () => { if (c._st) return; c._st = setInterval(() => { try { c.ground(true); } catch (e) {} }, 50); };
    c.unstand = () => { clearInterval(c._st); c._st = null; };
    // (riding: a real client sends where it looks and what it presses, every tick - never a position)
    c.ride = (yaw = 0, pitch = 0, inputs = {}) => { c.unstand(); c._yaw = yaw; c._pitch = pitch; c._in = inputs;
      if (!c._lk) c._lk = setInterval(() => { try { c.write('look', { yaw: c._yaw, pitch: c._pitch, flags: { onGround: false, hasHorizontalCollision: false } });
        c.write('player_input', { inputs: c._in || {} }); c.write('tick_end', {}); } catch (e) {} }, 50); };
    c.unride = () => { clearInterval(c._lk); c._lk = null; };
    c.walkTo = async (x, z, step = 0.2) => {      // (straight there over the ground at a walk; the server checks every move)
      c.unstand(); const tp0 = c.pos.teleportId;
      for (let k = 0; k < 400; k++) {
        if (c.pos.teleportId !== tp0) break;          // (the server moved us - a door, a portal: stop walking)
        const dx = x - c.pos.x, dz = z - c.pos.z, d = Math.hypot(dx, dz); if (d < 0.05) break;
        const t = Math.min(step, d); c.pos.x += dx / d * t; c.pos.z += dz / d * t; c.ground(true); await new Promise(r => setTimeout(r, 50));
      }
      c.stand();
    };
    // (what's on screen: each button's words and the command it runs)
    c.buttons = () => { const d = c.dialogN[c.dialogN.length - 1]; return d ? buttonsOf(d) : []; };
    c.click = (re) => {       // press the on-screen button whose words match - by sending exactly the command it carries
      const b = c.buttons().find(b => re.test(b.label)); if (!b || !b.command) return null;
      c.cmd(b.command.replace(/^\//, '')); return b;
    };
    c.press = async (re, ms = 2000) => {      // ...and wait for whatever screen comes next (null if no such button)
      const n0 = c.dialogN.length; const b = c.click(re); if (!b) return null;
      const t0 = Date.now(); while (Date.now() - t0 < ms && c.dialogN.length === n0) await new Promise(r => setTimeout(r, 50));
      b.next = c.dialogN.length > n0; return b;
    };
    c.useWait = async (ms = 1500) => {        // right-click the held item, let go - and wait for a screen
      const n0 = c.dialogN.length; c.use(); await new Promise(r => setTimeout(r, 350)); c.release();
      const t0 = Date.now(); while (Date.now() - t0 < ms && c.dialogN.length === n0) await new Promise(r => setTimeout(r, 50));
      return c.dialogN.length > n0;
    };
  });
}

// ---- RCON
function rcon() {
  return new Promise((res) => {
    const s = net.connect(25575, '127.0.0.1'); let id = 1; const wait = {}; let buf = Buffer.alloc(0);
    const send = (type, body) => new Promise((r) => {
      const i = id++; const b = Buffer.from(body, 'utf8'); const p = Buffer.alloc(14 + b.length);
      p.writeInt32LE(10 + b.length, 0); p.writeInt32LE(i, 4); p.writeInt32LE(type, 8); b.copy(p, 12); p.writeInt16LE(0, 12 + b.length);
      // (a reply that never comes would hang the whole test: after 15 s, give up on it - and say which command it was)
      const t = setTimeout(() => { if (wait[i]) { delete wait[i]; console.log('RCON TIMEOUT: ' + body.slice(0, 160)); r(''); } }, 15000);
      wait[i] = (v) => { clearTimeout(t); r(v); }; s.write(p);
    });
    s.on('data', (d) => {
      buf = Buffer.concat([buf, d]);
      while (buf.length >= 4) {
        const len = buf.readInt32LE(0); if (buf.length < len + 4) break;
        const i = buf.readInt32LE(4); const body = buf.slice(12, 4 + len - 2).toString('utf8'); buf = buf.slice(4 + len);
        if (wait[i]) { wait[i](body); delete wait[i]; }
      }
    });
    // (one request at a time: the server reads one request per read - a second one sent along with it is lost, and the
    //  connection with it)
    let chain = Promise.resolve();
    const run = (c) => { const p = chain.then(() => chunks.wrap(c, (cc) => send(2, cc))); chain = p.catch(() => {}); return p; };
    s.on('connect', async () => { await send(3, 'bmtest'); res({ run, end: () => s.end() }); });
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
module.exports = { bot, rcon, sleep, text, plain, flat, buttonsOf };
