"""Build original, portable Beans Central artwork from the supplied identity.

Run with Python + fonttools, brotli, Pillow and PyMuPDF. Native sources stay in
artwork/beans-central; web-ready art is committed under dist/assets/beans-central.
All type in the SVG masters is outlined. Logos retain the original PDF paths.
"""
from pathlib import Path
from base64 import b64encode
from xml.sax.saxutils import escape
import json, re, shutil, io
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image, ImageOps, ImageDraw
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'artwork/beans-central/source'
MASTERS = ROOT/'artwork/beans-central/masters'
WEB = ROOT/'dist/assets/beans-central'
GENERATED = ROOT/'artwork/beans-central/generated'
for p in (MASTERS, WEB): p.mkdir(parents=True, exist_ok=True)
RED, GOLD, BROWN, CREAM = '#E0012E', '#DB8A1F', '#2D120E', '#FFF7E7'
fonts = {k: TTFont(SRC/v) for k,v in {'bold':'Fredoka-Bold.ttf','medium':'Fredoka-Medium.ttf','body':'Quicksand_Book.otf'}.items()}
serial = 0

def rect(x,y,w,h,c,rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'

def circle(x,y,r,c): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def text(s,x,y,size=40,c=BROWN,font='bold',anchor='start',spacing=0):
    f=fonts[font]; gs=f.getGlyphSet(); cmap=f.getBestCmap(); up=f['head'].unitsPerEm
    scale=size/up; glyphs=[cmap.get(ord(ch),'.notdef') for ch in s]
    width=sum(gs[g].width*scale+spacing for g in glyphs)-spacing
    if anchor=='middle': x-=width/2
    if anchor=='end': x-=width
    out=[]
    for g in glyphs:
        pen=SVGPathPen(gs);gs[g].draw(pen)
        out.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale:.5f} {-scale:.5f})"/>')
        x+=gs[g].width*scale+spacing
    return f'<g fill="{c}" aria-label="{escape(s)}">'+''.join(out)+'</g>'

def lines(ss,x,y,size=40,c=BROWN,font='bold',leading=1.03,anchor='start'):
    return ''.join(text(s,x,y+i*size*leading,size,c,font,anchor) for i,s in enumerate(ss))

def img(file,x,y,w,h,fit='xMidYMid meet'):
    mime='image/svg+xml' if str(file).endswith('.svg') else 'image/png'
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{fit}" href="data:{mime};base64,{b64encode(Path(file).read_bytes()).decode()}"/>'

def logo(x,y,w,icon=False):
    # Embed exact vector paths, isolated IDs, not a re-created mark.
    global serial
    serial+=1
    s=(SRC/('icon-colour-original.svg' if icon else 'logo-colour-original.svg')).read_text()
    root=s[s.index('<svg'):]; inside=root[root.index('>')+1:root.rindex('</svg>')]
    vw,vh=map(float,re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',s).groups())
    inside=re.sub(r'(clip_\d+)',rf'bc{serial}_\1',inside)
    return f'<g transform="translate({x} {y}) scale({w/vw})">{inside}</g>'

def bean(x,y,scale=1,angle=0,c=BROWN,stroke=False):
    # Supporting ingredient illustration. Deliberately distinct from the logo.
    d='M-47,-14 C-60,-66 5,-76 42,-40 C77,-7 48,59 2,66 C-42,73 -73,34 -47,-14 Z'
    return f'<g transform="translate({x} {y}) rotate({angle}) scale({scale})"><path d="{d}" fill="{"none" if stroke else c}" stroke="{c if stroke else "none"}" stroke-width="4"/><path d="M-27,-37 C9,-23 -23,18 17,42" fill="none" stroke="{c if stroke else CREAM}" stroke-width="3" stroke-linecap="round"/></g>'

def rings(x,y,start,colour,count=5,gap=18):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{start+i*gap}" fill="none" stroke="{colour}" stroke-width="2"/>' for i in range(count))

manifest=[]
def save(name,w,h,art,title):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{art}</svg>'
    (MASTERS/f'{name}.svg').write_text(s)
    # MuPDF reads data-URI images and original vector paths; all typography is paths.
    doc=fitz.open(stream=s.encode(),filetype='svg')
    pix=doc[0].get_pixmap(matrix=fitz.Matrix(1600/w,1600/w),alpha=False)
    im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    im.save(MASTERS/f'{name}.png')
    shutil.copy2(MASTERS/f'{name}.svg',WEB/f'{name}.svg')
    for size in (640,1280,1600):
        out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS)
        out.save(WEB/f'{name}-{size}.webp',quality=88,method=6)
    manifest.append({'name':name,'width':w,'height':h,'title':title,'kind':'original vector artwork','svg':f'{name}.svg'})

dishes=[
 {'slug':'honey-akara','name':'Honey Akara','headline':['The golden','hour.'],'desc':['Golden bean fritters.','Crisp outside. Soft inside.'],'bg':RED,'fg':CREAM},
 {'slug':'beans-porridge','name':'Beans Porridge','headline':['Comfort,','by the bowl.'],'desc':['Beans, palm oil, pepper.','A familiar kind of comfort.'],'bg':GOLD,'fg':BROWN},
 {'slug':'ewa-agoyin','name':'Ewa Agoyin','headline':['Soft beans.','Bold company.'],'desc':['Creamy beans.','Caramelised pepper sauce.'],'bg':CREAM,'fg':RED},
 {'slug':'rice-and-beans','name':'Rice & Beans','headline':['Better','together.'],'desc':['Two everyday favourites.','One very good plate.'],'bg':BROWN,'fg':CREAM},
 {'slug':'waakye','name':'Waakye','headline':['A bowl with','more to say.'],'desc':['Rice, beans and all','the good company.'],'bg':RED,'fg':CREAM},
 {'slug':'moi-moi','name':'Moi Moi','headline':['A softer','side of beans.'],'desc':['Steamed bean pudding.','Comfort in another form.'],'bg':CREAM,'fg':BROWN},
]
for i,d in enumerate(dishes):
    bg,fg=d['bg'],d['fg'];a=rect(0,0,900,1125,bg)
    # Each dish has a different composition inside a shared typographic grammar.
    if i==0:
        a+=rings(685,565,285,CREAM,4,21)+lines(d['headline'],58,190,112,fg)
        a+=img(SRC/f'food-{d["slug"]}-original.png',200,380,660,610)
    elif i==1:
        a+=rings(890,100,130,BROWN,5,25)+lines(d['headline'],55,190,104,fg)
        a+=circle(450,650,300,CREAM)+img(SRC/f'food-{d["slug"]}-original.png',220,415,460,460)
        a+=bean(75,600,.46,-30,RED)+bean(808,847,.6,20,BROWN)
    elif i==2:
        a+=lines(d['headline'],55,195,105,fg)+rect(0,375,900,625,RED)
        a+=rings(450,685,290,CREAM,3,20)+img(SRC/f'food-{d["slug"]}-original.png',145,385,610,610)
    elif i==3:
        a+=lines(d['headline'],55,205,136,fg)+circle(630,737,330,GOLD)
        a+=img(SRC/f'food-{d["slug"]}-original.png',185,440,605,605)
        a+=bean(95,650,.62,-20,GOLD,True)
    elif i==4:
        a+=rect(0,0,220,1125,GOLD)+lines(d['headline'],65,190,104,BROWN)
        a+=circle(525,680,300,CREAM)+img(SRC/f'food-{d["slug"]}-original.png',275,425,500,500)
        a+=bean(96,665,.7,-25,BROWN,True)
    else:
        a+=rings(10,1125,360,GOLD,7,30)+lines(d['headline'],55,200,109,fg)
        a+=bean(780,385,.7,35,RED,True)+img(SRC/f'food-{d["slug"]}-original.png',200,425,500,500)
    # Logo is on an unprinted cream field, maintaining its colour integrity.
    a+=rect(0,995,900,130,CREAM)+logo(44,1017,140)
    a+=text(d['name'],855,1045,32,BROWN,anchor='end')+text('There’s more to beans.',855,1081,23,BROWN,'body',anchor='end')
    save('campaign-'+d['slug'],900,1125,a,d['name']+' — original campaign extension')

# Menu: clear reading hierarchy, actual supplied dishes, deliberately no prices,
# ordering phone, dietary claims or invented operational information.
a=rect(0,0,1200,1600,CREAM)+rect(0,0,1200,410,RED)
a+=rect(65,54,210,130,CREAM,12)+logo(85,68,168)
a+=lines(['There’s more','to beans.'],65,266,112,CREAM)+text('THE MENU',1130,87,23,CREAM,'body',anchor='end',spacing=3)
for i,d in enumerate(dishes):
    col=i%2;row=i//2;x=65+col*590;y=470+row*335
    a+=text(d['name'],x,y+44,40,BROWN)
    a+=lines(d['desc'],x,y+110,20,BROWN,'body',leading=1.5)
    a+=img(SRC/f'food-{d["slug"]}-original.png',x+270,y+72,220,220)
    a+=f'<path d="M{x} {y+312}H{x+500}" stroke="{GOLD}" stroke-width="1.5"/>'
a+=text('Good food. Many ways.',65,1555,38,RED)+bean(1110,1535,.33,40,BROWN)
save('menu',1200,1600,a,'Beans Central — six-dish menu concept')

# Brand graphics: ingredient shape, plate arcs and a restrained ingredient repeat.
a=rect(0,0,1600,1000,CREAM)+rect(0,0,800,1000,RED)
a+=lines(['One ingredient.','Many moods.'],65,155,81,CREAM)
a+=rings(400,710,210,CREAM,6,25)+bean(400,695,2.5,-25,GOLD)
for r in range(5):
    for c in range(5): a+=bean(855+c*170+(r%2)*50,55+r*205,.62,(r+c)*47,BROWN,True)
save('graphic-language',1600,1000,a,'Ingredient illustrations and plate-line graphic language')

# Print-ready flat label concepts: composition, not a generic mockup.
a=rect(0,0,1600,1000,CREAM)
a+=rect(60,65,620,870,GOLD)+lines(['There’s','more to','beans.'],110,235,130,BROWN,leading=1.05)+logo(280,700,150,True)
a+=text('BOWL SLEEVE / FRONT',110,899,20,BROWN,'body',spacing=2)
a+=rect(740,65,800,365,RED)+rect(790,110,280,175,CREAM,10)+logo(815,133,230)
a+=text('Good food.',1120,210,58,CREAM)+text('Many ways.',1120,271,58,CREAM)
a+=text('CARTON PANEL',790,386,20,CREAM,'body',spacing=2)
a+=circle(925,670,170,RED)+circle(925,670,124,CREAM)+logo(857,606,136,True)
a+=text('SEAL',925,899,20,BROWN,'body',anchor='middle',spacing=2)
a+=rect(1150,500,390,320,CREAM)
for r in range(2):
    for c in range(3): a+=bean(1195+c*130,555+r*165,.48,30*(c+r),BROWN,True)
a+=text('TISSUE REPEAT',1345,899,20,BROWN,'body',anchor='middle',spacing=2)
save('packaging-artwork',1600,1000,a,'Original bowl sleeve, carton panel, seal and tissue print artwork')

# Tall takeaway carrier face with a curved, plate-inspired base.
a=rect(0,0,900,1125,CREAM)+logo(170,255,560)
a+=f'<path d="M0 760C320 650 495 980 900 815V1125H0Z" fill="{GOLD}"/>'
a+=text('Good food.',68,1010,77,BROWN)+text('Many ways.',68,1085,77,BROWN)
a+=bean(750,1025,.85,25,BROWN,True)
save('carrier-artwork',900,1125,a,'Beans Central carrier bag — flat artwork')

# Type specimen in the real brand families; exact original logo displayed separately.
a=rect(0,0,1600,1000,BROWN)+text('FREDOKA',65,98,24,GOLD,'body',spacing=5)
a+=lines(['Full of beans.','Full of character.'],65,270,145,CREAM,leading=1.08)
a+=f'<path d="M65 530H1535" stroke="{GOLD}" stroke-width="1"/>'
a+=text('QUICKSAND',65,600,24,GOLD,'body',spacing=5)
a+=lines(['Familiar food. A fresh point of view.','A little warmth. A lot of personality.'],65,700,51,CREAM,'body',leading=1.5)
a+=text('Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm',65,920,39,GOLD,'body')
save('typography',1600,1000,a,'Fredoka display and Quicksand body typography')

# Hero campaign: a designed composition rather than a bare food photograph.
a=img(GENERATED/'meal-scene.png',0,0,1600,1067,'xMidYMid slice')
a+=rect(62,57,250,160,CREAM,8)+logo(87,80,200)
a+=lines(['There’s','more to','beans.'],60,420,110,CREAM,leading=.98)
a+=text('Ewa Agoyin & Honey Akara',65,992,29,CREAM,'body')
save('hero-campaign',1600,1067,a,'There’s more to beans — hero food campaign concept')

# The Works carousel uses a near-square crop. Give it a dedicated composition
# so the full logo and message remain visible, rather than cropping the hero.
a=rect(0,0,1200,1100,CREAM)+logo(60,54,370)
a+=lines(['Good food.','Many ways.'],660,140,76,BROWN)
a+=img(GENERATED/'meal-scene.png',0,340,1200,800,'xMidYMid slice')
save('project-cover',1200,1100,a,'Beans Central — dedicated portfolio project cover')

# Digital story composition: two intentionally different vertical campaign layouts.
a=rect(0,0,1600,1100,BROWN)+rect(90,65,620,970,RED,24)+rect(790,65,720,970,CREAM,24)
a+=rect(115,90,170,110,CREAM,8)+logo(125,99,150)+lines(['Your next','good bite.'],130,340,98,CREAM)
a+=rings(390,740,230,CREAM,3,17)+img(SRC/'food-honey-akara-original.png',130,490,500,490)
a+=text('Honey Akara',130,987,26,CREAM,'body')
a+=logo(840,100,150)+text('SIX WAYS',840,325,24,RED,'body',spacing=3)
a+=lines(['to love','beans.'],835,443,115,BROWN)
for i,d in enumerate(dishes):
    x=875+(i%3)*205;y=640+(i//3)*225
    a+=img(SRC/f'food-{d["slug"]}-original.png',x-25,y-10,180,180)
    a+=text(d['name'],x+65,y+185,18,BROWN,'body',anchor='middle')
save('digital-stories',1600,1100,a,'Vertical campaign and six-dish digital story concepts')

# Optimised photo exports, original transparent dishes, and exact identity files.
for name in ('meal-scene','packaging-family','carry-bag'):
    im=Image.open(GENERATED/f'{name}.png').convert('RGB');w,h=im.size
    for size in (640,1280,1600):
        out=im.copy();out.thumbnail((size,size*h/w),Image.Resampling.LANCZOS)
        out.save(WEB/f'{name}-{size}.webp',quality=87,method=6)
    manifest.append({'name':name,'width':w,'height':h,'title':name,'kind':'AI-assisted concept visualisation'})
for d in dishes:
    im=Image.open(SRC/f'food-{d["slug"]}-original.png').convert('RGBA')
    im.thumbnail((650,650),Image.Resampling.LANCZOS);im.save(WEB/f'food-{d["slug"]}.webp',quality=90,method=6)
for name in ('logo-colour-original','icon-colour-original'):
    shutil.copy2(SRC/f'{name}.svg',WEB/f'{name}.svg')
f=fonts['medium'];f.flavor='woff2';f.save(WEB/'fredoka-medium.woff2')
ofl=(ROOT/'Assets/Fonts/Rubik/OFL.txt').read_text().split('SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007',1)[1]
(WEB/'FONT-LICENSE.txt').write_text('Copyright 2016 The Fredoka Project Authors (https://github.com/hafontia/Fredoka-One)\n\nSIL OPEN FONT LICENSE Version 1.1 - 26 February 2007'+ofl)
(WEB/'artwork-manifest.json').write_text(json.dumps({'artworks':manifest,'dishes':dishes,'palette':{'red':RED,'ochre':GOLD,'brown':BROWN,'paper':CREAM}},indent=2))

# Local review contact sheet, not shipped to the website.
thumbs=[]
for item in manifest:
    p=MASTERS/f'{item["name"]}.png'
    if not p.exists(): continue
    im=Image.open(p);im.thumbnail((380,400))
    tile=Image.new('RGB',(400,440),'#e8e3d7');tile.paste(im,((400-im.width)//2,10))
    ImageDraw.Draw(tile).text((12,417),item['name'],fill='black');thumbs.append(tile)
sheet=Image.new('RGB',(1600,440*((len(thumbs)+3)//4)),'white')
for i,t in enumerate(thumbs):sheet.paste(t,((i%4)*400,(i//4)*440))
sheet.save(MASTERS/'review-contact-sheet.jpg',quality=90)
print(f'Prepared {len(manifest)} artworks and visualisations; six exact source food cutouts; portable vector masters.')
