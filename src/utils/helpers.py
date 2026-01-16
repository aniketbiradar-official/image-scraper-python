# src/utils/helpers.py
import os
import re
import hashlib
from urllib.parse import urlparse

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def sanitize_filename(name: str) -> str:
    # keep characters safe for file systems
    name = re.sub(r"[^0-9a-zA-Z._-]", "_", name)
    return name[:200]

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def ext_from_content_type(content_type: str) -> str:
    if not content_type:
        return ".jpg"
    c = content_type.lower()
    if "png" in c:
        return ".png"
    if "jpeg" in c or "jpg" in c:
        return ".jpg"
    if "gif" in c:
        return ".gif"
    if "webp" in c:
        return ".webp"
    return ".jpg"

def get_topic_image_dir(base_dir: str, query: str) -> str:
    """
    Creates and returns directory path like:
    images/cat/
    images/dog/
    """
    safe_query = sanitize_filename(query.lower())
    topic_dir = os.path.join(base_dir, safe_query)
    ensure_dir(topic_dir)
    return topic_dir
