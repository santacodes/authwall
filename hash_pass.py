"""Hash Password."""
import uuid
import hashlib


def hash_password(text):
    """Basic hashing function for a text using random unique salt."""
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt


def check_hash(hashedText, providedText):
    """Check for the text in the hashed text."""
    _hashedText, salt = hashedText.split(':')
    return _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()
