"""Original LizCraft application artwork. Run with Pillow/fontTools/Brotli/PyMuPDF.

Exact identity paths and supplied wording are the source of truth. Text is
outlined; photographs are optimised embedded images. Original files stay local.
"""
from pathlib import Path
from base64 import b64encode
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools import subset
from PIL import Image, ImageDraw
import pymupdf as fitz
import io, re, json, shutil
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'artwork/lizcraft/source'; GEN=ROOT/'artwork/lizcraft/generated'
MASTER=ROOT/'artwork/lizcraft/masters'; WEB=ROOT/'dist/assets/lizcraft'
MASTER.mkdir(parents=True,exist_ok=True);WEB.mkdir(parents=True,exist_ok=True)
BLUE,GOLD,PAPER,INK='#065784','#D2A857','#F5EFE3','#183C4B'
upright=SRC/'Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf'
italic=SRC/'Fraunces-Italic-VariableFont_SOFT,WONK,opsz,wght.ttf'
fonts={k:instantiateVariableFont(TTFont(p),{'opsz':72,'wght':weight,'SOFT':30,'WONK':1},inplace=False) for k,p,weight in [('display',upright,400),('italic',italic,400),('bold',upright,600)]}
fonts['body']=TTFont(ROOT/'Assets/Fonts/Rubik/static/Rubik-Regular.ttf')
serial=0; manifest=[]

def rect(x,y,w,h,c,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def line(x1,y1,x2,y2,c=BLUE,sw=1):return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
def circle(x,y,r,c):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def width(s,size,font='display'):
 f=fonts[font];g=f.getGlyphSet();m=f.getBestCmap();return sum(g[m.get(ord(ch),'.notdef')].width for ch in s)*size/f['head'].unitsPerEm
def text(s,x,y,size=40,c=BLUE,font='display',anchor='start',spacing=0):
 f=fonts[font];g=f.getGlyphSet();m=f.getBestCmap();scale=size/f['head'].unitsPerEm
 w=width(s,size,font)+(len(s)-1)*spacing
 if anchor=='middle':x-=w/2
 if anchor=='end':x-=w
 out=[]
 for ch in s:
  glyph=m.get(ord(ch),'.notdef');pen=SVGPathPen(g);g[glyph].draw(pen)
  out.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale:.6f} {-scale:.6f})"/>');x+=g[glyph].width*scale+spacing
 return f'<g fill="{c}" aria-label="{escape(s)}">'+''.join(out)+'</g>'
def lines(ss,x,y,size=40,c=BLUE,font='display',leading=1.12,anchor='start'):
 return ''.join(text(s,x,y+i*size*leading,size,c,font,anchor) for i,s in enumerate(ss))
def wrap(s,max_width,size,font='body'):
 result=[];current=''
 for word in s.split():
  nxt=(current+' '+word).strip()
  if current and width(nxt,size,font)>max_width:result.append(current);current=word
  else:current=nxt
 if current:result.append(current)
 return result
def paragraph(s,x,y,max_width,size=23,c=INK,font='body',leading=1.55):
 ss=wrap(s,max_width,size,font);return lines(ss,x,y,size,c,font,leading),y+len(ss)*size*leading
def img(path,x,y,w,h,fit='xMidYMid meet'):
 im=Image.open(path).convert('RGB');im.thumbnail((1800,1800),Image.Resampling.LANCZOS)
 buf=io.BytesIO();im.save(buf,format='JPEG',quality=94,optimize=True)
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{fit}" href="data:image/jpeg;base64,{b64encode(buf.getvalue()).decode()}"/>'
def vector(name,x,y,w,colour=None,opacity=1):
 global serial
 serial+=1;s=(SRC/(name+'.svg')).read_text();vw,vh=map(float,re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',s).groups())
 inside=s[s.index('>')+1:s.rindex('</svg>')]
 ids=re.findall(r'\bid="([^"]+)"',inside)
 for ident in ids:inside=inside.replace(ident,f'instance-{serial}-{ident}')
 if colour:inside=re.sub(r'fill="#[0-9A-Fa-f]{6}"',f'fill="{colour}"',inside)
 return f'<g opacity="{opacity}" fill="{colour or BLUE}" transform="translate({x} {y}) scale({w/vw})">{inside}</g>'
def logo(x,y,w,kind='horizontal',colour=None):
 # Use the supplied compound-path monochrome variant for reversed marks. This
 # retains the L knockout instead of merging a coloured L into its background.
 variant='black' if colour else 'colour'
 return vector(f'icon-{variant}-original' if kind=='icon' else f'logo-{kind}-{variant}-original',x,y,w,colour)
def contour(x,y,w,c=BLUE,opacity=1):return vector('contour-pattern-original',x,y,w,c,opacity)
def thread(d,c=BLUE,sw=2):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
def save(name,w,h,art,title):
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{art}</svg>'
 ET.fromstring(svg) # Deliver portable, strictly valid XML masters, not only PNGs.
 (MASTER/f'{name}.svg').write_text(svg);shutil.copy2(MASTER/f'{name}.svg',WEB/f'{name}.svg')
 doc=fitz.open(stream=svg.encode(),filetype='svg');pix=doc[0].get_pixmap(matrix=fitz.Matrix(1800/w,1800/w),alpha=False)
 im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB');im.save(MASTER/f'{name}.png')
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(WEB/f'{name}-{size}.webp',quality=89,method=6)
 manifest.append({'name':name,'width':w,'height':h,'title':title,'kind':'original application artwork','master':f'{name}.svg'})

# Signature composition: exact mark; generous space and quiet information.
a=rect(0,0,1600,1000,PAPER)+logo(150,340,950)+line(1250,120,1250,880,BLUE,.8)+logo(1323,322,190,'icon')
a+=text('A QUIET',1310,670,17,BLUE,'body',spacing=2)+text('CONFIDENCE.',1310,700,17,BLUE,'body',spacing=2)
a+=text('LizCraft',80,90,20,BLUE,'body')+text('THE ORIGINAL IDENTITY',1520,90,16,BLUE,'body',anchor='end',spacing=2)
a+=text('Blue  #065784',80,930,20,BLUE,'body')+text('Gold  #D2A857',600,930,20,BLUE,'body')
a+=rect(1190,905,130,40,BLUE)+rect(1320,905,200,40,GOLD)
save('signature-study',1600,1000,a,'LizCraft original signature, monogram and palette')

a=rect(0,0,1600,1100,BLUE)+text('FRAUNCES',80,90,17,PAPER,'body',spacing=4)
a+=lines(['A little time.'],80,310,150,PAPER)+lines(['A lot of care.'],80,480,150,GOLD,'italic')
a+=line(80,590,1520,590,GOLD,1)+text('Soft curves. A little character.',80,710,65,PAPER)
a+=lines(['Round shoulders, expressive terminals and an unhurried rhythm.','Fraunces carries the warmth of the original identity.'],80,800,25,PAPER,'body',1.7)
a+=text('Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm',80,1000,40,GOLD)
save('type-study',1600,1100,a,'LizCraft Fraunces display typography study')

# Deliberately different pattern densities, always using the source contour.
a=rect(0,0,1600,1100,PAPER)+rect(800,0,800,1100,BLUE)
a+=text('A thread,',70,160,100,BLUE)+text('carried through.',70,270,100,BLUE,'italic')
a+=contour(-180,490,850,BLUE)+contour(860,-360,1200,GOLD)
a+=rect(0,990,800,110,PAPER)+rect(800,990,800,110,BLUE)+text('Quiet detail',70,1050,24,BLUE,'body')+text('Expressive surface',870,1050,24,PAPER,'body')
save('contour-study',1600,1100,a,'Two scales of the exact original contour pattern')

# Gratitude: preserve the original maker's wording, without inventing a founder.
a=rect(0,0,1500,1000,BLUE)+contour(650,-330,1150,GOLD,.8)+logo(80,78,230,'horizontal',PAPER)
a+=text('Thank you',80,555,152,PAPER)+text('for trusting us.',85,643,46,PAPER,'italic')
a+=line(85,820,700,820,GOLD,1.5)+text('A little time. A lot of care.',85,885,26,PAPER,'body')
save('thank-you-front',1500,1000,a,'LizCraft thank-you card front concept')
a=rect(0,0,1500,1000,PAPER)+contour(1090,520,800,BLUE,.13)+logo(1135,65,270)
a+=text('Hello,',90,220,100,BLUE)
copy1='Thank you so much for your order! Every stitch in this piece was made with care and intention. I’m so excited for this to become a part of your wardrobe.'
copy2='When you wear lizcraft, you’re supporting a dream and the art of handmade craft. I hope you love wearing it as much as I loved creating it.'
t,y=paragraph(copy1,95,340,1040,29,BLUE);a+=t;t,y=paragraph(copy2,95,y+45,1040,29,BLUE);a+=t
a+=text('With gratitude,',95,795,27,BLUE,'body')+text('LizCraft',95,885,55,BLUE,'italic')
save('thank-you-back',1500,1000,a,'LizCraft thank-you card back with the original maker’s message')

# A five-instruction care foldout. Source instructions preserved verbatim.
def care_icon(kind,x,y):
 d={'wash':'M-43 10 L-31 47 H33 L45 10 M-30 19 Q-15 29 0 19 T30 19 M-15 -29 V2 Q-10 12 2 8 L20 -8 M-15 -28 Q-13 -40 -6 -30 L9 -12 M-2 -30 L14 -13 M11 -24 L27 -7',
 'soap':'M-30 -12 Q-36 -17 -36 -2 V33 Q-36 43 -22 43 H23 Q36 43 36 30 V-1 Q36 -14 23 -14 Z M-18 -14 V-31 H17 V-14 M-22 12 Q0 -2 23 12 M-21 22 Q1 8 23 22',
 'bleach':'M0 -38 L44 40 H-44 Z M-44 -42 L44 46',
 'iron':'M-42 28 Q-24 -1 10 -1 H38 V34 H-42 Z M-8 -1 V-25 Q15 -38 33 -14 M-44 -42 L44 46',
 'machine':'M-39 -42 H39 V43 H-39 Z M-39 -20 H39 M-24 -31 H-9 M14 -31 H23 M0 -10 A21 21 0 1 1 -1 -10 M-49 -48 L49 50'}[kind]
 return f'<g transform="translate({x} {y})">'+thread(d,BLUE,2.5)+'</g>'
a=rect(0,0,1800,1050,PAPER)+rect(0,0,600,1050,BLUE)+logo(80,70,245,'horizontal',PAPER)
a+=lines(['Keep the','care going.'],70,390,96,PAPER,'display',1.1)+contour(-100,650,720,GOLD)
a+=text('Crochet care',70,620,27,PAPER,'body')+line(600,50,600,1000,GOLD)+line(1200,50,1200,1000,GOLD)
care=[('wash','Hand wash gently'),('soap','Use mild soap'),('bleach','Do not bleach'),('machine','Do not machine wash'),('iron','Do not iron')]
for i,(kind,label) in enumerate(care):
 x=665+(i//3)*600;y=145+(i%3)*270;a+=care_icon(kind,x+55,y+12)
 ss=wrap(label,380,37);a+=lines(ss,x+130,y+8,37,BLUE)
 if i%3<2:a+=line(x,y+145,x+450,y+145,GOLD,.9)
a+=logo(1280,875,330)+text('For the pieces you love.',1280,1000,24,BLUE,'italic')
save('care-foldout',1800,1050,a,'LizCraft care foldout with all five original care instructions')

# Contour-shaped hangtags, garment label and practical piece card.
tag='M85 0 H360 Q415 0 425 55 L480 410 Q492 475 430 490 L130 555 Q65 570 50 505 L0 135 Q-10 60 55 24 Z'
a=rect(0,0,1500,1200,PAPER)
for x,y,angle,bg,fg in [(170,110,-9,BLUE,PAPER),(810,220,8,GOLD,BLUE)]:
 a+=f'<g transform="translate({x} {y}) rotate({angle} 240 275)"><path d="{tag}" fill="{bg}"/>'+circle(213,42,8,PAPER)
 if bg==BLUE:a+=logo(120,145,240,'vertical',PAPER)
 else:a+=lines(['A little time.','A lot of care.'],65,245,50,BLUE,'italic')+text('Made by hand.',65,395,22,BLUE,'body')+logo(65,420,250)
 a+='</g>'
a+=thread('M445 118C385 25 318 45 330 113S482 235 437 290',GOLD,3)
a+=thread('M1050 278C1100 120 1250 205 1190 298',BLUE,2)
a+=text('The small things, considered.',95,1100,65,BLUE,'italic')
save('hangtags',1500,1200,a,'LizCraft contour-shaped hangtag front and reverse concept')

a=rect(0,0,1600,1000,PAPER)+text('Close to the piece.',80,140,85,BLUE,'italic')
a+=rect(100,300,1400,280,'#FFFDF8')+line(135,320,135,560,BLUE,.8)+line(1465,320,1465,560,BLUE,.8)+logo(450,360,700)
a+=text('Woven label / artwork',100,660,21,BLUE,'body')
a+=rect(100,745,600,175,BLUE)+logo(185,785,430,'horizontal',PAPER)
a+=text('Made by hand.',850,805,50,BLUE)+text('A little time. A lot of care.',850,870,28,BLUE,'italic')
save('woven-label-artwork',1600,1000,a,'LizCraft woven label and small-format signature artwork')

a=rect(0,0,1600,1100,PAPER)+rect(0,0,1050,1100,BLUE)
for x,y,w in [(-350,-400,1250),(550,500,1050)]:a+=contour(x,y,w,GOLD,.78)
a+=rect(1050,0,550,1100,PAPER)+text('Wrapped with',1120,130,43,BLUE)+text('a little care.',1120,190,43,BLUE,'italic')
a+=circle(1325,470,155,GOLD)+logo(1220,360,210,'icon')
a+=rect(1130,730,390,230,BLUE)+logo(1170,790,310,'horizontal',PAPER)
a+=text('Tissue · seal · parcel band',1120,1045,19,BLUE,'body')
save('wrap-and-seal',1600,1100,a,'LizCraft original tissue repeat, seal and parcel band artwork')

a=rect(0,0,1000,1250,PAPER)+logo(200,180,600,'vertical')
a+=contour(540,720,780,BLUE)+text('Made by hand.',80,1045,50,BLUE,'italic')+text('A little time. A lot of care.',80,1135,23,BLUE,'body')
save('carrier-artwork',1000,1250,a,'LizCraft cream carrier artwork with exact original contour and signature')

# Campaign art: three purposes, three compositions, one voice.
a=rect(0,0,1200,1500,PAPER)+img(GEN/'making.png',0,400,1200,1100,'xMaxYMid slice')
a+=logo(70,50,310)+text('A little time.',70,230,110,BLUE)+text('A lot of care.',70,340,110,BLUE,'italic')
save('campaign-making',1200,1500,a,'LizCraft making campaign — a little time, a lot of care')
a=img(GEN/'wearing.png',0,0,1200,1500,'xMidYMid slice')+rect(0,1130,1200,370,PAPER)
a+=lines(['Made by hand.','Worn your way.'],65,1260,100,BLUE,'display',1.03)+logo(835,1400,300)
save('campaign-wearing',1200,1500,a,'LizCraft wearing campaign — made by hand, worn your way')
a=rect(0,0,1200,1500,BLUE)+logo(70,70,340,'horizontal',PAPER)+contour(390,-50,1100,GOLD,.62)
a+=lines(['Keep the','care going.'],70,760,132,PAPER,'display',1.08)+text('For the pieces you love.',75,1120,43,PAPER,'italic')
a+=line(75,1240,1125,1240,GOLD,1)+text('Hand wash gently. Use mild soap.',75,1330,26,PAPER,'body')+text('A little time. A lot of care.',75,1430,18,PAPER,'body')
save('campaign-care',1200,1500,a,'LizCraft care campaign — keep the care going')

# Vertical digital compositions: a material-led story and a quiet note.
a=rect(0,0,1600,1200,PAPER)+rect(65,65,700,1070,BLUE)
a+=img(GEN/'making.png',65,65,700,700,'xMaxYMid slice')+logo(110,820,230,'horizontal',PAPER)
a+=lines(['Every stitch,','with intention.'],110,975,62,PAPER,'italic')
a+=rect(835,65,700,1070,BLUE)+contour(1070,-120,720,GOLD,.55)+logo(890,115,230,'horizontal',PAPER)
a+=lines(['Hello,','there’s care','in this parcel.'],890,650,74,PAPER,'display',1.07)
a+=text('A small thank-you, from LizCraft.',890,1035,23,PAPER,'body')
save('digital-stories',1600,1200,a,'LizCraft material-led digital story and personal parcel note')

# Near-square carousel cover: readable at the existing site's card proportions.
a=rect(0,0,1200,1100,PAPER)+img(GEN/'wearing.png',490,0,710,1100,'xMidYMid slice')+logo(55,70,365)
a+=lines(['A little','time.'],55,420,103,BLUE)+lines(['A lot','of care.'],55,670,103,BLUE,'italic')
a+=contour(-140,895,480,BLUE,.4)
save('project-cover',1200,1100,a,'LizCraft dedicated portfolio cover')
for size in [640,1280]:shutil.copy2(WEB/f'project-cover-{size}.webp',ROOT/f'dist/assets/lizcraft-cover-{size}.webp')

# Photo exports are used directly where the image itself tells the story.
for p in sorted(GEN.glob('*.png')):
 im=Image.open(p).convert('RGB');w,h=im.size
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(WEB/f'{p.stem}-{size}.webp',quality=88,method=6)
 manifest.append({'name':p.stem,'width':w,'height':h,'title':p.stem,'kind':'AI-assisted concept visualisation'})
for name in ['logo-horizontal-colour-original','logo-vertical-colour-original','icon-colour-original','contour-pattern-original']:
 shutil.copy2(SRC/f'{name}.svg',WEB/f'{name}.svg')
# Preserve selected supplied pieces as explicitly original work, not new photography.
for name in ['bags-blue-gold-mockup-original','thank-you-front-original','thank-you-back-original','crochet-care-instructions-original']:
 im=Image.open(SRC/f'{name}.png').convert('RGB');w,h=im.size
 for size in [640,1280,1800]:
  out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS);out.save(WEB/f'{name}-{size}.webp',quality=88,method=6)
 manifest.append({'name':name,'width':w,'height':h,'title':name,'kind':'original supplied application'})
for name in ['display','italic']:
 f=fonts[name];opts=subset.Options();sub=subset.Subsetter(options=opts);sub.populate(unicodes=list(range(32,256))+[8211,8212,8216,8217,8220,8221,8230]);sub.subset(f);f.flavor='woff2';f.save(WEB/f'fraunces-{name}.woff2')
ofl=(ROOT/'Assets/Fonts/Rubik/OFL.txt').read_text().split('SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007',1)[1]
copyright=next(n.toUnicode() for n in TTFont(upright)['name'].names if n.nameID==0)
(WEB/'FONT-LICENSE.txt').write_text(copyright+'\n\nSIL OPEN FONT LICENSE Version 1.1 - 26 February 2007'+ofl)
(WEB/'artwork-manifest.json').write_text(json.dumps({'palette':{'blue':BLUE,'gold':GOLD,'paper':PAPER},'artworks':manifest,'care_instructions':[x[1] for x in care]},indent=2))
tiles=[]
for p in MASTER.glob('*.png'):
 im=Image.open(p);im.thumbnail((380,400));tile=Image.new('RGB',(400,440),'#e3ded2');tile.paste(im,((400-im.width)//2,0));ImageDraw.Draw(tile).text((10,418),p.stem,fill='black');tiles.append(tile)
sheet=Image.new('RGB',(1600,440*((len(tiles)+3)//4)),'white')
for i,t in enumerate(tiles):sheet.paste(t,((i%4)*400,(i//4)*440))
sheet.save(MASTER/'review-contact-sheet.jpg',quality=92)
print(f'Prepared {len(tiles)} original vector compositions and {len(manifest)-len(tiles)} supporting visuals/source pieces.')
