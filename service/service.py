import hashlib
import string
from datetime import datetime
from models.models import URLMapping
from repository.repository import url_repository

BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase  # 0-9, a-z, A-Z


def hash_to_base62(long_url: str, length: int = 7) -> str:
    """Hash a URL and convert to base62 string."""
    hash_bytes = hashlib.sha256(long_url.encode()).digest()

    num = int.from_bytes(hash_bytes[:8], byteorder='big')

    result = []
    while num and len(result) < length:
        num, remainder = divmod(num, 62)
        result.append(BASE62[remainder])

    while len(result) < length:
        result.append('0')

    return ''.join(result[:length])


def create_short_url(long_url: str) -> URLMapping:
    """
    Create a short URL for the given long URL.
    Checks for existing mappings and handles collisions.
    """
    existing_mapping = url_repository.get_by_long_url(long_url)
    if existing_mapping:
        return existing_mapping

    candidate = hash_to_base62(long_url)
    attempt = 0

    while attempt <= 10:
        existing_long_url = url_repository.exists(candidate)

        if existing_long_url is None:
            url_mapping = URLMapping(
                url_id=candidate,
                long_url=long_url,
                created_at=datetime.now()
            )
            url_repository.insert(url_mapping)
            return url_mapping

        if existing_long_url == long_url:
            return url_repository.get_by_url_id(candidate)

        attempt += 1
        candidate = hash_to_base62(f"{long_url}{attempt}")

    raise Exception("Too many collisions, something is wrong")


def get_long_url(url_id: str) -> str | None:
    """Get the long URL for a given short URL ID"""
    mapping = url_repository.get_by_url_id(url_id)
    return mapping.long_url if mapping else None