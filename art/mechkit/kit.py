# Scrapline mech kit: parts are functions of a spec. Roles: A armour, J limbs, F frame, W weapon, N accent, V void, gE eye glow, gL light glow
import numpy as _n
G='x'
def grp(g):
    global G;G=g
_add=add
def add(kind,c,mat,R=None,**k):_add(kind,c,mat,R,grp=G,**k)
V3=lambda *a:_n.array(a,float)
# ---------------- legs ----------------
def legs_heavy(S):
    hipY=S.get('hipY',25)
    for side,sx,zb in((-1,-8.5,4),(1,10,-6)):
        hip=V3(sx*.9,hipY,zb);knee=V3(sx*1.1,hipY*.62,zb+5.5);ank=V3(sx*1.15,5.5,zb+1)
        grp('thigh%d'%side);ctube(hip,knee,(4.2,4.4),'A',ch=1.6,tt=.7)
        grp('thighP%d'%side);ctube(hip+(knee-hip)*.45+V3(0,0,1.6),knee+V3(0,1,1.8),(3.6,3.4),'A',ch=1.2,tt=.6)
        grp('knee%d'%side);sph(knee,3.2,'F');cbox(knee+V3(0,.6,3),(3.2,2.8,1.4),'J',ch=1)
        grp('shin%d'%side);ctube(knee+V3(0,-1,0),ank,(4.8,4.6),'A',ch=1.7,tb=1,tt=.7)
        grp('shinP%d'%side);ctube(knee+V3(0,-1.5,2),knee+(ank-knee)*.55+V3(0,0,2.2),(4,3.4),'A',ch=1.2,tt=.75)
        cbox(ank+V3(0,3.5,4.2),(3.4,2.2,.8),'F',ch=.4)
        grp('foot%d'%side)
        cbox(ank+V3(0,-1,0),(5,1.5,5.5),'F',ch=.8)
        cbox(V3(ank[0],1.9,ank[2]+1.5),(6,1.9,8.5),'J',ch=1.2,tt=.85)
        cbox(V3(ank[0],1.3,ank[2]+10.5),(5.4,1.3,1.6),'F',ch=.6)
def legs_light(S):
    hipY=S.get('hipY',27)
    for side,sx,zb in((-1,-7,3),(1,8,-4)):
        hip=V3(sx*.9,hipY,zb);knee=V3(sx*1.05,hipY*.58,zb+6.5);ank=V3(sx*1.1,4.5,zb-1)
        grp('thigh%d'%side);ctube(hip,knee,(3,3.4),'A',ch=1,tt=.7)
        grp('knee%d'%side);sph(knee,2.2,'F');ctube(knee+V3(0,2,1.5),knee+V3(0,-2,3.5),(2,1),'A',ch=.6,tt=.5)
        grp('shin%d'%side);ctube(knee,ank,(2.8,3.2),'J',ch=.8,tt=.75)
        ctube(knee+V3(0,-2,1.8),ank+V3(0,3,1.5),(2.4,1),'A',ch=.5,tt=.6)
        grp('foot%d'%side);cbox(V3(ank[0],1.5,ank[2]+2),(3.6,1.5,6.5),'F',ch=.8,tt=.6)
def hips(S):
    grp('hip');cbox(V3(0,S.get('hipY',25)-1,-1),(8,5,5.5),'F',ch=1.4)
    cyl(V3(0,S.get('hipY',25)+5,-1),5.2,3,'J',R=look((0,1,0)),r=.6)
# ---------------- torso ----------------
def torso_hunch(S):
    Rt=rotm(0,D(S.get('pitch',36)))
    grp('torsoF');cbox(V3(0,38,-2),(8,7.5,6),'F',Rt,ch=1.5)
    grp('torso');cbox(V3(0,40,3),(7.5,6.5,5),'A',Rt,ch=2.4,tt=.7)
    grp('torsoK');cbox(V3(0,41,7.2),(1.2,5.5,1.4),'A',Rt,ch=.8)
    grp('chestS');cbox(V3(0,43.5,5),(5.5,1,3.5),'A',Rt,ch=.6,tt=.7)
    grp('chestL');cbox(V3(-4,35.5,7.5),(4,3,2.5),'A',rotm(D(-15),D(30)),ch=1.2,tt=.7)
    grp('core');cbox(V3(2.5,35,8.5),(3.2,3,2.2),'F',Rt,ch=.9)
    sph(V3(3.5,35.6,10.6),.9,'gE');sph(V3(5,34.4,10),.7,'gE')
    grp('neck');cap((0,43,4),(0,45,9),2,'F')
def torso_slim(S):
    Rt=rotm(0,D(S.get('pitch',12)))
    grp('torsoF');cbox(V3(0,37,-1),(6,7,4.5),'F',Rt,ch=1.2)
    grp('torso');cbox(V3(0,40,2),(6.5,5,4.5),'A',Rt,ch=2,tt=.6)
    grp('chestL');cbox(V3(0,34.5,3),(4.5,2.5,3.5),'J',Rt,ch=1,tt=.8)
    grp('core');sph(V3(-2.5,40,6.4),.8,'gL')
    grp('neck');cap((0,43,1),(0,45,3),1.6,'F')
# ---------------- heads ----------------
def head_horned(S):
    grp('head');cbox(V3(0,47,10.5),(3.8,3.3,5),'A',rotm(0,D(12)),ch=1.4,tt=.75)
    grp('brow');ctube((0,48.5,12),(0,46,17.5),(3,1.5),'A',ch=.8,tt=.5)
    grp('visor');cbox(V3(0,44.6,14.6),(3.2,1.4,2),'V',ch=.5)
    sph(V3(2.2,45,16.4),1,'gE')
    grp('horn');cap((0,49,8),(0,57,3),1.6,'A',rb=.25)
def head_visor(S):
    grp('head');cbox(V3(0,47.5,4),(3.2,3,4.2),'A',ch=1.2,tt=.55)
    grp('visor');cbox(V3(0,47.3,7.6),(2.6,.9,.8),'V',ch=.3);sph(V3(0,47.3,8.4),.9,'gE')
    grp('fin');ctube((0,50,2),(0,52,-5),(.6,1.6),'A',ch=.3,tt=.3)
# ---------------- shoulders ----------------
def shoulders_heavy(S):
    Rp=rotm(D(-10),D(18),D(-24))
    grp('pauldN');cbox(V3(-12.5,46,1.5),(4.5,3.4,6.5),'A',Rp,ch=2,tt=.6)
    grp('pauldNt');cbox(V3(-11.5,48.6,1),(3.4,1.2,5.2),'A',Rp,ch=1,tt=.6)
    grp('pauldN2');cbox(V3(-14.6,41.2,2.5),(3.6,2.4,5.6),'A',Rp,ch=1.2,tt=.8)
    grp('pauldNd');cbox(V3(-11,42,-3),(3,3,3),'F',Rp,ch=.8)
    Rf=rotm(0,0,D(12))
    grp('pauldF');cbox(V3(12.5,43,-1),(4.2,5,5.6),'F',Rf,ch=1.4)
    cbox(V3(14,46.5,3),(3,1.4,2.6),'J',Rf,ch=.6)
def shoulders_light(S):
    grp('pauldN');cbox(V3(-9.5,45,1),(3,2.6,4.5),'A',rotm(0,D(8),D(-30)),ch=1.2,tt=.6)
    grp('pauldF');cbox(V3(9.5,45,1),(3,2.6,4.5),'A',rotm(0,D(8),D(30)),ch=1.2,tt=.6)
# ---------------- arms + weapons ----------------
def arm_near_rifle(S):
    grp('armN');cap((-15,40,1),(-24,32,-1),2.4,'J')
    grp('foreN');ctube((-24,32,-1),(-28,22,1),(3.2,3),'J',ch=1.3,tt=.65)
    grp('foreA');ctube((-27,31,-1),(-30.5,24,.8),(.9,2.2),'A',ch=.4,tt=.6)
    grp('rifle');ctube((-27,22,4),(-34,25,-10),(1,1.4),'F',ch=.4)
    ctube((-28,22,2),(-28,18,2.5),(.8,1),'F',ch=.3)
def arm_far_cannon(S):
    grp('armF');cap((14,40,1),(16,32,3),2.6,'J');cap((16,32,3),(13.5,27,9),2.4,'J')
    ca=V3(12,33,-5);cb=V3(15,6,36);cd=(cb-ca)/_n.linalg.norm(cb-ca)
    grp('cannon');ctube(ca,cb,(2.8,2.8),'W',ch=1.3,tt=.8)
    grp('housing');ctube(ca+cd*13,ca+cd*24,(4,4),'N',ch=1.2)
    for t in(15,18,21):grp('rib%d'%t);ctube(ca+cd*t,ca+cd*(t+1),(4.3,4.3),'N',ch=1.3)
    sph(ca+cd*24.5+V3(-1.5,3.6,2),.8,'gL')
    grp('muzzle');cyl(cb+cd*1.5,2.2,3.5,'N',R=look(cd),r=.4);sph(ca+cd*33+V3(-1.5,3,1),.7,'gL')
def arms_rifle_pair(S):
    for sd in(-1,1):
        x=10.5*sd
        grp('arm%d'%sd);cap((x,42,1),(x*1.15,34,4),1.9,'J')
        grp('fore%d'%sd);ctube((x*1.15,34,4),(x*1.05,28,10),(2.2,2.4),'A',ch=.8,tt=.7)
    grp('rifle');ctube((10,29,6),(9,30,26),(1,1.5),'W',ch=.5);ctube((10,27.5,10),(10,25,10.5),(.7,1),'F',ch=.3)
    cbox(V3(9.6,31.5,13),(1,1,3),'N',ch=.4)
# ---------------- backs ----------------
def back_drums(S):
    for nm,c,ax,post in(('drumN',(-10,60,-8),(-.75,.15,.65),(-7,47,-6)),('drumF',(10,59,-4),(-.35,.2,.95),(8,47,-6))):
        a=_n.array(ax,float);a/=_n.linalg.norm(a);Rd=look(a);cc=_n.array(c,float)
        grp(nm+'p');ctube(post,c,(1.8,1.8),'F',ch=.6)
        grp(nm);cyl(cc-a*1.4,6.2,3.2,'N',R=Rd,r=.6);cyl(cc+a*1.4,6.8,1.4,'J',R=Rd,r=.5)
        grp(nm+'face');cyl(cc+a*2.2,5.4,1,'V',R=Rd,r=.3)
        grp(nm+'f')
        for i in range(5):
            th=i/5*6.283+.5;u=Rd[:,0]*math.cos(th)+Rd[:,1]*math.sin(th)
            ctube(cc+a*3.4+u*2,cc+a*3.4+u*5.2,(1.05,1.2),'J',ch=.5,tt=1.4)
        cyl(cc+a*4.4,1.8,1,'F',R=Rd,r=.3)
        sph(cc+Rd[:,1]*4.5-a*3.5+Rd[:,0]*-4,.8,'gL')
def back_missiles(S):
    for sd in(-1,1):
        grp('pod%d'%sd);cbox(V3(8*sd,52,-5),(3.6,5,4.5),'A',rotm(0,D(-20)),ch=1.2,tt=.85)
        grp('podf%d'%sd)
        for i in range(2):
            for j in range(2):sph(V3(8*sd+(i-.5)*3,54+(j-.5)*3.6-1.5,-.8),.9,'V')
        grp('podarm%d'%sd);ctube((4*sd,44,-4),(8*sd,48,-5),(1.2,1.2),'F',ch=.3)
def back_none(S):pass
# ================= sharp / faceted parts =================
def blade(a,b,w,t,mat,tt=.08,ch=None,roll=0):
    ctube(a,b,(w,t),mat,ch=min(w,t)*.9 if ch is None else ch,tt=tt,roll=roll)
def legs_digi(S):
    hy=S.get('hipY',44)
    for side,sx,zb in((-1,-7,3),(1,8,-4)):
        hip=V3(sx,hy,zb);knee=V3(sx*1.12,hy*.66,zb+8);ank=V3(sx*1.12,hy*.3,zb-3);ball=V3(sx*1.1,2.6,zb+2);toe=V3(sx*1.1,1.4,zb+10)
        grp('thigh%d'%side);ctube(hip,knee,(4.2,4.8),'A',ch=2,tt=.6)
        grp('thighT%d'%side);blade(hip+V3(sx*.45,-3,1.6),knee+V3(sx*.4,3,1),2.6,1,'A',tt=.2)
        grp('knee%d'%side);sph(knee,2.8,'F')
        grp('kneeB%d'%side);blade(knee+V3(0,-4,3),knee+V3(0,8,6.5),3.6,1.2,'A',tt=.06)
        grp('shin%d'%side);ctube(knee,ank,(2.8,3.2),'J',ch=1.2,tt=.8)
        grp('shinB%d'%side);blade(ank+V3(0,0,3.2),knee+V3(0,-2,5.2),4,1.5,'A',tt=.3);cbox(knee+(ank-knee)*.6+V3(0,0,5),(1.5,1.1,1),'T',look(knee-ank),ch=.4)
        grp('ankle%d'%side);sph(ank,2.4,'F')
        grp('spur%d'%side);blade(ank+V3(0,1,-1.5),ank+V3(0,5,-9),2,1,'A',tt=.05)
        grp('meta%d'%side);ctube(ank,ball,(2.4,2.6),'J',ch=1,tt=.8)
        grp('foot%d'%side);blade(ball+V3(0,0,-2),toe,4,1.6,'A',tt=.3,ch=1.2);cbox(ball+V3(0,1.2,1),(1.4,.6,1.2),'T',ch=.3)
        grp('heel%d'%side);blade(ball+V3(0,0,-1),ball+V3(0,-1,-7),1.6,1.1,'J',tt=.15)
def torso_wedge(S):
    hy=S.get('hipY',44)
    grp('pelvis');cbox(V3(0,hy+2,-1),(5.5,3,4.5),'J',ch=2.2,tt=.7)
    for sd in(-1,1):grp('skirt%d'%sd);blade(V3(4*sd,hy+2,3),V3(5.2*sd,hy-7,6),2.4,.7,'A',tt=.15)
    grp('waist');cyl(V3(0,hy+6,-1),2.8,2.6,'F',R=look((0,1,0)),r=.4)
    Rc=rotm(0,D(-8))
    grp('chest');cbox(V3(0,hy+13,0),(10,6,7.5),'A',Rc,ch=4.2,tt=.55)
    grp('chestL');cbox(V3(0,hy+9.5,1.5),(5,2,5),'J',Rc,ch=1.8,tt=.6)
    grp('prow');blade(V3(0,hy+16,-4),V3(0,hy+13.5,10),2,1.4,'A',tt=.12)
    for sd in(-1,1):grp('chT%d'%sd);cbox(V3(4.6*sd,hy+12,4.6),(1.2,1.6,1.6),'T',Rc,ch=.5)
    grp('core');sph(V3(-1.8,hy+11,6.4),.7,'gL')
def head_spike(S):
    hy=S.get('hipY',44)
    grp('head');blade(V3(0,hy+18.5,0),V3(0,hy+17.5,11),2.6,2,'A',tt=.2,ch=1.4)
    grp('visor');blade(V3(0,hy+17.4,6),V3(0,hy+17,10.5),1.9,.6,'V',tt=.4,ch=.3);sph(V3(1.6,hy+17.3,9),.75,'gE')
    grp('ant');blade(V3(0,hy+20,1),V3(0,hy+25,-5),.5,.5,'F',tt=.3,ch=.2)
def shoulders_wing(S):
    hy=S.get('hipY',44)
    for sd in(-1,1):
        x=9.5*sd
        x=11*sd
        grp('sh%d'%sd);cbox(V3(x*1.1,hy+16,-1),(4.8,4.6,5.8),'J',ch=2,tt=.7)
        grp('shP%d'%sd);cbox(V3(x+1.2*sd,hy+18.5,0),(3.6,1.6,5.6),'A',rotm(0,0,D(-14*sd)),ch=1.4,tt=.6)
        grp('wing%d'%sd);blade(V3(x+2*sd,hy+18,-4),V3(x+12*sd,hy+28,-8),5,1.1,'A',tt=.2)
        grp('wingT%d'%sd);blade(V3(x+3*sd,hy+19.4,-3.6),V3(x+6.5*sd,hy+23.6,-5),3.2,1.25,'T',tt=.7,ch=.5)
        grp('wing2%d'%sd);blade(V3(x+2*sd,hy+13,-4),V3(x+9*sd,hy+11,-11),3.4,.9,'A',tt=.15)
def arms_longrifle(S):
    hy=S.get('hipY',44)
    for sd in(-1,1):
        x=12*sd;sh=V3(x,hy+14,0);el=V3(x*1.2,hy+6,3);ha=V3(x*1.05,hy-2,8)
        grp('ua%d'%sd);ctube(sh,el,(1.8,2),'J',ch=.8)
        grp('fa%d'%sd);ctube(el,ha,(3,3.2),'A',ch=1.5,tt=.7)
        grp('faB%d'%sd);blade(el+V3(1.6*sd,1,-1),ha+V3(1.8*sd,-1,0),1.6,.7,'T',tt=.3)
        grp('hand%d'%sd);cbox(ha+V3(0,-1.5,.6),(1.6,1.6,1.6),'F',ch=.6)
    a=V3(13,hy+1,-8);b=V3(13,hy-24,32);d=(b-a)/_n.linalg.norm(b-a)
    grp('rifle');ctube(a,a+d*26,(2.2,3.2),'W',ch=1.1)
    grp('rifleB');ctube(a+d*22,b,(1,1.1),'W',ch=.5)
    grp('scope');ctube(a+d*9+V3(0,3,0),a+d*17+V3(0,3,0),(.9,1),'J',ch=.4)
    grp('mag');ctube(a+d*13+V3(0,-2,0),a+d*13+V3(0,-6,-2),(1.2,1.6),'J',ch=.5,tt=.7)
    grp('rifT');cbox(a+d*19+V3(-1.6,0,0),(.6,1,1.6),'T',look(d),ch=.3)
def back_fins(S):
    hy=S.get('hipY',44)
    for sd in(-1,1):grp('fin%d'%sd);blade(V3(3*sd,hy+14,-5),V3(5*sd,hy+22,-12),2.2,.8,'J',tt=.1)
# ================= posing rig =================
def ik2(H,A,L1,L2,bend):
    H=_n.array(H,float);A=_n.array(A,float);d=_n.linalg.norm(A-H);d=min(d,L1+L2-.01);u=(A-H)/_n.linalg.norm(A-H)
    a=(L1*L1-L2*L2+d*d)/(2*d);h=max(0,L1*L1-a*a)**.5
    b=_n.array(bend,float);n=b-u*(b@u);n/=_n.linalg.norm(n)
    return H+u*a+n*h
def xform(prims,piv,R):
    piv=_n.array(piv,float)
    for p in prims:
        p['c']=piv+R@(p['c']-piv);p['R']=R@p['R']
        if p['kind']=='cap':p['a']=piv+R@(p['a']-piv);p['b']=piv+R@(p['b']-piv)
def legs_posed(S):
    P=S['pose'];hy=P['hipY'];L1,L2=P.get('thigh',15),P.get('shin',14)
    for side,leg in((-1,P['near']),(1,P['far'])):
        sx=P.get('hipW',7)*side
        hip=V3(sx,hy,leg.get('hipZ',0));ball=V3(*leg['ball']);
        fa=D(leg.get('footYaw',0));fwd=V3(math.sin(fa),0,math.cos(fa))
        ank=ball+V3(0,P.get('ankH',9),0)-fwd*P.get('ankBack',4)
        knee=ik2(hip,ank,L1,L2,V3(*leg.get('bend',(sx*.4,0,1))))
        toe=ball+fwd*8+V3(0,-1.2,0)
        grp('thigh%d'%side);ctube(hip,knee,(4.6,5.2),'A',ch=2.2,tt=.6)
        grp('thighT%d'%side);ov=V3(side*1.8,0,0);blade(hip+(knee-hip)*.15+ov+V3(0,0,1.5),knee+ov*.6+V3(0,2,1),2.8,1,'A',tt=.2)
        grp('knee%d'%side);sph(knee,3,'F')
        sd=(knee-ank)/_n.linalg.norm(knee-ank);fw=_n.cross(V3(1,0,0),sd);fw=fw if fw[2]>0 else -fw
        grp('kneeB%d'%side);blade(knee-sd*3+fw*3,knee+sd*7+fw*7.5,3.8,1.2,'A',tt=.06)
        grp('shin%d'%side);ctube(knee,ank,(3,3.4),'J',ch=1.2,tt=.8)
        grp('shinB%d'%side);blade(ank+fw*3.4,knee-sd*2+fw*5,4.2,1.5,'A',tt=.3);cbox(knee+(ank-knee)*.6+fw*5,(1.5,1.1,1),'T',look(knee-ank),ch=.4)
        grp('ankle%d'%side);sph(ank,2.5,'F')
        grp('spur%d'%side);blade(ank-fwd*1.5+V3(0,1,0),ank-fwd*9+V3(0,4,0),2,1,'A',tt=.05)
        grp('meta%d'%side);ctube(ank,ball,(2.6,2.8),'J',ch=1,tt=.8)
        grp('foot%d'%side);blade(ball-fwd*2,toe,4.4,1.8,'A',tt=.3,ch=1.3);cbox(ball+V3(0,1.3,0)+fwd,(1.4,.6,1.2),'T',ch=.3)
        grp('heel%d'%side);blade(ball-fwd,ball-fwd*7+V3(0,-1,0),1.8,1.2,'J',tt=.15)
def upper_posed(S):
    P=S['pose'];hy=P['hipY'];n0=len(PR)
    S2=dict(S,hipY=hy)
    torso_wedge(S2);head_spike(S2);shoulders_wing(S2);back_fins(S2)
    # arms from pose: shoulder fixed on torso, elbow and hand given relative to shoulder
    for sd,arm in((-1,P['armN']),(1,P['armF'])):
        sh=V3(12.5*sd,hy+14,0);el=sh+V3(*arm['elbow']);ha=sh+V3(*arm['hand'])
        grp('ua%d'%sd);ctube(sh,el,(2.2,2.4),'J',ch=.9)
        grp('elb%d'%sd);sph(el,2.2,'F')
        grp('fa%d'%sd);ctube(el,ha,(3.2,3.4),'A',ch=1.5,tt=.7)
        grp('faB%d'%sd);blade(el+V3(1.8*sd,1,-1),ha+V3(2*sd,-1,0),1.8,.8,'T',tt=.3)
        grp('hand%d'%sd);cbox(ha,(1.8,1.8,1.8),'F',ch=.7)
        if arm.get('rifle'):
            d=V3(*arm['rifle']);d/=_n.linalg.norm(d);a=ha-d*9
            grp('rifle');ctube(a,a+d*26,(2.2,3.2),'W',ch=1.1)
            grp('rifleB');ctube(a+d*24,a+d*40,(1,1.1),'W',ch=.5)
            grp('scope');ctube(a+d*9+V3(0,3.2,0),a+d*17+V3(0,3.2,0),(.9,1),'J',ch=.4)
            grp('mag');ctube(a+d*13+V3(0,-2.4,0),a+d*13+V3(0,-6.5,-2),(1.2,1.6),'J',ch=.5,tt=.7)
            grp('rifT');cbox(a+d*19+V3(1.8*sd,0,0),(.6,1,1.6),'T',look(d),ch=.3)
    R=rotm(D(P.get('twist',0)),D(P.get('lean',0)),D(P.get('roll',0)))
    xform(PR[n0:],(0,hy+5,-1),R)
PARTS=dict(legs=dict(heavy=legs_heavy,light=legs_light,digi=legs_digi),torso=dict(hunch=torso_hunch,slim=torso_slim,wedge=torso_wedge),head=dict(horned=head_horned,visor=head_visor,spike=head_spike),
 shoulders=dict(heavy=shoulders_heavy,light=shoulders_light,wing=shoulders_wing),arms=dict(rifle_cannon=lambda S:(arm_near_rifle(S),arm_far_cannon(S)),rifle_pair=arms_rifle_pair,longrifle=arms_longrifle),
 back=dict(drums=back_drums,missiles=back_missiles,none=back_none,fins=back_fins),posed=dict(sharp=upper_posed))
def build(S):
    PR.clear()
    if 'pose' in S:
        legs_posed(S);upper_posed(S);return
    PARTS['legs'][S['legs']](S)
    if S['torso']!='wedge':hips(S)
    for k in('torso','head','shoulders','arms','back'):PARTS[k][S[k]](S)
    up=S.get('up',3);fz=S.get('fz',3);low=('thigh','knee','shin','foot')
    for p in PR:
        if not p['grp'].startswith(low):
            p['c']=p['c']+V3(0,up,fz)
            if p['kind']=='cap':p['a']=p['a']+V3(0,up,fz);p['b']=p['b']+V3(0,up,fz)
