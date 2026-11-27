import numpy as np, math, sys, json
from PIL import Image
def rotm(yaw=0,pitch=0,roll=0):
    cy,sy,cp,sp,cr,sr=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch),math.cos(roll),math.sin(roll)
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);Rx=np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]]);Rz=np.array([[cr,-sr,0],[sr,cr,0],[0,0,1]])
    return Ry@Rx@Rz
D=math.radians
def look(axis):  # rotation whose local +z points along axis
    a=np.array(axis,float);a/=np.linalg.norm(a);up=np.array([0,1.,0]) if abs(a[1])<.95 else np.array([1.,0,0])
    x=np.cross(up,a);x/=np.linalg.norm(x);y=np.cross(a,x);return np.stack([x,y,a],1)
PR=[]
def add(kind,c,mat,R=None,**k):PR.append(dict(kind=kind,c=np.array(c,float),R=np.eye(3) if R is None else R,mat=mat,**k))
def box(c,h,mat,R=None,r=0.):add('box',c,mat,R,h=np.array(h,float),r=r)
def cbox(c,h,mat,R=None,ch=.8,tt=1.,tb=1.):add('cbox',c,mat,R,h=np.array(h,float),ch=ch,tt=tt,tb=tb)
def ctube(a,b,h,mat,ch=.8,tt=1.,tb=1.,roll=0):
    a=np.array(a,float);b=np.array(b,float);R=look(b-a)
    if roll:R=R@rotm(0,0,D(roll))
    cbox((a+b)/2,(h[0],h[1],np.linalg.norm(b-a)/2),mat,R,ch,tt,tb)
def cyl(c,rad,hh,mat,R=None,r=0.):add('cyl',c,mat,R,rad=rad,hh=hh,r=r)
def cap(a,b,rad,mat,rb=None):add('cap',[0,0,0],mat,None,a=np.array(a,float),b=np.array(b,float),rad=rad,rb=rad if rb is None else rb)
def sph(c,rad,mat):add('sph',c,mat,None,rad=rad)
def tubeb(a,b,h,mat,r=.6,up=None):  # box along segment a->b with half sizes h=(hx,hy) across
    a=np.array(a,float);b=np.array(b,float);m=(a+b)/2;L=np.linalg.norm(b-a);R=look(b-a)
    box(m,(h[0],h[1],L/2),mat,R,r)
def sdf(p,pr):
    q=(p-pr['c'])@pr['R'] if pr['kind']!='cap' else p
    k=pr['kind']
    if k=='box':
        d=np.abs(q)-(pr['h']-pr['r']);return np.linalg.norm(np.maximum(d,0),axis=1)+np.minimum(d.max(1),0)-pr['r']
    if k=='cbox':
        h=pr['h'];f=np.clip((q[:,2]+h[2])/(2*h[2]),0,1);sc=pr['tb']+(pr['tt']-pr['tb'])*f
        ax,ay,az=np.abs(q[:,0]/sc),np.abs(q[:,1]/sc),np.abs(q[:,2])
        d=np.maximum.reduce([ax-h[0],ay-h[1],az-h[2]])
        c=pr['ch']
        d=np.maximum.reduce([d,(ax+ay-(h[0]+h[1]-c))*.7071,(ax+az-(h[0]+h[2]-c))*.7071,(ay+az-(h[1]+h[2]-c))*.7071])
        return d*np.minimum(sc,1)*.8
    if k=='cyl':
        r=pr['r'];d=np.stack([np.hypot(q[:,0],q[:,1])-(pr['rad']-r),np.abs(q[:,2])-(pr['hh']-r)],1)
        return np.linalg.norm(np.maximum(d,0),axis=1)+np.minimum(d.max(1),0)-r
    if k=='sph':return np.linalg.norm(q,axis=1)-pr['rad']
    if k=='hull':return (q@pr['N'].T-pr['d']).max(1)
    if k=='cap':
        a,b=pr['a'],pr['b'];ba=b-a;pa=p-a;h=np.clip(pa@ba/(ba@ba),0,1)
        return np.linalg.norm(pa-h[:,None]*ba,axis=1)-(pr['rad']+(pr['rb']-pr['rad'])*h)
def bound(pr):
    k=pr['kind']
    if k=='box':return pr['c'],np.linalg.norm(pr['h'])
    if k=='cbox':return pr['c'],np.linalg.norm(pr['h'])*max(1,pr['tt'],pr['tb'])
    if k=='cyl':return pr['c'],np.hypot(pr['rad'],pr['hh'])
    if k=='sph':return pr['c'],pr['rad']
    if k=='hull':return pr['c'],pr['br']
    if k=='cap':return (pr['a']+pr['b'])/2,np.linalg.norm(pr['b']-pr['a'])/2+max(pr['rad'],pr['rb'])
def scene(p):
    best=np.full(len(p),1e9);idx=np.full(len(p),-1)
    for i,pr in enumerate(PR):
        if '_b' not in pr:pr['_b']=bound(pr)
        c,r=pr['_b'];lb=np.linalg.norm(p-c,axis=1)-r
        sel=np.where(lb<best)[0]
        if len(sel)==0:continue
        far=lb[sel]>4.0
        d=np.empty(len(sel));d[far]=lb[sel][far]
        nf=sel[~far]
        if len(nf):d[~far]=sdf(p[nf],pr)
        m=d<best[sel];best[sel[m]]=d[m];idx[sel[m]]=i
    return best,idx
def render(W,H,ss,yaw,pitch,ox,oy,Lc,Rim,scale=1.):
    Mcam=rotm(0,pitch)@rotm(yaw,0)
    Minv=Mcam.T
    n=W*ss;m=H*ss
    xs=((np.arange(n)+.5)/ss-ox)/scale;ys=(oy-(np.arange(m)+.5)/ss)/scale
    X,Y=np.meshgrid(xs,ys);N=X.size
    o=np.stack([X.ravel(),Y.ravel(),np.full(N,120.)],1)@Minv.T
    dvec=np.array([0,0,-1.])@Minv.T
    t=np.zeros(N);hit=np.zeros(N,bool);alive=np.ones(N,bool)
    for _ in range(220):
        a=np.where(alive)[0]
        if len(a)==0:break
        d,_=scene(o[a]+t[a,None]*dvec)
        t[a]+=d*0.9
        h=d<0.03;hit[a[h]]=True;alive[a[h]]=False
        alive[a[t[a]>260]]=False
    P=o+t[:,None]*dvec
    res=dict(hit=hit.reshape(m,n),depth=t.reshape(m,n))
    hi=np.where(hit)[0];ph=P[hi]
    d0,mi=scene(ph);e=.05
    nr=np.stack([scene(ph+np.array(v))[0]-scene(ph-np.array(v))[0] for v in([e,0,0],[0,e,0],[0,0,e])],1)
    nr/=np.linalg.norm(nr,axis=1,keepdims=True)+1e-9
    L=np.array(Lc,float);L/=np.linalg.norm(L);Lw=L@Minv.T
    Rm=np.array(Rim,float);Rm/=np.linalg.norm(Rm);Rw=Rm@Minv.T
    V=-dvec
    # shadows
    sh=np.ones(len(ph));st=np.full(len(ph),.6);al=np.ones(len(ph),bool)
    for _ in range(60):
        a=np.where(al)[0]
        if len(a)==0:break
        d,_=scene(ph[a]+nr[a]*.3+st[a,None]*Lw)
        sh[a]=np.minimum(sh[a],np.clip(6*d/st[a],0,1))
        st[a]+=np.maximum(d,.2);al[a[(d<.02)|(st[a]>80)]]=False
        sh[a[d<.02]]=0
    diff=np.clip(nr@Lw,0,1)*(.4+.6*sh)
    # ambient occlusion
    ao=np.zeros(len(ph))
    for k in(1,2,3.5):ao+=np.clip(k-scene(ph+nr*k)[0],0,k)/k
    ao=1-ao/3*0.7
    rim=np.clip(1-np.abs(nr@V),0,1)**2*np.clip(nr@Rw,0,1)
    refl=2*(nr@Lw)[:,None]*nr-Lw;spec=np.clip(refl@V,0,1)**18*sh
    def full(v):
        a=np.full(N,np.nan);a[hi]=v;return a.reshape(m,n)
    res.update(diff=full(diff),ao=full(ao),rim=full(rim),spec=full(spec),mat=full(mi),camn=full((nr@Mcam.T)[:,2]))
    return res
