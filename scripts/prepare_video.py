"""Optional poster regeneration. Requires ffmpeg or imageio-ffmpeg and Pillow."""
import subprocess, shutil, tempfile
from pathlib import Path
from PIL import Image, ImageOps
root=Path(__file__).resolve().parents[1]
ffmpeg=shutil.which('ffmpeg')
if not ffmpeg:
    import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
target=Path(tempfile.mkdtemp())/'frame.png'
subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-ss','6.5','-i',str(root/'dist/assets/birthday-motion.mp4'),'-frames:v','1','-update','1',str(target)],check=True)
with Image.open(target) as im:
    for width in [640,1280]:
        ImageOps.contain(im.convert('RGB'),(width,width)).save(root/f'dist/assets/birthday-still-{width}.webp','WEBP',quality=89,method=6)
