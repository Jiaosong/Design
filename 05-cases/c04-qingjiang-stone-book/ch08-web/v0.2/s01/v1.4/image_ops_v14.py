from pathlib import Path
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'assets' / 'ch08_s01_qingjiang_landscape_official_20230711.jpg'
OUT = ROOT / 'assets'
SEED = 40814

RIVER_BLACK = np.array([17,25,24], np.float32)
DEEP_WATER = np.array([19,59,60], np.float32)
JADE = np.array([46,117,113], np.float32)
WET_STONE = np.array([101,112,106], np.float32)
BONE = np.array([241,237,228], np.float32)

rgb = np.array(Image.open(SRC).convert('RGB')).astype(np.float32) / 255.0
h,w,_ = rgb.shape
Y,X=np.mgrid[0:h,0:w].astype(np.float32)
x=X/(w-1); y=Y/(h-1)
bgr8 = cv2.cvtColor((rgb*255).astype(np.uint8), cv2.COLOR_RGB2BGR)
# edge-preserving smoothing; removes photographic micro-contrast before tonal mapping
sm_bgr = cv2.bilateralFilter(bgr8, d=7, sigmaColor=34, sigmaSpace=5)
sm = cv2.cvtColor(sm_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)/255.0

gray = cv2.cvtColor((sm*255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)/255.0
# gentle local luminance compression: preserve big masses, suppress screen-like contrast
large = cv2.GaussianBlur(gray, (0,0), 9.0)
detail = gray - large
lum = np.clip(large + detail*0.52, 0, 1)
lum = np.clip((lum-0.04)/0.94,0,1)
lum = np.power(lum, 0.93)
# smooth wash bands rather than hard posterize
anchors_x = np.array([0,.10,.22,.38,.56,.72,.86,1.0], np.float32)
anchors_y = np.array([.10,.16,.27,.42,.60,.77,.90,.98], np.float32)
L = np.interp(lum, anchors_x, anchors_y).astype(np.float32)

# chroma masks from source; keep river identity, heavily subordinate vegetation/settlement colour
hsv = cv2.cvtColor((rgb*255).astype(np.uint8), cv2.COLOR_RGB2HSV)
H,S,V = [hsv[...,i].astype(np.float32) for i in range(3)]
river = ((H>80)&(H<105)&(S>70)&(V>70)&(y>0.42)).astype(np.float32)
river = cv2.GaussianBlur(river,(0,0),4)
veg = ((H>28)&(H<80)&(S>45)&(V>45)).astype(np.float32)
veg = cv2.GaussianBlur(veg,(0,0),3)

# neutral ink-on-paper palette by luminance: warm wet-stone midtones, not a teal wash
SEDIMENT = np.array([216,201,177], np.float32)
low_t = np.clip(L/.50,0,1)[...,None]
high_t = np.clip((L-.50)/.50,0,1)[...,None]
low_col = RIVER_BLACK + (WET_STONE-RIVER_BLACK)*low_t
high_col = WET_STONE + (BONE-WET_STONE)*high_t
mid = np.where((L[...,None] < .50), low_col, high_col)
mid = np.clip(mid,0,255)/255.0
# source chroma is only a faint memory; the river alone keeps a bounded jade identity
orig_gray = np.repeat(gray[...,None],3,axis=2)
soft_color = orig_gray*0.90 + sm*0.10
river_color = (DEEP_WATER/255.0)[None,None,:]*(1-L[...,None]) + (JADE/255.0)[None,None,:]*L[...,None]
color_weight = 0.075 + 0.055*veg[...,None]
tonal = mid*(1-color_weight) + soft_color*color_weight
tonal = tonal*(1-river[...,None]*0.50) + river_color*(river[...,None]*0.50)
# sky/high atmosphere recedes toward paper rather than retaining blue compression artifacts
sky_paper = np.clip((0.34-y)/0.28,0,1) * np.clip((L-.48)/.40,0,1)
tonal = tonal*(1-sky_paper[...,None]*0.16) + (BONE/255.0)[None,None,:]*(sky_paper[...,None]*0.16)
tonal = np.clip(tonal,0,1)

# deterministic multi-scale paper absorption field: no radial CSS blobs
rng = np.random.default_rng(SEED)
def noise_field(sh, scale, blur):
    gh=max(2,int(sh[0]/scale)); gw=max(2,int(sh[1]/scale))
    n=rng.random((gh,gw),dtype=np.float32)
    n=cv2.resize(n,(sh[1],sh[0]),interpolation=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(n,(0,0),blur)
macro=noise_field((h,w),70,10)
meso=noise_field((h,w),22,3.6)
micro=noise_field((h,w),5,0.55)
field=(macro*0.50+meso*0.35+micro*0.15)
field=(field-field.min())/(field.max()-field.min()+1e-6)

# absorb more in atmosphere/highlights; protect central karst mass from whitening
left_atmos=np.clip(1.0-x/0.43,0,1)
sky=np.clip((0.47-y)/0.28,0,1)
high=np.clip((L-.58)/.42,0,1)
protect=np.exp(-(((x-.39)/.23)**2 + ((y-.60)/.30)**2)*2.0)
absorb=(0.13*left_atmos + 0.065*sky + 0.10*high) * (0.48+0.52*field)
absorb*= (1-0.70*protect)
absorb=np.clip(absorb,0,0.20)
# river remains visually continuous; no paper hole through primary water mass
absorb*= (1-river*0.62)
washed = tonal*(1-absorb[...,None]) + (BONE/255.0)[None,None,:]*absorb[...,None]

# pigment variation / matte paper: minute density variation, not screen scanlines
paper=(macro*0.45+meso*0.35+micro*0.20)-0.5
paper_strength=(0.010 + 0.010*(1-L))[...,None]
washed=np.clip(washed + paper[...,None]*paper_strength,0,1)
# subtle darker pooling where tonal masses meet; derived from source luminance
blur1=cv2.GaussianBlur(lum,(0,0),1.2)
gradx=cv2.Sobel(blur1,cv2.CV_32F,1,0,ksize=3)
grady=cv2.Sobel(blur1,cv2.CV_32F,0,1,ksize=3)
grad=np.sqrt(gradx*gradx+grady*grady)
grad/= (np.percentile(grad,99)+1e-6)
grad=np.clip(grad,0,1)
pool=np.clip((grad-.16)/.56,0,1)*0.028
washed=np.clip(washed*(1-pool[...,None]),0,1)

# INK EDGE: only high-value structural boundaries. Suppress settlement micro-detail / sky texture.
g8=(gray*255).astype(np.uint8)
g8=cv2.GaussianBlur(g8,(0,0),2.05)
canny=cv2.Canny(g8,72,156).astype(np.float32)/255.0
# retain strong source gradients
edge_strength=np.clip((grad-.18)/.58,0,1)
edge=canny*edge_strength
# spatial owner masks: main karst + distant ridge + river/shore; settlement receives only weak residual
main=np.exp(-(((x-.36)/.28)**2 + ((y-.58)/.36)**2)*1.35)
ridge=np.exp(-(((x-.54)/.58)**2 + ((y-.30)/.13)**2)*1.2)*0.42
shore=np.clip(river + cv2.GaussianBlur(river,(0,0),8),0,1)*0.42
owner=np.clip(main+ridge+shore,0,1)
settlement_suppress=np.where((x>.54)&(y<.67),0.28,1.0).astype(np.float32)
edge=edge*owner*settlement_suppress
edge=cv2.GaussianBlur(edge,(0,0),0.36)
edge=np.clip(edge*0.38,0,0.22)
ink=(RIVER_BLACK/255.0)[None,None,:]
final=washed*(1-edge[...,None]) + ink*edge[...,None]
# final matte finish: compress white point slightly, no glow
final=np.clip(final*0.985 + (BONE/255.0)[None,None,:]*0.015,0,1)

def save(name, arr):
    Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8),'RGB').save(OUT/name, compress_level=7)

save('ch08_s01_src05_WASH-TONAL_v1_4.png', tonal)
save('ch08_s01_src05_WASH-MASK_v1_4.png', washed)
save('ch08_s01_src05_INK-EDGE_v1_4.png', final)
# masks for audit, not displayed
Image.fromarray(np.uint8(np.clip(absorb,0,1)*255),'L').save(OUT/'ch08_s01_src05_WASH-MASK_OWNER_v1_4.png')
Image.fromarray(np.uint8(np.clip(edge/0.22,0,1)*255),'L').save(OUT/'ch08_s01_src05_INK-EDGE_OWNER_v1_4.png')
print('generated', w,h, 'absorb_max',float(absorb.max()),'edge_max',float(edge.max()))
