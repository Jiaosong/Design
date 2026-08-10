#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_member(name: str) -> bool:
    p = PurePosixPath(name)
    return not p.is_absolute() and '..' not in p.parts


def fail(result, message, code=2):
    result['status'] = 'FAIL'
    result.setdefault('errors', []).append(message)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip', required=True, dest='zip_path')
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--dest', required=True)
    parser.add_argument('--result', required=True)
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    manifest_path = Path(args.manifest)
    dest = Path(args.dest)
    result_path = Path(args.result)
    result_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    result = {
        'gate': 'Timer Light Basin v3.3 staged deployment package',
        'schema': manifest.get('schema'),
        'package': zip_path.name,
        'status': 'RUNNING',
        'checks': {},
        'errors': [],
        'boundary': manifest.get('boundary', {})
    }

    if not zip_path.is_file():
        code = fail(result, f'missing package: {zip_path}')
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return code

    outer_sha = sha256_file(zip_path)
    result['checks']['package_sha256'] = {
        'status': 'PASS' if outer_sha == manifest['package_sha256'] else 'FAIL',
        'actual': outer_sha,
        'expected': manifest['package_sha256']
    }
    if outer_sha != manifest['package_sha256']:
        result['status'] = 'FAIL'
        result['errors'].append('outer package SHA-256 mismatch')
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 3

    root = manifest['package_root'].rstrip('/') + '/'
    required = manifest['required_files']

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        unsafe = [name for name in names if not safe_member(name)]
        if unsafe:
            result['status'] = 'FAIL'
            result['errors'].append(f'unsafe archive path(s): {unsafe[:5]}')
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 4

        missing = []
        mismatched = []
        for rel, expected in required.items():
            name = root + rel
            try:
                data = zf.read(name)
            except KeyError:
                missing.append(rel)
                continue
            actual = sha256_bytes(data)
            if actual != expected:
                mismatched.append({'path': rel, 'expected': expected, 'actual': actual})

        result['checks']['required_files'] = {
            'status': 'PASS' if not missing and not mismatched else 'FAIL',
            'required_count': len(required),
            'missing': missing,
            'mismatched': mismatched
        }
        if missing or mismatched:
            result['status'] = 'FAIL'
            result['errors'].append('required deploy asset verification failed')
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 5

        sums_name = root + 'SHA256SUMS.txt'
        try:
            sums_text = zf.read(sums_name).decode('utf-8')
        except KeyError:
            result['status'] = 'FAIL'
            result['errors'].append('SHA256SUMS.txt missing')
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 6

        checksum_entries = []
        checksum_errors = []
        pattern = re.compile(r'^([0-9a-f]{64})\s{2}(.+)$')
        for raw in sums_text.splitlines():
            line = raw.strip('\n')
            if not line.strip():
                continue
            match = pattern.match(line)
            if not match:
                checksum_errors.append({'line': line, 'error': 'invalid checksum line'})
                continue
            expected, rel = match.groups()
            name = root + rel
            try:
                actual = sha256_bytes(zf.read(name))
            except KeyError:
                checksum_errors.append({'path': rel, 'error': 'missing'})
                continue
            checksum_entries.append(rel)
            if actual != expected:
                checksum_errors.append({'path': rel, 'expected': expected, 'actual': actual})

        result['checks']['internal_sha256sums'] = {
            'status': 'PASS' if not checksum_errors else 'FAIL',
            'verified_count': len(checksum_entries),
            'errors': checksum_errors
        }
        if checksum_errors:
            result['status'] = 'FAIL'
            result['errors'].append('internal SHA256SUMS verification failed')
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 7

        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for info in zf.infolist():
            if not info.filename.startswith(root) or info.filename == root:
                continue
            rel = info.filename[len(root):]
            if not rel:
                continue
            out = dest / PurePosixPath(rel)
            if info.is_dir():
                out.mkdir(parents=True, exist_ok=True)
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, out.open('wb') as dst:
                shutil.copyfileobj(src, dst)

    result['checks']['extraction'] = {'status': 'PASS', 'dest': str(dest)}
    result['status'] = 'PASS'
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
