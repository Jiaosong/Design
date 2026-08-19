from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
chunks=root/'source-chunks'
out=root/'reassembled'
out.mkdir(exist_ok=True)
expected={'index.html':'9dcc6fc4d0faf163c60f146dcd26486aa925bf45','app.css':'4171b3dfd9cd21a13c87f97551221e50315c5f55','app.js':'9a80016e2c07608c1e28403ea474ca7290142941'}
for target,prefix in [('index.html','index.part'),('app.css','app.css.part'),('app.js','app.js.part')]:
    data=b''.join(p.read_bytes() for p in sorted(chunks.glob(prefix+'*')))
    (out/target).write_bytes(data)
    got=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    if got!=expected[target]: raise SystemExit(f'{target}: {got} != {expected[target]}')
    print(target,got,'EXACT')
