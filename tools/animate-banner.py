"""Create a seamless local cinemagraph from the approved clean banner."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/gta'
W, H, N = 1200, 400, 40
image = Image.open(OUT / 'gtaxiom-banner-clean.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
base = np.asarray(image).astype(np.float32)
y,x = np.mgrid[:H,:W].astype(np.float32)
water = np.clip((y/H-.64)/.08,0,1)
# Protect the full emblem and portraits from the water displacement.
protect = Image.new('L',(W,H))
ImageDraw.Draw(protect).polygon([(int(.39*W),0),(int(.60*W),0),(int(.62*W),int(.57*H)),(int(.63*W),int(.86*H)),(int(.35*W),int(.86*H)),(int(.38*W),int(.57*H))],fill=255)
protected = np.asarray(protect.filter(ImageFilter.GaussianBlur(3))).astype(np.float32)/255
water *= 1-protected
brightness = base.max(axis=2)/255
neon = np.clip((base[:,:,0]-base[:,:,1]-25)/110,0,1)*np.clip((brightness-.25)/.6,0,1)
neon *= 1-protected
frames=[]
for i in range(N):
 t=2*math.pi*i/N
 dx=(1.8*np.sin(y*.22+t)+.7*np.sin(y*.1-2*t+x*.008))*water
 dy=.5*np.sin(x*.018+y*.08-t)*water
 sx=np.clip(x+dx,0,W-1); sy=np.clip(y+dy,0,H-1)
 x0=sx.astype(int);y0=sy.astype(int);x1=np.minimum(x0+1,W-1);y1=np.minimum(y0+1,H-1)
 fx=(sx-x0)[...,None];fy=(sy-y0)[...,None]
 warped=(base[y0,x0]*(1-fx)+base[y0,x1]*fx)*(1-fy)+(base[y1,x0]*(1-fx)+base[y1,x1]*fx)*fy
 # Slow breathing neon and traveling ripples in the reflected lights.
 glow=(.055*np.sin(t)+.025*np.sin(2*t+x*.008))*neon
 shimmer=.075*np.sin(y*.30+x*.012-2*t)*water*brightness
 rgb=np.clip(warped*(1+glow[...,None]+shimmer[...,None]),0,255).astype('uint8')
 frames.append(Image.fromarray(rgb))

# One palette for every frame prevents color flicker at the loop seam.
palette=Image.fromarray(np.concatenate([np.asarray(frames[i])[::4,::4] for i in (0,10,20,30)],axis=0)).quantize(colors=256)
for name,size in [('gtaxiom-banner-animated.gif',(1200,400)),('gtaxiom-banner-animated-small.gif',(600,200))]:
 indexed=[f.resize(size,Image.Resampling.LANCZOS).quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 target=OUT/name
 indexed[0].save(target,save_all=True,append_images=indexed[1:],duration=80,loop=0,optimize=True,disposal=1)
 with Image.open(target) as gif:
  assert gif.n_frames==N and gif.size==size and gif.info['loop']==0
  gif.seek(0); first=gif.convert('RGB');gif.seek(N//2)
  assert ImageChops.difference(first,gif.convert('RGB')).getbbox() is not None
  print(f'{name}: {gif.size}, {gif.n_frames} frames, 3.2 seconds, {target.stat().st_size/1024/1024:.2f} MB')
frames[0].save(ROOT/'output/animated-banner-first.png')
