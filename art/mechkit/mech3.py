#!/usr/bin/env python3
"""(AC-study copy) Render a Scrapline mech spec (JSON) to pixel sprites: python3 mech.py spec.json outdir"""
import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import r3d
from r3d import *
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'kit.py')).read(),r3d.__dict__)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'kit2.py')).read(),r3d.__dict__)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'kit3.py')).read(),r3d.__dict__)
from PIL import Image
HEX=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
RAMPS={'cream':['#231c19','#373330','#665e59','#a49a93','#e4d7cf'],
 'brown':['#211512','#352523','#553d3a','#66544e','#8c766f'],
 'dark':['#0b0705','#211512','#231c19','#40332f','#665e59'],
 'navy':['#0b0705','#121820','#1c242f','#333942','#665e59'],
 'gun':['#0b0705','#211512','#40332f','#553d3a','#66544e'],
 'void':['#0b0705','#0b0705','#121820','#1c242f','#333942'],
 'olive':['#14160c','#2b2f18','#4c5228','#7d8441','#b9bf72'],
 'rust':['#1a0c08','#3d1a10','#6e3420','#a85a32','#e0955a'],
 'steel':['#0e1116','#232a33','#3e4955','#6b7a89','#b3c2cf'],
 'gunmetal':['#0d0e12','#1f2128','#363942','#5a5e69','#9ca0ac'],
 'gunframe':['#08090c','#15161b','#25272e','#3d4049','#6a6e79'],
 'gundark':['#060709','#0d0e12','#16171c','#262830','#3e414a'],
 'gold':['#2a1d0c','#5c421c','#9a7638','#d4ae66','#f6e1a4'],
 'crimson':['#1a0608','#3e0d12','#6e1a1f','#a8333a','#e46a5e']}
BIAS={'F':-.12,'N':-.08,'V':-.3,'W':-.1}
def sprite(S,yaw,W=73,H=None,ox=None,oy=None,ss=4,bg=True):
    H=H or S.get('H',74);oy=oy or H-3
    r3d.build(S);ox=S.get('ox',27) if ox is None else ox
    res=render(W,H,ss,D(yaw),D(S.get('camPitch',14)),ox,oy,S.get('L',(-.6,.45,.7)),(.8,.5,-.5),S.get('scale',1.))
    roles=dict(A='cream',J='brown',F='dark',W='gun',N='navy',V='void',T='gold');roles.update(S.get('ramps',{}))
    glow={'gE':S.get('eye',['#a46007','#f89a20']),'gL':S.get('light',['#1a89e7','#53b6f5'])};glow['gK']=RAMPS[roles['T']][2:4]
    mats=[p['mat'] for p in r3d.PR];grps=[p['grp'] for p in r3d.PR];Gs=sorted(set(grps))
    n=np.nan_to_num
    v=0.08+0.8*n(res['diff'])*(.5+.5*n(res['ao']))+0.14*n(res['ao'])+0.6*n(res['rim'])+0.6*n(res['spec'])
    hit=res['hit'];mi=n(res['mat'],nan=-1).astype(int);dep=res['depth'];ao=n(res['ao'],nan=1)
    TH=[.15,.28,.45,.66]
    LV=np.full((H,W),-1);MT=np.full((H,W),'',object);gid=np.full((H,W),-1);pd=np.full((H,W),999.)
    for y in range(H):
        for x in range(W):
            b=(slice(y*ss,y*ss+ss),slice(x*ss,x*ss+ss));h=hit[b]
            if h.sum()<ss*ss*.45:continue
            ms=mi[b][h];gl=[i for i in np.unique(ms) if mats[i].startswith('g')]
            if gl:MT[y,x]=mats[gl[0]];LV[y,x]=1 if (ms==gl[0]).sum()<ss*ss*.3 else 2;gid[y,x]=Gs.index(grps[gl[0]]);pd[y,x]=dep[b][h].min();continue
            u,c=np.unique(ms,return_counts=True);m=u[c.argmax()];sel=ms==m
            val=v[b][h][sel].mean()+BIAS.get(mats[m],0)+S.get('lift',0);lvl=sum(val>t for t in TH)
            if ao[b][h][sel].mean()<.42:lvl=0
            LV[y,x]=lvl;MT[y,x]=mats[m];gid[y,x]=Gs.index(grps[m]);pd[y,x]=dep[b][h][sel].mean()
    cov=LV>=0
    # cleanup: lone pixels take the majority level of same-material neighbours
    for it in range(2):
        L2=LV.copy()
        for y in range(1,H-1):
            for x in range(1,W-1):
                if not cov[y,x] or MT[y,x].startswith('g'):continue
                nb=[(LV[y+dy,x+dx]) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if MT[y+dy,x+dx]==MT[y,x] and gid[y+dy,x+dx]==gid[y,x]]
                if len(nb)>=3 and all(q!=LV[y,x] for q in nb):
                    vals,cn=np.unique(nb,return_counts=True)
                    if cn.max()>=3:L2[y,x]=vals[cn.argmax()]
        LV=L2
    if S.get('wear',0):
        for y in range(H):
            for x in range(W):
                if MT[y,x]=='A' and LV[y,x] in(2,3) and ((x*73856093)^(y*19349663))%997/997<S['wear']:LV[y,x]+=1
    col=lambda y,x,l:HEX(glow[MT[y,x]][min(l,1)]) if MT[y,x].startswith('g') else HEX(RAMPS[roles[MT[y,x]]][max(0,min(4,l))])
    img=np.zeros((H,W,4),np.uint8)
    O=HEX('#0b0705')+(255,)
    for y in range(H):
        for x in range(W):
            if not cov[y,x]:continue
            l=LV[y,x]
            if MT[y,x] in('A','J','W','T') and l>=1:   # lit edges catch a highlight
                up=y>0 and ((not cov[y-1,x]) or (gid[y-1,x]!=gid[y,x] and pd[y-1,x]>pd[y,x]+.4))
                lf=x>0 and ((not cov[y,x-1]) or (gid[y,x-1]!=gid[y,x] and pd[y,x-1]>pd[y,x]+.4))
                if up or lf:l+=1
            img[y,x]=col(y,x,l)+(255,)
            if S.get('seams',True) and not MT[y,x].startswith('g'):
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):   # dark seam on the farther part
                    X,Y=x+dx,y+dy
                    if 0<=X<W and 0<=Y<H and cov[Y,X] and gid[Y,X]!=gid[y,x] and pd[y,x]>pd[Y,X]+.4:img[y,x]=O;break
    for y in range(H):
        for x in range(W):
            if not cov[y,x] and any(0<=x+dx<W and 0<=y+dy<H and cov[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):img[y,x]=O
    im=Image.fromarray(img,'RGBA')
    if bg:
        b=Image.new('RGBA',(W,H),HEX('#4b4b4b')+(255,));b.paste(Image.new('RGBA',(W,H-oy),HEX('#9f9f9f')+(255,)),(0,oy));b.alpha_composite(im);im=b
    return im
def clay(S,yaw,W=200,H=190,scale=2.4,ox=None,oy=None,pitch=12):
    """smooth high-res grey render for judging 3D form"""
    r3d.build(S);ox=W//2 if ox is None else ox;oy=oy or H-6
    res=render(W,H,2,D(yaw),D(pitch),ox,oy,S.get('L',(-.6,.45,.7)),(.8,.5,-.5),scale)
    n=np.nan_to_num;mats=[p['mat'] for p in r3d.PR];mi=n(res['mat'],nan=0).astype(int)
    base={'A':.95,'J':.62,'F':.38,'W':.5,'N':.45,'V':.2,'T':1.0}
    tint=np.ones(res['hit'].shape+(3,))
    for i,m in enumerate(mats):
        sel=mi==i
        if m=='T':tint[sel]=(1.15,.95,.6)
        elif m.startswith('g'):tint[sel]=(1.6,.5,.4) if m=='gE' else ((1.1,.8,.4) if m=='gK' else (.6,1.,1.6))
        tint[sel]*=base.get(m,1.)
    v=0.06+0.75*n(res['diff'])*(.45+.55*n(res['ao']))+.12*n(res['ao'])+.45*n(res['rim'])+.5*n(res['spec'])
    img=np.clip(v[...,None]*tint,0,1)*255
    img[~res['hit']]=(34,38,48)
    from PIL import Image as I
    return I.fromarray(img.astype(np.uint8)).resize((W*2,H*2),I.BILINEAR) if False else I.fromarray(img.astype(np.uint8)).resize((W,H),I.LANCZOS)

if __name__=='__main__':
    S=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
    what=sys.argv[3] if len(sys.argv)>3 else 'all'
    if what in('all','main'):sprite(S,S.get('yaw',50),W=S.get('W',73)).save(f'{out}/main.png')
    if what=='clay1':clay(S,S.get('yaw',30),W=300,H=290,scale=3.6).save(f'{out}/clay0.png')
    if what=='clay':
        for k,yw in enumerate(S.get('clayYaws',[S.get('yaw',30),40,90])):clay(S,yw,W=300,H=290,scale=3.6).save(f'{out}/clay{k}.png')
    if what.startswith('t'):
        i=int(what[1:]);sprite(S,S.get('yaw',50)+i*45,W=S.get('W',96),ox=S.get('W',96)//2,oy=(S.get('H',74)-3)).save(f'{out}/t{i}.png')
