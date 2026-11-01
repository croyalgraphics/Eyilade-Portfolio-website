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
R=Path(__file__).resolve().parents[1];S=R/'artwork/natoral/source';G=R/'artwork/natoral-supplied/generated';M=R/'artwork/natoral-supplied/masters';W=R/'dist/assets/natoral-supplied'
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
 im=Image.open((G if (G/(name+'.png')).exists() else M)/(name+'.png')).convert('RGB');iw,ih=im.size;ratio=w/h
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

# Originals are embedded byte-for-byte; only their SVG viewport is clipped to
# the product silhouette area so stray transparent canvas is not scaled as art.
P=R/'artwork/natoral-supplied/source'
BOX={1:(407,12,846,1241),2:(377,12,880,1246),3:(359,12,842,1238),4:(117,67,1135,1185),5:(202,20,1048,1233),6:(115,27,1145,1215),7:(217,12,1035,1243),8:(223,8,1022,1245)}
pngs={i:b64encode((P/f'N{i}.png').read_bytes()).decode() for i in BOX}
uses=[]
def pack(i,x,bottom,h,shadow=True):
 global serial
 serial+=1;l,t,r,b=BOX[i];scale=h/(b-t);w=(r-l)*scale;clip=f'pack-{serial}'
 a=''
 if shadow:
  for j in range(10):a+=f'<ellipse cx="{x+w/2}" cy="{bottom+2}" rx="{w*(.44+j*.014)}" ry="{3+j*1.5}" fill="#25201B" opacity=".018"/>'
 a+=f'<defs><clipPath id="{clip}"><rect width="{r-l}" height="{b-t}"/></clipPath></defs><g transform="translate({x} {bottom-h}) scale({scale})"><g clip-path="url(#{clip})"><image x="{-l}" y="{-t}" width="1254" height="1254" href="data:image/png;base64,{pngs[i]}"/></g></g>'
 uses.append({'source':f'N{i}.png','x':x,'baseline':bottom,'height':h})
 return a
def detail(i,x,y,w,h,bbox):
 global serial
 serial+=1;l,t,r,b=bbox;clip=f'detail-{serial}';scale=max(w/(r-l),h/(b-t))
 return f'<defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs><g clip-path="url(#{clip})"><g transform="translate({x} {y}) scale({scale})"><image x="{-l}" y="{-t}" width="1254" height="1254" href="data:image/png;base64,{pngs[i]}"/></g></g>'

ROSE,PLUM,CREAM,COBALT,TEAL,GOLD,BLACK='#F4CBD2','#700D2C','#FCF5E9','#07339C','#00695F','#F8C622','#101214'

# Large supplied-design boards, rather than reconstructed labels.
for slug,title,bg,ink,items in [
 ('body-faces','Dewskin / Softmelt',CREAM,PLUM,[(3,360,1040,840),(4,930,1040,650)]),
 ('hair-faces','Root Ritual / Curl Veil','#EEF7F5',COBALT,[(1,325,1040,850),(2,1000,1040,850)]),
 ('baby-faces','First Spoon / Little Drops','#FFF5DE',PLUM,[(5,210,1040,840),(6,870,1040,700)]),
 ('active-faces','Form Daily / Vanilla & Cocoa','#EDEDEA',BLACK,[(7,190,1040,830),(8,900,1040,830)])]:
 a=rect(0,0,1600,1200,bg)+text(title,80,85,42,ink,'body')+text('SUPPLIED PACKAGING DESIGNS',80,140,16,ink,'body')
 for i,x,base,h in items:a+=pack(i,x,base,h)
 a+=text('Natoral / Product artwork supplied by the designer',80,1150,20,ink,'body')
 save(slug,1600,1200,a,title+' supplied packaging artwork')

# Real photographic environments around unaltered supplied product images.
compositions=[
 ('body-ritual','body-scene',[(3,115,925,740),(4,415,925,450)],'Supplied Dewskin and Softmelt packaging in a fictional contemporary body-care scene'),
 ('hair-ritual','hair-scene',[(1,850,940,730),(2,1140,940,730)],'Supplied Root Ritual and Curl Veil packaging in a fictional contemporary haircare scene'),
 ('active-moment','gym-scene',[(7,890,885,490),(8,1220,885,465)],'Supplied Form Daily tubs in a fictional gym scene'),
 ('family-moment','family-scene',[(5,1160,748,350)],'Supplied First Spoon carton in a fictional modern family scene'),
 ('dispatch-set','dispatch-scene',[(3,105,920,700),(4,400,920,450)],'Supplied body-care packaging beside a burgundy mailer in a fictional unboxing scene')]
for name,scene,items,title in compositions:
 a=photo(scene,0,0,1536,1024)
 for i,x,base,h in items:a+=pack(i,x,base,h)
 save(name,1536,1024,a,title)
a=photo('studio-scene',0,0,1600,1100)+pack(5,200,980,830)+pack(6,930,980,620)
save('baby-range',1600,1100,a,'Supplied First Spoon and Little Drops packaging in a studio arrangement')
a=photo('studio-scene',0,0,1600,1100)+pack(7,230,975,840)+pack(8,930,975,780)
save('active-range',1600,1100,a,'Supplied Form Daily Vanilla and Cocoa tubs in a studio arrangement')
a=rect(0,0,1000,1200,'#F8E4E6')+pack(3,290,1130,1060)
save('label-detail',1000,1200,a,'Close-up of the exact supplied Dewskin packaging')

# Hero has every supplied design, not generated replacement packs.
a=photo('studio-scene',0,0,2400,1000)
items=[(1,65,860,470),(2,270,860,470),(3,510,860,550),(4,765,860,340),(5,1110,860,490),(6,1485,860,385),(7,1840,860,400),(8,2130,860,400)]
for i,x,base,h in items:a+=pack(i,x,base,h)
save('family-lineup',2400,1000,a,'All eight designer-supplied Natoral products together')

# Original identity remains historical context, never a replacement pack label.
for name,h in [('identity-study',1050),('pattern-study',1100)]:
 for ext in ['svg','png']:shutil.copy2(R/'artwork/natoral/masters'/f'{name}.{ext}',M/f'{name}.{ext}')
 for size in [640,1280,1800]:shutil.copy2(R/'dist/assets/natoral'/f'{name}-{size}.webp',W/f'{name}-{size}.webp')
 manifest.append({'name':name,'width':1600,'height':h,'kind':'original concept artwork'})

a=rect(0,0,1800,1550,'#FFFEFA')+text('Four worlds. One family.',75,115,65,GREEN,'body')
groups=[('BODY',CREAM,PLUM,[(3,150,740,430),(4,430,740,300)]),('HAIR','#DCEFF1',COBALT,[(1,1080,740,430),(2,1400,740,430)]),('BABY','#FFF0D1',PLUM,[(5,100,1380,460),(6,480,1380,350)]),('ACTIVE','#E7E7E3',BLACK,[(7,1040,1380,440),(8,1420,1380,440)])]
for j,(label,bg,ink,items) in enumerate(groups):
 x=(j%2)*900;y=200+(j//2)*620;a+=rect(x,y,900,620,bg)+text(label,x+40,y+65,20,ink,'body')
 for i,px,base,h in items:a+=pack(i,px,base,h)
a+=text('Designer-supplied packaging / N1–N8',75,1510,21,GREEN,'body')
save('range-architecture',1800,1550,a,'Supplied body hair baby and active nutrition packaging architecture')

# Close-ups showcase the actual supplied typography and illustration.
a=rect(0,0,1800,1200,CREAM)+text('Every detail. In place.',70,100,60,GREEN,'body')
for i,x,h in [(3,100,850),(1,520,850),(5,905,570),(7,1380,570)]:a+=pack(i,x,1040,h)
a+=text('Product names, hierarchy and illustration / Supplied artwork',70,1150,20,GREEN,'body')
save('type-study',1800,1200,a,'Supplied product lettering hierarchy and label illustrations')

# Category stationery supports the packs without proposing new labels.
a=rect(0,0,1600,1100,CREAM)+rect(100,100,840,880,ROSE)+logo(170,170,660)+lines(['A moment','for you.'],170,600,95,PLUM,'body')+text('Dewskin / Softmelt',170,875,24,PLUM,'body')+pack(3,1040,980,770)
save('dispatch-details',1600,1100,a,'Body-care thank-you note concept alongside the supplied Dewskin pack')

# Campaigns deliberately have their own compositions, always with supplied packs.
a=rect(0,0,1200,1500,ROSE)+photo('body-ritual',0,0,1200,800)+text('A moment',65,1080,112,PLUM,'body')+text('for you.',65,1220,112,PLUM,'body')+text('Dewskin / Softmelt',65,1420,24,PLUM,'body')
save('campaign-body',1200,1500,a,'Body-care campaign with the supplied Dewskin and Softmelt designs')
a=rect(0,0,1200,1500,COBALT)+text('YOUR OWN',60,150,105,GOLD,'body')+text('RHYTHM.',60,275,105,GOLD,'body')+photo('hair-ritual',0,390,1200,800)+text('ROOT RITUAL / CURL VEIL',60,1380,28,WHITE,'body')
save('campaign-hair',1200,1500,a,'Haircare campaign with supplied Root Ritual and Curl Veil designs')
a=rect(0,0,1200,1500,BLACK)+photo('active-moment',0,0,1200,800)+text('ROOM FOR',60,1090,112,WHITE,'body')+text('MOVEMENT.',60,1230,112,GOLD,'body')+line(60,1370,1140,1370,'#777',1)+text('FORM DAILY / ACTIVE NUTRITION',60,1450,24,WHITE,'body')
save('campaign-active',1200,1500,a,'Active nutrition campaign with the supplied Form Daily packaging')
a=rect(0,0,1600,1200,CREAM)+rect(60,60,700,1080,ROSE)+photo('body-ritual',60,180,700,467)+text('A moment',110,860,70,PLUM,'body')+text('for you.',110,950,70,PLUM,'body')+rect(840,60,700,1080,BLACK)+photo('active-range',840,180,700,481.25)+text('YOUR PACE.',890,860,67,WHITE,'body')+text('YOUR RITUAL.',890,970,67,GOLD,'body')
save('digital-stories',1600,1200,a,'Body and fitness digital compositions featuring supplied product artwork')
a=rect(0,0,1200,1100,'#F3FFF8')+logo(70,60,850)+text('Nature’s care. In your day.',70,325,36,GREEN,'body')+photo('family-lineup',0,450,1200,500)
save('project-cover',1200,1100,a,'Natoral portfolio cover featuring all eight supplied product designs')
for size in [640,1280]:shutil.copy2(W/f'project-cover-{size}.webp',R/f'dist/assets/natoral-cover-{size}.webp')
for name in ['logo-horizontal-colour-original','logo-horizontal-white-original','logo-stacked-colour-original','icon-colour-original','icon-white-original']:
 shutil.copy2(S/(name+'.svg'),W/(name+'.svg'))
for size in [640,1280,1800]:shutil.copy2(R/f'dist/assets/natoral/original-usage-{size}.webp',W/f'original-usage-{size}.webp')
old=json.loads((R/'dist/assets/natoral/artwork-manifest.json').read_text());manifest.append(next(a for a in old['artworks'] if a['name']=='original-usage'))
shutil.copy2(R/'dist/assets/natoral/FONT-LICENSE.txt',W/'FONT-LICENSE.txt')
# Public supplied PNGs make fidelity independently inspectable.
for i in BOX:shutil.copy2(P/f'N{i}.png',W/f'N{i}.png')
(W/'artwork-manifest.json').write_text(json.dumps({'revision':'owner-supplied-N1-N8','sources':json.loads((P/'manifest.json').read_text()),'artworks':manifest},indent=2)+'\n')
(M/'placement-records.json').write_text(json.dumps(uses,indent=2)+'\n')
tiles=[]
for p in sorted(M.glob('*.png')):
 im=Image.open(p);im.thumbnail((380,330));t=Image.new('RGB',(400,370),CREAM);t.paste(im,((400-im.width)//2,0));ImageDraw.Draw(t).text((10,347),p.stem,fill=INK);tiles.append(t)
sheet=Image.new('RGB',(1600,370*((len(tiles)+3)//4)),WHITE)
for i,t in enumerate(tiles):sheet.paste(t,((i%4)*400,(i//4)*370))
sheet.save(M/'review-contact-sheet.jpg',quality=94)
print(f'Prepared {len(tiles)} compositions using byte-identical N1–N8 supplied PNGs.')

