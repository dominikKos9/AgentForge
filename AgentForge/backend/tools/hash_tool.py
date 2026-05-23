import hashlib
from PIL import Image
import io


def generate_hash(file_path):
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    # optional normalization (removes metadata differences)
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    normalized_bytes = img.tobytes()

    return hashlib.sha256(normalized_bytes).hexdigest()