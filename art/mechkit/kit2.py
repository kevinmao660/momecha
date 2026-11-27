# ===== Scrapline mech kit v2: posable hull + swappable, detailed part slots =====
_build_v1=build
def vent(c,R,w,h,n=3,d=.5,mat='J'):
    """recessed dark vent with n horizontal ribs; R orients it, local z = outward"""
    c=_n.array(c,float);cbox(c,(w,h,d),'V',R,ch=.3)
    for i in range(n):
        y=-h+(i+.5)*2*h/n;cbox(c+R@V3(0,y,d*.7),(w*.92,h/n*.42,d*.7),mat,R,ch=.15)
def piston(a,b,r=.75):
    a=_n.array(a,float);b=_n.array(b,float);m=a+(b-a)*.55
    cap(a,m,r,'F');cap(m,b,r*.6,'J')
def bolt(p):sph(p,.5,'gK')
def light(p,r=.75,c='gL'):sph(p,r,c)
def frame_at(a,b):
    """orthonormal frame along a->b: (u=along, s=side, f=forward-ish)"""
    a=_n.array(a,float);b=_n.array(b,float);u=(b-a)/_n.linalg.norm(b-a)
    s=_n.cross(V3(0,1,0) if abs(u[1])<.9 else V3(0,0,1),u);s/=_n.linalg.norm(s);f=_n.cross(u,s);return u,s,f
# ---------------- LEGS (per side) ----------------
def leg_blade(S,L):
    sd,hip,knee,ank,ball,fwd=L['sd'],L['hip'],L['knee'],L['ank'],L['ball'],L['fwd'];side=sd
    toe=ball+fwd*8+V3(0,-1.2,0)
    sdv=(knee-ank)/_n.linalg.norm(knee-ank);fw=_n.cross(V3(1,0,0),sdv);fw=fw if fw[2]>0 else -fw
    grp('thigh%d'%side);ctube(hip,knee,(4.4,5),'A',ch=2.2,tt=.6)
    grp('thighO%d'%side);ov=V3(side*2.2,0,0);blade(hip+(knee-hip)*.12+ov+V3(0,0,1.2),knee+ov*.7+V3(0,2.5,.6),2.8,1,'A',tt=.2)
    grp('thighF%d'%side);ctube(hip+(knee-hip)*.35+V3(0,0,3.8),hip+(knee-hip)*.8+V3(0,0,3.6),(2.6,.9),'J',ch=.5,tt=.7)
    grp('thighH%d'%side);piston(hip+V3(0,-1,-3.5),knee+V3(0,1.5,-2.6))
    grp('knee%d'%side);sph(knee,3,'F')
    grp('kneeB%d'%side);blade(knee-sdv*3+fw*3,knee+sdv*7+fw*7.5,3.8,1.2,'A',tt=.06)
    grp('kneeT%d'%side);cbox(knee+sdv*1.5+fw*4.4,(1.6,1,1),'T',look(fw),ch=.3)
    grp('shin%d'%side);ctube(knee,ank,(3,3.4),'J',ch=1.2,tt=.8)
    grp('shinB%d'%side);blade(ank+fw*3.4,knee-sdv*2+fw*5,4.2,1.5,'A',tt=.3)
    grp('shinS%d'%side);vent(knee+(ank-knee)*.5+V3(side*3,0,0),look(V3(side,0,0)),1.4,2.2,3,.5)
    grp('shinT%d'%side);cbox(knee+(ank-knee)*.62+fw*5.2,(1.5,1.1,.9),'T',look(knee-ank),ch=.4)
    grp('ankle%d'%side);sph(ank,2.5,'F');piston(knee-fw*2.4,ank-fw*2.2+V3(0,1,0),.6)
    grp('spur%d'%side);blade(ank-fwd*1.5+V3(0,1,0),ank-fwd*9+V3(0,4,0),2,1,'A',tt=.05)
    grp('meta%d'%side);ctube(ank,ball,(2.6,2.8),'J',ch=1,tt=.8)
    grp('foot%d'%side);blade(ball-fwd*2,toe,4.4,1.8,'A',tt=.3,ch=1.3)
    grp('footT%d'%side);cbox(ball+V3(0,1.4,0)+fwd,(1.4,.6,1.2),'T',ch=.3)
    grp('claw%d'%side)
    for k in(-1,1):blade(toe-fwd*2+_n.cross(V3(0,1,0),fwd)*2.6*k,toe+fwd*1.5+_n.cross(V3(0,1,0),fwd)*3.4*k+V3(0,-.4,0),1,.8,'J',tt=.2)
    grp('heel%d'%side);blade(ball-fwd,ball-fwd*7+V3(0,-1,0),1.8,1.2,'J',tt=.15)
def leg_heavy(S,L):
    sd,hip,knee,ank,ball,fwd=L['sd'],L['hip'],L['knee'],L['ank'],L['ball'],L['fwd'];side=sd
    sdv=(knee-ank)/_n.linalg.norm(knee-ank);fw=_n.cross(V3(1,0,0),sdv);fw=fw if fw[2]>0 else -fw
    grp('thigh%d'%side);ctube(hip,knee,(5,5.4),'A',ch=1.8,tt=.8)
    grp('thighP%d'%side);ctube(hip+(knee-hip)*.3+V3(side*2.4,0,0),knee+V3(side*2.6,2,0),(3.6,3.8),'A',ch=1.4,tt=.75)
    grp('thighH%d'%side);piston(hip+V3(0,-1,-4),knee+V3(0,1.4,-3.4),.9)
    grp('knee%d'%side);sph(knee,3.4,'F');cbox(knee+fw*3.6+sdv*.5,(3.6,3.2,1.6),'J',look(fw),ch=1)
    grp('kneeB%d'%side);bolt(knee+fw*5.3+sdv*.6)
    grp('shin%d'%side);ctube(knee,ank,(5,5.2),'A',ch=1.8,tt=1.15)
    grp('shinV%d'%side);vent(knee+(ank-knee)*.45+fw*5.2,look(fw),2.4,2.4,3,.5)
    grp('shinT%d'%side);cbox(knee+(ank-knee)*.8+V3(side*5.4,0,0),(.6,1.6,2.2),'T',ch=.3)
    grp('ankle%d'%side);sph(ank,3,'F')
    grp('foot%d'%side);cbox(V3(ball[0],2.1,ball[2])+fwd*1.5,(6,2.1,8.5),'J',look(fwd),ch=1.2,tt=.8)
    grp('toe%d'%side);cbox(V3(ball[0],1.5,ball[2])+fwd*10.5,(5.4,1.5,1.8),'A',look(fwd),ch=.8)
    grp('heel%d'%side);cbox(V3(ball[0],1.6,ball[2])-fwd*7,(4,1.6,1.6),'F',look(fwd),ch=.6)
# ---------------- CORE (torso-local, built at hip height hy) ----------------
def core_wedge(S,hy):
    grp('pelvis');cbox(V3(0,hy+2,-1),(5.5,3,4.5),'J',ch=2.2,tt=.7)
    for sd in(-1,1):
        grp('skirt%d'%sd);blade(V3(4*sd,hy+2,3),V3(5.2*sd,hy-7,6),2.4,.7,'A',tt=.15)
        grp('skirtS%d'%sd);blade(V3(6.5*sd,hy+2,-1),V3(8*sd,hy-6,-1),2.2,.7,'A',tt=.2)
    grp('waist');cyl(V3(0,hy+6,-1),2.8,2.6,'F',R=look((0,1,0)),r=.4)
    for sd in(-1,1):grp('waistH%d'%sd);piston(V3(2.6*sd,hy+3.5,1),V3(3.4*sd,hy+9,2),.55)
    Rc=rotm(0,D(-8))
    grp('chest');cbox(V3(0,hy+13,0),(10,6,7.5),'A',Rc,ch=4.2,tt=.55)
    grp('chestL');cbox(V3(0,hy+9.5,1.5),(6,2.2,5.6),'J',Rc,ch=1.8,tt=.6)
    grp('collar');cbox(V3(0,hy+17.4,-1),(5.5,1.3,4),'J',Rc,ch=1,tt=.7)
    grp('prow');blade(V3(0,hy+16,-4),V3(0,hy+13.5,11),2.2,1.5,'A',tt=.12)
    for sd in(-1,1):
        grp('chT%d'%sd);cbox(V3(4.8*sd,hy+12.5,5.6),(1.3,1.8,1.4),'T',Rc,ch=.5)
        grp('chV%d'%sd);vent(V3(8.6*sd,hy+12,1.2),look(V3(sd,0,.35)),1.5,2.2,3,.5,mat='T')
        grp('chP%d'%sd);blade(V3(3*sd,hy+16.6,4),V3(8*sd,hy+14,6),2,.8,'A',tt=.3)
    grp('core');light(V3(-1.9,hy+10,6.8),.7);bolt(V3(2.4,hy+10,6.6))
def core_block(S,hy):
    grp('pelvis');cbox(V3(0,hy+2,-1),(6.5,3.4,5),'J',ch=1.6)
    for sd in(-1,1):grp('skirt%d'%sd);cbox(V3(4.6*sd,hy-.5,4),(2.6,3,1),'A',rotm(0,D(14)),ch=.8,tt=.7)
    grp('waist');cyl(V3(0,hy+6,-1),3.6,2.6,'F',R=look((0,1,0)),r=.4)
    grp('chest');cbox(V3(0,hy+13,0),(10.5,6.4,7.6),'A',ch=2.4,tt=.85)
    grp('chestT');cbox(V3(0,hy+19,-.5),(8.6,1.4,6.4),'A',ch=1,tt=.8)
    grp('hatch');cbox(V3(0,hy+12,7.4),(4,3.4,.8),'J',ch=.8,tt=.8)
    grp('hatchT');cbox(V3(0,hy+15.6,7.6),(3.4,.5,.5),'T',ch=.2)
    for sd in(-1,1):grp('chV%d'%sd);vent(V3(7*sd,hy+10.5,7.2),_n.eye(3),2,2.6,4,.5);bolt(V3(4.6*sd,hy+16.6,7.2))
    grp('core');light(V3(0,hy+9.2,7.8),.7)
# ---------------- HEADS (torso-local) ----------------
def head_spike(S,hy):
    grp('neck');cap((0,hy+16,1),(0,hy+18,3),1.8,'F')
    grp('head');blade(V3(0,hy+19.5,0),V3(0,hy+18.5,11),2.8,2.2,'A',tt=.2,ch=1.5)
    grp('cheek');blade(V3(0,hy+18,2),V3(0,hy+16.6,9),3.2,1.2,'J',tt=.4)
    grp('visor');blade(V3(0,hy+18.4,6),V3(0,hy+18,10.6),2,.6,'V',tt=.4,ch=.3);light(V3(1.6,hy+18.3,9),.75,'gE');light(V3(-1.6,hy+18.3,9),.6,'gE')
    grp('ant');blade(V3(1,hy+21,1),V3(2,hy+27,-5),.5,.5,'F',tt=.3,ch=.2);blade(V3(-1,hy+21,1),V3(-2,hy+26,-4),.5,.5,'F',tt=.3,ch=.2)
def head_visor(S,hy):
    grp('neck');cap((0,hy+16,1),(0,hy+18,2),1.8,'F')
    grp('head');cbox(V3(0,hy+19.6,2.5),(4.2,2.8,4.4),'A',ch=1.5,tt=.7)
    grp('visor');cbox(V3(0,hy+19.4,6.8),(3.6,.7,.5),'gE',ch=.2)
    grp('crest');blade(V3(0,hy+22,0),V3(0,hy+23.5,-6),.7,1.8,'T',tt=.25)
    grp('ear');[cbox(V3(4.4*s,hy+19.4,2),(.8,1.6,2),'J',ch=.4) for s in(-1,1)]
def head_mono(S,hy):
    grp('neck');cap((0,hy+16,1),(0,hy+18,2),1.8,'F')
    grp('head');cyl(V3(0,hy+19.5,2.5),3.6,3.4,'A',R=look((0,0,1)),r=1.2)
    grp('hood');blade(V3(0,hy+22,-1),V3(0,hy+21.5,7),3.8,1,'J',tt=.6)
    grp('lens');cyl(V3(0,hy+19.3,6),1.6,.6,'V',R=look((0,0,1)),r=.2);light(V3(.4,hy+19.4,6.6),1,'gE')
# ---------------- ARMS + SHOULDER UNITS (torso-local, per side) ----------------
def arm_blade(S,A):
    sd,sh,el,ha=A['sd'],A['sh'],A['el'],A['ha'];hy=A['hy'];x=11*sd
    grp('sh%d'%sd);cbox(V3(x*1.1,hy+16,-1),(4.8,4.6,5.8),'J',ch=2,tt=.7)
    grp('shP%d'%sd);cbox(V3(x*1.1+1.3*sd,hy+18.8,0),(3.8,1.6,5.8),'A',rotm(0,0,D(-14*sd)),ch=1.4,tt=.6)
    grp('shB%d'%sd);bolt(V3(x*1.1+4.6*sd,hy+16,3));vent(V3(x*1.1,hy+16,4.9),_n.eye(3),2.4,2,3,.4,mat='T')
    grp('wing%d'%sd);blade(V3(x+2*sd,hy+18,-4),V3(x+12*sd,hy+28,-8),5,1.1,'A',tt=.2)
    grp('wingL%d'%sd);blade(V3(x+3*sd,hy+17,-5),V3(x+9.5*sd,hy+24,-8.5),3.2,1.3,'J',tt=.3)
    grp('wingT%d'%sd);blade(V3(x+3*sd,hy+19.4,-3.6),V3(x+6.5*sd,hy+23.6,-5),3.2,1.25,'T',tt=.7,ch=.5)
    grp('wing2%d'%sd);blade(V3(x+2*sd,hy+13,-4),V3(x+9*sd,hy+11,-11),3.4,.9,'A',tt=.15)
    grp('ua%d'%sd);ctube(sh,el,(2.2,2.4),'J',ch=.9)
    grp('elb%d'%sd);sph(el,2.2,'F')
    grp('fa%d'%sd);ctube(el,ha,(3.2,3.4),'A',ch=1.5,tt=.7)
    grp('faB%d'%sd);u,s,f=frame_at(el,ha);blade(el+s*sd*2.4+u*1,ha+s*sd*2.6-u*1,1.8,.8,'T',tt=.3)
    grp('faH%d'%sd);piston(sh+V3(0,-2,-2),el+V3(0,0,-2),.5)
    grp('hand%d'%sd);cbox(ha,(1.8,1.8,1.8),'F',ch=.7)
def arm_heavy(S,A):
    sd,sh,el,ha=A['sd'],A['sh'],A['el'],A['ha'];hy=A['hy'];x=11*sd
    grp('sh%d'%sd);cbox(V3(x*1.15,hy+16,-.5),(5.4,5,6.4),'A',ch=2.4,tt=.85)
    grp('shP%d'%sd);cbox(V3(x*1.15+.8*sd,hy+20.8,-.5),(4.6,1.2,5.4),'J',ch=.9,tt=.8)
    grp('shV%d'%sd);vent(V3(x*1.15+5.4*sd,hy+16,-.5),look(V3(sd,0,0)),2.2,2.4,3,.5)
    grp('shT%d'%sd);cbox(V3(x*1.15+2*sd,hy+16,5.9),(1.6,2.6,.6),'T',ch=.3)
    grp('ua%d'%sd);ctube(sh,el,(2.6,2.8),'J',ch=1)
    grp('elb%d'%sd);sph(el,2.6,'F')
    grp('fa%d'%sd);ctube(el,ha,(4,4.2),'A',ch=1.6,tt=1.15)
    grp('faV%d'%sd);u,s,f=frame_at(el,ha);vent(el+(ha-el)*.5+s*sd*4.4,_n.stack([f,u,s*sd],1),1.4,2,3,.5)
    grp('hand%d'%sd);cbox(ha+u*1.5,(2.4,2.4,2.4),'F',ch=.9);bolt(el+(ha-el)*.2+f*4.2)
# ---------------- BACK UNITS (torso-local) ----------------
def back_fins(S,hy):
    for sd in(-1,1):grp('fin%d'%sd);blade(V3(3*sd,hy+14,-5),V3(5*sd,hy+23,-12),2.4,.8,'J',tt=.1)
def back_booster(S,hy):
    grp('pack');cbox(V3(0,hy+13,-8),(6,5,2.6),'J',ch=1.4,tt=.8)
    for sd in(-1,1):
        grp('noz%d'%sd);cyl(V3(3.2*sd,hy+9,-10),2,3,'F',R=look((0,-1,-.4)),r=.4);light(V3(3.2*sd,hy+6.6,-11),1,'gL')
        grp('fin%d'%sd);blade(V3(5*sd,hy+16,-8),V3(9*sd,hy+24,-12),2,.8,'A',tt=.1)
def back_missiles(S,hy):
    for sd in(-1,1):
        grp('pod%d'%sd);cbox(V3(7*sd,hy+22,-6),(3.6,3.6,5),'A',rotm(0,D(-25)),ch=1.2,tt=.85)
        grp('podF%d'%sd)
        for i in(-1,1):
            for j in(-1,1):sph(V3(7*sd+i*1.5,hy+24.6+j*1.5,-2),.8,'V')
        grp('podT%d'%sd);cbox(V3(7*sd+3.7*sd,hy+21.6,-6),(.4,1.4,2.6),'T',rotm(0,D(-25)),ch=.2)
        grp('podA%d'%sd);ctube(V3(3*sd,hy+16,-6),V3(6*sd,hy+19,-6),(1.2,1.2),'F',ch=.3)
def back_drums(S,hy):
    for sd,c,ax in((-1,(-9,hy+24,-8),(-.75,.15,.65)),(1,(9,hy+23,-6),(-.3,.2,.95))):
        a=_n.array(ax,float);a/=_n.linalg.norm(a);Rd=look(a);cc=_n.array(c,float)
        grp('drP%d'%sd);ctube(V3(4*sd,hy+15,-6),cc,(1.6,1.6),'F',ch=.5)
        grp('dr%d'%sd);cyl(cc-a*1.2,5.4,2.8,'N',R=Rd,r=.5);cyl(cc+a*1.2,5.9,1.2,'J',R=Rd,r=.4)
        grp('drF%d'%sd);cyl(cc+a*1.9,4.6,.9,'V',R=Rd,r=.3)
        grp('drB%d'%sd)
        for i in range(5):
            th=i/5*6.283+.5;u=Rd[:,0]*math.cos(th)+Rd[:,1]*math.sin(th)
            ctube(cc+a*3+u*1.8,cc+a*3+u*4.6,(.95,1.1),'J',ch=.45,tt=1.4)
        light(cc+Rd[:,1]*4-a*3,.7)
# ---------------- WEAPONS (in hand; d = aim direction) ----------------
def wpn_rifle(S,ha,d,sd):
    a=ha-d*9
    grp('rifle');ctube(a,a+d*30,(2.2,3.2),'W',ch=1.1)
    grp('rifleP');ctube(a+d*20,a+d*30,(2.5,2.4),'A',ch=1,tt=.8)
    grp('rifleR');ctube(a+d*3+V3(0,2.6,0),a+d*24+V3(0,2.6,0),(1.4,.6),'A',ch=.3)
    grp('rifleB');ctube(a+d*28,a+d*48,(1,1.1),'W',ch=.5)
    grp('rifleM');ctube(a+d*47,a+d*51,(1.5,1.5),'J',ch=.5)
    grp('scope');ctube(a+d*9+V3(0,3.6,0),a+d*17+V3(0,3.6,0),(.9,1),'J',ch=.4);light(a+d*17.4+V3(0,3.6,0),.5,'gL')
    grp('mag');ctube(a+d*13+V3(0,-2.4,0),a+d*13+V3(0,-6.5,-2),(1.2,1.6),'J',ch=.5,tt=.7)
    grp('rifT');cbox(a+d*19+V3(2*sd,0,0),(.6,1,1.8),'T',look(d),ch=.3)
    grp('stock');blade(a+d*1,a-d*5+V3(0,-1.5,0),1.6,2.4,'W',tt=.5)
def wpn_cannon(S,ha,d,sd):
    a=ha-d*10
    grp('cannon');ctube(a,a+d*40,(2.8,2.8),'W',ch=1.2,tt=.85)
    grp('housing');ctube(a+d*4,a+d*16,(4,4),'N',ch=1.2)
    for t in(6,9,12):grp('rib%d'%t);ctube(a+d*t,a+d*(t+1),(4.3,4.3),'N',ch=1.3)
    light(a+d*15+V3(0,4,0),.7)
    grp('muzzle');cyl(a+d*41,2.4,2,'N',R=look(d),r=.4)
def wpn_blade(S,ha,d,sd):
    grp('hilt');ctube(ha-d*3,ha+d*3,(1.2,1.2),'J',ch=.4)
    grp('guard');cbox(ha+d*3.2,(3,1,1),'T',look(d),ch=.3)
    grp('edge');ctube(ha+d*4,ha+d*30,(1.5,.8),'gL',ch=.3,tt=.25)
SLOTS=dict(legs=dict(blade=leg_blade,heavy=leg_heavy),core=dict(wedge=core_wedge,block=core_block),
 head=dict(spike=head_spike,visor=head_visor,mono=head_mono),arms=dict(blade=arm_blade,heavy=arm_heavy),
 back=dict(fins=back_fins,booster=back_booster,missiles=back_missiles,drums=back_drums,none=lambda S,hy:None),
 weapon=dict(rifle=wpn_rifle,cannon=wpn_cannon,blade=wpn_blade))
def build_v2(S):
    PR.clear();P=S['pose'];hy=P['hipY'];L1,L2=P.get('thigh',15),P.get('shin',14);sl=S['slots']
    for side,leg in((-1,P['near']),(1,P['far'])):
        sx=P.get('hipW',7)*side;hip=V3(sx,hy,leg.get('hipZ',0));ball=V3(*leg['ball'])
        fa=D(leg.get('footYaw',0));fwd=V3(math.sin(fa),0,math.cos(fa))
        ank=ball+V3(0,P.get('ankH',9),0)-fwd*P.get('ankBack',4)
        knee=ik2(hip,ank,L1,L2,V3(*leg.get('bend',(sx*.4,0,1))))
        if sl['legs']=='heavy':ank=ball+V3(0,5,0);knee=ik2(hip,ank,L1,L2+3,V3(*leg.get('bend',(sx*.4,0,1))))
        SLOTS['legs'][sl['legs']](S,dict(sd=side,hip=hip,knee=knee,ank=ank,ball=ball,fwd=fwd))
    n0=len(PR)
    SLOTS['core'][sl['core']](S,hy);SLOTS['head'][sl['head']](S,hy);SLOTS['back'][sl['back']](S,hy)
    for sd,arm in((-1,P['armN']),(1,P['armF'])):
        sh=V3(12.5*sd,hy+14,0);el=sh+V3(*arm['elbow']);ha=sh+V3(*arm['hand'])
        SLOTS['arms'][sl['arms']](S,dict(sd=sd,sh=sh,el=el,ha=ha,hy=hy))
        if arm.get('weapon') or (sd==1 and not P['armN'].get('weapon') and 'weapon' in sl):
            d=V3(*arm.get('aim',(0,-.4,1)));d/=_n.linalg.norm(d);SLOTS['weapon'][sl['weapon']](S,ha,d,sd)
    R=rotm(D(P.get('twist',0)),D(P.get('lean',0)),D(P.get('roll',0)))
    xform(PR[n0:],(0,hy+5,-1),R)
def build(S):
    if 'slots' in S:return build_v2(S)
    return _build_v1(S)
