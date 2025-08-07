"""
Utilities for encrypting and decrypting text

If failing, create the file keys.py and fill with a key generated from generate_key()
ENCRYPTION_KEY = 'your_key_here'

pip dependencies:
cryptography
"""

__author__ = "Ryan Clark"


from cryptography.fernet import Fernet


class DecryptedValue:
    def __init__(self, value: str):
        self._value = value
    
    def __str__(self):
        return self._value
    
    def __repr__(self):
        return f"DecryptedValue('***HIDDEN***')"
    
    @property
    def value(self):
        return self._value


def generate_key() -> str:
    key = Fernet.generate_key()
    return key.decode()


def load_key() -> bytes:
    try:
        from .keys import ENCRYPTION_KEY
    except:
        raise RuntimeError(f"Failed to load encryption key from keys file. In lib, create file keys.py and populate variable ENCRYPTION_KEYS with a valid key from the generate_key() function.")

    return ENCRYPTION_KEY.encode()


def encrypt(text: str) -> str:
    key_bytes: bytes = load_key()
    
    fernet = Fernet(key_bytes)
    encrypted_bytes = fernet.encrypt(text.encode())
    return encrypted_bytes.decode()


def decrypt(text: str) -> DecryptedValue:
    key_bytes: bytes = load_key()

    fernet = Fernet(key_bytes)
    decrypted_bytes = fernet.decrypt(text.encode())
    return DecryptedValue(decrypted_bytes.decode())
