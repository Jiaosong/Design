from pathlib import Path
import cv2, numpy as np, subprocess, math, json, trimesh
from PIL import Image, ImageDraw, ImageFont
BASE=Path('/mnt/data/C04_F_FINAL_20260815'); OUT=BASE/'revision_v04/video'; OUT.mkdir(parents=True,exist_ok=True)
D=BASE/'inputs/d_v11/QJD_v1.1_PUBLIC_DISPLAY/01_PUBLIC_ASSETS'; C22=BASE/'inputs/c22/rendered'; SEC=BASE/'inputs/model_bridge/extracted/C04_CONCEPT_MODEL_PACK_v1/sections'; GLB=BASE/'inputs/model_bridge/extracted/C04_CONCEPT_MODEL_PACK_v1/model/C04_QINGJIANG_CONCEPT_MODEL_v1.glb'; AUDIO=BASE/'video/C04_F_FILM_86s_audio_master.m4a'; R13P=BASE/'inputs/image2_rev04/湿润峡谷中的远眺者.png'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; FONTB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SW,SH,FPS0=960,540,12; FW,FH,FPS=1920,1080,24
TEAL=(47,110,112); RUST=(180,92,69); GOLD=(162,132,86); WHITE=(248,246,239); PALE=(220,232,227); INK=(16,37,33); DARK=(15,33,29); PAPER=(241,238,230); MUTED=(103,115,111)
def load(p): return cv2.cvtColor(np.array(Image.open(p).convert('RGB')),cv2.COLOR_RGB2BGR)
def cover(img,w=SW,h=SH,zoom=1,pan=(0,0)):
 ih,iw=img.shape[:2]; r=max(w/iw,h/ih)*zoom; nw,nh=max(w,int(iw*r)),max(h,int(ih*r)); im=cv2.resize(img,(nw,nh),interpolation=cv2.INTER_AREA if r<1 else cv2.INTER_LINEAR); cx=(nw-w)//2+int(pan[0]); cy=(nh-h)//2+int(pan[1]); cx=max(0,min(cx,nw-w)); cy=max(0,min(cy,nh-h)); return im[cy:cy+h,cx:cx+w].copy()
def contain(img,w=SW,h=SH,bg=PAPER):
 ih,iw=img.shape[:2]; r=min(w/iw,h/ih); nw,nh=int(iw*r),int(ih*r); o=np.full((h,w,3),bg[::-1],np.uint8); im=cv2.resize(img,(nw,nh),interpolation=cv2.INTER_AREA); o[(h-nh)//2:(h-nh)//2+nh,(w-nw)//2:(w-nw)//2+nw]=im; return o
def rectalpha(frame,box,color,alpha):
 x1,y1,x2,y2=box; ov=frame.copy(); cv2.rectangle(ov,(x1,y1),(x2,y2),color[::-1],-1); cv2.addWeighted(ov,alpha,frame,1-alpha,0,frame)
def text_layer(lines):
 im=Image.new('RGBA',(SW,SH),(0,0,0,0)); d=ImageDraw.Draw(im)
 for item in lines:
  x,y,s,sz,c,b,mono=item; f=ImageFont.truetype(MONO if mono else (FONTB if b else FONT),sz); d.text((x,y),s,font=f,fill=(*c,255))
 return cv2.cvtColor(np.array(im),cv2.COLOR_RGBA2BGRA)
def apply_layer(frame,lay,alpha=1):
 a=(lay[:,:,3:4].astype(np.float32)/255*alpha); return (frame.astype(np.float32)*(1-a)+lay[:,:,:3].astype(np.float32)*a).astype(np.uint8)
def base_layer(kicker,title,sub='',dark=True,footer=True):
 c1=PALE if dark else TEAL; c2=WHITE if dark else INK; c3=PALE if dark else MUTED
 lines=[(36,20,kicker,9,c1,True,True),(36,47,title,31,c2,True,False)]
 if sub: lines.append((36,88,sub,13,c3,False,False))
 if footer: lines.append((36,513,'FIELD 0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION',7,RUST,True,True))
 return text_layer(lines)
def lerp(a,b,t): return a+(b-a)*t
def sm(t): return t*t*(3-2*t)
def blend(a,b,t): return cv2.addWeighted(a,1-t,b,t,0)
hero=load(D/'QJD_V11_01_HERO_1920x1080.png'); r06a=load(D/'QJD_V11_03A_R06_LANDSCAPE_FIRST_1920x1080.png'); r06b=load(D/'QJD_V11_03B_R06_RELATION_REVEAL_1920x1080.png'); ret=load(D/'QJD_V11_05_RETURN_UNKNOWN_CLOSED_1920x1080.png'); master=load(C22/'page-2.png'); seca=load(SEC/'SEC_A_CABLE_RELATION.png'); r13=load(R13P)
LAY={
'hero':base_layer('OLEANDER / C04 / LANDSCAPE FIRST','清江石书','先越江，再入山；最后回到同一片清江。',True),
'map':base_layer('ROUTE / MACRO NETWORK','地图线生长：先到达，再越江，再进入分支网络','NTS / relation only / not actual walking time sequence',False),
'seca':base_layer('SECTION / PRIMARY ALLOWED','SEC-A 切入：跨江不是章节，是尺度转换','1056 m / ΔH≈156 m source-grounded relation; non-survey profile',False),
'model':base_layer('MODEL / PROCESS SUPPORT','模型绕行：关系与层级，不是现场形态','GLB source reopen PASS / process support',False),
'r06a':base_layer('R06 / ENTER','先看景观整体','不先数层数，不先解释。',True),
'r06b':base_layer('R06 / RELATION REVEAL','看左右，而不是数层数','D v1.1 relation visual / AI R06 not used',True),
'r13':base_layer('R13 / WITHDRAWAL','自然收束：从湿润岩隙重新看见清江','AI-assisted conceptual visualization',True),
'return':base_layer('RETURN FIRST','回程不是尾声，而是系统的安全主线','NORMAL / DEGRADED / CLOSED / UNKNOWN',True),
'end':base_layer('RETURN / RE-RECOGNITION','回到同一片清江','route closes / landscape remains',True,footer=False),
}
R13NOTE=text_layer([(36,470,'DOES NOT PROVE: ACTUAL LANDFORM / FACILITY / PATH / RAILING / SAFETY',8,RUST,True,True)])
scene=trimesh.load(GLB,force='scene'); parts=[]
for name,g in scene.geometry.items():
 if any(k in name for k in ['SITE_','CABLE_','ROUTE_','R06_PLATFORM','R13_APERTURE','R01_CABIN','A2_NORTH','A3_SOUTH']):
  v=np.asarray(g.vertices,dtype=np.float32); faces=np.asarray(g.faces,dtype=np.int32)
  if len(faces)>250: faces=faces[::6]
  if 'RIVER' in name:c=(124,174,184)
  elif 'ROUTE' in name:c=(70,131,128)
  elif 'CABLE' in name:c=(32,48,44)
  elif 'R13' in name:c=(55,61,58)
  elif 'R06' in name:c=(170,135,92)
  elif 'SOUTH_BANK' in name:c=(126,130,113)
  elif 'NORTH_BANK' in name:c=(150,147,133)
  else:c=(95,101,93)
  parts.append((v,faces,c))
center=np.array([0,60,190],np.float32)
def model_frame(t):
 f=np.full((SH,SW,3),PAPER[::-1],np.uint8); yaw=math.radians(lerp(-30,42,sm(t))); pitch=math.radians(lerp(24,30,sm(t))); scale=lerp(.31,.38,sm(t)); cz,sz=math.cos(yaw),math.sin(yaw); cx,sx=math.cos(pitch),math.sin(pitch); R=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]],np.float32)@np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]],np.float32); polys=[]
 for v,faces,c in parts:
  vv=(v-center)@R.T; px=SW/2+vv[:,0]*scale; py=330-vv[:,2]*scale-vv[:,1]*.05*scale; dep=vv[:,1]
  for face in faces:
   pts=np.stack([px[face],py[face]],1).astype(np.int32); polys.append((float(dep[face].mean()),pts,c))
 polys.sort(key=lambda a:a[0])
 for dep,pts,c in polys: cv2.fillConvexPoly(f,pts,c[::-1],cv2.LINE_AA); cv2.polylines(f,[pts],True,(85,87,81),1,cv2.LINE_AA)
 rectalpha(f,(0,0,SW,115),PAPER,.94); return apply_layer(f,LAY['model'])
model_cache=[model_frame(i/47) for i in range(48)]

def frame(name,t):
 if name=='hero':
  f=cover(hero,zoom=lerp(1,1.08,sm(t)),pan=(lerp(-22,18,t),lerp(5,-5,t))); rectalpha(f,(0,0,SW,130),DARK,.35); return apply_layer(f,LAY['hero'])
 if name=='map':
  f=contain(master); f=apply_layer(f,LAY['map']); pts=np.array([(80,260),(255,245),(425,205),(545,195),(630,240),(695,278),(755,260),(820,325),(758,395),(700,360)],np.int32); prog=t*(len(pts)-1); idx=min(len(pts)-2,int(prog)); frac=prog-idx; shown=[tuple(p) for p in pts[:idx+1]]; p=pts[idx]*(1-frac)+pts[idx+1]*frac; shown.append(tuple(p.astype(int))); cv2.polylines(f,[np.array(shown,np.int32)],False,TEAL[::-1],5,cv2.LINE_AA); [cv2.circle(f,p,5,RUST[::-1],-1,cv2.LINE_AA) for p in shown[:-1]]; return f
 if name=='seca':
  q=contain(seca); f=cover(q,zoom=lerp(1,1.10,sm(t)),pan=(lerp(-8,18,t),0)); x=int(lerp(90,865,t)); cv2.line(f,(x,110),(x,450),RUST[::-1],2,cv2.LINE_AA); return apply_layer(f,LAY['seca'])
 if name=='model': return model_cache[min(47,int(t*47))].copy()
 if name=='r06':
  if t<.45:
   q=cover(r06a,zoom=lerp(1,1.07,sm(t/.45)),pan=(lerp(-12,18,t/.45),0)); rectalpha(q,(0,0,SW,118),DARK,.36); return apply_layer(q,LAY['r06a'])
  tt=(t-.45)/.55; a=cover(r06a,zoom=1.05); b=cover(r06b,zoom=lerp(1,1.05,sm(tt)),pan=(lerp(10,-10,tt),0)); q=blend(a,b,sm(min(1,tt*1.4))); rectalpha(q,(0,0,SW,118),DARK,.36); return apply_layer(q,LAY['r06b'])
 if name=='r13':
  q=cover(r13,zoom=lerp(1.0,1.095,sm(t)),pan=(lerp(0,32,sm(t)),lerp(0,5,t)))
  if t<.18: q=blend(cover(r06b,zoom=1.04),q,sm(t/.18))
  rectalpha(q,(0,0,SW,120),DARK,.50); q=apply_layer(q,LAY['r13']); q=apply_layer(q,R13NOTE); return q
 if name=='return':
  q=cover(ret,zoom=lerp(1.0,1.035,sm(t)),pan=(lerp(-8,8,t),0))
  if t<.22: q=blend(cover(r13,zoom=1.09,pan=(30,4)),q,sm(t/.22))
  rectalpha(q,(0,0,SW,118),DARK,.34); q=apply_layer(q,LAY['return']); labs=[('NORMAL',TEAL),('DEGRADED',GOLD),('CLOSED',RUST),('UNKNOWN',MUTED)]
  for i,(lab,c) in enumerate(labs):
   tt=max(0,min(1,(t-i*.08)/.28)); x=45+i*218; y=int(lerp(520,418,sm(tt))); rectalpha(q,(x,y,x+185,y+52),c,.70); cv2.putText(q,lab,(x+12,y+23),cv2.FONT_HERSHEY_SIMPLEX,.40,WHITE[::-1],1,cv2.LINE_AA)
  return q
 q=cover(hero,zoom=lerp(1.065,1.0,sm(t)),pan=(lerp(12,-5,t),0))
 if t<.22: q=blend(cover(ret,zoom=1.03),q,sm(t/.22))
 rectalpha(q,(0,0,SW,145),DARK,.34); q=apply_layer(q,LAY['end'])
 cv2.line(q,(36,485),(400,485),TEAL[::-1],2,cv2.LINE_AA); cv2.putText(q,'LANDSCAPE FIRST / RETURN FIRST',(36,510),cv2.FONT_HERSHEY_SIMPLEX,.38,PALE[::-1],1,cv2.LINE_AA)
 return q
segments=[('hero',8),('map',10),('seca',10),('model',10),('r06',13),('r13',10),('return',7),('end',18)]
low=OUT/'C04_F_FILM_86s_REV04_low.mp4'; silent=OUT/'C04_F_FILM_86s_REV04_silent.mp4'; final=OUT/'C04_F_FILM_86s_REV04.mp4'
cmd=['ffmpeg','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{SW}x{SH}','-r',str(FPS0),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',str(low)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
for name,dur in segments:
 n=dur*FPS0
 for i in range(n): p.stdin.write(frame(name,i/max(1,n-1)).tobytes())
p.stdin.close(); err=p.stderr.read(); rc=p.wait()
if rc: raise RuntimeError(err.decode('utf-8','ignore')[-2000:])
subprocess.run(['ffmpeg','-y','-i',str(low),'-vf',f'scale={FW}:{FH}:flags=lanczos,fps={FPS}','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-t','86',str(silent)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
if AUDIO.exists():
 subprocess.run(['ffmpeg','-y','-i',str(silent),'-i',str(AUDIO),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-t','86','-shortest',str(final)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
else: final=silent
shot={'schema':'oleander.c04.f-motion-revision/0.4','status':'EXECUTED / REVISE','independent_review_inherited':{'structure':'KEEP','targeted_revise':['51-61s R13','Return UI length','audit-card ending']},'duration_s':86,'output':final.name,'r13_source':str(R13P),'r13_label':'AI-assisted conceptual visualization','r13_does_not_prove':['actual landform','actual facility','path width','railing','safety condition'],'segments':[]}; ts=0
for i,(n,dur) in enumerate(segments,1): shot['segments'].append({'scene_id':f'SCENE-F-{i:02d}','name':n,'start_s':ts,'duration_s':dur,'end_s':ts+dur}); ts+=dur
(OUT/'C04_F_FILM_86s_REV04_shotlist.json').write_text(json.dumps(shot,ensure_ascii=False,indent=2),encoding='utf-8')
print(final)
