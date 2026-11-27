# Heron game sprite sheet: 8 directions (rows) x 16 frames (columns)
# usage: python3 heron_sheet.py out.png 88 .86 38   [direction] [rifle-aim sign]
#   88 = frame size px, .86 = model scale (~46 px tall = 10 m), 38 = camera pitch in degrees
# rows: 0 down, 1 down-right, 2 right, 3 up-right, 4 up, 5 up-left, 6 left, 7 down-left
# 0-3   idle loop in the angled study stance (3/4 to camera via IYAW, staggered feet, rifle low), breathing
# 4-12  move blend: torso lean level a (0..2) x leg sweep level b (0..2) -> 4+a*3+b
# 13    full flight (same as 12; legs hold still in flight)
# 14,15 brake light / hard
import sys,json,copy;import os;HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,os.path.join(HERE,'..','mechkit'))
import mech3
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
base=json.load(open(os.path.join(HERE,'..','mechkit','specs','ac_heron.json')))
F=int(sys.argv[2]);SC=float(sys.argv[3]);PITCH=float(sys.argv[4]);NP=16;IYAW=float(os.environ.get('IYAW','-35'));IDLE='angled';SGN=float(sys.argv[6]) if len(sys.argv)>6 else 1
def lerp(a,b,u):return [x+(y-x)*u for x,y in zip(a,b)]
def armset(u,sw=0):
    # u: 0 carried low (idle) .. 1 rifle forward, free arm swept back for balance
    n={"elbow":lerp([-2,-7.5,2],[-2,-7,3],u),"hand":lerp([-1.5,-11,7],[-1,-10,9],u),"aim":[-0.04,-0.3,1],"weapon":True}
    f={"elbow":lerp([3,-8,0+sw],[3.5,-5,-4],u),"hand":lerp([2.5,-13,2+sw],[3.5,-8,-7],u)}
    return n,f
def frame(args):
    d,f=args;S=copy.deepcopy(base);P=S['pose'];S['camPitch']=PITCH;S['scale']=SC;S['wear']=0;S['lift']=.2;S['seams']=False
    P['twist']=0;P['roll']=0;P['near']['footYaw']=-7;P['far']['footYaw']=7
    if f<4:
        # the study stance: body twisted off-axis, slight roll, wide staggered feet turned out, rifle held low-forward
        ph=[0,.5,1,.5][f];sw=[0,.6,0,-.6][f]
        P['lean']=5+1.5*ph;P['hipY']=27-.6*ph;P['twist']=14;P['roll']=-2
        near=[-12,1.2,5];far=[12,1.2,-5];P['near']['footYaw']=-10;P['far']['footYaw']=12
        a=({"elbow":[-2.5,-8,1],"hand":[-3,-13-.4*ph,7],"aim":[-0.12,-0.7,1],"weapon":True},{"elbow":[4,-7,-1+sw],"hand":[3,-13,2+sw]})
    elif f<13:
        A,B=divmod(f-4,3)
        P['lean']=[16,28,40][A];P['hipY']=[27,26,25.5][A]-[0,.5,.5][B]
        nb=[[-8,1.2,2],[-7,3.5,-4],[-6,7.5,-10]][B];fb=[[8,1.2,-1.5],[7,3,-7],[6,6.5,-13]][B]
        near,far=nb,fb;a=armset([.55,.85,1][A])
    elif f==13:
        P['lean']=40;P['hipY']=25;near=[-6,7.5,-10];far=[6,6.5,-13];a=armset(1)
    else:
        k=f-14;P['lean']=[-8,-16][k];P['hipY']=[26,24.5][k];near=[[-8,1.2,6],[-8.5,1.2,9]][k];far=[[8,1.2,3],[8.5,1.2,5]][k];a=armset(.3)
    import math;L=math.radians(P['lean']);ay=a[0]['aim'][1];
    if f>=4:a[0]['aim']=[a[0]['aim'][0],ay+math.tan(L)*SGN,1]
    P['armN'],P['armF']=a;P['near']['ball']=near;P['far']['ball']=far
    im=mech3.sprite(S,d*45+(IYAW if f<4 else 0),W=F,H=F,ox=F//2,oy=F-10,ss=4,bg=False)
    return d,f,im
if __name__=='__main__':
    out=sys.argv[1];sheet=Image.new('RGBA',(F*NP,F*8))
    jobs=[(d,f) for d in range(8) for f in range(NP)] if len(sys.argv)<6 else [(int(sys.argv[5]),f) for f in range(NP)]
    with ProcessPoolExecutor(4) as ex:
        for d,f,im in ex.map(frame,jobs):sheet.paste(im,(f*F,d*F))
    sheet.save(out)
