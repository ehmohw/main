"""Package dist/ zips deterministically (fixed timestamps), so an unchanged resource pack keeps the same SHA1."""
import os, zipfile, hashlib, shutil
root = '/home/claude/bm_build'; dist = root + '/dist'


def add(z, path, arc):
    zi = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    z.writestr(zi, open(path, 'rb').read())


def zipdir(src, dst, extra=()):
    with zipfile.ZipFile(dst, 'w') as z:
        for base, dirs, files in sorted(os.walk(src)):
            dirs.sort()
            for f in sorted(files):
                p = os.path.join(base, f); add(z, p, os.path.relpath(p, src))
        for p, arc in extra: add(z, p, arc)


sha = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()
# 2.94b: only a finished build is packaged - each generator stamps its pack with the file count once it is whole
for _pk in ('BlackMarket_DP', 'BlackMarket_RP'):
    _st = f'{root}/out_p2/{_pk}.done'
    _n = sum(len(fs) for _b, _d, fs in os.walk(f'{root}/out_p2/{_pk}'))
    assert os.path.exists(_st), f'{_pk}: no finished build (a generator is running, or failed) - rebuild before packaging'
    assert int(open(_st).read()) == _n, f'{_pk}: {_n} files, but the build finished with {open(_st).read()} - rebuild'
# 2.21: one pack - the full build (dungeons included) is the release
for f in os.listdir(dist): os.remove(os.path.join(dist, f))
zipdir(root + '/out_p2/BlackMarket_DP', dist + '/BlackMarket_DP.zip', [(root + '/README.md', 'README.md'), (root + '/README_PHASE2.md', 'README_DUNGEONS.md')])
zipdir(root + '/out_p2/BlackMarket_RP', dist + '/BlackMarket_RP.zip')
with zipfile.ZipFile(dist + '/BlackMarket_source.zip', 'w') as z:
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in ('out', 'out_p2', 'dist', '__pycache__'))
        for f in sorted(files):
            p = os.path.join(base, f); add(z, p, 'bm_build/' + os.path.relpath(p, root))
open(dist + '/SHA1.txt', 'w').write(f"BlackMarket_RP.zip  {sha(dist + '/BlackMarket_RP.zip')}\n")
for f in ('README.md', 'README_PHASE2.md'): shutil.copy(f'{root}/{f}', f'{dist}/{f}')
for _pk in ('BlackMarket_DP', 'BlackMarket_RP'):               # (and the zips hold every file of it)
    _n = sum(len(fs) for _b, _d, fs in os.walk(f'{root}/out_p2/{_pk}'))
    _z = len([i for i in zipfile.ZipFile(f'{dist}/{_pk}.zip').infolist() if not i.filename.startswith('README')])
    assert _z == _n, f'{_pk}.zip holds {_z} files, the build {_n}'
print(open(dist + '/SHA1.txt').read())
