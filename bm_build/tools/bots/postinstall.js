// After `npm install`: teach minecraft-protocol 1.68.0 / minecraft-data 3.117.0 to speak 26.3, the way the bots need it.
//  - minecraft-data's 26.1 protocol table is replaced by the 26.3 one (patches/; the 26.1 original is kept as .orig)
//  - setProtocol.js: the handshake announces process.env.PV when set (lib.js / lib_resp.js set PV=777, 26.3's number)
//  - client.js: bundle delimiters are passed through as packets instead of holding everything back
// Safe to run again; stops loudly if the packages ever change under it (the versions are pinned in package.json).
const fs = require('fs');
const path = require('path');
const nm = path.join(__dirname, 'node_modules');
const proto = path.join(nm, 'minecraft-data/minecraft-data/data/pc/26.1/protocol.json');
const ours = path.join(__dirname, 'patches/minecraft-data-26.1-protocol-as-26.3.json');
if (!fs.existsSync(proto + '.orig')) fs.copyFileSync(proto, proto + '.orig');
fs.copyFileSync(ours, proto);
function edit(rel, from, to) {
  const f = path.join(nm, rel); const s = fs.readFileSync(f, 'utf8');
  if (s.includes(to)) return;
  if (!s.includes(from)) throw new Error(`postinstall: ${rel} has changed - can't patch it (expected: ${from})`);
  fs.writeFileSync(f, s.replace(from, to));
}
edit('minecraft-protocol/src/client/setProtocol.js', 'protocolVersion: options.protocolVersion,',
     'protocolVersion: process.env.PV ? parseInt(process.env.PV) : options.protocolVersion,');
edit('minecraft-protocol/src/client.js', "if (this._hasBundlePacket && parsed.metadata.name === 'bundle_delimiter') {",
     "if (false && this._hasBundlePacket && parsed.metadata.name === 'bundle_delimiter') {");
console.log('bm-bots: minecraft-protocol patched for 26.3');
