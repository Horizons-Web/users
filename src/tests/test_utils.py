from unittest.mock import patch, MagicMock

from src.utils.utils import _hash, verify

def test_hash_generation():
    plain_password = "test_password"
    hashed_password = _hash(plain_password)
    assert hashed_password != plain_password
    assert isinstance(hashed_password, str)
    assert verify(plain_password, hashed_password) is None 
