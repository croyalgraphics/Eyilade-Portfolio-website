from pathlib import Path
from PIL import Image, ImageOps, ImageChops
import subprocess,tempfile,json
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'dist/assets/logos';out.mkdir(parents=True,exist_ok=True)
tmp=Path(tempfile.mkdtemp(prefix='eyilade-logos-',dir='/private/tmp'))
p='/Users/joshuaoridamisi/Documents/Joshua/Career/Eyilade Oridamisi - Visual Designer Portfolio.pdf'
subprocess.run(['pdftoppm','-f','5','-singlefile','-scale-to','5400','-png',p,str(tmp/'sheet')],check=True,capture_output=True)
sheet=Image.open(tmp/'sheet.png').convert('RGB')
names=[('agrohub','Agrohub & Investment'),('beans-central','Beans Central'),('clenstreet','ClenStreet'),('docs-apothecary',"Doc’s Apothecary"),('efame','Efame Real Estate'),('feasts-and-flavours','Feasts & Flavours'),('genesis-orb','Genesis Orb'),('intelligentsia-orb','Intelligentsia Orb'),('lecco-inn','Lecco Inn'),('lizcraft','LizCraft'),('lizinterior','LizInterior'),('ppcl','PPCL'),('purehive','Pure Hive Honey'),('rebeks-savour','Rebeks Savour'),('swift-tern','Swift Tern Airways')]
xs=[(85,390),(410,710),(745,1055),(1080,1395),(1425,1735)]
ys=[(280,490),(570,785),(870,1080)]
def export(im,slug):
 diff=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda a:255 if a>35 else 0)
 box=diff.getbbox()
 if box:im=im.crop(box)
 im=ImageOps.contain(im,(760,610))
 canvas=Image.new('RGB',(1024,850),'white');canvas.paste(im,((1024-im.width)//2,(850-im.height)//2))
 canvas.save(out/(slug+'.webp'),'WEBP',quality=94,method=6)
for i,(slug,name) in enumerate(names):
 x1,x2=xs[i%5];y1,y2=ys[i//5]
 export(sheet.crop((x1*3,y1*3,x2*3,y2*3)),slug)
extra='/Users/joshuaoridamisi/Documents/Joshua/Graphic/CRG Project/Natoral/Natoral.ai'
subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','1400','-png',extra,str(tmp/'natoral')],check=True,capture_output=True)
# Natoral’s artwork has an intentional pale mint background; retain its full composition.
im=Image.open(tmp/'natoral.png').convert('RGB');im.thumbnail((1024,1024));im.save(out/'natoral.webp','WEBP',quality=94)
names.append(('natoral','Natoral'))
(ROOT/'content/logos.json').write_text(json.dumps([{'slug':s,'name':n,'image':'/assets/logos/'+s+'.webp'} for s,n in names],ensure_ascii=False,indent=2))
print('Prepared',len(names),'original logo artworks')
