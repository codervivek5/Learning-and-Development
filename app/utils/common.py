import uuid
from typing import Optional


def is_valid_uuid(uuid_to_test: str) -> bool:
    """Check if a string is a valid UUID version 4."""
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
