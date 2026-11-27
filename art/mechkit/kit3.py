# ===== AC-study kit (v3): faceted shells over a dark inner frame =====
# Structural rules (see study page): thin faceted plates with ridges and chamfers, tapered to points;
# armour shells sit on a visible dark frame (drums, pistons, struts); plates stack in shingle order.
import itertools as _it
_build_v2=build
def _orient(u,f):
    """R whose local y = u (along), local z = f (outward), local x = y cross z"""
    y=_n.array(u,float);y/=_n.linalg.norm(y);z=_n.array(f,float);z=z-y*(z@y);z/=_n.linalg.norm(z);x=_n.cross(y,z);return _n.stack([x,y,z],1)
def _hull_add(c,R,N,d,br,mat):
    add('hull',c,mat,R,N=_n.array(N,float),d=_n.array(d,float),br=br)
def hullp(pts,mat):
    """convex hull of world points -> faceted solid (brute-force planes, fine for <=16 pts)"""
    P=_n.array(pts,float);c=P.mean(0);Q=P-c;N=[];dd=[]
    for i,j,k in _it.combinations(range(len(Q)),3):
        n=_n.cross(Q[j]-Q[i],Q[k]-Q[i]);l=_n.linalg.norm(n)
        if l<1e-6:continue
        n/=l;o=n@Q[i];s=Q@n-o
        if s.max()<=1e-5:pass
        elif s.min()>=-1e-5:n,o=-n,-o
        else:continue
        if any(abs(n@m-1)<1e-6 and abs(o-q)<1e-5 for m,q in zip(N,dd)):continue
        N.append(n);dd.append(o)
    _hull_add(c,_n.eye(3),N,dd,_n.linalg.norm(Q,axis=1).max(),mat)
def plate(c,R,poly,t,mat,bev=.5,ridge=0.,bevb=None,keel=0):
    """flat convex outline (local xy, CCW) extruded +-t along local z; chamfered front edges (bev);
    ridge>0 folds the front face along local y into two facets (degrees); keel folds along local x."""
    V=_n.array(poly,float);N=[];dd=[];bevb=bev*.4 if bevb is None else bevb
    e1,e2=V[1]-V[0],V[2]-V[1]
    if e1[0]*e2[1]-e1[1]*e2[0]<0:V=V[::-1]
    for i in range(len(V)):
        a,b=V[i],V[(i+1)%len(V)];e=b-a;n=_n.array([e[1],-e[0]])/_n.linalg.norm(e);o=n@a
        N.append([n[0],n[1],0]);dd.append(o)
        for zs,bv in((1,bev),(-1,bevb)):
            if bv<=0:continue
            m=_n.array([n[0],n[1],zs]);m/=_n.linalg.norm(m);p=_n.array([*(a-n*bv),zs*t]);N.append(m);dd.append(m@p)
    N+=[[0,0,1],[0,0,-1]];dd+=[t,t]
    if ridge:
        r=D(ridge)
        for sx in(-1,1):N.append([sx*math.sin(r),0,math.cos(r)]);dd.append(math.cos(r)*t)
    if keel:
        r=D(keel)
        for sy in(-1,1):N.append([0,sy*math.sin(r),math.cos(r)]);dd.append(math.cos(r)*t)
    _hull_add(_n.array(c,float),R,N,dd,_n.linalg.norm(V,axis=1).max()+t,mat)
def drum(c,axis,r,h,mat='F'):cyl(c,r,h,mat,R=look(axis),r=min(.4,r*.3))
def strut(a,b,r=.7,mat='F'):cap(a,b,r,mat)
def _lf(knee,ank):
    sd=(knee-ank)/_n.linalg.norm(knee-ank);fw=_n.cross(V3(1,0,0),sd);fw=fw if fw[2]>0 else -fw;return sd,fw
# ---------------- shell helper: tapered faceted tube between two points ----------------
def shell(a,b,f,wa,da,wb,db,mat,fo=0.,cham=.28,front=0.):
    """faceted 8-sided section tube a->b; f=forward hint; w=half width, d=half depth at each end;
    fo shifts the section forward; front>0 pushes a ridge point out on the front face (keel line)."""
    a=_n.array(a,float);b=_n.array(b,float);u=(b-a)/_n.linalg.norm(b-a);fz=_n.array(f,float);fz=fz-u*(fz@u);fz/=_n.linalg.norm(fz);x=_n.cross(u,fz)
    pts=[]
    for c,w,d in((a,wa,da),(b,wb,db)):
        c=c+fz*fo;cw,cd=w*cham,d*cham
        for sx,sz in((1,1),(-1,1),(1,-1),(-1,-1)):
            pts.append(c+x*sx*w+fz*sz*(d-cd));pts.append(c+x*sx*(w-cw)+fz*sz*d)
        if front:pts.append(c+fz*(d+front))
    hullp(pts,mat)
# ================= LEGS =================
def legac_mid(S,L):
    """medium biped: leaf thigh guard, pointed knee shield, calf mass high on the shin tapering to a slim ankle"""
    sd,hip,knee,ank,ball,fwd=L['sd'],L['hip'],L['knee'],L['ank'],L['ball'],L['fwd'];side=sd;out=V3(side,0,0)
    sdv,fw=_lf(knee,ank);side_v=_n.cross(V3(0,1,0),fwd)
    grp('hipJ%d'%side);drum(hip,(1,0,0),2.2,2.0)
    grp('thighF%d'%side);strut(hip,knee,1.1);strut(hip+V3(0,-1,-1.8),knee+V3(0,1.4,-1.6),.45,'J')
    tu=(knee-hip)/_n.linalg.norm(knee-hip)
    grp('thigh%d'%side);shell(hip+tu*1.8,hip+tu*(_n.linalg.norm(knee-hip)*.62),V3(0,0,1),2.5,2.7,1.3,1.5,'A',fo=.4,front=.8)
    grp('thighO%d'%side);plate(hip+tu*7+out*3.4+V3(0,0,.6),_orient(tu,out+V3(0,0,.25)),[(-2.4,-5.5),(2.2,-6.5),(2.6,4),(0,7.5),(-2.2,3)],.55,'J',bev=.5,ridge=14)
    grp('knee%d'%side);drum(knee,(1,0,0),1.7,2.0)
    grp('kneeC%d'%side);plate(knee+fw*2.0+sdv*1.5,_orient(sdv,fw),[(-2,-3),(2,-3),(2.2,2.5),(0,7.5),(-2.2,2.5)],.55,'A',bev=.6,ridge=20)
    grp('kneeT%d'%side);cbox(knee+fw*3.4+sdv*.6,(1.2,.8,.5),'T',_orient(sdv,fw),ch=.3)
    grp('shinF%d'%side);strut(knee,ank,.95);strut(knee-fw*1.4+sdv*-1,ank-fw*1+sdv*1,.4,'J')
    # calf: the dominant leg mass, deep near the knee, narrowing to the ankle
    top=knee-sdv*2.5;bot=ank+sdv*2.2
    grp('shin%d'%side);shell(top,top+(bot-top)*.62,fw,2.4,3.3,.9,1.2,'A',fo=.5,front=1.0)
    grp('shinP%d'%side);plate(knee-sdv*7+fw*3.8,_orient(sdv,fw+V3(0,.0,0)),[(-1.7,-6.5),(0,-10),(1.7,-6.5),(2.2,4),(0,6),(-2.2,4)],.45,'J',bev=.45,ridge=18)
    grp('shinS%d'%side);plate(knee-sdv*5.5+out*2.9-fw*.6,_orient(sdv,out),[(-3,-5),(1,-8),(2.6,2),(0,4),(-3,2.5)],.35,'A',bev=.35,ridge=10)
    grp('shinV%d'%side);vent(knee-sdv*9+out*2.5-fw*1.2,_orient(sdv,out),1,1.6,3,.35,mat='T')
    grp('shinD%d'%side);cbox(knee-sdv*11+fw*2.4,(1,1.6,.35),'F',_orient(sdv,fw),ch=.2);bolt(knee-sdv*13.4+fw*2.9)
    grp('thighD%d'%side);cbox(hip+tu*8+V3(0,0,3.9),(.8,1.8,.3),'T',_orient(tu,V3(0,0,1)),ch=.2)
    grp('ankle%d'%side);drum(ank,side_v,1.4,1.6);strut(ank,ball+V3(0,1.2,0),1.0)
    # foot: long pointed wedge, separate heel block, toe cap plate
    toe=ball+fwd*8.5+V3(0,-1.2,0);heel=ball-fwd*5
    grp('foot%d'%side);hullp([ball+side_v*3.4+V3(0,-.4,-1),ball-side_v*3.4+V3(0,-.4,-1),ball+side_v*2.6+V3(0,2.4,0),ball-side_v*2.6+V3(0,2.4,0),
        toe+side_v*1.6+V3(0,-.2,0),toe-side_v*1.6+V3(0,-.2,0),toe+V3(0,.9,-1.5),ball+fwd*3.5+side_v*3+V3(0,-1.6,0),ball+fwd*3.5-side_v*3+V3(0,-1.6,0)],'A')
    grp('footT%d'%side);plate(ball+fwd*3+V3(0,1.7,0),_orient(fwd+V3(0,-.35,0),V3(0,1,0)+fwd*.35),[(-1.8,-2.5),(1.8,-2.5),(1.4,2.5),(0,3.8),(-1.4,2.5)],.35,'J',bev=.3,ridge=16)
    grp('heel%d'%side);hullp([heel+side_v*2.2+V3(0,-.6,0),heel-side_v*2.2+V3(0,-.6,0),heel+side_v*1.8+V3(0,2.4,1.5)*1,heel-side_v*1.8+V3(0,2.4,0)+fwd*1.5,ball+side_v*2+V3(0,-.6,0),ball-side_v*2+V3(0,-.6,0),heel-fwd*2+V3(0,0,0)],'J')
    grp('heelS%d'%side);plate(ank-fwd*2.5+V3(0,1,0),_orient(-fwd+V3(0,.8,0),V3(0,1,0)-fwd),[(-1.2,-1),(1.2,-1),(0,5)],.35,'A',bev=.3,ridge=20)
def legac_heavy(S,L):
    """heavy biped: stacked shin armour, box-faceted thigh, broad flat foot with toe and heel shoes"""
    sd,hip,knee,ank,ball,fwd=L['sd'],L['hip'],L['knee'],L['ank'],L['ball'],L['fwd'];side=sd;out=V3(side,0,0)
    sdv,fw=_lf(knee,ank);side_v=_n.cross(V3(0,1,0),fwd);tu=(knee-hip)/_n.linalg.norm(knee-hip)
    grp('hipJ%d'%side);drum(hip,(1,0,0),3.2,2.6)
    grp('thighF%d'%side);strut(hip,knee,1.6);strut(hip+V3(0,-1,-2.6),knee+V3(0,1.5,-2.2),.7,'J')
    grp('thigh%d'%side);shell(hip+tu*1.6,hip+tu*(_n.linalg.norm(knee-hip)*.7),V3(0,0,1),3.6,3.6,2.2,2.4,'A',fo=.4,front=.8)
    grp('thighO%d'%side);plate(hip+tu*5.5+out*3.6,_orient(tu,out),[(-3.4,-5),(3,-6),(3.4,4),(-3,5)],.7,'J',bev=.6,ridge=10)
    grp('knee%d'%side);drum(knee,(1,0,0),3.2,3.2)
    grp('kneeC%d'%side);plate(knee+fw*3.3+sdv*.5,_orient(sdv,fw),[(-3.6,-3.2),(3.6,-3.2),(3.8,2.6),(0,5.5),(-3.8,2.6)],.9,'J',bev=.7,ridge=16)
    top=knee-sdv*2.2;bot=ank+sdv*1.8
    grp('shinF%d'%side);strut(knee,ank,1.4)
    grp('shin%d'%side);shell(top,top+(bot-top)*.75,fw,3.6,4.2,1.8,2.2,'A',fo=.5,front=.9)
    for i,(t0,w) in enumerate(((3.5,4.6),(8.5,4.3))):
        grp('shinP%d%d'%(side,i));plate(knee-sdv*t0+fw*(5.4-i*.1),_orient(sdv,fw+sdv*.18),[(-w,-2.6),(w,-2.6),(w*.9,2.2),(0,3.2),(-w*.9,2.2)],.6,'J' if i else 'A',bev=.5,ridge=14)
    grp('shinV%d'%side);vent(knee-sdv*7.5+out*3.4,_orient(sdv,out),1.5,2.4,3,.5,mat='T')
    grp('ankle%d'%side);drum(ank,side_v,2.6,2.8)
    grp('sole%d'%side);hullp([ball+fwd*f+side_v*k*w+V3(0,y,0) for f,w in((-9.5,4.6),(11,4.8)) for k in(-1,1) for y in(-.3,1.2)]+[ball+fwd*12.4+V3(0,.4,0)],'F')
    grp('foot%d'%side);hullp([ball+side_v*4.6+V3(0,1,-5),ball-side_v*4.6+V3(0,1,-5),ball+side_v*3.6+V3(0,4.4,-3),ball-side_v*3.6+V3(0,4.4,-3),
        ball+fwd*10+side_v*4.4+V3(0,1,0),ball+fwd*10-side_v*4.4+V3(0,1,0),ball+fwd*8+side_v*3.2+V3(0,3.2,0),ball+fwd*8-side_v*3.2+V3(0,3.2,0),ball+fwd*11.6+V3(0,1.4,0)],'J')
    grp('toe%d'%side);plate(ball+fwd*7.5+V3(0,3.4,0),_orient(fwd+V3(0,-.4,0),V3(0,1,0)+fwd*.4),[(-3.4,-2.5),(3.4,-2.5),(3,2),(0,3.6),(-3,2)],.5,'A',bev=.5,ridge=14)
    grp('heel%d'%side);hullp([ball-fwd*5+side_v*3.6+V3(0,1,0),ball-fwd*5-side_v*3.6+V3(0,1,0),ball-fwd*9+side_v*2.6+V3(0,1,0),ball-fwd*9-side_v*2.6+V3(0,1,0),ball-fwd*5+V3(0,4.4,0),ball-fwd*8.5+V3(0,2.8,0)],'A')
def legac_rj(S,L):
    """reverse joint: short forward thigh, backward-folded shin to a raised hock, long metatarsus, splayed toes"""
    sd,hip,ball,fwd=L['sd'],L['hip'],L['ball'],L['fwd'];side=sd;out=V3(side,0,0);side_v=_n.cross(V3(0,1,0),fwd)
    hy=hip[1];knee=hip+V3(side*.8,-hy*.3,0)+fwd*9;hock=V3(ball[0],hy*.46,ball[2])-fwd*7
    grp('hipJ%d'%side);drum(hip,(1,0,0),2.6,2.2)
    tu=(knee-hip)/_n.linalg.norm(knee-hip)
    grp('thighF%d'%side);strut(hip,knee,1.8)
    grp('thigh%d'%side);shell(hip+tu*1.5,knee-tu*1.6,V3(0,1,.2),2.4,3.0,1.4,1.7,'A',fo=.4,front=.9)
    grp('thighO%d'%side);plate(hip+tu*4.5+out*3.3+V3(0,.5,0),_orient(tu,out),[(-2,-4),(2.6,-4.5),(2.6,3),(-1,6)],.45,'J',bev=.4,ridge=12)
    grp('knee%d'%side);drum(knee,(1,0,0),2.4,2.6)
    grp('kneeC%d'%side);plate(knee+fwd*2.2+V3(0,.6,0),_orient(V3(0,1,0)-fwd*.4,fwd),[(-2.4,-2.6),(2.4,-2.6),(2.2,2.4),(0,5.5),(-2.2,2.4)],.6,'A',bev=.5,ridge=18)
    su=(hock-knee)/_n.linalg.norm(hock-knee)
    grp('shinF%d'%side);strut(knee,hock,1.0);strut(knee+V3(0,-1.5,0),hock+V3(0,1.8,0)+fwd*1.2,.6,'J')
    grp('shin%d'%side);shell(knee+su*1.8,hock-su*2,V3(0,-1,0)+fwd*.2,2.2,2.8,.9,1.1,'A',fo=.4,front=.9)
    grp('shinB%d'%side);plate(knee+su*7+V3(0,2.6,0)-fwd*.4,_orient(su,V3(0,1,0)-fwd*.3),[(-2.2,-5),(2.2,-5),(1.6,6),(0,9),(-1.6,6)],.4,'J',bev=.4,ridge=16)
    grp('hock%d'%side);drum(hock,(1,0,0),1.9,2)
    grp('hockS%d'%side);plate(hock-fwd*2.2+V3(0,1,0),_orient(-fwd+V3(0,.6,0),-fwd+V3(0,-.6,0)),[(-1.2,-1),(1.2,-1),(0,5.5)],.4,'A',bev=.3,ridge=20)
    mu=(ball+V3(0,1,0)-hock);mu/=_n.linalg.norm(mu)
    grp('meta%d'%side);shell(hock+mu*1,ball+V3(0,1.2,0),fwd,1.1,1.4,.8,1.0,'J',front=.5)
    grp('metaP%d'%side);plate(hock+mu*5+fwd*2,_orient(mu,fwd),[(-1.6,-3),(1.6,-3),(1.4,3),(0,4.4),(-1.4,3)],.35,'A',bev=.3,ridge=18)
    grp('foot%d'%side)
    for k,a in((-1,-24),(0,0),(1,24)):
        r=D(a);d=fwd*math.cos(r)+side_v*math.sin(r);plate(ball+d*3.6+V3(0,.9,0),_orient(d,V3(0,1,0)),[(-1.1,-3.5),(1.1,-3.5),(.8,2.6),(0,4.2),(-.8,2.6)],.75,'A' if k==0 else 'J',bev=.5,ridge=16)
    grp('heel%d'%side);plate(ball-fwd*2.8+V3(0,.8,0),_orient(-fwd,V3(0,1,0)),[(-1,-1.5),(1,-1.5),(0,3)],.7,'J',bev=.4,ridge=16)
# ================= CORE =================
def coreac_layer(S,hy):
    """layered chest: wide faceted upper hull narrowing to the waist, a forward prow, V-collar plates,
    stacked abdomen segments and a rear generator block; head sits low in the collar"""
    sc=S.get('coreScale',1.)
    grp('pelvis');hullp([V3(sx*4.2,hy+2.6,sz*3.2) for sx in(-1,1) for sz in(-1,1)]+[V3(sx*2.2,hy-1.2,sz*2.2) for sx in(-1,1) for sz in(-1,1)]+[V3(0,hy+1,4.6)],'J')
    grp('crotch');plate(V3(0,hy-.5,4.6),_orient(V3(0,-1,.25),V3(0,.2,1)),[(-2.2,-3),(2.2,-3),(1.6,2),(0,4),(-1.6,2)],.6,'A',bev=.5,ridge=18)
    for sd in(-1,1):
        grp('skirt%d'%sd);plate(V3(6.6*sd,hy-2.5,5.4),_orient(V3(.2*sd,-1,.28),V3(.6*sd,0,1)),[(-3,-4),(3.2,-4.6),(3.2,3.5),(.6,11),(-2.6,3)],.55,'A',bev=.6,ridge=18)
        grp('skirtI%d'%sd);plate(V3(6.8*sd,hy-2,4.7),_orient(V3(.2*sd,-1,.28),V3(.6*sd,0,1)),[(-2.2,-3),(2.2,-3.4),(2.4,2.5),(.3,8),(-1.8,2.2)],.5,'T',bev=.3,ridge=0)
        grp('skirtS%d'%sd);plate(V3(6.6*sd,hy+.5,-1.2),_orient(V3(.2*sd,-1,0),V3(sd,0,0)),[(-2.6,-2.5),(2.4,-2.5),(2,3),(-.4,6.5),(-2.6,2.5)],.45,'J',bev=.4,ridge=12)
    grp('waist');drum(V3(0,hy+5,-.5),(0,1,0),1.7,2.4)
    for sd in(-1,1):grp('waistH%d'%sd);piston(V3(2.2*sd,hy+3,1.2),V3(2.8*sd,hy+9,2.0),.4)
    grp('abd');hullp([V3(sx*1.8,hy+6,sz*2.2+.6) for sx in(-1,1) for sz in(-1,1)]+[V3(sx*3.0,hy+9,sz*3.0+.8) for sx in(-1,1) for sz in(-1,1)]+[V3(0,hy+7.5,4.2)],'A')
    grp('abdB');plate(V3(0,hy+9,4),_orient(V3(0,1,-.15),V3(0,.1,1)),[(-2.4,-1),(2.4,-1),(3.4,1.2),(-3.4,1.2)],.5,'J',bev=.4,ridge=12)
    # main upper chest hull: wide high shoulders line, narrower bottom, prow pushed forward
    w=10*sc;y0=hy+9.5;y1=hy+18.5
    grp('chest');hullp([V3(sx*w*.36,y0,3.6) for sx in(-1,1)]+[V3(sx*w*.42,y0,-3.4) for sx in(-1,1)]+[V3(sx*w,y1-2,5) for sx in(-1,1)]+[V3(sx*w*.95,y1-1,-5.5) for sx in(-1,1)]+
        [V3(sx*w*.7,y1+.8,2.8) for sx in(-1,1)]+[V3(sx*w*.6,y1+.6,-4.5) for sx in(-1,1)]+[V3(0,y0+3.5,9.4),V3(0,y1-1.5,8.2)],'A')
    # V collar plates (horseshoe framing of the upper chest)
    for sd in(-1,1):
        grp('collar%d'%sd);plate(V3(5.2*sd,y1-2.6,6.4),_orient(V3(-.5*sd,-1,.45),V3(.35*sd,.3,1)),[(-1.8,-3.4),(2,-3.4),(2.2,2.4),(0,4.2),(-2,2.6)],.55,'J',bev=.5,ridge=16)
        grp('pec%d'%sd);plate(V3(6.0*sd,y0+4.4,6.0),_orient(V3(.3*sd,-1,.25),V3(.45*sd,-.1,1)),[(-2.4,-2.6),(2.6,-3),(2.8,2.6),(-2.6,3)],.5,'A',bev=.45,ridge=12)
        grp('chV%d'%sd);vent(V3((w-.4)*sd,y1-4.6,1.2),_orient(V3(0,1,0),V3(sd,0,.25)),1.4,2.2,4,.45,mat='T')
        grp('chT%d'%sd);cbox(V3(2.2*sd,y0+2.4,8.2),(.9,.7,.5),'T',_orient(V3(0,1,0),V3(.3*sd,0,1)),ch=.3)
    grp('prow');plate(V3(0,y0+5.5,8.8),_orient(V3(0,-1,.38),V3(0,.38,1)),[(-1.8,-4.5),(1.8,-4.5),(1.2,3.5),(0,6),(-1.2,3.5)],.6,'J',bev=.5,ridge=22)
    grp('gen');hullp([V3(sx*6,y0+1,-4) for sx in(-1,1)]+[V3(sx*7,y1,-5) for sx in(-1,1)]+[V3(sx*5,y0+2,-9) for sx in(-1,1)]+[V3(sx*5.5,y1-.5,-9.5) for sx in(-1,1)],'J')
    grp('genV');vent(V3(0,y0+5,-9.6),_orient(V3(0,1,0),V3(0,0,-1)),3.6,2.6,4,.5)
    grp('core');light(V3(-2.4,y0+1.6,7.6),.6);bolt(V3(2.6,y0+1.6,7.6))
def coreac_heavy(S,hy):
    S2=dict(S,coreScale=1.18);coreac_layer(S2,hy)
    for sd in(-1,1):
        grp('chA%d'%sd);plate(V3(9.6*sd,hy+11.5,3.4),_orient(V3(0,1,0),V3(sd,0,.5)),[(-3,-3),(3,-3),(3,3),(-3,3)],.7,'J',bev=.6,ridge=10)
# ================= HEADS =================
def headac_blade(S,hy):
    """low wedge head: pointed chin, visor slit, swept side fins"""
    y=hy+20.6-S.get('headDrop',0)
    grp('neck');strut(V3(0,y-4.5,0),V3(0,y-1,1.4),1.6)
    grp('head');hullp([V3(sx*2.4,y-1,-1.5) for sx in(-1,1)]+[V3(sx*2.8,y+1.4,-.5) for sx in(-1,1)]+[V3(sx*1.8,y+2.2,2.5) for sx in(-1,1)]+[V3(sx*2.3,y-.6,3.6) for sx in(-1,1)]+[V3(0,y-1.8,5.6),V3(0,y+.8,5.2)],'A')
    # sensor: recessed dark visor band under an overhanging brow, one thin straight slit (no 'two dot' face)
    grp('visor');cbox(V3(0,y-.2,4.9),(2.1,.6,.7),'V',ch=.25)
    grp('slit')
    cbox(V3(0,y-.12,5.62),(1.9,.15,.12),'gE',ch=.05)
    grp('brow');plate(V3(0,y+.75,5.1),_orient(V3(1,0,0),V3(0,.75,1)),[(-.5,-2.6),(.5,-2.6),(.7,0),(.5,2.6),(-.5,2.6),(-.7,0)],.3,'A',bev=.25)
    for sd in(-1,1):grp('fin%d'%sd);plate(V3(2.9*sd,y+1.2,-.6),_orient(V3(.35*sd,.4,-1),V3(sd,0,0)),[(-.8,-1.5),(1,-1.5),(0,5)],.25,'J',bev=.2,ridge=14)
    grp('ant');strut(V3(-1,y+2,-.5),V3(-1.6,y+7,-2.5),.25)
def headac_hood(S,hy):
    """sensor-cluster head under a pointed hood plate"""
    y=hy+20.2-S.get('headDrop',0)
    grp('neck');strut(V3(0,y-3.5,0),V3(0,y-1,1),1.6)
    grp('head');shell(V3(0,y,-1.5),V3(0,y-.3,3.2),V3(0,1,0),2.4,2.0,2.0,1.6,'J')
    grp('hood');plate(V3(0,y+1.8,1.6),_orient(V3(0,0,1),V3(0,1,.15)),[(-2.8,-3.5),(2.8,-3.5),(2.2,2.5),(0,5),(-2.2,2.5)],.45,'A',bev=.4,ridge=24)
    # camera-style sensor cluster: one main lens with a small recessed glow, two dark secondary lenses
    grp('lens');drum(V3(.7,y-.3,3.3),(0,0,1),1.05,.6,'J');drum(V3(.7,y-.3,3.7),(0,0,1),.75,.4,'V');light(V3(.7,y-.3,3.95),.28,'gE')
    grp('lens2');drum(V3(-1.2,y+.1,3.3),(0,0,1),.5,.4,'V');drum(V3(-1.3,y-.9,3.2),(0,0,1),.38,.35,'V')
    grp('ant');strut(V3(2,y+2,-1),V3(3,y+7,-2.5),.25);strut(V3(-2,y+2,-1),V3(-2.6,y+5.5,-2),.25)
def headac_hawk(S,hy):
    """hawk head: hood sweeps forward into a beak point that overhangs a recessed dark face;
    a V cluster of four small slanted slit sensors under the hood; swept crest and back-raked cheeks"""
    k=S.get('headScale',1.);y=hy+22.2-S.get('headDrop',0);P=lambda x,yy,z:V3(x*k,y+yy*k,z*k+.8)
    grp('neck');strut(V3(0,y-6,0),V3(0,y-1,1.4),1.4)
    grp('head');hullp([P(-2.3,1.3,-2.6),P(2.3,1.3,-2.6),P(0,2.5,-.6),P(-2.7,.4,.6),P(2.7,.4,.6),P(-1.5,.9,3.6),P(1.5,.9,3.6),
        P(0,-.5,7.6),P(-1.2,-.55,4.6),P(1.2,-.55,4.6),P(-2.2,-.6,-1.8),P(2.2,-.6,-1.8)],'A')
    grp('face');hullp([P(-1.6,-.4,.8),P(1.6,-.4,.8),P(-1.3,-.6,3.9),P(1.3,-.6,3.9),P(-1.4,-2,.6),P(1.4,-2,.6),P(0,-2.6,3.6),P(0,-1.8,4.4)],'V')
    grp('sens')
    for sx,yy,z,r in((-.75,-.95,4.0,24),(.75,-.95,4.0,-24),(-.55,-1.75,3.55,-18),(.55,-1.75,3.55,18)):
        cbox(P(sx,yy,z),(.42*k,.1*k,.1*k),'gE',rotm(0,0,D(r)),ch=.04)
    for sd in(-1,1):
        grp('cheek%d'%sd);plate(P(2.3*sd,-.6,1.2),_orient(V3(.25*sd,.15,-1),V3(sd,-.3,.2)),[(-.9,-1.6),(.9,-1.6),(0,4.2)],.22,'J',bev=.18,ridge=14)
    grp('crest');plate(P(0,2.6,-2),_orient(V3(0,.55,-1),V3(1,0,0)),[(-.7,-1.5),(.7,-1.5),(.3,2),(0,4.5),(-.3,2)],.22,'J',bev=.15,ridge=10)
def headac_raptor(S,hy):
    """raptor head: narrow hooked beak, twin swept crest blades, chin spike, paired slanted slit sensors"""
    k=S.get('headScale',1.);y=hy+22.2-S.get('headDrop',0);P=lambda x,yy,z:V3(x*k,y+yy*k,z*k+.8)
    grp('neck');strut(V3(0,y-6,0),V3(0,y-1,1.4),1.3)
    grp('head');hullp([P(-1.9,1,-2.4),P(1.9,1,-2.4),P(0,2.2,-.4),P(-2.1,.3,1),P(2.1,.3,1),P(-1.1,.7,3.6),P(1.1,.7,3.6),
        P(0,-1.3,6.4),P(0,.1,5.6),P(-.9,-.6,4.2),P(.9,-.6,4.2),P(-1.8,-.7,-1.6),P(1.8,-.7,-1.6)],'A')
    grp('face');hullp([P(-1.3,-.5,.8),P(1.3,-.5,.8),P(-1,-.7,3.7),P(1,-.7,3.7),P(-1.1,-1.9,.6),P(1.1,-1.9,.6),P(0,-2.2,3.2)],'V')
    grp('chin');plate(P(0,-2.2,2.2),_orient(V3(0,-.5,1),V3(0,-1,-.4)),[(-.6,-1),(.6,-1),(0,2.4)],.25,'J',bev=.15,ridge=16)
    grp('sens')
    for sd in(-1,1):
        cbox(P(.62*sd,-.95,3.75),(.5*k,.1*k,.1*k),'gE',rotm(0,0,D(-28*sd)),ch=.04)
        cbox(P(.5*sd,-1.55,3.5),(.28*k,.09*k,.09*k),'gE',rotm(0,0,D(-28*sd)),ch=.04)
    for sd in(-1,1):
        grp('crest%d'%sd);plate(P(.9*sd,2.0,-1.4),_orient(V3(.3*sd,.5,-1),V3(sd,.4,0)),[(-.6,-1.4),(.6,-1.4),(.2,2.4),(0,5),(-.2,2.4)],.2,'J',bev=.15,ridge=12)
# ================= ARMS (shoulder unit + arm) =================
def armac_kite(S,A):
    """kite pauldron: faceted hull flaring up and out to a point, top fin plate, lower lip; slim frame upper arm; boxy tapered forearm"""
    sd,sh,el,ha=A['sd'],A['sh'],A['el'],A['ha'];hy=A['hy'];o=V3(sd,0,0)
    c=V3(13*sd,hy+16.5,0)
    grp('shJ%d'%sd);drum(V3(10.8*sd,hy+15,0),(1,0,0),2.8,2.4)
    grp('paul%d'%sd);hullp([c+V3(-3.2*sd,3,-4.5),c+V3(-3.2*sd,3,4),c+V3(3.4*sd,4.2,-3),c+V3(3.4*sd,4,3),c+V3(6.6*sd,6.4,-1),
        c+V3(-3*sd,-3.6,-4.2),c+V3(-3*sd,-3.6,4.2),c+V3(4*sd,-2.8,-3.6),c+V3(4*sd,-2.8,3.6),c+V3(2*sd,0,6),c+V3(5.4*sd,1.6,0)],'A')
    grp('paulT%d'%sd);plate(c+V3(1.4*sd,5,.4),_orient(V3(sd,.55,0),V3(-.4*sd,1,.1)),[(-2.6,-3.4),(2.6,-3.4),(2,3),(0,5.5),(-2.4,3)],.45,'J',bev=.4,ridge=14)
    grp('paulL%d'%sd);plate(c+V3(2.6*sd,-3.8,.4),_orient(V3(.3*sd,-1,0),V3(sd,-.2,.3)),[(-3.2,-1.6),(3.2,-1.6),(2.4,1.6),(-2.4,1.6),(0,-3.4)],.4,'J',bev=.35,ridge=12)
    grp('paulG%d'%sd);cbox(c+V3(3*sd,1.2,5.2),(1.2,.6,.4),'T',_orient(V3(sd,.3,0),V3(0,0,1)),ch=.25);vent(c+V3(5.2*sd,.4,0),_orient(V3(0,1,0),V3(sd,.3,0)),1.4,1.3,3,.35,mat='T')
    grp('ua%d'%sd);strut(sh,el,1.0);piston(sh+V3(0,-1.2,-1.2),el+V3(0,.5,-1.2),.35)
    u,s,f=frame_at(sh,el);grp('uaP%d'%sd);plate((sh+el)/2+s*sd*1.9,_orient(u,s*sd),[(-1.6,-3),(1.6,-3),(1.4,3),(-1.4,3)],.35,'J',bev=.3,ridge=12)
    grp('elb%d'%sd);drum(el,s,1.4,1.6)
    u,s,f=frame_at(el,ha)
    grp('fa%d'%sd);shell(el+u*.6,ha-u*1.6,f,2.0,2.3,1.1,1.3,'A',front=.6)
    grp('faP%d'%sd);plate(el+u*3.4+s*sd*2.0,_orient(u,s*sd),[(-1.8,-4),(1.8,-3.2),(1.6,3),(0,4.4),(-1.6,3)],.4,'J',bev=.35,ridge=14)
    grp('hand%d'%sd);hullp([ha+u*-.6+s*1.4+f*1.4,ha+u*-.6-s*1.4+f*1.4,ha+u*-.6+s*1.4-f*1.4,ha+u*-.6-s*1.4-f*1.4,ha+u*2+s*1.2+f*1.6,ha+u*2-s*1.2+f*1.6,ha+u*2.4+s*1.1-f*1,ha+u*2.4-s*1.1-f*1],'F')
def armac_heavy(S,A):
    """heavy: stacked rectangular pauldron (3 shingles), thick faceted forearm with outer shield"""
    sd,sh,el,ha=A['sd'],A['sh'],A['el'],A['ha'];hy=A['hy']
    c=V3(13.6*sd,hy+16.5,0)
    grp('shJ%d'%sd);drum(V3(11*sd,hy+15,0),(1,0,0),3.2,2.6)
    grp('paul%d'%sd);shell(c+V3(0,4.2,0),c+V3(.4*sd,-4,0),V3(0,0,1),4.6,5.6,4.0,5.0,'A',front=.8)
    for i in range(3):
        grp('paulS%d%d'%(sd,i));plate(c+V3((4.9+i*.35)*sd,3.4-i*3.0,0),_orient(V3(.12*sd,-1,0),V3(sd,.25,0)),[(-5.4,-1.9),(5.4,-1.9),(5,1.4),(-5,1.4)],.45,'J' if i==1 else 'A',bev=.4,ridge=8)
    grp('paulT%d'%sd);plate(c+V3(.4*sd,5.4,0),_orient(V3(0,0,1),V3(.15*sd,1,0)),[(-4,-5.6),(4,-5.6),(4,4.6),(0,6.6),(-4,4.6)],.5,'J',bev=.5,ridge=10)
    grp('paulG%d'%sd);cbox(c+V3(1.6*sd,0,5.4),(1.6,2.4,.5),'T',ch=.3)
    grp('ua%d'%sd);strut(sh,el,1.4);piston(sh+V3(0,-1.6,-1.6),el+V3(0,.5,-1.6),.5)
    u,s,f=frame_at(sh,el)
    grp('elb%d'%sd);drum(el,s,2.4,2.4)
    u,s,f=frame_at(el,ha)
    grp('fa%d'%sd);shell(el+u*.6,ha-u*1.6,f,2.8,3.0,1.6,1.8,'A',front=.7)
    grp('faP%d'%sd);plate(el+u*4+s*sd*2.9,_orient(u,s*sd),[(-2.6,-4.6),(2.6,-4.6),(2.4,3.6),(0,5.4),(-2.4,3.6)],.5,'J',bev=.45,ridge=12)
    grp('faV%d'%sd);vent(el+u*4.5+f*2.9,_orient(u,f),1.6,1.8,3,.45,mat='T')
    grp('hand%d'%sd);hullp([ha+u*-.6+s*1.8+f*1.8,ha+u*-.6-s*1.8+f*1.8,ha+u*-.6+s*1.8-f*1.8,ha+u*-.6-s*1.8-f*1.8,ha+u*2.4+s*1.5+f*1.8,ha+u*2.4-s*1.5+f*1.8,ha+u*2.8+s*1.4-f*1.2,ha+u*2.8-s*1.4-f*1.2],'F')
# ================= BACK =================
def backac_pylons(S,hy):
    """two long tapered blade pylons on drum mounts, angled up and out"""
    for sd in(-1,1):
        m=V3(6*sd,hy+17,-7.5)
        grp('pyM%d'%sd);drum(m,(1,0,0),1.8,1.8);strut(V3(3*sd,hy+15,-6),m,1)
        d=V3(.45*sd,1,-.4);d/=_n.linalg.norm(d)
        grp('py%d'%sd);shell(m-d*2,m+d*15,V3(sd,0,.3),1.5,1.9,.4,.6,'J',front=.6)
        grp('pyP%d'%sd);plate(m+d*5.5+V3(sd,0,.3)*1.8,_orient(d,V3(sd,0,.3)),[(-1.4,-5),(1.4,-5),(1,4),(0,7),(-1,4)],.35,'A',bev=.3,ridge=16)
        grp('pyT%d'%sd);plate(m+d*12.5+V3(sd,0,.3)*.9,_orient(d,V3(sd,0,.3)),[(-1,-2),(1,-2),(0,3)],.4,'T',bev=.3,ridge=16)
def backac_pods(S,hy):
    """angular missile pods on arms: faceted box, slanted face with cell grid"""
    for sd in(-1,1):
        c=V3(7.8*sd,hy+23,-6.5);R=_orient(V3(0,1,-.45),V3(0,.45,1))
        grp('podA%d'%sd);strut(V3(3.5*sd,hy+16,-6),c+V3(0,-2,0),1.1)
        grp('pod%d'%sd);shell(c-R[:,1]*4.5,c+R[:,1]*4.5,R[:,2],3.4,3.0,3.0,2.4,'A',front=.0)
        grp('podF%d'%sd);cbox(c+R[:,2]*2.6+R[:,1]*1,(2.6,2.6,.4),'V',R,ch=.2)
        for i in(-1,0,1):
            for j in(-1,1):cbox(c+R[:,2]*2.9+R[:,1]*(1+j*1.2)+R[:,0]*i*1.6,(.55,.45,.3),'N',R,ch=.15)
        grp('podT%d'%sd);cbox(c+R[:,0]*3.5*sd,(.3,2.2,1.6),'T',R,ch=.15)
SLOTS3=dict(legs=dict(mid=legac_mid,heavy=legac_heavy,rj=legac_rj),core=dict(layer=coreac_layer,heavy=coreac_heavy),
 head=dict(blade=headac_blade,hood=headac_hood,hawk=headac_hawk,raptor=headac_raptor),arms=dict(kite=armac_kite,heavy=armac_heavy),
 back=dict(pylons=backac_pylons,pods=backac_pods,none=lambda S,hy:None),weapon=SLOTS['weapon'])
def build_ac(S):
    PR.clear();P=S['pose'];hy=P['hipY'];L1,L2=P.get('thigh',15),P.get('shin',14);sl=S['ac']
    for side,leg in((-1,P['near']),(1,P['far'])):
        sx=P.get('hipW',7)*side;hip=V3(sx,hy,leg.get('hipZ',0));ball=V3(*leg['ball'])
        fa=D(leg.get('footYaw',0));fwd=V3(math.sin(fa),0,math.cos(fa))
        ank=ball+V3(0,P.get('ankH',6),0)-fwd*P.get('ankBack',1.5)
        if P.get('matchKnees',True):
            # both knees share one pose: thigh hangs nearly straight under the hip, knee points forward;
            # only the shin swings to reach each staggered, spread foot
            zc=(P['near']['ball'][2]+P['far']['ball'][2])/2;dz=P.get('kneeFwd',0)
            kn=ik2(V3(0,hy,0),V3(0,ank[1],zc-P.get('ankBack',1.5)),L1,L2,V3(0,0,1))
            # the knee follows its own foot forward/back (same bend, shifted), so a back foot doesn't over-rake its shin
            kf=P.get('kneeFollow',1.0)*(ank[2]-(zc-P.get('ankBack',1.5)))
            knee=hip+V3(side*P.get('kneeOut',1.0),kn[1]-hy,kn[2]+dz+kf)
        else:knee=ik2(hip,ank,L1,L2,V3(*leg.get('bend',(sx*.2,0,1))))
        SLOTS3['legs'][sl['legs']](S,dict(sd=side,hip=hip,knee=knee,ank=ank,ball=ball,fwd=fwd))
    n0=len(PR)
    SLOTS3['core'][sl['core']](S,hy);h0=len(PR);SLOTS3['head'][sl['head']](S,hy)
    xform(PR[h0:],(0,hy+16,0),rotm(0,-D(P.get('lean',0))*S.get('headLevel',.75)))   # head counter-pitches to keep looking ahead
    SLOTS3['back'][sl['back']](S,hy)
    for sd,arm in((-1,P['armN']),(1,P['armF'])):
        sh=V3(11.5*sd,hy+14,0);el=sh+V3(*arm['elbow']);ha=sh+V3(*arm['hand'])
        SLOTS3['arms'][sl['arms']](S,dict(sd=sd,sh=sh,el=el,ha=ha,hy=hy))
        if arm.get('weapon'):
            d=V3(*arm.get('aim',(0,-.4,1)));d/=_n.linalg.norm(d);SLOTS3['weapon'][arm['weapon'] if isinstance(arm['weapon'],str) else sl['weapon']](S,ha,d,sd)
    R=rotm(D(P.get('twist',0)),D(P.get('lean',0)),D(P.get('roll',0)))
    xform(PR[n0:],(0,hy+5,-1),R)
def build(S):
    if 'ac' in S:return build_ac(S)
    return _build_v2(S)
