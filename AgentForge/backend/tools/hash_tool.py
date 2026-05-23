import hashlib


def generate_hash(file_path):

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    return hashlib.sha256(file_bytes).hexdigest()