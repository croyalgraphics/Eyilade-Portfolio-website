"""Prepare the supplied master-brief artwork without changing any originals.

macOS: use the bundled Python (Pillow), sips, Node and bundled sharp.
For WOFF2 export only, install fonttools==4.67.0 + brotli==1.2.0 to
/private/tmp/eyilade-asset-tools and set PYTHONPATH to that directory.
Run: PYTHONPATH=/private/tmp/eyilade-asset-tools <bundled-python> scripts/prepare_master_assets.py
No runtime website package is needed. SVG rasterisation uses bundled sharp,
not a downloaded web service. The script may run repeatedly without touching
any source file under Assets.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageChops
import hashlib
import json
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "Assets"
OUT = ROOT / "dist/assets/master"
FONTS = ROOT / "dist/assets/fonts"
SHARP = Path("/Users/joshuaoridamisi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp")
OUT.mkdir(parents=True, exist_ok=True)
FONTS.mkdir(parents=True, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None  # Original dimensions were audited; sips bounds decoding.
records = []

LOGOS = [
    ("agrohub", "Agrohub & Investment", "Agrohub investment/Agrohub investment main logo.png", None),
    ("beans-central", "Beans Central", "Beans Cental Logo/Beans Cental Logo.png", "/work/beans-central/"),
    ("clenstreet", "ClenStreet", "ClenStreet/Main logo.svg", None),
    ("docs-apothecary", "Doc’s Apothecary", "Doc's Apothecary.png", "/work/docs-apothecary/"),
    ("efame", "Efame Real Estate", "Efame real estate.png", None),
    ("feasts-and-flavours", "Feasts & Flavours", "Feast and flavours/Feast and flavours Full colored logo.png", "/work/feasts-and-flavours/"),
    ("genesis-orb", "Genesis Orb", "Genesis Orb/Genesis orb Logo 1.png", "/work/genesis-orb/"),
    ("intelligentsia-orb", "Intelligentsia Orb", "Intelligentsial orb.png", None),
    ("lecco-inn", "Lecco Inn", "Lecco Inn/Lecco Inn Logo 1.png", None),
    ("lizcraft", "LizCraft", "Lizcraft/LizCraft Logo 2.png", "/work/lizcraft/"),
    ("lizinterior", "LizInterior", "LizInterior/Liz Interior Secondary logo.png", None),
    ("ppcl", "PPCL", "PPCL logo.png", None),
    ("purehive", "Pure Hive Honey", "Pure Hive Honey.png", "/work/purehive/"),
    ("rebeks-savour", "Rebeks Savour", "Rebeks savour.png", None),
    ("swift-tern", "Swift Tern Airways", "Swift tern/Swift Tern Logo.png", None),
    ("natoral", "Natoral", "Natoral/Natoral Logo 2.png", "/work/natoral/"),
    ("crg", "CRGraphics", "CRG logos/Full Logo.png", None),
    ("primefits", "PrimeFits", "PrimeFits/Prmefits main Logo.svg", None),
    ("yoma", "Yoma", "Yoma/Yoma Logo.png", None),
]
TOOLS = [
    ("Photoshop", "photoshop", "Adobe_Photoshop_CC_icon.svg.webp"),
    ("Illustrator", "illustrator", "Adobe_Illustrator_CC_icon.svg.webp"),
    ("InDesign", "indesign", "Adobe_InDesign_CC_icon.svg.webp"),
    ("After Effects", "after-effects", "Adobe_After_Effects_CC_icon.svg.webp"),
    ("Premiere Pro", "premiere-pro", "Adobe_Premiere_Pro_CC_icon.svg.webp"),
    ("Codex", "codex", "codex-logo.png"),
    ("Figma", "figma", "Figma-logo.svg.webp"),
    ("GitHub", "github", "Github.png"),
    ("Leonardo AI", "leonardo-ai", "Leonardo.Ai-Symbol.png"),
]
BRANDS = [
    ("Dabur", "dabur", "Dabur_Logo.svg.webp"),
    ("PZ Cussons", "pz-cussons", "PZ_Cussons_logo.svg.webp"),
    ("Sandtex", "sandtex", "Sandtex.png"),
]


def raster(source, temp):
    """Render safe local SVGs or downsample large rasters before Pillow reads pixels."""
    if source.suffix.lower() == ".svg":
        tree = ET.parse(source)
        for item in tree.iter():
            tag = item.tag.rsplit("}", 1)[-1].lower()
            if tag in {"script", "foreignobject", "image", "use"}:
                raise ValueError(f"SVG needs manual resource inspection: {source}")
            for key, value in item.attrib.items():
                if key.lower().startswith("on") or "href" in key.lower() or "http" in value.lower():
                    raise ValueError(f"Unexpected SVG resource/event: {source}")
        target = temp / (source.stem + ".png")
        js = "const sharp=require(process.argv[1]); sharp(process.argv[2],{density:144}).resize({width:1800}).png().toFile(process.argv[3]).catch(e=>{console.error(e);process.exit(1)});"
        subprocess.run(["node", "-e", js, str(SHARP), str(source), str(target)], check=True, capture_output=True)
        return Image.open(target).convert("RGBA"), "SVG viewBox rendered at 1800px width"
    with Image.open(source) as original:
        size = original.size
    if max(size) > 4000:
        target = temp / (source.stem + ".png")
        subprocess.run(["sips", "-Z", "4000", str(source), "--out", str(target)], check=True, capture_output=True)
        return Image.open(target).convert("RGBA"), f"sips bounded intermediate; original {size[0]}x{size[1]}"
    return Image.open(source).convert("RGBA"), "original raster"


def prepare(source_rel, output_name, box, temp, trim=True, lossless=True):
    source = ASSETS / source_rel
    im, decoding = raster(source, temp)
    decoded = im.size
    crop = [0, 0, im.width, im.height]
    if trim:
        alpha = im.getchannel("A")
        alpha_bounds = alpha.point(lambda a: 255 if a > 4 else 0).getbbox()
        if alpha_bounds and alpha_bounds != (0, 0, im.width, im.height):
            crop = list(alpha_bounds)
        else:
            # The two Genesis originals are RGB with empty white artboard margins.
            # Trim only their exterior white space; never replace or recolour pixels.
            composite = Image.new("RGBA", im.size, "white")
            composite.alpha_composite(im)
            difference = ImageChops.difference(composite.convert("RGB"), Image.new("RGB", im.size, "white"))
            bounds = difference.convert("L").point(lambda a: 255 if a > 8 else 0).getbbox()
            if bounds:
                crop = list(bounds)
        # Keep a small safety margin for antialiasing, diacritics and fine rules.
        margin = max(2, round(max(crop[2]-crop[0], crop[3]-crop[1]) * .025))
        crop = [max(0,crop[0]-margin), max(0,crop[1]-margin), min(im.width,crop[2]+margin), min(im.height,crop[3]+margin)]
        im = im.crop(crop)
    im.thumbnail(box, Image.Resampling.LANCZOS)
    target = OUT / (output_name + ".webp")
    im.save(target, "WEBP", lossless=lossless, quality=88, method=6)
    item = {"image": "/assets/master/" + target.name, "width": im.width, "height": im.height, "source": "Assets/" + source_rel}
    records.append({**item, "bytes": target.stat().st_size, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "decoded_size": list(decoded), "crop_in_decoded_pixels": crop, "processing": decoding, "lossless": lossless})
    return item


def font(source_rel, filename):
    from fontTools.ttLib import TTFont
    source = ASSETS / source_rel
    face = TTFont(source)
    names = {str(n.nameID): n.toUnicode() for n in face['name'].names if n.nameID in [1,2,4,6]}
    face.flavor = "woff2"
    target = FONTS / filename
    face.save(target)
    records.append({"font": "/assets/fonts/"+filename, "source": "Assets/"+source_rel, "names": names, "bytes": target.stat().st_size, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest()})


def main():
    with tempfile.TemporaryDirectory(prefix="eyilade-master-assets-", dir="/private/tmp") as temp_name:
        temp = Path(temp_name)
        logos = []
        for slug, name, source, project in LOGOS:
            item = prepare(source, "logo-"+slug, (840, 570), temp)
            item = {"slug": slug, "name": name, **item}
            if project:
                item["project"] = project
            logos.append(item)
        full_source = "Eyilade illustration(full pose view).png"
        close_source = "Eyilade illustration (close-up view).png"
        full640 = prepare(full_source, "eyilade-full-640", (640,960), temp, trim=False, lossless=False)
        full1024 = prepare(full_source, "eyilade-full-1024", (1024,1536), temp, trim=False, lossless=False)
        close400 = prepare(close_source, "eyilade-close-400", (400,400), temp, trim=False, lossless=False)
        close800 = prepare(close_source, "eyilade-close-800", (800,800), temp, trim=False, lossless=False)
        tools = [{"name": name, "slug": slug, **prepare("Career and skills/"+source, "tool-"+slug, (192,192), temp)} for name, slug, source in TOOLS]
        brands = [{"name": name, "slug": slug, **prepare("Career and skills/"+source, "brand-"+slug, (480,260), temp)} for name, slug, source in BRANDS]
        # Add a newly supplied PwC mark when present. Never fetch or fabricate one.
        pwc_files = [p for p in (ASSETS/"Career and skills").glob("*") if "pwc" in p.name.lower() and p.suffix.lower() in {".png", ".webp", ".svg", ".jpg"}]
        if pwc_files:
            if len(pwc_files) != 1:
                raise ValueError("Multiple PwC candidates require visual selection")
            brands.append({"name":"PwC", "slug":"pwc", **prepare(str(pwc_files[0].relative_to(ASSETS)), "brand-pwc", (480,260), temp)})
        timeline = {"crg": {k: logos[16][k] for k in ["image","width","height"]}, "intelligentsia": {k: logos[7][k] for k in ["image","width","height"]}}
        if pwc_files:
            timeline["pwc"] = {k: brands[-1][k] for k in ["image","width","height"]}
        data = {"hero": {"full640":full640["image"], "full1024":full1024["image"], "close400":close400["image"], "close800":close800["image"], "fullWidth":1024, "fullHeight":1536, "closeWidth":1254, "closeHeight":1254, "sources":[full_source, close_source]}, "tools":tools, "brands":brands, "timelineLogos":timeline}
        (ROOT/"content/logos.json").write_text(json.dumps(logos, ensure_ascii=False, indent=2)+"\n")
        (ROOT/"content/master-assets.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")
        font("Fonts/BeachSound.otf", "beach-sound.woff2")
        font("Fonts/Rubik/Rubik-VariableFont_wght.ttf", "rubik-variable.woff2")
        shutil.copyfile(ASSETS/"Fonts/Rubik/OFL.txt", FONTS/"Rubik-OFL.txt")
        provenance = "Beach Sound / BeachSound. Supplied at Assets/Fonts/BeachSound.otf. Designer metadata: Ikiikowrk. No accompanying licence document was supplied. Font conversion preserves the name and full character set; it does not establish webfont publication rights.\n"
        (FONTS/"BeachSound-PROVENANCE.txt").write_text(provenance)
        report = {"logo_families":len(logos), "tool_count":len(tools), "missing":[] if pwc_files else ["PwC logo: not found in Assets/Career and skills"], "choices":["Horizontal lockups selected where supplied, allowing readable moving rows with object-fit:contain.", "PPCL PNG selected: purple/charcoal identity matches the portfolio; PPCL SVG is a distinct four-colour variant.", "White Feasts & Flavours and PrimeFits variants retained only in original Assets; full-colour primary variants chosen.", "Entire hero image bounds retained; no head/foot or figure cropping.", "BeachSound licence documentation remains absent; user publication rights require confirmation before public release."], "assets": records}
        (ROOT/"docs/MASTER_ASSET_MAP.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
        print(json.dumps({"logos":len(logos),"tools":len(tools),"brands":len(brands),"generated_bytes":sum(x["bytes"] for x in records),"missing":report["missing"]}, indent=2))


if __name__ == "__main__":
    main()
