"""PixelLab (api.pixellab.ai/v2) - the little client the 2.94 sprites were made with. The key: $PIXELLAB_KEY, or none at all
where a proxy adds it. Every job is logged (prompt, seed, result) to tools/pixellab/log.jsonl, so a sprite can be traced back.
   python3 pl.py balance"""
import base64, io, json, os, sys, time, urllib.request
from PIL import Image

API = 'https://api.pixellab.ai/v2'
HERE = os.path.dirname(os.path.abspath(__file__))


def _req(method, path, body=None):
    h = {'Content-Type': 'application/json'}
    if os.environ.get('PIXELLAB_KEY'):
        h['Authorization'] = 'Bearer ' + os.environ['PIXELLAB_KEY']
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=300) as f:
            return json.loads(f.read() or b'{}')
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} {path}: {e.code} {e.read()[:600]}')


def b64(im):
    if isinstance(im, str):
        im = Image.open(im)
    buf = io.BytesIO(); im.save(buf, 'PNG')
    return {'type': 'base64', 'base64': base64.b64encode(buf.getvalue()).decode(), 'format': 'png'}


def img(o):
    """an image from a response (base64 or url)"""
    if isinstance(o, dict) and o.get('base64'):
        return Image.open(io.BytesIO(base64.b64decode(o['base64']))).convert('RGBA')
    url = o.get('url') if isinstance(o, dict) else o
    with urllib.request.urlopen(url, timeout=120) as f:
        return Image.open(io.BytesIO(f.read())).convert('RGBA')


def log(kind, body, res):
    keep = {k: v for k, v in body.items() if not (isinstance(v, dict) and 'base64' in v)}
    with open(os.path.join(HERE, 'log.jsonl'), 'a') as f:
        f.write(json.dumps({'t': time.strftime('%Y-%m-%d %H:%M'), 'kind': kind, 'body': keep,
                            'result': {k: v for k, v in res.items() if k in ('background_job_id', 'character_id', 'object_id', 'animation_group_id', 'effect_id', 'status')}}) + '\n')


def post(path, body):
    res = _req('POST', path, body); log(path, body, res)
    return res


def get(path):
    return _req('GET', path)


def wait(job, every=5, limit=900):
    t0 = time.time()
    while time.time() - t0 < limit:
        r = get(f'/background-jobs/{job}')
        if r.get('status') in ('completed', 'failed', 'cancelled'):
            return r
        time.sleep(every)
    raise TimeoutError(job)


if __name__ == '__main__':
    if sys.argv[1] == 'balance':
        print(get('/balance'))
    elif sys.argv[1] == 'get':
        print(json.dumps(get(sys.argv[2]), indent=1)[:4000])
