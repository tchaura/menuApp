from PIL import Image
import os


def compress(img_path, compress_ratio = None):
    size_mb = os.path.getsize(img_path) / 1000000
    if size_mb < 0.5:
        return
    
    img = Image.open(img_path)
    width, height = img.size
    if not compress_ratio:
        compress_ratio = 3 if size_mb > 2 else 2
    new_size = (width//compress_ratio, height//compress_ratio)
    resized_image = img.resize(new_size)
    relative_path, name = os.path.split(img_path)
    resized_image.save(os.path.join(relative_path, name), optimize=True, quality=50)
