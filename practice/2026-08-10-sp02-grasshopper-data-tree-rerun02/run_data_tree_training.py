"""
OLEANDER SP02 Rerun 02 — deterministic offline Data Tree specification.
Evidence boundary: NOT Rhino/Grasshopper runtime.
"""
ZONES=4; ITEMS=6; DX=2.4; DY=3.6
def pth(*idx): return "{"+";".join(map(str,idx))+"}"
def base(): return {pth(z):[{"zone":z,"item":i,"x":i*DX,"y":z*DY,"z":0.0} for i in range(ITEMS)] for z in range(ZONES)}
def graft(tree):
    out={}
    for p,vals in tree.items():
        z=int(p.strip("{}").split(";")[0])
        for i,item in enumerate(vals): out[pth(z,i)]=[item]
    return out
def flatten(tree): return {pth(0):[item for p in sorted(tree) for item in tree[p]]}
def path_mapper_A_B_to_B(grafted):
    out={}
    for p,vals in grafted.items():
        a,b=[int(x) for x in p.strip("{}").split(";")]
        out.setdefault(pth(b),[]).extend(vals)
    return out
def summary(tree): return len(tree),sum(len(v) for v in tree.values()),[len(tree[k]) for k in sorted(tree)]
if __name__=="__main__":
    b=base(); g=graft(b); f=flatten(b); t=path_mapper_A_B_to_B(g)
    assert summary(b)==(4,24,[6]*4)
    assert summary(g)==(24,24,[1]*24)
    assert summary(f)==(1,24,[24])
    assert summary(t)==(6,24,[4]*6)
    print("BASE",summary(b))
    print("GRAFT",summary(g))
    print("FLATTEN",summary(f))
    print("TRANSPOSE",summary(t))
