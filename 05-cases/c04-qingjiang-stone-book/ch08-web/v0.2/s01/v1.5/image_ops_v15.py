from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np, hashlib, json

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'assets/ch08_s01_qingjiang_landscape_official_20230711.jpg'
OUT=ROOT/'assets'
source=Image.open(SRC).convert('RGB')
w,h=source.size

# CH14 correction: real photography remains first-read. Image Ops is medium response, not a style takeover.
# Stage 1 / WASH-TONAL — restrained contemporary print tonal compression.
ton=ImageEnhance.Color(source).enhance(0.84)
ton=ImageEnhance.Contrast(ton).enhance(0.94)
ton=ImageEnhance.Brightness(ton).enhance(1.015)
# a very small Bone Mist paper-white influence; no sepia / antique cast.
bone=Image.new('RGB', ton.size, '#F1EDE4')
ton=Image.blend(ton,bone,0.025)
ton_path=OUT/'ch08_s01_src05_WASH-TONAL_v1_5.png'
ton.save(ton_path,optimize=True)

# Stage 2 / WASH-MASK — optical decay only in atmospheric/high-distance zones.
# No white fog, torn edges, watercolor blooms or fake paper texture.
arr=np.asarray(ton).astype(np.float32)
soft=np.asarray(ton.filter(ImageFilter.GaussianBlur(1.25))).astype(np.float32)
soft_img=Image.fromarray(np.uint8(np.clip(soft,0,255)))
soft_img=ImageEnhance.Contrast(soft_img).enhance(0.92)
soft=np.asarray(soft_img).astype(np.float32)
Y,X=np.mgrid[0:h,0:w]
yn=Y/(h-1); xn=X/(w-1)
# upper atmosphere fade + distant left valley; both subtle and bounded
m_top=np.clip((0.58-yn)/0.58,0,1)*0.15
m_left=np.exp(-(((xn-0.12)/0.28)**2 + ((yn-0.35)/0.30)**2))*0.08
mask=np.clip(m_top+m_left,0,0.18)[...,None]
wash=arr*(1-mask)+soft*mask
wash=np.uint8(np.clip(wash,0,255))
wash_img=Image.fromarray(wash,'RGB')
wash_path=OUT/'ch08_s01_src05_WASH-MASK_v1_5.png'
wash_img.save(wash_path,optimize=True)

# Stage 3 / INK-EDGE — not an outline. Local structure/finish behaviour only.
# Use a soft unsharp version, confined to main rock mass + a faint distant ridge band.
sharp=wash_img.filter(ImageFilter.UnsharpMask(radius=1.35, percent=55, threshold=4))
base=np.asarray(wash_img).astype(np.float32)
sh=np.asarray(sharp).astype(np.float32)
# Main rock mass soft elliptical owner
rock=np.exp(-(((xn-0.39)/0.30)**2 + ((yn-0.58)/0.36)**2))*0.46
# distant ridge second-read, much weaker
ridge=np.exp(-(((yn-0.25)/0.07)**2))*0.08
# reduce sharpening in sky / water
protect_sky=np.clip((0.18-yn)/0.18,0,1)
protect_water=np.exp(-(((xn-0.72)/0.24)**2 + ((yn-0.72)/0.19)**2))*0.65
edge_mask=np.clip((rock+ridge)*(1-protect_sky)*(1-protect_water),0,0.50)[...,None]
final=base*(1-edge_mask)+sh*edge_mask
final=np.uint8(np.clip(final,0,255))
final_img=Image.fromarray(final,'RGB')
final_path=OUT/'ch08_s01_src05_INK-EDGE_v1_5.png'
final_img.save(final_path,optimize=True)

# owner masks for deterministic readback/debug only
Image.fromarray(np.uint8(np.clip(mask[...,0]/0.18,0,1)*255),'L').save(OUT/'ch08_s01_src05_WASH-MASK_OWNER_v1_5.png',optimize=True)
Image.fromarray(np.uint8(np.clip(edge_mask[...,0]/0.50,0,1)*255),'L').save(OUT/'ch08_s01_src05_INK-EDGE_OWNER_v1_5.png',optimize=True)

meta={
 'source': {'path':SRC.name,'size':[w,h],'sha256':hashlib.sha256(SRC.read_bytes()).hexdigest()},
 'intent':'CH14 contemporary editorial print response; real photography remains first-read',
 'stages':{
   'WASH-TONAL':{'saturation':0.84,'contrast':0.94,'brightness':1.015,'bone_mist_blend':0.025},
   'WASH-MASK':{'gaussian_radius':1.25,'max_owner_opacity':0.18,'role':'atmospheric optical decay only'},
   'INK-EDGE':{'operator':'localized unsharp / not outline','radius':1.35,'percent':55,'threshold':4,'max_owner_strength':0.50}
 },
 'prohibited':['sepia','antique paper','watercolor bloom','torn edge','full-image outline','selective fake river recolor','source overwrite'],
 'does_not_prove':['field truth','material print proof','design keep','source resolution upgrade']
}
(ROOT/'IMAGE_OPS_CONTRACT_CH08_S01_v1_5.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(meta,ensure_ascii=False,indent=2))
