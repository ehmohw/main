// 3.0e: the Vorn Armada's placement, read from p2/armadacfg.py (ORIGIN, SIZE, OLD_SITES, CATCH_LOW) - so the tests follow it
// wherever it's moved (3.0-3.0d: 2560 24 -3328; 3.0e: high in the End's sky).
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', '..', 'p2', 'armadacfg.py'), 'utf8');
const tup = (re) => { const m = src.match(re); if (!m) throw new Error('armadacfg: ' + re); return m[1].split(',').map(s => +s.trim()); };
const AO = tup(/^ORIGIN = \(([^)]*)\)/m), AS = tup(/^SIZE = \(([^)]*)\)/m);
const OLD = {}; for (const m of src.matchAll(/'(s\d+)': \(([-\d, ]+)\)/g)) OLD[m[1]] = m[2].split(',').map(s => +s.trim());
const CATCH_LOW = +(src.match(/^CATCH_LOW = (\d+)/m) || [0, NaN])[1];
module.exports = { AO, AS, OLD, CATCH_LOW, W: (x, y, z) => [AO[0] + x, AO[1] + y, AO[2] + z] };
