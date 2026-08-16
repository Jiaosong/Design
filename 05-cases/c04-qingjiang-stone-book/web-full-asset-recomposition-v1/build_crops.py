from PIL import Image
from pathlib import Path
import sys

ROOT = Path(__file__).parent
OUT = ROOT / 'assets'
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    'hero_clean.jpg': (
        'QJD_V11_01_HERO_1920x1080.png',
        (600, 90, 1920, 850),
        '16xgXoszQX3-LH150FPH_q5YO2GSfzeAB'
    ),
    'r06_valley_clean.jpg': (
        'QJD_V11_03_R06_TWO_STAGE_1920x1080.png',
        (240, 255, 930, 670),
        '1AJx_ZioWfdq6EcVVIWpzK0kea6HUjkkn'
    ),
    'r13_exit_clean.jpg': (
        'QJD_V11_04_R13_FOUR_FRAME_1920x1080.png',
        (976, 175, 1426, 812),
        '1EHXruXgv1EIU4HGpLsRqU7ciGWLG2NEf'
    ),
    'return_clean.jpg': (
        'QJD_V11_05_RETURN_UNKNOWN_CLOSED_1920x1080.png',
        (650, 0, 1920, 560),
        '19mkQdgTj0ASkGh0Ott6JIMNrPcaHd4Y7'
    ),
}

# Supply a directory containing the four existing D source PNGs.
# This performs deterministic non-generative crops only.
src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
for out_name, (name, box, drive_id) in SOURCES.items():
    p = src / name
    if not p.exists():
        raise FileNotFoundError(f'{name} missing; Drive source id={drive_id}')
    im = Image.open(p)
    im.crop(box).convert('RGB').save(OUT / out_name, quality=92, optimize=True)
    print(out_name, box, drive_id)
