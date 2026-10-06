import numpy as np, wave
from PIL import Image, ImageDraw
sr=48000; rng=np.random.default_rng(1)
def save(n,x):
    x=(np.clip(x,-1,1)*32767*0.9).astype(np.int16); st=np.stack([x,x],1).flatten()
    w=wave.open(f'public/sfx/{n}.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes()); w.close()
n=int(sr*.55); t=np.arange(n)/sr; nz=rng.standard_normal(n); cut=200+6000*np.sin(np.pi*t/t[-1])**2; y=np.zeros(n); lp=0
for i in range(n): a=1-np.exp(-2*np.pi*cut[i]/sr); lp+=a*(nz[i]-lp); y[i]=lp
y=y-np.convolve(y,np.ones(40)/40,'same'); y*=np.sin(np.pi*t/t[-1])**1.5; save('whoosh',y/np.abs(y).max()*.8)
n=int(sr*.12); t=np.arange(n)/sr; save('pop',np.sin(2*np.pi*np.cumsum(900*np.exp(-t*25)+300)/sr)*np.exp(-t*35)*.8)
n=int(sr*1.); t=np.arange(n)/sr; y=np.sin(2*np.pi*np.cumsum(120*np.exp(-t*4)+40)/sr)*np.exp(-t*3.5)+.5*rng.standard_normal(n)*np.exp(-t*25); y=np.tanh(y*1.8); save('impact',y/np.abs(y).max()*.9)
n=int(sr*.03); t=np.arange(n)/sr; save('tick',np.sin(2*np.pi*2400*t)*np.exp(-t*200)*.5)
n=int(sr*1.2); t=np.arange(n)/sr; y=(.5*np.sin(2*np.pi*np.cumsum(200+1800*(t/t[-1])**2)/sr)+.15*rng.standard_normal(n))*(t/t[-1])**2; save('riser',y/np.abs(y).max()*.6)
n=int(sr*.8); t=np.arange(n)/sr; y=sum(np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,k in [(1318,5),(1760,6),(2637,8)]); save('ding',y/np.abs(y).max()*.6)
W,H=1080,1920; yy,xx=np.mgrid[0:H,0:W]
rad=lambda cx,cy,rx,ry: np.clip(1-np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2),0,1)
img=np.zeros((H,W,3)); img[:]=(24,14,10)
img+=(rad(540,730,760,860)**1.6)[...,None]*np.array([232,87,42])*.35+(rad(540,1920,650,580)**1.6)[...,None]*np.array([255,201,77])*.18
Image.fromarray(np.clip(img,0,255).astype('uint8')).save('public/assets/bg.png')
gh=H+80; g=Image.new('RGBA',(W,gh),(0,0,0,0)); d=ImageDraw.Draw(g)
for x in range(0,W,80): d.line([(x,0),(x,gh)],fill=(255,190,140,70))
for y in range(0,gh,80): d.line([(0,y),(W,y)],fill=(255,190,140,70))
Y,X=np.mgrid[0:gh,0:W]; m=np.clip(1-np.sqrt(((X-540)/860)**2+((Y-860)/1150)**2),0,1)**1.2
a=np.array(g); a[...,3]=(a[...,3]*m*.5).astype('uint8'); Image.fromarray(a).save('public/assets/grid.png')
