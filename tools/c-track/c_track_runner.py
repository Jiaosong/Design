import bpy,sys,argparse,json,math,traceback
from pathlib import Path
MODS=["C01","C03","C04","C05","C06","C07","C08","C09"]
def A():
 a=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [];p=argparse.ArgumentParser();p.add_argument("--out",required=True);p.add_argument("--samples",type=int,default=8);return p.parse_args(a)
def si(n,k,v):
 if isinstance(k,str):k=[k]
 for x in k:
  if x in n.inputs:n.inputs[x].default_value=v;return x
def mat(n):
 m=bpy.data.materials.new(n);m.use_nodes=True;t=m.node_tree;t.nodes.clear();o=t.nodes.new("ShaderNodeOutputMaterial");e=t.nodes.new("ShaderNodeEmission");si(e,"Strength",1.0);t.links.new(e.outputs["Emission"],o.inputs["Surface"]);c=t.nodes.new("ShaderNodeTexCoord");return m,t,e,c.outputs["Generated"]
def nz(t,v,s=3):
 n=t.nodes.new("ShaderNodeTexNoise");si(n,"Scale",s);si(n,"Detail",2.0);si(n,"Roughness",.5);t.links.new(v,n.inputs["Vector"]);return n
def vm(t,op,a,b=None):
 n=t.nodes.new("ShaderNodeVectorMath");n.operation=op;t.links.new(a,n.inputs[0])
 if b is not None:n.inputs[1].default_value=b
 return n
def mm(t,op,a,b=None):
 n=t.nodes.new("ShaderNodeMath");n.operation=op;t.links.new(a,n.inputs[0])
 if b is not None:n.inputs[1].default_value=b
 return n
def out(t,e,s):t.links.new(s,e.inputs["Color"])
def c01():
 r=[]
 for q in ["RAW","MAP","POWER","ABS","HARD","SOFT","RING"]:
  m,t,e,v=mat("C01_"+q);n=nz(t,v);s=n.outputs["Fac"]
  if q=="MAP":
   x=t.nodes.new("ShaderNodeMapRange");si(x,"To Min",.25);si(x,"To Max",.75);t.links.new(s,x.inputs["Value"]);s=x.outputs["Result"]
  elif q=="POWER":s=mm(t,"POWER",s,3).outputs[0]
  elif q=="ABS":s=mm(t,"ABSOLUTE",mm(t,"SUBTRACT",s,.5).outputs[0]).outputs[0]
  elif q=="HARD":s=mm(t,"GREATER_THAN",s,.55).outputs[0]
  elif q=="SOFT":
   x=t.nodes.new("ShaderNodeValToRGB");x.color_ramp.elements[0].position=.43;x.color_ramp.elements[1].position=.62;t.links.new(s,x.inputs["Fac"]);s=x.outputs["Color"]
  elif q=="RING":
   d=vm(t,"SUBTRACT",v,(.5,.5,0));l=t.nodes.new("ShaderNodeVectorMath");l.operation="LENGTH";t.links.new(d.outputs["Vector"],l.inputs[0]);s=mm(t,"LESS_THAN",mm(t,"ABSOLUTE",mm(t,"SUBTRACT",l.outputs["Value"],.32).outputs[0]).outputs[0],.045).outputs[0]
  out(t,e,s);r.append((q,m))
 return r
def c03():
 r=[]
 for n0 in [2,4,8,16,32]:
  m,t,e,v=mat("C03");sp=t.nodes.new("ShaderNodeSeparateXYZ");t.links.new(v,sp.inputs["Vector"]);z=[]
  for ch in ["X","Y"]:
   f=mm(t,"FRACT",mm(t,"MULTIPLY",sp.outputs[ch],n0).outputs[0]);z.append(mm(t,"SUBTRACT",f.outputs[0],.5).outputs[0])
  cb=t.nodes.new("ShaderNodeCombineXYZ");t.links.new(z[0],cb.inputs["X"]);t.links.new(z[1],cb.inputs["Y"]);ln=t.nodes.new("ShaderNodeVectorMath");ln.operation="LENGTH";t.links.new(cb.outputs["Vector"],ln.inputs[0]);s=mm(t,"LESS_THAN",ln.outputs["Value"],.28).outputs[0];out(t,e,s);r.append((str(n0),m))
 return r
def c04():
 r=[]
 for q in ["VALUE","Q2","Q4","P25","P50","COLOR"]:
  m,t,e,v=mat("C04");sp=t.nodes.new("ShaderNodeSeparateXYZ");t.links.new(v,sp.inputs["Vector"]);z=[]
  for ch in ["X","Y"]:z.append(mm(t,"FLOOR",mm(t,"MULTIPLY",sp.outputs[ch],12).outputs[0]).outputs[0])
  cb=t.nodes.new("ShaderNodeCombineXYZ");t.links.new(z[0],cb.inputs["X"]);t.links.new(z[1],cb.inputs["Y"]);w=t.nodes.new("ShaderNodeTexWhiteNoise");w.noise_dimensions="3D";t.links.new(cb.outputs["Vector"],w.inputs["Vector"]);s=w.outputs["Color"] if q=="COLOR" else w.outputs["Value"]
  if q=="Q2":s=mm(t,"GREATER_THAN",s,.5).outputs[0]
  if q=="Q4":s=mm(t,"DIVIDE",mm(t,"FLOOR",mm(t,"MULTIPLY",s,4).outputs[0]).outputs[0],3).outputs[0]
  if q=="P25":s=mm(t,"LESS_THAN",s,.25).outputs[0]
  if q=="P50":s=mm(t,"LESS_THAN",s,.5).outputs[0]
  out(t,e,s);r.append((q,m))
 return r
def c05():
 r=[]
 for q in ["ADD","MULTIPLY","MINIMUM","MAXIMUM","DIFF","MIX","WARP"]:
  m,t,e,v=mat("C05");a=nz(t,v,3.5);w=t.nodes.new("ShaderNodeTexWave");si(w,"Scale",8.0);t.links.new(v,w.inputs["Vector"]);A0=a.outputs["Fac"];B=w.outputs["Fac"]
  if q=="ADD":
   x=t.nodes.new("ShaderNodeMath");x.operation="ADD";t.links.new(mm(t,"MULTIPLY",A0,.5).outputs[0],x.inputs[0]);t.links.new(mm(t,"MULTIPLY",B,.5).outputs[0],x.inputs[1]);s=x.outputs[0]
  elif q in ["MULTIPLY","MINIMUM","MAXIMUM"]:
   x=t.nodes.new("ShaderNodeMath");x.operation=q;t.links.new(A0,x.inputs[0]);t.links.new(B,x.inputs[1]);s=x.outputs[0]
  elif q=="DIFF":
   x=t.nodes.new("ShaderNodeMath");x.operation="SUBTRACT";t.links.new(A0,x.inputs[0]);t.links.new(B,x.inputs[1]);y=t.nodes.new("ShaderNodeMath");y.operation="ABSOLUTE";t.links.new(x.outputs[0],y.inputs[0]);s=y.outputs[0]
  elif q=="MIX":
   k=nz(t,v,1.4);x=t.nodes.new("ShaderNodeMixRGB");t.links.new(k.outputs["Fac"],x.inputs[0]);t.links.new(A0,x.inputs[1]);t.links.new(B,x.inputs[2]);s=x.outputs["Color"]
  elif q=="WARP":
   d=vm(t,"SUBTRACT",a.outputs["Color"],(.5,.5,.5));sc=t.nodes.new("ShaderNodeVectorMath");sc.operation="SCALE";t.links.new(d.outputs["Vector"],sc.inputs[0]);si(sc,"Scale",.18);ad=t.nodes.new("ShaderNodeVectorMath");ad.operation="ADD";t.links.new(v,ad.inputs[0]);t.links.new(sc.outputs["Vector"],ad.inputs[1]);t.links.new(ad.outputs["Vector"],w.inputs["Vector"]);s=w.outputs["Fac"]
  out(t,e,s);r.append((q,m))
 return r
def c06():
 r=[]
 for q in ["ID","MOVE","ROTATE","SCALE","STRETCH","MIRROR","REPEAT","WARP"]:
  m,t,e,v=mat("C06");mp=t.nodes.new("ShaderNodeMapping");t.links.new(v,mp.inputs["Vector"]);s=mp.outputs["Vector"]
  if q=="MOVE":si(mp,"Location",(.25,.1,0))
  if q=="ROTATE":si(mp,"Rotation",(0,0,.6))
  if q=="SCALE":si(mp,"Scale",(2,2,2))
  if q=="STRETCH":si(mp,"Scale",(4,.7,1))
  if q=="MIRROR":
   sp=t.nodes.new("ShaderNodeSeparateXYZ");t.links.new(s,sp.inputs["Vector"]);ab=mm(t,"ABSOLUTE",mm(t,"SUBTRACT",sp.outputs["X"],.5).outputs[0]);cb=t.nodes.new("ShaderNodeCombineXYZ");t.links.new(ab.outputs[0],cb.inputs["X"]);t.links.new(sp.outputs["Y"],cb.inputs["Y"]);s=cb.outputs["Vector"]
  if q=="REPEAT":
   sp=t.nodes.new("ShaderNodeSeparateXYZ");t.links.new(s,sp.inputs["Vector"]);cb=t.nodes.new("ShaderNodeCombineXYZ")
   for ch in ["X","Y"]:t.links.new(mm(t,"FRACT",mm(t,"MULTIPLY",sp.outputs[ch],3).outputs[0]).outputs[0],cb.inputs[ch])
   s=cb.outputs["Vector"]
  if q=="WARP":
   n=nz(t,s,2);d=vm(t,"SUBTRACT",n.outputs["Color"],(.5,.5,.5));sc=t.nodes.new("ShaderNodeVectorMath");sc.operation="SCALE";t.links.new(d.outputs["Vector"],sc.inputs[0]);si(sc,"Scale",.18);ad=t.nodes.new("ShaderNodeVectorMath");ad.operation="ADD";t.links.new(s,ad.inputs[0]);t.links.new(sc.outputs["Vector"],ad.inputs[1]);s=ad.outputs["Vector"]
  k=t.nodes.new("ShaderNodeTexChecker");si(k,"Scale",6);t.links.new(s,k.inputs["Vector"]);out(t,e,k.outputs["Color"]);r.append((q,m))
 return r
def c07():
 r=[]
 for q in ["BX","BY","BZ","BD","RX","RZ","DIST"]:
  m,t,e,v=mat("C07");w=t.nodes.new("ShaderNodeTexWave");si(w,"Scale",8);t.links.new(v,w.inputs["Vector"])
  if q.startswith("B"):w.wave_type="BANDS";w.bands_direction={"BX":"X","BY":"Y","BZ":"Z","BD":"DIAGONAL"}[q]
  elif q.startswith("R"):w.wave_type="RINGS";w.rings_direction={"RX":"X","RZ":"Z"}[q]
  else:w.wave_type="BANDS";w.bands_direction="X";si(w,"Distortion",4);si(w,"Detail",3)
  out(t,e,w.outputs["Color"]);r.append((q,m))
 return r
def c08():
 r=[]
 for q in ["F1","EDGE","SMOOTH","WF1","WEDGE"]:
  m,t,e,v=mat("C08")
  if q.startswith("W"):
   n=nz(t,v,2);d=vm(t,"SUBTRACT",n.outputs["Color"],(.5,.5,.5));sc=t.nodes.new("ShaderNodeVectorMath");sc.operation="SCALE";t.links.new(d.outputs["Vector"],sc.inputs[0]);si(sc,"Scale",.15);ad=t.nodes.new("ShaderNodeVectorMath");ad.operation="ADD";t.links.new(v,ad.inputs[0]);t.links.new(sc.outputs["Vector"],ad.inputs[1]);v=ad.outputs["Vector"]
  x=t.nodes.new("ShaderNodeTexVoronoi");x.voronoi_dimensions="2D";si(x,"Scale",8);x.feature="DISTANCE_TO_EDGE" if "EDGE" in q else ("SMOOTH_F1" if q=="SMOOTH" else "F1");si(x,"Smoothness",.5);t.links.new(v,x.inputs["Vector"]);out(t,e,x.outputs["Distance"]);r.append((q,m))
 return r
G={}
def c09():
 r=[]
 for q,a in [("NOISE",.7),("STRETCH",.7),("WAVE",.7),("G70",.7),("G0",0),("G35",.35),("G70B",.7),("G100",1)]:
  m,t,e,v=mat("C09")
  if q=="NOISE":s=nz(t,v,8).outputs["Fac"]
  elif q=="STRETCH":mp=t.nodes.new("ShaderNodeMapping");si(mp,"Scale",(8,.8,1));t.links.new(v,mp.inputs["Vector"]);s=nz(t,mp.outputs["Vector"],4).outputs["Fac"]
  elif q=="WAVE":w=t.nodes.new("ShaderNodeTexWave");si(w,"Scale",8);t.links.new(v,w.inputs["Vector"]);s=w.outputs["Fac"]
  else:
   g=t.nodes.new("ShaderNodeTexGabor");t.links.new(v,g.inputs["Vector"]);si(g,["Scale","Frequency"],8);si(g,"Anisotropy",a);s=g.outputs.get("Value") or g.outputs.get("Intensity") or g.outputs[0];G.update(inputs=[x.name for x in g.inputs],outputs=[x.name for x in g.outputs])
  out(t,e,s);r.append((q,m))
 return r
B={"C01":c01,"C03":c03,"C04":c04,"C05":c05,"C06":c06,"C07":c07,"C08":c08,"C09":c09}
def render(mid,items,O,a):
 bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False);n=len(items);cols=min(4,n);rows=math.ceil(n/cols)
 for i,(lab,m) in enumerate(items):
  x=(i%cols-(cols-1)/2)*2.25;y=((rows-1)/2-i//cols)*2.25;bpy.ops.mesh.primitive_plane_add(size=1.8,location=(x,y,0));bpy.context.object.name=mid+"_"+lab;bpy.context.object.data.materials.append(m)
 c=bpy.data.cameras.new("CAM");c.type="ORTHO";o=bpy.data.objects.new("CAM",c);bpy.context.collection.objects.link(o);o.location=(0,0,10);o.rotation_euler=(0,0,0);c.ortho_scale=max(cols*2.25,rows*2.25*1.5)*1.08;bpy.context.scene.camera=o;s=bpy.context.scene;s.render.engine="CYCLES";s.cycles.samples=a.samples;s.render.resolution_x=1800;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.render.image_settings.file_format="PNG";s.world.color=(0,0,0);O.mkdir(parents=True,exist_ok=True);(O/"renders").mkdir(exist_ok=True);(O/"blends").mkdir(exist_ok=True);s.render.filepath=str(O/"renders"/(mid+".png"));bpy.ops.wm.save_as_mainfile(filepath=str(O/"blends"/(mid+".blend")));bpy.ops.render.render(write_still=True);return {"module":mid,"labels":[x[0] for x in items],"status":"RENDERED_POST_REVIEW_REQUIRED"}
def main():
 a=A();O=Path(a.out);R={"blender":bpy.app.version_string,"build_hash":str(bpy.app.build_hash),"modules":[]}
 for mid in MODS:
  try:R["modules"].append(render(mid,B[mid](),O,a))
  except Exception as e:R["modules"].append({"module":mid,"status":"FAILED","error":repr(e),"traceback":traceback.format_exc()});R["status"]="STOPPED_"+mid+"_FAILED";(O/"MASTER_RECEIPT.json").write_text(json.dumps(R,indent=2));raise
 R["status"]="ALL_RENDERED_POST_REVIEW_REQUIRED";R["gabor"]=G;(O/"MASTER_RECEIPT.json").write_text(json.dumps(R,indent=2));print(json.dumps(R,indent=2))
main()
