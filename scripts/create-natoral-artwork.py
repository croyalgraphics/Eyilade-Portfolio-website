"""Natoral concept range: native source geometry, outlined licensed typography, and photographic applications."""
from pathlib import Path
from base64 import b64encode
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools import subset
from PIL import Image,ImageDraw
import pymupdf as fitz
import io,re,json,shutil,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];S=R/'artwork/natoral/source';G=R/'artwork/natoral/generated';M=R/'artwork/natoral/masters';W=R/'dist/assets/natoral'
M.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
GREEN,LIME,INK,WHITE,MINT,PINK,BLUE,LILAC='#006837','#8CC63F','#4D4D4D','#FFFFFF','#F3FFF8','#EBD1C8','#D8E8EF','#DFD8EC'
fonts={'body':TTFont(R/'Assets/Fonts/Rubik/static/Rubik-Regular.ttf',recalcTimestamp=False),'display':TTFont(S/'CherryBombOne-Regular.ttf',recalcTimestamp=False)};serial=0;manifest=[]
def rect(x,y,w,h,c,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x,y,x2,y2,c=GREEN,sw=1):return f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
def width(s,z,font='display'):
 f=fonts[font];g=f.getGlyphSet();m=f.getBestCmap();return sum(g[m.get(ord(ch),'.notdef')].width for ch in s)*z/f['head'].unitsPerEm
def text(s,x,y,z=40,c=INK,font='display',anchor='start'):
 f=fonts[font];g=f.getGlyphSet();m=f.getBestCmap();sc=z/f['head'].unitsPerEm
 if anchor=='middle':x-=width(s,z,font)/2
 if anchor=='end':x-=width(s,z,font)
 o=[]
 for ch in s:
  n=m.get(ord(ch),'.notdef');p=SVGPathPen(g);g[n].draw(p);o.append(f'<path d="{p.getCommands()}" transform="translate({x:.3f} {y}) scale({sc:.6f} {-sc:.6f})"/>');x+=g[n].width*sc
 return f'<g fill="{c}" aria-label="{escape(s)}">'+''.join(o)+'</g>'
def lines(ss,x,y,z=40,c=INK,font='display',leading=1.06):return ''.join(text(s,x,y+i*z*leading,z,c,font) for i,s in enumerate(ss))
def vector(name,x,y,w):
 global serial
 serial+=1;s=(S/(name+'.svg')).read_text();vw,vh=map(float,re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',s).groups());inside=s[re.search(r'<svg\b[^>]*>',s).end():s.rindex('</svg>')]
 for ident in re.findall(r'\bid="([^"]+)"',inside):inside=inside.replace(ident,f'art-{serial}-{ident}')
 return f'<defs><clipPath id="viewport-{serial}"><rect width="{vw}" height="{vh}"/></clipPath></defs><g transform="translate({x} {y}) scale({w/vw})"><g clip-path="url(#viewport-{serial})">{inside}</g></g>'
def logo(x,y,w,white=False):return vector('logo-horizontal-white-original' if white else 'logo-horizontal-colour-original',x,y,w)
def icon(x,y,w,white=False):return vector('icon-white-original' if white else 'icon-colour-original',x,y,w)
def photo(name,x,y,w,h):
 im=Image.open(G/(name+'.png')).convert('RGB');iw,ih=im.size;ratio=w/h
 if iw/ih>ratio:
  cw=ih*ratio;im=im.crop(((iw-cw)/2,0,(iw+cw)/2,ih))
 else:
  ch=iw/ratio;im=im.crop((0,(ih-ch)/2,iw,(ih+ch)/2))
 im.thumbnail((1800,1800),Image.Resampling.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=93,optimize=True)
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/jpeg;base64,{b64encode(b.getvalue()).decode()}"/>'
def stroke(d,c=GREEN,sw=4):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def save(name,w,h,a,title):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{a}</svg>';ET.fromstring(s);(M/f'{name}.svg').write_text(s);shutil.copy2(M/f'{name}.svg',W/f'{name}.svg')
 d=fitz.open(stream=s.encode(),filetype='svg');pix=d[0].get_pixmap(matrix=fitz.Matrix(1800/w,1800/w),alpha=False);im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB');im.save(M/f'{name}.png')
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(W/f'{name}-{size}.webp',quality=89,method=6)
 manifest.append({'name':name,'width':w,'height':h,'kind':'original concept artwork','title':title})

def face(x,y,w,h,category,name,desc,size,colour,variant=''):
 global serial
 serial+=1;clip=f'face-{serial}';a=f'<defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath></defs>'
 a+=rect(x,y,w,h,'#FFFEF7',12)+logo(x+55,y+45,w-110)+line(x+55,y+235,x+w-55,y+235,GREEN,.8)
 a+=text(category,x+55,y+290,19,GREEN,'body')
 a+=lines(name.split('|'),x+55,y+390,67,GREEN,leading=1.13)+text(desc,x+55,y+540,26,INK,'body')
 a+=f'<g clip-path="url(#{clip})">'+f'<path d="M{x} {y+h-145}Q{x+w*.3} {y+h-340} {x+w*.58} {y+h-145}Q{x+w*.8} {y+h-345} {x+w} {y+h-200}V{y+h}H{x}Z" fill="{colour}"/>'+'</g>'
 if variant:a+=text(variant,x+55,y+h-105,30,GREEN,'body')
 if size:a+=text(size,x+55,y+h-45,23,GREEN,'body')
 return a

# Precise flat artwork comes before material visualisation.
a=rect(0,0,1600,1050,MINT)+logo(100,130,950)+line(100,560,1500,560,GREEN,1)+text('Nature’s care. A familiar signature.',100,680,50,GREEN,'body')
for i,(c,label) in enumerate([(GREEN,'Deep green / #006837'),(LIME,'Leaf green / #8CC63F'),(INK,'Tagline grey / #4D4D4D')]):
 x=100+i*500;a+=rect(x,790,420,65,c)+text(label,x,920,22,INK,'body')
save('identity-study',1600,1050,a,'Exact original Natoral identity and verified source colours')
a=rect(0,0,1800,1100,MINT)+logo(85,70,570)+text('One signature. Four worlds.',85,350,76,GREEN,'body')
families=[('01','BODY','Dewskin','Softmelt',LIME),('02','HAIR','Root Ritual','Curl Veil','#DDE8CE'),('03','BABY','First Spoon','Little Drops',PINK),('04','ACTIVE','Form Daily','Vanilla / Cocoa',BLUE)]
for i,(n,cat,one,two,c) in enumerate(families):
 x=85+i*435;a+=line(x,470,x+370,470,GREEN)+text(n,x,535,23,GREEN,'body')+text(cat,x,610,26,GREEN,'body')+text(one,x,745,44,GREEN)+text(two,x,805,30,GREEN,'body')+rect(x,885,370,80,c)
a+=text('Proposed product architecture / Portfolio development',85,1040,21,INK,'body')
save('range-architecture',1800,1100,a,'Natoral body, hair, baby and active nutrition proposed range architecture')
boards=[('body-faces','BODY','Dewskin','Body lotion','250 ml',LIME,'Softmelt','Body butter','200 g',LIME),('hair-faces','HAIR','Root|Ritual','Shampoo','250 ml','#DDE8CE','Curl|Veil','Leave-in conditioner','200 ml','#DDE8CE'),('baby-faces','BABY FOOD','First|Spoon','Baby cereal','400 g',PINK,'Little|Drops','Baby supplement','',LILAC),('active-faces','ACTIVE NUTRITION','Form|Daily','Protein blend','500 g',BLUE,'Form|Daily','Protein blend','500 g','#E7C8B5')]
for slug,cat,n1,d1,s1,c1,n2,d2,s2,c2 in boards:
 a=rect(0,0,1600,1200,WHITE)+text('natoral / '+slug.split('-')[0],80,75,24,GREEN,'body')
 a+=face(100,150,620,900,cat,n1,d1,s1,c1,'Vanilla' if slug=='active-faces' else '')
 a+=face(880,150,620,900,'BABY SUPPLEMENT' if slug=='baby-faces' else cat,n2,d2,s2,c2,'Cocoa' if slug=='active-faces' else '')
 a+=text('Proposed front faces / Concept names and nominal sizes',100,1150,21,INK,'body')
 save(slug,1600,1200,a,'Natoral '+slug.split('-')[0]+' proposed product label faces')
a=rect(0,0,1600,1100,MINT)+text('The shape of the family.',80,130,68,GREEN,'body')
for row in range(3):
 for col in range(7):a+=icon(-90+col*270,260+row*250,215)
a+=rect(940,280,580,690,WHITE)+logo(1010,350,440)+lines(['A small mark.','A wider world.'],1010,690,50,GREEN,'body')
save('pattern-study',1600,1100,a,'Original Natoral symbol used in a new supporting repeat study')
a=rect(0,0,1600,1100,MINT)+rect(90,130,900,800,WHITE)+logo(180,210,690)+lines(['A little care,','for the everyday.'],180,630,65,GREEN,'body')+text('nature’s care',180,840,28,INK,'body')
a+=rect(1100,130,400,400,GREEN)+icon(1180,230,240,True)+rect(1100,630,400,300,LIME)+text('natoral',1150,815,65,GREEN)
save('dispatch-details',1600,1100,a,'Natoral dispatch note and brand seal artwork')
a=rect(0,0,1600,1050,WHITE)+text('Clear names.',85,150,85,GREEN,'body')+text('A generous character.',85,270,85,GREEN,'body')+text('Dewskin',85,520,140,GREEN)+text('Root Ritual',85,690,112,GREEN)
a+=line(85,805,1515,805,GREEN)+text('Cherry Bomb One / Original wordmark family',85,890,25,INK,'body')+text('Rubik / Supporting information',85,955,25,INK,'body')
save('type-study',1600,1050,a,'Natoral original Cherry Bomb One and licensed Rubik supporting typography')
if '--flats-only' in sys.argv:
 print('Prepared nine Natoral flat compositions.');sys.exit(0)

for slug,src,copy,c in [('campaign-body','body-ritual',['A moment','for you.'],MINT),('campaign-hair','hair-ritual',['Your own','rhythm.'],'#DDE8CE'),('campaign-active','active-moment',['Room for','movement.'],BLUE)]:
 a=rect(0,0,1200,1500,c)+logo(70,55,500)+photo(src,0,440,1200,850)+lines(copy,70,305,76,GREEN,'body')+text('natoral / nature’s care',70,1410,27,GREEN,'body')
 save(slug,1200,1500,a,'Natoral '+slug.split('-')[1]+' campaign concept')
a=rect(0,0,1600,1200,MINT)+rect(70,70,690,1060,GREEN)+photo('body-ritual',70,70,690,650)+logo(120,790,500,True)+text('Care, in the everyday.',120,1035,37,WHITE,'body')
a+=rect(840,70,690,1060,BLUE)+photo('active-range',840,70,690,650)+logo(900,790,500)+text('Your pace. Your ritual.',900,1035,37,GREEN,'body')
save('digital-stories',1600,1200,a,'Natoral personal care and active nutrition digital story concepts')
a=rect(0,0,1200,1100,MINT)+photo('family-lineup',0,380,1200,720)+logo(70,65,850)+text('Nature’s care. In your day.',70,330,36,GREEN,'body')
save('project-cover',1200,1100,a,'Natoral dedicated portfolio product-family cover')
for size in [640,1280]:shutil.copy2(W/f'project-cover-{size}.webp',R/f'dist/assets/natoral-cover-{size}.webp')
for p in sorted(G.glob('*.png')):
 im=Image.open(p).convert('RGB');w,h=im.size
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(W/f'{p.stem}-{size}.webp',quality=89,method=6)
 manifest.append({'name':p.stem,'width':w,'height':h,'kind':'AI-assisted concept visualisation'})
for name in ['logo-horizontal-colour-original','logo-horizontal-white-original','logo-stacked-colour-original','icon-colour-original','icon-white-original']:
 shutil.copy2(S/(name+'.svg'),W/(name+'.svg'))
im=Image.open(S/'page-03.png').convert('RGB');w,h=im.size
for size in [640,1280,1800]:
 out=im.copy();out.thumbnail((size,size),Image.Resampling.LANCZOS);out.save(W/f'original-usage-{size}.webp',quality=90,method=6)
manifest.append({'name':'original-usage','width':w,'height':h,'kind':'original supplied work'})
for name,f in fonts.items():
 sub=subset.Subsetter();sub.populate(unicodes=list(range(32,256))+[8211,8212,8216,8217,8220,8221,8230]);sub.subset(f);f.flavor='woff2';f.save(W/f'natoral-{name}.woff2')
lic=(R/'Assets/Fonts/Rubik/OFL.txt').read_text();copyright=next(n.toUnicode() for n in TTFont(S/'CherryBombOne-Regular.ttf')['name'].names if n.nameID==0)
ofl='SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007'+lic.split('SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007',1)[1]
(W/'FONT-LICENSE.txt').write_text('Rubik\n'+lic+'\n\nCherry Bomb One\n'+copyright+'\n\n'+ofl)
(W/'artwork-manifest.json').write_text(json.dumps({'palette':{'green':GREEN,'lime':LIME,'grey':INK,'mint':MINT},'artworks':manifest},indent=2)+'\n')
tiles=[]
for p in sorted(M.glob('*.png')):
 im=Image.open(p);im.thumbnail((380,390));t=Image.new('RGB',(400,430),MINT);t.paste(im,((400-im.width)//2,0));ImageDraw.Draw(t).text((10,407),p.stem,fill=INK);tiles.append(t)
sheet=Image.new('RGB',(1600,430*((len(tiles)+3)//4)),WHITE)
for i,t in enumerate(tiles):sheet.paste(t,((i%4)*400,(i//4)*430))
sheet.save(M/'review-contact-sheet.jpg',quality=94)
print(f'Prepared {len(tiles)} native Natoral compositions and {len(manifest)-len(tiles)} supporting images.')
