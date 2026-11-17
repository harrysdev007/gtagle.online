"""Local 3:1 animation with animated reflections, neon traces and typography glints."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/gta'
SRC=Path('C:/Users/LaPasion/Downloads/Изображение ChatGPT 17 нояб. 2026 г., 15_13_15.png')
W,H,N=1200,400,60
im=Image.open(SRC).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
base=np.asarray(im).astype(np.float32)
y,x=np.mgrid[:H,:W].astype(np.float32)
protect=Image.new('L',(W,H));d=ImageDraw.Draw(protect)
d.polygon([(int(.39*W),0),(int(.60*W),0),(int(.62*W),int(.57*H)),(int(.63*W),int(.86*H)),(int(.35*W),int(.86*H)),(int(.38*W),int(.57*H))],fill=255)
protect=np.asarray(protect.filter(ImageFilter.GaussianBlur(3))).astype(np.float32)/255
water=np.clip((y/H-.64)/.06,0,1)*(1-protect)
lum=base.max(axis=2)/255
neon=np.clip((base[:,:,0]-base[:,:,1]-20)/90,0,1)*np.clip((lum-.3)/.5,0,1)*(1-protect)
text=((x>.655*W)&(x<.98*W)&(y>.34*H)&(y<.55*H)&(base[:,:,0]>175)&(base[:,:,1]>145)&(base[:,:,2]>120)).astype(np.float32)
text_glow=np.asarray(Image.fromarray((text*255).astype('uint8')).filter(ImageFilter.GaussianBlur(5))).astype(np.float32)/255
paths=[[(.423,.547),(.487,.255),(.558,.547),(.423,.547)],[(.363,.839),(.421,.603),(.578,.603),(.616,.839),(.363,.839)]]
paths=[[(a*W,b*H) for a,b in p] for p in paths]
logo_mask=Image.new('L',(W,H));md=ImageDraw.Draw(logo_mask)
for p in paths:md.polygon(p,fill=255)
logo_mask=np.asarray(logo_mask).astype(np.float32)/255

def trace(draw,points,phase):
 segments=[math.dist(a,b) for a,b in zip(points,points[1:])];total=sum(segments)
 for k in range(85):
  pos=((phase-k*.0018)%1)*total
  for a,b,length in zip(points,points[1:],segments):
   if pos<=length:
    u=pos/length;px=a[0]+u*(b[0]-a[0]);py=a[1]+u*(b[1]-a[1]);fade=(1-k/85)**1.5
    radius=1.1+1.3*fade
    draw.ellipse((px-radius,py-radius,px+radius,py+radius),fill=(int(255*fade),int(220*fade),int(245*fade)))
    break
   pos-=length

def star(draw,cx,cy,strength):
 if strength<=0:return
 r=4+8*strength;color=(int(255*strength),int(245*strength),int(235*strength))
 draw.polygon([(cx,cy-r),(cx+1.5,cy-1.5),(cx+r,cy),(cx+1.5,cy+1.5),(cx,cy+r),(cx-1.5,cy+1.5),(cx-r,cy),(cx-1.5,cy-1.5)],fill=color)

frames=[]
for i in range(N):
 phase=i/N;t=phase*2*math.pi
 # The palms shift gently; faces, typography and emblem are not warped.
 palm=((x<.19*W)|(x>.93*W))*np.clip((.43*H-y)/(.43*H),0,1)
 dx=(6*np.sin(y*.19+t)+2*np.sin(y*.085-2*t+x*.01))*water+3*np.sin(t)*palm
 dy=.8*np.sin(x*.025+y*.1-t)*water
 sx=np.clip(x+dx,0,W-1);sy=np.clip(y+dy,0,H-1)
 ax=sx.astype(int);ay=sy.astype(int);bx=np.minimum(ax+1,W-1);by=np.minimum(ay+1,H-1)
 fx=(sx-ax)[...,None];fy=(sy-ay)[...,None]
 rgb=(base[ay,ax]*(1-fx)+base[ay,bx]*fx)*(1-fy)+(base[by,ax]*(1-fx)+base[by,bx]*fx)*fy
 shimmer=.24*np.sin(y*.27+x*.013-2*t)*water*lum
 pulse=(.20*np.sin(t)+.09*np.sin(2*t+x*.008))*neon
 rgb*=1+(shimmer+pulse)[...,None]
 # Two strong diagonal gloss passes over the original letter pixels.
 sweep_x=.59*W+(phase*2%1)*.48*W
 sweep=np.exp(-((x-sweep_x+(y-.45*H)*.45)/(W*.014))**2)
 rgb+=text[...,None]*sweep[...,None]*np.array([85,95,110])
 rgb+=text_glow[...,None]*(.8+.6*math.sin(t))*np.array([65,6,50])
 # Broad moving neon shafts in the sky, kept behind the subjects and lettering.
 sky=np.clip((.67*H-y)/(.22*H),0,1)*(1-protect)
 sky*=1-np.clip(text_glow*3,0,1)
 for origin,offset in [(.15,0),(.81,2.1)]:
  axis=origin*W+.07*W*math.sin(t+offset)+(y-.2*H)*(.5+.18*math.sin(t+offset))
  shaft=np.exp(-((x-axis)/(W*.009))**2)*sky
  halo=np.exp(-((x-axis)/(W*.03))**2)*sky
  rgb+=shaft[...,None]*np.array([38,6,45])+halo[...,None]*np.array([12,1,15])
 # Ripples of reflected light travel out from beneath the emblem.
 distance=np.sqrt(((x-.49*W)/2)**2+((y-.83*H)*1.2)**2)
 rings=np.maximum(0,np.cos(distance*.12-2*t))**12*water*lum
 rgb+=rings[...,None]*np.array([25,10,24])
 logo_sweep=np.exp(-((x-(.32+.35*phase)*W+(y-.55*H)*.25)/(W*.012))**2)
 # Fade out at both ends to make the sweep itself loop cleanly.
 rgb+=logo_mask[...,None]*logo_sweep[...,None]*(math.sin(math.pi*phase)**2)*np.array([45,55,55])
 light=Image.new('RGB',(W,H));ld=ImageDraw.Draw(light)
 for index,p in enumerate(paths):
  trace(ld,p,(phase+index*.24)%1)
  trace(ld,p,(phase+.5+index*.24)%1)
 for cx,cy,offset in [(.697,.40,.08),(.735,.39,.23),(.779,.50,.34),(.833,.39,.46),(.879,.40,.59),(.924,.37,.81)]:
  distance=((phase-offset+.5)%1)-.5
  strength=max(0,1-abs(distance)/.14)**2
  star(ld,cx*W,cy*H,strength*1.15)
 raw=np.asarray(light).astype(np.float32)
 glow=np.asarray(light.filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
 rgb=np.clip(rgb+raw*1.1+glow*2.8,0,255).astype('uint8')
 frames.append(Image.fromarray(rgb))
palette=Image.fromarray(np.concatenate([np.asarray(frames[i])[::3,::3] for i in (0,10,20,30,40,50)],axis=0)).quantize(colors=256)
for name,size in [('gtaxiom-banner-effects-v4.gif',(1200,400)),('gtaxiom-banner-effects-v4-small.gif',(600,200))]:
 indexed=[f.resize(size,Image.Resampling.LANCZOS).quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 file=OUT/name;indexed[0].save(file,save_all=True,append_images=indexed[1:],duration=80,loop=0,optimize=True,disposal=1)
 with Image.open(file) as gif:
  assert gif.size==size and gif.n_frames==N and gif.info['loop']==0
  gif.seek(0);first=gif.convert('RGB');gif.seek(20)
  assert ImageChops.difference(first,gif.convert('RGB')).getbbox()
 print(f'{name}: {size}, {N} frames, 4.8s, {file.stat().st_size/1024/1024:.2f} MB')
strip=Image.new('RGB',(1200,400*3))
for row,index in enumerate([5,20,40]):strip.paste(frames[index],(0,row*400))
strip.save(ROOT/'output/banner-effects-v4-contact.png')
