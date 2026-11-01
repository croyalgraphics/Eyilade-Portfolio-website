"""Package the supplied-label revision without overwriting earlier deliveries."""
from pathlib import Path
import zipfile,hashlib,json
R=Path(__file__).resolve().parents[1]
A=R/'artwork/natoral-supplied';O=R/'output/natoral-supplied'
O.mkdir(parents=True,exist_ok=True)
out=O/'Natoral-Supplied-Labels-and-Campaign-Artwork-2026-11-01.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((A/'masters').glob('*')):
  if p.suffix in ['.svg','.png','.json']:z.write(p,'compositions/'+p.name)
 for p in sorted((A/'source').glob('*')):z.write(p,'supplied-originals/'+p.name)
 for p in sorted((A/'generated').glob('*.png')):z.write(p,'scene-plates/'+p.name)
 for n in ['NATORAL_SUPPLIED_LABELS_2026-11-01.md','NATORAL_SCENE_BRIEFS_2026-11-01.json']:
  z.write(R/'docs'/n,n)
 z.write(R/'dist/assets/natoral-supplied/FONT-LICENSE.txt','FONT-LICENSE.txt')
 z.write(O/'source-verification.json','SOURCE-VERIFICATION.json')
 z.writestr('README.md',"# Natoral — supplied-label revision\n\nN1–N8 are the designer-supplied packaging masters and remain byte-identical to the inputs. Native SVG compositions embed supplied product PNGs, outlined typography and photographic scene plates. Product labels have not been redrawn or retyped. The eight supplied files supersede all previously generated label concepts.\n\nSurrounding scenes were generated with the built-in image tool and depict fictional models. The scene prompts are included. Label statements are supplied artwork, not independently verified claims. These are portfolio compositions, not print-ready dielines or production approval. Earlier deliveries remain preserved separately.\n")
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 names=z.namelist();assert len(names)==len(set(names))
receipt={'file':str(out.relative_to(R)),'files':len(names),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(O/'artwork-package.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
