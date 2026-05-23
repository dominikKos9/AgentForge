from PIL import Image

def validate_image(path):
    try:
        img = Image.open(path)
        return img.format in ["JPEG", "PNG", "WEBP"]
    except:
        return False