"""Package selected contemporary concept artwork, preserving prior deliveries."""
from pathlib import Path
import zipfile,json,hashlib,sys
R=Path(__file__).resolve().parents[1]
sets=[('purehive','Pure-Hive-Honey-Artwork-2026-10-30.zip',['jar-modern','breakfast-modern','tea-modern','gift-modern','pour-modern'],['logo-horizontal-colour-original','logo-vertical-colour-original','icon-colour-original']),('lizcraft','LizCraft-Modern-Collection-2026-10-30.zip',['dress-modern','woman-modern','man-modern','family-modern','objects-modern','making-modern','parcel-open-modern','parcel-closed-modern','woven-label'],['logo-horizontal-colour-original','logo-vertical-colour-original','icon-colour-original','contour-pattern-original'])]
sets.append(('feasts','Feasts-and-Flavours-Catering-Artwork-2026-10-30.zip',['owanbe-service','wedding-reception','professional-service','birthday-celebration','guest-table','takeaway-service','shared-table','rice-chicken','crispy-chicken','curry-bowl','pass-a-bowl'],['logo-colour-original','logo-white-original','icon-red-original','icon-white-original']))
for brand,name,photos,identity in sets:
 if len(sys.argv)>1 and brand!=sys.argv[1]:continue
 root=R/'artwork'/brand;out=R/'output'/brand/name;out.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((root/'masters').glob('*')):
   if p.suffix in ['.svg','.png']:z.write(p,'masters/'+p.name)
  for n in photos:z.write(root/'generated'/(n+'.png'),'concept-photography/'+n+'.png')
  for n in identity:z.write(root/'source'/(n+'.svg'),'original-identity/'+n+'.svg')
  z.write(R/'dist/assets'/brand/'FONT-LICENSE.txt','FONT-LICENSE.txt')
  z.writestr('README.md',f'# {brand} portfolio artwork\n\nOriginal identity by Eyilade Oridamisi. New collection/product photographs and mockups are AI-assisted portfolio concepts with fictional models. They are not proof of real products, stock, customers or endorsements. Native SVG artwork contains outlined type and embedded optimised photographs; full PNG masters are included. Label/sleeve artwork is conceptual, not approved for production. Source originals stay untouched.\n')
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None;names=z.namelist();assert len(names)==len(set(names))
 receipt={'file':name,'files':len(names),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
 (out.parent/'artwork-package.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
