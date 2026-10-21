"""Prepare only the visual-design assets supplied for the public portfolio.
Run with the bundled Python runtime. Original files are never changed.
"""
from pathlib import Path
import subprocess, tempfile, shutil, json
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/assets'
OUT.mkdir(parents=True,exist_ok=True)
TMP=Path(tempfile.mkdtemp(prefix='eyilade-assets-',dir='/private/tmp'))
BASE=Path('/Users/joshuaoridamisi/Documents/Joshua/Graphic/CRG Project')
PORT=Path('/Users/joshuaoridamisi/Documents/Joshua/Career/Eyilade Oridamisi - Visual Designer Portfolio.pdf')
Image.MAX_IMAGE_PIXELS=None
manifest=[]

def save(im,name,widths=(640,1280)):
    im=im.convert('RGB')
    for width in widths:
        img=ImageOps.contain(im,(width,width*3)) if im.width>width else im
        path=OUT/f'{name}-{width}.webp'
        img.save(path,'WEBP',quality=86,method=6)
    manifest.append({'asset':name,'source_size':list(im.size)})

def image_file(p,name,widths=(640,1280)):
    with Image.open(p) as im:save(ImageOps.exif_transpose(im),name,widths)

def art(p,page,name,crop=None):
    target=TMP/name
    subprocess.run(['pdftoppm','-f',str(page),'-singlefile','-scale-to','1800','-png',str(p),str(target)],check=True,capture_output=True)
    im=Image.open(str(target)+'.png').convert('RGB')
    if crop:im=im.crop(tuple(int(v*s) for v,s in zip(crop,[im.width,im.height,im.width,im.height])))
    save(im,name)

image_file('/Users/joshuaoridamisi/Documents/blue.png','lizcraft-blue')
image_file('/Users/joshuaoridamisi/Documents/white.png','lizcraft-white')
image_file('/Users/joshuaoridamisi/Desktop/My Passport pics.jpg','portrait')
for name,page in [('lizcraft-mark',5),('lizcraft-type',7),('lizcraft-system',4),('lizcraft-pattern',8)]:
    art(BASE/'Lizcraft rebranding/LizCraft/LizCraft.ai',page,name)
for name,page in [('natoral-mark',1),('natoral-lockup',2),('natoral-colour',3),('natoral-pattern',4)]:
    art(BASE/'Natoral/Natoral.ai',page,name)
for name,page in [('beans-mark',2),('beans-system',5),('beans-akara',6),('beans-porridge',7),('beans-agoyin',8),('beans-rice',9)]:
    art(BASE/'Tobi Product/Beans Central.ai',page,name)
for name,page in [('feasts-mark',3),('feasts-system',5),('feasts-curry',6),('feasts-rice',7),('feasts-table',8),('feasts-chicken',9)]:
    art(BASE/'Tobi Product/Feast and Flavours.ai',page,name)
for page,name in [(6,'purehive-intro'),(7,'purehive-world'),(9,'swift-world'),(11,'rebeks-world'),(12,'social-collection'),(13,'carex-social'),(14,'medimax-social'),(15,'cocoa-world'),(16,'wedding-world'),(17,'editorial-world'),(18,'music-world'),(20,'coca-cola-world'),(21,'carex-3d-world')]:
    art(PORT,page,name,(.035,.15,.965,.91))
# Export the supplied original image layers for selected hero images.
r=PdfReader(PORT)
for page,name,index in [(7,'purehive-jar',0),(15,'cocoa-pack',0),(20,'coca-cola-study',0),(21,'carex-study',0)]:
    im=r.pages[page-1].images[index].image
    save(im,name)
image_file(BASE/'Genesis Orb/Brand Identity/Artboard 1 copy.png','genesis-logo')
image_file(BASE/'Genesis Orb/Brand Identity/4.png','genesis-colour')
# Label art is presented as graphic design, without manufacturing claims.
labels=BASE/"DOC's A/New Labels/Final Print"
for p,name in [(labels/'Hair/Herbal Bomb oil.pdf','docs-herbal'),(labels/'Skin/Lipsluxe.pdf','docs-lips'),(labels/'Skin/INCANDESCENCE (WHIPPED SHEA BUTTER).pdf','docs-shea')]:
    art(p,1,name)
shutil.copyfile('/Users/joshuaoridamisi/Documents/HBD Opemidun.mp4',OUT/'birthday-motion.mp4')
# Curated public portfolio: exclude the index and logo sheets containing a private idea.
writer=PdfWriter()
for page in [0,*range(5,22)]:writer.add_page(r.pages[page])
writer.add_metadata({'/Title':'Selected Visual Design — Eyilade Oridamisi','/Author':'Eyilade Oridamisi'})
with (OUT/'Eyilade-Oridamisi-Selected-Work.pdf').open('wb') as f:writer.write(f)
# A public CV edition excludes named internal initiatives and private concepts.
c=canvas.Canvas(str(OUT/'Eyilade-Oridamisi-CV.pdf'),pagesize=(595,842))
c.setTitle('Eyilade J. Oridamisi — CV');c.setAuthor('Eyilade Oridamisi')
c.setFillColor(HexColor('#f5f3ed'));c.rect(0,0,595,842,fill=1,stroke=0)
c.setFillColor(HexColor('#2445dc'));c.setFont('Helvetica-Bold',29)
c.drawString(42,785,'EYILADE J. ORIDAMISI')
c.setFillColor(HexColor('#20201e'));c.setFont('Helvetica',10)
c.drawString(42,760,'SENIOR GRAPHIC DESIGNER  /  EXPERIENCE DESIGN  /  CREATIVE PROTOTYPING')
c.drawString(42,736,'eyilade@gmail.com  |  linkedin.com/in/eyiladeoridamisi')
c.drawString(42,720,'behance.net/eyiladeoridamisi  |  Nigeria')
y=684
def title(t):
    global y
    c.setFillColor(HexColor('#2445dc'));c.setFont('Helvetica-Bold',10);c.drawString(42,y,t);y-=21
def body(t):
    global y
    c.setFillColor(HexColor('#20201e'));c.setFont('Helvetica',10.5)
    for line in simpleSplit(t,'Helvetica',10.5,505):c.drawString(42,y,line);y-=15
    y-=10
title('PROFILE')
body('Senior Graphic Designer at PwC Nigeria with 5+ years of professional design experience. Combines visual design, stakeholder discovery, experience design and a Computer Science background. Uses AI-assisted prototyping to explore and develop ideas into functional digital experiences.')
title('EXPERIENCE')
for heading,date,text in [
('Senior Graphic Designer — PwC Nigeria','July 2025 - present','Lead concepts and execution for campaigns, presentations, reports and branded experiences. Clarify stakeholder needs, present design rationale and guide junior designers.'),
('Graphic Designer — PwC Nigeria','February 2022 - June 2025','Created campaign assets, corporate communications, print-ready reports and presentations. Supported motion design with Adobe After Effects.'),
('Graphic Designer — Redot Digital Marketing and Consultancy Agency','March 2021 - January 2022','Developed campaign visuals, social content, wireframes and interactive prototypes across client accounts.')]:
    c.setFillColor(HexColor('#20201e'));c.setFont('Helvetica-Bold',10.5);c.drawString(42,y,heading);y-=16
    c.setFont('Helvetica',9);c.drawString(42,y,date);y-=19;body(text)
title('CAPABILITIES')
body('Brand identity and visual systems; editorial and presentation design; visual and interaction design; wireframing and prototyping; stakeholder collaboration; creative direction; AI-assisted development.')
title('TOOLS & EDUCATION')
body('Adobe Illustrator, Photoshop, InDesign and After Effects. Microsoft PowerPoint and SharePoint. AI-assisted design and development workflows.')
body('BSc Computer Science — Lagos State University. Certifications: Fundamentals of Graphic Design (CalArts); Data-driven Decision Making (PwC); AI for Business Professionals (HP LIFE).')
c.save()
(ROOT/'docs/ASSET_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print(f'Prepared {len(manifest)} public image groups, motion clip and curated downloads.')
