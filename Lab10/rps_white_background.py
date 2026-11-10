import numpy as np, os, sys
from PIL import Image, ImageFilter
try:
    from scipy import ndimage
except ImportError:
    ndimage = None
SRC = r"C:/Users/Stas/Desktop/Deep learning/Lab10/rps_my_photos/original"
DST = r"C:/Users/Stas/Desktop/Deep learning/Lab10/rps_my_photos"
TH = float(sys.argv[1]) if len(sys.argv) > 1 else 44
for fn in sorted(os.listdir(SRC)):
    img = Image.open(os.path.join(SRC, fn)).convert('RGB')
    ycc = np.array(img.convert('YCbCr')).astype(float)
    d = ycc[..., 2] - ycc[..., 1]                     # Cr - Cb: шкіра має більше червоного відтінку
    d = np.array(Image.fromarray(np.clip(d * 3, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))) / 3
    mask = d > TH
    if ndimage is not None:
        mask = ndimage.binary_opening(mask, iterations=4)
        lab, n = ndimage.label(mask)
        if n:
            sizes = ndimage.sum(mask, lab, range(1, n + 1))
            mask = lab == (np.argmax(sizes) + 1)        # найбільша зв'язна область - рука
        mask = ndimage.binary_fill_holes(ndimage.binary_closing(mask, iterations=8))
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    white = Image.new('RGB', img.size, (255, 255, 255))
    out = Image.composite(img, white, m)
    out.save(os.path.join(DST, fn), quality=95)
    print(fn, mask.mean().round(3))
