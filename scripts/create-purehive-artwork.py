"""Pure Hive portfolio concept artwork. Exact supplied identity; all new text outlined in OFL Nunito."""
from pathlib import Path
from base64 import b64encode
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools import subset
from PIL import Image, ImageDraw
import pymupdf as fitz
import io,re,json,shutil,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];S=R/'artwork/purehive/source';G=R/'artwork/purehive/generated';M=R/'artwork/purehive/masters';W=R/'dist/assets/purehive'
M.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
LEMON,AMBER,ORANGE,RED,PAPER,INK='#FCEF91','#FB9E3A','#F97C00','#E6521F','#FFF9ED','#29231D'
fonts={k:instantiateVariableFont(TTFont(S/'Nunito-VariableFont_wght.ttf'),{'wght':v},inplace=False) for k,v in [('body',500),('display',900)]};serial=0;manifest=[]
def rect(x,y,w,h,c,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x,y,x2,y2,c=INK,sw=1):return f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
def width(s,z,font='display'):
 f=fonts[font];g=f.getGlyphSet();c=f.getBestCmap();return sum(g[c.get(ord(ch),'.notdef')].width for ch in s)*z/f['head'].unitsPerEm
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
def logo(x,y,w,vertical=False):return vector('logo-vertical-colour-original' if vertical else 'logo-horizontal-colour-original',x,y,w)
def photo(name,x,y,w,h,fit='xMidYMid slice'):
 im=Image.open(G/(name+'.png')).convert('RGB');iw,ih=im.size;ratio=w/h
 if iw/ih>ratio:
  cw=ih*ratio;im=im.crop(((iw-cw)/2,0,(iw+cw)/2,ih))
 else:
  ch=iw/ratio;im=im.crop((0,(ih-ch)/2,iw,(ih+ch)/2))
 im.thumbnail((1800,1800),Image.Resampling.LANCZOS);b=io.BytesIO();im.save(b,'JPEG',quality=93,optimize=True)
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{fit}" href="data:image/jpeg;base64,{b64encode(b.getvalue()).decode()}"/>'
def flow(x,y,w,h,c=ORANGE):
 return f'<path transform="translate({x} {y}) scale({w/1000} {h/300})" fill="{c}" d="M0 40C150-55 260 125 420 65S710 0 1000 55V300H0Z"/>'
def hexagon(x,y,r,c=ORANGE,sw=2):
 import math
 pts=' '.join(f'{x+r*math.cos(math.pi/3*i-math.pi/2):.2f},{y+r*math.sin(math.pi/3*i-math.pi/2):.2f}' for i in range(6))
 return f'<polygon points="{pts}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
def save(name,w,h,a,title):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{a}</svg>';ET.fromstring(s);(M/f'{name}.svg').write_text(s);shutil.copy2(M/f'{name}.svg',W/f'{name}.svg')
 d=fitz.open(stream=s.encode(),filetype='svg');pix=d[0].get_pixmap(matrix=fitz.Matrix(1800/w,1800/w),alpha=False);im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB');im.save(M/f'{name}.png')
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(W/f'{name}-{size}.webp',quality=89,method=6)
 manifest.append({'name':name,'width':w,'height':h,'kind':'original concept artwork','title':title})
# The identity stays exact. New graphic devices support it; they do not replace it.
a=rect(0,0,1600,1050,PAPER)+logo(130,190,1040)+vector('icon-colour-original',1280,160,160)
a+=text('A little golden moment.',130,670,92)+line(130,760,1470,760,INK,.7)
for i,(c,label) in enumerate([(LEMON,'Lemon'),(AMBER,'Amber'),(ORANGE,'Orange'),(RED,'Ember')]):
 x=130+i*335;a+=rect(x,820,300,90,c)+text(label,x,960,20,INK,'body')+text(c,x+300,960,17,INK,'body','end')
save('identity-study',1600,1050,a,'Pure Hive exact original identity and four-colour palette')
# Face artwork only, not a regulatory-ready packaging file.
a=rect(0,0,1600,1100,LEMON)+text('One identity. Different touchpoints.',80,110,52)+text('LABEL FACE / GIFT SLEEVE / LID SEAL',80,170,19,INK,'body')
a+=rect(90,310,820,510,PAPER)+logo(390,340,220,True)+flow(90,690,820,130,ORANGE)
a+=rect(1010,270,480,650,ORANGE)+logo(1115,330,270,True)+flow(1010,750,480,170,AMBER)
a+=text('Wrap-label face',90,1000,23,INK,'body')+text('Gift sleeve face',1010,1000,23,INK,'body')
save('label-system',1600,1100,a,'Pure Hive new label and gift sleeve face artwork')
a=rect(0,0,1500,1000,PAPER)+circle(410,450,280,ORANGE)+vector('icon-colour-original',265,287,290)
a+=circle(1120,450,280,LEMON)+logo(960,240,320,True)+text('A small detail,',90,870,54)+text('a familiar face.',90,940,54)
save('lid-seals',1500,1000,a,'Pure Hive circular lid seals with exact original mark')
a=rect(0,0,1600,1100,PAPER)+rect(80,160,650,790,ORANGE)+logo(230,240,350,True)+flow(80,710,650,240,AMBER)
a+=rect(830,160,690,790,LEMON)+text('A little golden',900,340,58)+text('moment.',900,415,58)+line(900,510,1450,510,INK,1)
a+=lines(['For the table.','For the tea.','For a moment together.'],900,620,33,INK,'body',1.7)+logo(900,785,320)
save('gift-note',1600,1100,a,'Pure Hive gift sleeve and table note concept')
# Three campaign posters, each grounded in a different lived moment.
a=rect(0,0,1200,1500,PAPER)+photo('breakfast-modern',0,0,1200,800)+lines(['Good mornings','are for sharing.'],60,990,96)+logo(60,1290,400)+flow(820,1270,380,230,ORANGE)
save('campaign-breakfast',1200,1500,a,'Pure Hive shared breakfast campaign concept')
a=rect(0,0,1200,1500,LEMON)+photo('tea-modern',420,0,780,1150)+logo(60,70,310)+lines(['Take','a little','time.'],55,390,112)+flow(0,1120,1200,380,ORANGE)+text('A little golden moment.',60,1370,55)
save('campaign-tea',1200,1500,a,'Pure Hive everyday tea campaign concept')
a=rect(0,0,1200,1500,RED)+photo('pour-modern',0,390,1200,850)+logo(60,65,380)+text('Make it golden.',60,315,111,INK)+text('Pure Hive Honey',60,1390,35,INK,'body')
save('campaign-pour',1200,1500,a,'Pure Hive honey pour campaign concept')
a=rect(0,0,1600,1050,PAPER)+photo('pour-modern',0,0,800,1050)+rect(800,0,800,1050,LEMON)+logo(870,80,300)
a+=lines(['A spoonful.','A slow moment.'],870,430,68)+text('A little golden moment.',870,650,26,INK,'body')
for x,y in [(950,830),(1037,880),(1124,830),(1211,880),(1298,830)]:a+=hexagon(x,y,52,ORANGE,3)
save('table-card',1600,1050,a,'Pure Hive table card and food detail concept')
a=rect(0,0,1600,1200,LEMON)+rect(70,65,690,1070,PAPER)+photo('tea-modern',70,65,690,740)+logo(120,860,290)+text('Take a little time.',120,1060,48)
a+=rect(840,65,690,1070,ORANGE)+logo(900,130,350)+lines(['Good','mornings,','together.'],900,520,92)+flow(840,900,690,235,AMBER)
save('digital-stories',1600,1200,a,'Pure Hive vertical digital campaign story concepts')
a=rect(0,0,1200,1100,PAPER)+photo('jar-modern',480,0,720,1100,'xMidYMid slice')+logo(45,70,350)
a+=lines(['A little','golden','moment.'],45,470,79)+text('PURE HIVE HONEY',45,995,19,INK,'body')
save('project-cover',1200,1100,a,'Pure Hive dedicated portfolio cover')
for size in [640,1280]:shutil.copy2(W/f'project-cover-{size}.webp',R/f'dist/assets/purehive-cover-{size}.webp')
for p in sorted(G.glob('*.png')):
 im=Image.open(p).convert('RGB');w,h=im.size
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(W/f'{p.stem}-{size}.webp',quality=88,method=6)
 manifest.append({'name':p.stem,'width':w,'height':h,'kind':'AI-assisted concept visualisation'})
for name in ['logo-horizontal-colour-original','logo-vertical-colour-original','icon-colour-original']:
 shutil.copy2(S/(name+'.svg'),W/(name+'.svg'))
# Original jar artwork, kept as a historical work sample, never a new claims source.
p=S/'supplied-Honey Jar 1.png';im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,PAPER);bg.alpha_composite(im);im=bg.convert('RGB');w,h=im.size
for size in [640,1280,1800]:
 out=im.copy();out.thumbnail((size,size),Image.Resampling.LANCZOS);out.save(W/f'jar-original-{size}.webp',quality=88,method=6)
manifest.append({'name':'jar-original','width':w,'height':h,'kind':'original supplied application'})
f=TTFont(S/'Nunito-VariableFont_wght.ttf');sub=subset.Subsetter();sub.populate(unicodes=list(range(32,256))+[8211,8212,8216,8217,8220,8221,8230,8594]);sub.subset(f);f.flavor='woff2';f.save(W/'nunito-variable.woff2')
license=(R/'Assets/Fonts/Rubik/OFL.txt').read_text().split('SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007',1)[1]
(W/'FONT-LICENSE.txt').write_text('Copyright 2014 The Nunito Project Authors (https://github.com/googlefonts/nunito)\n\nSIL OPEN FONT LICENSE Version 1.1 - 26 February 2007'+license)
(W/'artwork-manifest.json').write_text(json.dumps({'palette':[LEMON,AMBER,ORANGE,RED],'artworks':manifest},indent=2))
tiles=[]
for p in M.glob('*.png'):
 im=Image.open(p);im.thumbnail((380,390));t=Image.new('RGB',(400,430),PAPER);t.paste(im,((400-im.width)//2,0));ImageDraw.Draw(t).text((10,408),p.stem,fill=INK);tiles.append(t)
sheet=Image.new('RGB',(1600,430*((len(tiles)+3)//4)),PAPER)
for i,t in enumerate(tiles):sheet.paste(t,((i%4)*400,(i//4)*430))
sheet.save(M/'review-contact-sheet.jpg',quality=93)
print(f'Prepared {len(tiles)} Pure Hive artwork compositions; {len(manifest)} total pieces.')
