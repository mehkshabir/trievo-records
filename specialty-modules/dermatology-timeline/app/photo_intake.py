"""Quality-check-before-accept gate (same pattern as Trievo Vision): reject blurry/tiny images."""
import io
from PIL import Image, ImageFilter, ImageStat

MIN_SIDE, MIN_SHARPNESS = 480, 60.0

def quality_check(data: bytes):
    try:
        img = Image.open(io.BytesIO(data)); img.load()
    except Exception:
        return False, "File is not a readable image. Upload a JPG or PNG."
    if min(img.size) < MIN_SIDE:
        return False, f"Image is too small ({img.size[0]}x{img.size[1]}). Use at least {MIN_SIDE}px on the short side."
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES)
    if ImageStat.Stat(edges).var[0] < MIN_SHARPNESS:
        return False, "Image looks blurry. Retake it in focus and good light."
    return True, "ok"
