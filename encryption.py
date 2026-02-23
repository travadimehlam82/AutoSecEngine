# encryption.py
# Small helpers: compute entropy of a file safely (reads sample) and AES helper (used only on copies)
import math
from collections import Counter
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def shannon_entropy_bytes(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    ent = 0.0
    for cnt in counts.values():
        p = cnt / length
        ent -= p * math.log2(p)
    return ent

def compute_entropy(filepath, samplesize=4096):
    try:
        with open(filepath, 'rb') as f:
            data = f.read(samplesize)
        return shannon_entropy_bytes(data)
    except Exception:
        return 0.0

# AES helper (for demonstration). Encrypts input bytes with AES-GCM and returns ciphertext.
def aes_encrypt_bytes(key: bytes, plaintext: bytes, associated_data: bytes = None):
    # key must be 16/24/32 bytes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, associated_data)
    return nonce + ct  # prepend nonce
