from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A1, landscape
from reportlab.lib.utils import ImageReader
import json,csv,hashlib,shutil,math,os

BASE=Path('/mnt/data/C04_F_FINAL_20260815')
REV3=BASE/'revision_v03'
OUT=BASE/'revision_v04'
BOARDS=OUT/'boards'; SCREENS=OUT/'screens'; WEB=OUT/'web'; MAN=OUT/'manifest'; PREV=OUT/'preview'; WORK=OUT/'work'; AUD=OUT/'audit'
for d in [OUT,BOARDS,SCREENS,WEB,MAN,PREV,WORK,AUD]: d.mkdir(parents=True,exist_ok=True)
D=BASE/'inputs/d_v11/QJD_v1.1_PUBLIC_DISPLAY/01_PUBLIC_ASSETS'
A=BASE/'inputs/a_current'
E=BASE/'inputs/e/C04_QJE_Remote-Digital-Materialization_v0.1.0_CAND_E2_20260815/preview'
C22=BASE/'inputs/c22/rendered'
M=BASE/'inputs/model_bridge/extracted/C04_CONCEPT_MODEL_PACK_v1'; SEC=M/'sections'; RND=M/'renders'
R13=BASE/'inputs/image2_rev04/湿润峡谷中的远眺者.png'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; FONTB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
if not Path(FONTB).exists(): FONTB=FONT
PAPER='#F1EEE6'; INK='#102521'; MUTED='#67736F'; TEAL='#2F6E70'; PALE='#DCE8E3'; RUST='#B45C45'; GOLD='#A28456'; DARK='#0F211D'; WHITE='#F8F6EF'; LINE='#B9C1BC'; SOFT='#E3E5DE'

def rgb(h):
 h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def fnt(sz,b=False,mono=False): return ImageFont.truetype(MONO if mono else (FONTB if b else FONT),sz)
def text(d,xy,s,sz,fill=INK,b=False,maxw=None,spacing=1.18,mono=False,anchor=None):
 f=fnt(sz,b,mono); x,y=xy
 if maxw is None: d.text((x,y),str(s),font=f,fill=rgb(fill),anchor=anchor); return
 lines=[]
 for p in str(s).split('\n'):
  if not p: lines.append(''); continue
  line=''
  for ch in p:
   t=line+ch
   if d.textlength(t,font=f)>maxw and line: lines.append(line); line=ch
   else: line=t
  lines.append(line)
 lh=int(sz*spacing)
 for i,l in enumerate(lines): d.text((x,y+i*lh),l,font=f,fill=rgb(fill))
def fit(path,size,mode='cover',brightness=1.0):
 im=Image.open(path).convert('RGB'); w,h=size
 if mode=='contain':
  im.thumbnail((w,h),Image.Resampling.LANCZOS); bg=Image.new('RGB',(w,h),rgb(WHITE)); bg.paste(im,((w-im.width)//2,(h-im.height)//2)); im=bg
 else:
  r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r),int(im.height*r)),Image.Resampling.LANCZOS); im=im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))
 if brightness!=1: im=ImageEnhance.Brightness(im).enhance(brightness)
 return im
def paste(dst,path,box,mode='cover',brightness=1.0,outline=None):
 x,y,w,h=box; dst.paste(fit(path,(w,h),mode,brightness),(x,y));
 if outline: ImageDraw.Draw(dst).rectangle((x,y,x+w-1,y+h-1),outline=rgb(outline),width=2)
def overlay(dst,rgba,box):
 x,y,w,h=box; lay=Image.new('RGBA',(w,h),rgba); dst.paste(lay,(x,y),lay)
def line(d,pts,fill=LINE,w=2): d.line(pts,fill=rgb(fill),width=w)
def tag(d,x,y,s,fill=TEAL,txtc=WHITE,sz=18):
 f=fnt(sz,True,True); ww=int(d.textlength(s,font=f)+34); hh=sz+20; d.rounded_rectangle((x,y,x+ww,y+hh),radius=hh//2,fill=rgb(fill)); d.text((x+17,y+8),s,font=f,fill=rgb(txtc)); return ww
def foot_screen(im,code):
 d=ImageDraw.Draw(im); line(d,[(74,1010),(1845,1010)],LINE if im.getpixel((0,0))!=rgb(DARK) else TEAL,1)
 text(d,(74,1022),'FIELD 0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION',13,RUST,True,mono=True)
 d.text((1845,1022),f'{code} · EXECUTED/REVISE',font=fnt(12,True,True),fill=rgb(MUTED),anchor='ra')
def footer_a1(im,code,state='EXECUTED / REVISE · REV04 NARROW FIX · INDEPENDENT READBACK REQUIRED'):
 d=ImageDraw.Draw(im); W,H=im.size; y=H-92; line(d,[(120,y),(W-120,y)],TEAL,2)
 text(d,(120,y+19),'FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION',18,RUST,True,mono=True)
 d.text((W-120,y+19),f'{code}   {state}',font=fnt(17,True,True),fill=rgb(MUTED),anchor='ra')
def base(pid,title,eyebrow,dark=False):
 im=Image.new('RGB',(1920,1080),rgb(DARK if dark else PAPER)); d=ImageDraw.Draw(im); col=WHITE if dark else INK
 text(d,(74,44),eyebrow,17,RUST,True,mono=True); text(d,(74,86),title,62,col,True,maxw=1500); d.text((1845,52),pid[-2:],font=fnt(22,True,True),fill=rgb(col),anchor='ra'); return im,d

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

# ----- Carry forward KEEP assets exactly -----
for i in [1,2]: shutil.copy2(REV3/'boards'/f'C04_F_A1_BOARD_{i:02d}_REV03.png',BOARDS/f'C04_F_A1_BOARD_{i:02d}_REV04.png')
for i in range(1,21): shutil.copy2(REV3/'screens'/f'PAGE-{i:02d}_REV03.png',SCREENS/f'PAGE-{i:02d}_REV04.png')

# ----- A1-03 only: R13 v3 binding -----
def board3():
 W,H=4967,3508; im=Image.new('RGB',(W,H),rgb(DARK)); d=ImageDraw.Draw(im)
 text(d,(120,70),'OLEANDER / C04 / EXPERIENCE SEQUENCE',22,RUST,True,mono=True)
 text(d,(120,122),'SEE → ENTER → WITHDRAW → RETURN',80,WHITE,True,maxw=3800)
 text(d,(120,220),'A1-03 REV04 / only R13 is replaced; R06 remains D v1.1.',31,PALE,maxw=3600)
 d.text((W-120,82),'F-A1-03',font=fnt(30,True,True),fill=rgb(WHITE),anchor='ra'); line(d,[(120,310),(W-120,310)],TEAL,3)
 paste(im,D/'QJD_V11_01_HERO_1920x1080.png',(120,355,4727,950),'cover',.80); overlay(im,(5,20,18,90),(120,355,4727,950))
 text(d,(180,450),'01 / CROSS THE RIVER',25,PALE,True,mono=True); text(d,(180,510),'先越江，再入山。',64,WHITE,True)
 line(d,[(260,1148),(1550,1148),(2920,1148),(4470,1148)],WHITE,5)
 for x,lab in [(260,'HERO'),(1550,'R06'),(2920,'R13 v3'),(4470,'RETURN')]: d.ellipse((x-13,1135,x+13,1161),fill=rgb(RUST)); text(d,(x-42,1176),lab,18,PALE,True,mono=True)
 text(d,(120,1300),'02 / R06 · D v1.1 RELATION REVEAL',22,RUST,True,mono=True)
 paste(im,D/'QJD_V11_03B_R06_RELATION_REVEAL_1920x1080.png',(120,1355,2110,1190),'cover')
 text(d,(2320,1300),'03 / R13 · WITHDRAWAL → APERTURE → RE-RECOGNITION',22,RUST,True,mono=True)
 paste(im,R13,(2320,1355,2527,1190),'cover')
 overlay(im,(5,20,18,150),(2320,2382,2527,163))
 text(d,(2360,2402),'AI-ASSISTED CONCEPTUAL VISUALIZATION',24,WHITE,True,mono=True)
 text(d,(2360,2444),'does-not-prove: actual landform / facility / path width / railing / safety condition',19,PALE,True,mono=True)
 paste(im,D/'QJD_V11_05_RETURN_UNKNOWN_CLOSED_1920x1080.png',(120,2630,4727,590),'cover',.78); overlay(im,(5,20,18,70),(120,2630,4727,590))
 text(d,(180,2710),'04 / RETURN FIRST',24,WHITE,True,mono=True); text(d,(180,2770),'回程不是尾声，而是系统的安全主线。',46,WHITE,True,maxw=2200)
 x=3100
 for s,c in [('NORMAL',TEAL),('DEGRADED',GOLD),('CLOSED',RUST),('UNKNOWN',MUTED)]: x+=tag(d,x,2780,s,c,WHITE,18)+18
 text(d,(180,3105),'R13 v3 = KEEP by controller visual review · R06 AI version NOT USED · D v1.1 relation visual retained.',20,PALE,True,mono=True)
 footer_a1(im,'A1-03 / REV04 R13 v3 BIND')
 return im
b3=board3(); b3.save(BOARDS/'C04_F_A1_BOARD_03_REV04.png',quality=95)

# ----- seven narrow screen fixes -----
im,d=base('PAGE-02','远程研究 ≠ 现场完成','BOUNDARY / REMOTE CONCEPT STATUS',False)
text(d,(74,205),'0',110,RUST,True,mono=True); text(d,(220,225),'FIELD OBSERVED',28,INK,True,mono=True); text(d,(220,273),'没有新增现场观察；远程概念展示仍可继续。',26,MUTED,maxw=610)
text(d,(74,430),'0',110,RUST,True,mono=True); text(d,(220,450),'FIELD MEASURED',28,INK,True,mono=True); text(d,(220,498),'坡度、净宽、视距、GPS、真实安全边界待现场替换。',26,MUTED,maxw=610)
line(d,[(860,205),(860,900)],LINE,2)
text(d,(950,215),'G1F',30,GOLD,True,mono=True); text(d,(950,265),'HOLD',86,GOLD,True,mono=True); text(d,(950,380),'实施 / 合规 / 施工门保持关闭。',31,INK,True,maxw=760)
line(d,[(950,500),(1740,500)],TEAL,4)
text(d,(950,550),'PRESENTATION',25,TEAL,True,mono=True); text(d,(950,596),'EXECUTED / REVISE',48,TEAL,True,mono=True); text(d,(950,680),'远程概念成果可被展示；但 Professional Gate 必须由独立审查关闭。',28,MUTED,maxw=760,spacing=1.25)
text(d,(74,910),'FIELD=0 是 Authority 边界，不等于“远程概念展示未完成”。',26,INK,True,maxw=1600)
foot_screen(im,'BOUNDARY-01 / REV04'); im.save(SCREENS/'PAGE-02_REV04.png',quality=95)

im,d=base('PAGE-10','R01｜视点正在过江','MOVING VIEW / NO FORCED UI',False)
paste(im,SEC/'SEC_A_CABLE_RELATION.png',(74,205,1180,720),'contain',outline=LINE)
text(d,(95,225),'SEC-A / PRIMARY SECTION ALLOWED',20,TEAL,True,mono=True)
paste(im,D/'QJD_V11_01_HERO_1920x1080.png',(1300,205,545,300),'cover',.80)
text(d,(1300,545),'VIEW ONLY',48,INK,True,mono=True); line(d,[(1300,620),(1810,620)],TEAL,5)
text(d,(1300,660),'索道移动视点不设置强制 UI、Relation Mark、长解释或必做触发。',28,MUTED,maxw=520,spacing=1.25)
text(d,(1300,835),'路线 / 回程主权高于解释层。',27,RUST,True,maxw=520)
foot_screen(im,'R01 / SEC-A + VIEW CUE'); im.save(SCREENS/'PAGE-10_REV04.png',quality=95)

im,d=base('PAGE-14','十三印是一座可选阅读库','READING LIBRARY / OPTIONAL',False)
text(d,(74,220),'8',108,TEAL,True,mono=True); text(d,(205,245),'CORE',36,INK,True,mono=True); text(d,(74,350),'R01  R02  R05  R06  R07  R09  R12  R13',29,INK,True,mono=True)
text(d,(74,475),'5',108,GOLD,True,mono=True); text(d,(205,500),'COMPANION',36,INK,True,mono=True); text(d,(74,605),'R03  R04  R08  R10  R11',29,INK,True,mono=True)
line(d,[(720,220),(720,905)],LINE,2)
text(d,(800,220),'R01 / S0 VIEW ONLY',28,TEAL,True,mono=True); text(d,(800,270),'移动视点禁止强制 UI / Relation Mark / 必做触发。',29,INK,True,maxw=930)
text(d,(800,420),'PRIORITY',24,RUST,True,mono=True); text(d,(800,470),'SERVICE / RETURN',44,RUST,True,mono=True); text(d,(800,540),'→ ROUTE → OBSERVATION → EXPLANATION',31,INK,True,mono=True,maxw=930); text(d,(800,600),'→ MEMORY → SHARE',31,INK,True,mono=True)
text(d,(800,735),'可跳过 · 可重排 · 可关闭',37,TEAL,True); text(d,(800,800),'十三印不成为十三个强制实体任务站。',27,MUTED,maxw=900)
foot_screen(im,'READING-8+5 / REV04'); im.save(SCREENS/'PAGE-14_REV04.png',quality=95)

im,d=base('PAGE-15','Evidence → Relation → Withdrawal → Re-recognition','EXPERIENCE LOGIC / 4 STEPS',True)
assets=[A/'FIG-C04-A00_web_hero_1920x1080.png',D/'QJD_V11_03B_R06_RELATION_REVEAL_1920x1080.png',R13,D/'QJD_V11_05_RETURN_UNKNOWN_CLOSED_1920x1080.png']
labels=[('01','EVIDENCE','关系证据'),('02','RELATION','景观先于解释'),('03','WITHDRAWAL','收束 / 再识别'),('04','RETURN','安全主线')]
x=74; gap=18; ww=429; y=210; hh=640
for i,(a,lab) in enumerate(zip(assets,labels)):
 paste(im,a,(x,y,ww,hh),'cover',.94); overlay(im,(5,20,18,55),(x,y,ww,hh)); text(d,(x+20,y+20),f'{lab[0]} / {lab[1]}',21,WHITE,True,mono=True); text(d,(x+20,y+555),lab[2],26,WHITE,True,maxw=ww-40)
 if i==2:
  overlay(im,(5,20,18,145),(x,y+490,ww,150)); text(d,(x+20,y+500),'AI-ASSISTED CONCEPTUAL',15,WHITE,True,mono=True); text(d,(x+20,y+525),'does-not-prove landform / facility',14,PALE,True,mono=True)
 x+=ww+gap
line(d,[(165,900),(1755,900)],TEAL,4); text(d,(74,930),'不是四个强制打卡点，而是一次阅读强度逐步退场的连续体验。',27,PALE,True,maxw=1500)
foot_screen(im,'E2S / REV04'); im.save(SCREENS/'PAGE-15_REV04.png',quality=95)

im,d=base('PAGE-17','Digital OFF，主旅程仍然成立','OFFLINE FIRST / PHONE OUT',False)
paste(im,E/'interaction-map-frame.png',(74,205,1160,700),'cover',outline=LINE); text(d,(95,225),'ROUTE / SERVICE FIRST',20,TEAL,True,mono=True)
paste(im,E/'digital-silence-frame.png',(1280,205,565,315),'cover',outline=LINE); text(d,(1300,225),'DIGITAL SILENCE',18,RUST,True,mono=True)
text(d,(1280,570),'NO GPS REQUIRED',27,INK,True,mono=True); text(d,(1280,620),'NO NETWORK REQUIRED',27,INK,True,mono=True); text(d,(1280,670),'NO FORCED READING',27,INK,True,mono=True)
line(d,[(1280,745),(1815,745)],TEAL,4); text(d,(1280,785),'手机退出后，路线、安全与回程仍完整。',28,MUTED,maxw=535,spacing=1.2)
foot_screen(im,'E-OFFLINE / REV04'); im.save(SCREENS/'PAGE-17_REV04.png',quality=95)

im,d=base('PAGE-18','容量、时间与风险｜附录','APPENDIX / RANGE + FORMULA + SENSITIVITY',False)
cols=[74,410,810,1250,1580,1845]; y0=225
for x in cols: line(d,[(x,y0),(x,900)],LINE,2)
for y in [225,340,455,570,685,800,900]: line(d,[(74,y),(1845,y)],LINE,2)
heads=['ITEM','RECOMMENDED','RANGE / RULE','DOES NOT PROVE','FUTURE CALIBRATION']
for i,h in enumerate(heads): text(d,(cols[i]+18,245),h,18,RUST,True,mono=True)
rows=[
 ('ROUTE BUDGET','182 min','138–230 min','field timing','pace / stops / closure'),
 ('CAPACITY','Csystem = min(...)','cable/station/walk/node/return','trail capacity from cable','width / dwell / density'),
 ('CABLE','2700 p/h','official design capacity','node/walk throughput','operations / queues'),
 ('STATE','N / D / C / U','NORMAL / DEGRADED / CLOSED / UNKNOWN','UNKNOWN as OPEN','live status / closure'),
 ('RISK','FIELD OPEN','slope / wetness / lighting / evacuation','compliance / safety','site survey / operations')]
y=355
for r in rows:
 for i,val in enumerate(r): text(d,(cols[i]+18,y),val,22 if i else 20,INK if i else TEAL,True if i<2 else False,maxw=cols[i+1]-cols[i]-36,mono=(i<2))
 y+=115
text(d,(74,930),'推荐值 + 合理区间 + 依据 + 敏感因素 + 未来现场校正项；禁止单点伪精确。',24,MUTED,True,maxw=1700)
foot_screen(im,'APPX-A / REV04'); im.save(SCREENS/'PAGE-18_REV04.png',quality=95)

im,d=base('PAGE-20','回到同一片清江','RETURN / RE-RECOGNITION',False)
paste(im,D/'QJD_V11_05_RETURN_UNKNOWN_CLOSED_1920x1080.png',(74,205,1180,720),'cover',outline=LINE)
text(d,(1300,245),'RETURN FIRST',24,RUST,True,mono=True); text(d,(1300,300),'路线可以结束，\n回程不能消失。',50,INK,True,maxw=520,spacing=1.15)
line(d,[(1300,520),(1815,520)],TEAL,5); text(d,(1300,565),'NORMAL / DEGRADED / CLOSED / UNKNOWN',21,TEAL,True,mono=True,maxw=520); text(d,(1300,640),'UNKNOWN ≠ OPEN',36,RUST,True,mono=True); text(d,(1300,715),'回到熟悉的清江，完成再识别；不是审计卡，也不是第二次 Hero。',28,MUTED,maxw=520,spacing=1.25)
foot_screen(im,'RETURN / REV04'); im.save(SCREENS/'PAGE-20_REV04.png',quality=95)

# ----- Assemble PDFs -----
pdf=BOARDS/'C04_F_A1_BOARDS_REV04.pdf'; c=canvas.Canvas(str(pdf),pagesize=landscape(A1)); pw,ph=landscape(A1)
for i in range(1,4): c.drawImage(ImageReader(str(BOARDS/f'C04_F_A1_BOARD_{i:02d}_REV04.png')),0,0,width=pw,height=ph); c.showPage()
c.save()
pdf20=OUT/'C04_F_Landscape_Atlas_20screen_REV04.pdf'; c=canvas.Canvas(str(pdf20),pagesize=(1920,1080))
for i in range(1,21): c.drawImage(ImageReader(str(SCREENS/f'PAGE-{i:02d}_REV04.png')),0,0,width=1920,height=1080); c.showPage()
c.save()
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C04 Landscape Atlas REV04</title><style>*{box-sizing:border-box}html,body{margin:0;background:#0f211d;font-family:Arial,sans-serif}.atlas{scroll-snap-type:y mandatory}section{height:100vh;display:grid;place-items:center;scroll-snap-align:start;background:#0f211d}img{width:100vw;height:100vh;object-fit:contain;display:block}nav{position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:8;display:grid;gap:6px}nav a{width:7px;height:7px;border-radius:50%;background:#f8f6ef;opacity:.25}nav a:hover{opacity:1}</style></head><body><nav>'''
for i in range(1,21): html+=f'<a href="#PAGE-{i:02d}" title="PAGE-{i:02d}"></a>'
html+='</nav><main class="atlas">'
for i in range(1,21): html+=f'<section id="PAGE-{i:02d}"><img src="../screens/PAGE-{i:02d}_REV04.png" alt="PAGE-{i:02d}"></section>'
html+='</main></body></html>'
(WEB/'index.html').write_text(html,encoding='utf-8')
narrow={2,10,14,15,17,18,20}
rows=[]
for i in range(1,21):
 p=SCREENS/f'PAGE-{i:02d}_REV04.png'; rows.append({'page_id':f'PAGE-{i:02d}','rev04_action':'NARROW_REVISE' if i in narrow else 'CARRY_FORWARD_BYTE_IDENTICAL_FROM_REV03','sha256':sha(p),'status':'EXECUTED / REVISE' if i in narrow else 'KEEP / CARRIED FROM REV03 INDEPENDENT REVIEW'})
with open(MAN/'PAGE_REV04_DELTA_REGISTER.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
manifest={
 'schema':'oleander.c04.f-presentation-revision/0.4','status':'EXECUTED / REVISE','scope':'NARROW_FIX_ONLY','do_not_redo_KEEP':True,
 'independent_review_input':{'A1_01':'KEEP','A1_02':'KEEP','A1_03':'REVISE','screens_revise':['P02','P10','P14','P15','P17','P18','P20'],'film_structure':'KEEP','film_revise':['51-61s R13','overlong Return UI','audit-card ending']},
 'rev04_actions':{'A1_03':'bind R13 v3 only; R06 stays D v1.1','screens':['P02 typography/boundary hierarchy','P10 remove repeated full-bleed Hero; SEC-A main','P14 denser optional-reading logic','P15 R13 v3 + stronger sequence labels','P17 larger offline interaction evidence','P18 denser appendix table','P20 no repeated Hero; Return composition'],'film':'separate REV04 motion script'},
 'r13_v3':{'source_file':str(R13),'source_sha256':sha(R13),'review_decision':'KEEP by controller actual visual review','label':'AI-assisted conceptual visualization','does_not_prove':['actual landform','actual facility','path width','railing','safety condition']},
 'r06':{'source':'D v1.1 relation visual','ai_version':'NOT USED'},
 'hard_state':{'FIELD_OBSERVED':0,'FIELD_MEASURED':0,'G1F':'HOLD','PROMOTION':'NO_PROMOTION','NTS':True,'NOT_FOR_CONSTRUCTION':True},
 'merge_gate':'WAIT_FOR_E_LIVE_BROWSER_READBACK','professional_completion_claim':'PROHIBITED','outputs':{'A1':'boards/C04_F_A1_BOARDS_REV04.pdf','P20':'C04_F_Landscape_Atlas_20screen_REV04.pdf','web':'web/index.html'}
}
(MAN/'C04_F_PRESENTATION_REVISION_MANIFEST_v0.4.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'out':str(OUT),'r13_sha256':sha(R13),'a1_01_unchanged':sha(BOARDS/'C04_F_A1_BOARD_01_REV04.png')==sha(REV3/'boards/C04_F_A1_BOARD_01_REV03.png'),'a1_02_unchanged':sha(BOARDS/'C04_F_A1_BOARD_02_REV04.png')==sha(REV3/'boards/C04_F_A1_BOARD_02_REV03.png')},ensure_ascii=False,indent=2))
