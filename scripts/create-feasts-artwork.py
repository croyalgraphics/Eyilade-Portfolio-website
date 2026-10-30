"""Feasts & Flavours event-catering concepts using exact source paths and licensed Fredoka."""
from pathlib import Path
from base64 import b64encode
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools import subset
from PIL import Image,ImageDraw
import pymupdf as fitz
import io,re,json,shutil,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];S=R/'artwork/feasts/source';G=R/'artwork/feasts/generated';M=R/'artwork/feasts/masters';W=R/'dist/assets/feasts'
M.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
RED,INK,WHITE,PINK='#E0012E','#333333','#FFFFFF','#FBE7ED'
fonts={k:TTFont(S/f'Fredoka-{v}.ttf',recalcTimestamp=False) for k,v in [('body','Regular'),('display','SemiBold')]};serial=0;manifest=[]
def rect(x,y,w,h,c,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x,y,x2,y2,c=RED,sw=1):return f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
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
def logo(x,y,w,white=False):return vector('logo-white-original' if white else 'logo-colour-original',x,y,w)
def icon(x,y,w,white=False):return vector('icon-white-original' if white else 'icon-red-original',x,y,w)
def photo(name,x,y,w,h):
 im=Image.open(G/(name+'.png')).convert('RGB');iw,ih=im.size;ratio=w/h
 if iw/ih>ratio:
  cw=ih*ratio;im=im.crop(((iw-cw)/2,0,(iw+cw)/2,ih))
 else:
  ch=iw/ratio;im=im.crop((0,(ih-ch)/2,iw,(ih+ch)/2))
 im.thumbnail((1800,1800),Image.Resampling.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=93,optimize=True)
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/jpeg;base64,{b64encode(b.getvalue()).decode()}"/>'
def stroke(d,c=RED,sw=4):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def serving(kind,x,y,scale=1,c=RED):
 # Original line illustrations for the service system, not additional logos.
 d={'cloche':'M4 65H156M20 65C20 10 140 10 140 65M72 22V12H88V22M12 78H148','plate':'M20 45C20 5 140 5 140 45C140 85 20 85 20 45M40 45C40 20 120 20 120 45C120 70 40 70 40 45','spoon':'M35 10C5 10 5 60 35 60C65 60 65 10 35 10M35 60V115M110 10V115M92 10V40Q110 65 128 40V10M110 10V45','glass':'M30 10H120L105 75Q75 100 45 75ZM75 90V120M50 120H100'}[kind]
 return f'<g transform="translate({x} {y}) scale({scale})">{stroke(d,c)}</g>'
def save(name,w,h,a,title):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{a}</svg>';ET.fromstring(s);(M/f'{name}.svg').write_text(s);shutil.copy2(M/f'{name}.svg',W/f'{name}.svg')
 d=fitz.open(stream=s.encode(),filetype='svg');pix=d[0].get_pixmap(matrix=fitz.Matrix(1800/w,1800/w),alpha=False);im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB');im.save(M/f'{name}.png')
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(W/f'{name}-{size}.webp',quality=89,method=6)
 manifest.append({'name':name,'width':w,'height':h,'kind':'original concept artwork','title':title})
# Identity and guest-facing details.
a=rect(0,0,1600,1050,WHITE)+logo(140,95,585)+rect(920,0,680,1050,RED)+logo(1090,195,350,True)
a+=text('Original, with appetite.',80,835,61,INK)+text('Red #E0012E',80,965,24,RED,'body')+text('Charcoal #333333',480,965,24,INK,'body')
save('identity-study',1600,1050,a,'Feasts and Flavours exact original identity and palette')
a=rect(0,0,1600,1100,PINK)+text('A familiar flourish.',80,130,79,RED)+text('From a small seal to the edge of a celebration.',80,200,28,INK,'body')
for row in range(3):
 for col in range(7):a+=icon(-70+col*260,340+row*250,210)
a+=rect(980,240,540,760,WHITE)+logo(1075,300,350)+line(1060,710,1440,710)+lines(['Professional catering','Parties & events'],1060,800,31,INK,'body',1.5)
save('pattern-language',1600,1100,a,'Original rosette repeated as a supporting border and pattern')
a=rect(0,0,1000,1400,WHITE)+rect(0,0,1000,500,RED)+logo(350,65,300,True)+text('For the occasion.',500,660,65,RED,anchor='middle')
a+=lines(['Curry bowl','Rice & chicken','Crispy chicken'],110,820,47,INK,'display',1.55)+line(110,1100,890,1100)+text('Professional catering',500,1190,29,INK,'body','middle')
a+=icon(430,1250,140)
save('menu-face',1000,1400,a,'Feasts table menu presentation concept without prices or claims')
a=rect(0,0,1600,1100,WHITE)+rect(80,160,970,370,RED)+logo(130,205,280,True)+lines(['Every occasion.','Full of flavour.'],520,320,58,WHITE)
a+=rect(80,660,970,240,PINK)+icon(120,705,160)+text('Something worth sharing.',330,800,47,RED)
a+=circle(1330,355,170,RED)+icon(1230,260,200,True)+circle(1330,790,170,PINK)+icon(1230,695,200)
a+=text('Tray band / small wrap',80,1000,22,INK,'body')+text('Closure seals',1160,1040,22,INK,'body')
save('wrap-and-seals',1600,1100,a,'Catering tray wrap, food band and closure seal artwork')
a=rect(0,0,1600,1100,PINK)+rect(80,130,600,840,RED)+logo(200,220,360,True)+text('For the occasion.',380,820,49,WHITE,anchor='middle')
a+=rect(780,130,740,840,WHITE)+icon(900,210,150)+lines(['A place for you.','A plate to enjoy.'],890,500,58,RED)+line(890,630,1410,630)+text('Professional catering',890,710,28,INK,'body')+text('Parties, events & intimate gatherings.',890,770,25,INK,'body')
save('guest-details',1600,1100,a,'Feasts guest table card and invitation to the meal concept')
a=rect(0,0,1600,1000,WHITE)+text('The little things, together.',80,125,68,RED)
for i,(kind,label) in enumerate([('cloche','The service'),('plate','The table'),('spoon','The details'),('glass','The gathering')]):
 x=90+i*390;a+=serving(kind,x+45,330,1.55)+text(label,x,700,32,INK,'body')
a+=text('Original line illustrations / Supporting service graphics',80,930,23,INK,'body')
save('service-illustrations',1600,1000,a,'Original catering-service line illustration family')
if '--flats-only' in sys.argv:
 print('Prepared six native flat concepts.');sys.exit(0)
# Food and campaign imagery.
a=rect(0,0,1600,1050,WHITE)+text('A little play.',80,135,100,RED)+text('A lot of presence.',80,255,100,RED)
a+=text('Fredoka',80,480,135,INK)+lines(['Rounded, generous, easy to read.','A clear supporting voice for the original wordmark.'],85,610,30,INK,'body',1.5)
a+=line(85,770,1515,770)+logo(85,835,170)+text('The supplied wordmark stays intact.',420,955,32,INK,'body')
save('type-study',1600,1050,a,'Fredoka supporting typography and exact source wordmark')
for name,src,label,headline in [('campaign-curry','curry-bowl','Curry bowl',['Pass it','around.']),('campaign-rice','rice-chicken','Rice & chicken',['Made for','the occasion.']),('campaign-crunch','crispy-chicken','Crispy chicken',['A little','more crunch.'])]:
 a=rect(0,0,1200,1500,RED if name!='campaign-rice' else WHITE)+photo(src,0,400,1200,850)
 a+=logo(55,50,255,name!='campaign-rice')+lines(headline,410,160,99,WHITE if name!='campaign-rice' else RED)
 a+=text(label,60,1380,40,WHITE if name!='campaign-rice' else INK)+icon(1000,1300,130,name!='campaign-rice')
 save(name,1200,1500,a,f'Feasts {label} campaign concept')
a=rect(0,0,1600,1100,RED)+photo('wedding-reception',0,0,1000,1100)+logo(1110,100,310,True)+lines(['Every','occasion.'],1080,650,83,WHITE)+text('Full of flavour.',1080,900,40,WHITE,'body')
save('event-campaign',1600,1100,a,'Feasts wedding and event service campaign concept')
a=rect(0,0,1600,1200,PINK)+rect(60,60,710,1080,RED)+photo('owanbe-service',60,60,710,650)+logo(110,770,260,True)+lines(['Bring on','the occasion.'],405,900,54,WHITE)
a+=rect(830,60,710,1080,WHITE)+logo(1045,120,280)+lines(['Professional','catering.'],900,650,78,RED)+text('Parties. Weddings. Birthdays.',900,920,30,INK,'body')
save('digital-stories',1600,1200,a,'Feasts event-led digital story concepts')
a=rect(0,0,1200,1100,RED)+photo('owanbe-service',450,0,750,1100)+logo(65,60,320,True)+lines(['Every','occasion.'],60,640,80,WHITE)+text('Full of flavour.',60,890,43,WHITE,'body')
save('project-cover',1200,1100,a,'Feasts dedicated event-catering portfolio cover')
for size in [640,1280]:shutil.copy2(W/f'project-cover-{size}.webp',R/f'dist/assets/feasts-cover-{size}.webp')
for p in sorted(G.glob('*.png')):
 im=Image.open(p).convert('RGB');w,h=im.size
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(W/f'{p.stem}-{size}.webp',quality=88,method=6)
 manifest.append({'name':p.stem,'width':w,'height':h,'kind':'AI-assisted concept visualisation'})
for name in ['logo-colour-original','logo-white-original','icon-red-original','icon-white-original']:
 shutil.copy2(S/(name+'.svg'),W/(name+'.svg'))
# The source identity guide establishes provenance without old flyer contact details.
im=Image.open(R/'Assets/Feast and flavours/Feast and flavours Brand guide.png').convert('RGB');w,h=im.size
for size in [640,1280,1800]:
 out=im.copy();out.thumbnail((size,size),Image.Resampling.LANCZOS);out.save(W/f'identity-guide-original-{size}.webp',quality=88,method=6)
manifest.append({'name':'identity-guide-original','width':w,'height':h,'kind':'original supplied identity guide'})
for name in ['body','display']:
 f=fonts[name];sub=subset.Subsetter();sub.populate(unicodes=list(range(32,256))+[8211,8212,8216,8217,8220,8221,8230]);sub.subset(f);f.flavor='woff2';f.save(W/f'fredoka-{name}.woff2')
license=(R/'Assets/Fonts/Rubik/OFL.txt').read_text().split('SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007',1)[1]
copyright=next(n.toUnicode() for n in TTFont(S/'Fredoka-Regular.ttf')['name'].names if n.nameID==0)
(W/'FONT-LICENSE.txt').write_text(copyright+'\n\nSIL OPEN FONT LICENSE Version 1.1 - 26 February 2007'+license)
(W/'artwork-manifest.json').write_text(json.dumps({'palette':{'red':RED,'charcoal':INK,'supporting_pink':PINK},'artworks':manifest},indent=2))
tiles=[]
for p in sorted(M.glob('*.png')):
 im=Image.open(p);im.thumbnail((380,390));t=Image.new('RGB',(400,430),PINK);t.paste(im,((400-im.width)//2,0));ImageDraw.Draw(t).text((10,407),p.stem,fill=INK);tiles.append(t)
sheet=Image.new('RGB',(1600,430*((len(tiles)+3)//4)),WHITE)
for i,t in enumerate(tiles):sheet.paste(t,((i%4)*400,(i//4)*430))
sheet.save(M/'review-contact-sheet.jpg',quality=93)
print(f'Prepared {len(tiles)} original Feasts compositions and {len(manifest)-len(tiles)} supporting images.')
