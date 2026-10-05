"""Minimal RCON client for driving a local test server.

usage: python3 tools/rcon.py "cmd1" "cmd2" ...      (prints each reply)
       echo cmds | python3 tools/rcon.py -           (one command per line)
env: RCON_PORT (25575), RCON_PASS (bmtest)
"""
import os, socket, struct, sys


class Rcon:
    def __init__(self, host='127.0.0.1', port=None, pw=None):
        self.s = socket.create_connection((host, int(port or os.environ.get('RCON_PORT', 25575))), timeout=30)
        self.i = 0
        self._send(3, pw or os.environ.get('RCON_PASS', 'bmtest'))
        if self._recv()[0] == -1: raise SystemExit('rcon auth failed')

    def _send(self, kind, body):
        self.i += 1
        b = body.encode('utf-8')
        self.s.sendall(struct.pack('<iii', len(b) + 10, self.i, kind) + b + b'\0\0')

    def _recv(self):
        def n(k):
            d = b''
            while len(d) < k:
                c = self.s.recv(k - len(d))
                if not c: raise ConnectionError('closed')
                d += c
            return d
        ln = struct.unpack('<i', n(4))[0]
        d = n(ln)
        rid, kind = struct.unpack('<ii', d[:8])
        return rid, d[8:-2].decode('utf-8', 'replace')

    def cmd(self, c):
        self._send(2, c)
        return self._recv()[1]


if __name__ == '__main__':
    r = Rcon()
    cmds = [l.strip() for l in sys.stdin if l.strip()] if sys.argv[1:] == ['-'] else sys.argv[1:]
    for c in cmds:
        out = r.cmd(c)
        print(f'> {c}\n{out}' if len(cmds) > 1 else out)
