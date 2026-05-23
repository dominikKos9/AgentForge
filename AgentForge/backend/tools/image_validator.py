from PIL import Image


def validate_image(path):
    try:
        img = Image.open(path)

        allowed = ["JPEG", "PNG", "WEBP"]

        return img.format in allowed

    except Exception:
        return False