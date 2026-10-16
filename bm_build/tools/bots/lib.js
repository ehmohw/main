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

function bot(name) {
  return new Promise((res, rej) => {
    const c = mc.createClient({ host: '127.0.0.1', port: 25565, username: name, version: '26.1.2', auth: 'offline', hideErrors: true });
    c.seq = 1; c.bars = []; c.chats = []; c.ents = {}; c.pos = null; c.windows = [];
    c.on('error', () => {});
    c.on('position', (p) => { c.write('teleport_confirm', { teleportId: p.teleportId, x: p.x, y: p.y, z: p.z, yaw: p.yaw, pitch: p.pitch }); c.pos = p; });
    c.on('action_bar', (p) => c.bars.push(text(p.text)));
    c.on('system_chat', (p) => (p.isActionBar ? c.bars : c.chats).push(text(p.content)));
    c.on('spawn_entity', (p) => { c.ents[p.entityId] = p; });
    c.on('entity_destroy', (p) => { for (const id of p.entityIds) delete c.ents[id]; });
    c.on('open_window', (p) => c.windows.push(p));
    c.on('chunk_batch_finished', () => { try { c.write('chunk_batch_received', { chunksPerTick: 20 }); } catch (e) {} });   // (else the server stops sending chunks after a long teleport)
    c.on('update_health', (p) => { c.health = p.health; if (p.health <= 0) setTimeout(() => { try { c.write('client_command', { actionId: 0 }); } catch (e) {} }, 300); });
    if (process.env.BOT_RESPAWN) c.on('respawn', () => { setTimeout(() => { try { c.write('player_loaded', {}); } catch (e) {} }, 300); });   // (cross-dimension tests: report loaded after each respawn)
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
    c.input = (flags) => c.write('player_input', { inputs: flags });
    c.interact = (eid, sneaking = false) => c.write('use_entity', { target: eid, hand: 'main_hand', location: { x: 0, y: 0.5, z: 0 }, sneaking });
    c.attack = (eid) => c.write('attack', { entityId: eid });
    c.useOn = (x, y, z, face = 1) => c.write('block_place', { hand: 'main_hand', location: { x, y, z }, direction: face, cursorX: 0.5, cursorY: 0.5, cursorZ: 0.5,
                                                            insideBlock: false, worldBorderHit: false, sequence: c.seq++ });
    c.close = (id) => c.write('close_window', { windowId: id });
    c.cmd = (s) => c.write('chat_command', { command: s });
  });
}

// ---- RCON
function rcon() {
  return new Promise((res) => {
    const s = net.connect(25575, '127.0.0.1'); let id = 1; const wait = {}; let buf = Buffer.alloc(0);
    const send = (type, body) => new Promise((r) => {
      const i = id++; const b = Buffer.from(body, 'utf8'); const p = Buffer.alloc(14 + b.length);
      p.writeInt32LE(10 + b.length, 0); p.writeInt32LE(i, 4); p.writeInt32LE(type, 8); b.copy(p, 12); p.writeInt16LE(0, 12 + b.length);
      wait[i] = r; s.write(p);
    });
    s.on('data', (d) => {
      buf = Buffer.concat([buf, d]);
      while (buf.length >= 4) {
        const len = buf.readInt32LE(0); if (buf.length < len + 4) break;
        const i = buf.readInt32LE(4); const body = buf.slice(12, 4 + len - 2).toString('utf8'); buf = buf.slice(4 + len);
        if (wait[i]) { wait[i](body); delete wait[i]; }
      }
    });
    s.on('connect', async () => { await send(3, 'bmtest'); res({ run: (c) => chunks.wrap(c, (cc) => send(2, cc)), end: () => s.end() }); });
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
module.exports = { bot, rcon, sleep, text };
