import os, yaml, secrets, re, base64
from utils.utils import get_or_create_key

KEY_FILE = ".logfuscate.key"

OBFUSCATION_KEY = get_or_create_key()


def xor_with_key(input_string, key):
    """ XORs a given string with a key """
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, key * len(input_string)))

def deobfuscate_string(value, pattern):
    """ Deobfuscate a string """
    try:
        # Base64 decode the value
        decoded = base64.b64decode(value).decode()
        return xor_with_key(decoded, OBFUSCATION_KEY)
    except:
        # If base64 decoding fails or the value wasn't obfuscated, return the original value
        return value

def deobfuscate_data(data, patterns):
    """ Recursive function to deobfuscate data """
    if isinstance(data, dict):
        for key, value in data.items():
            if key in patterns:
                data[key] = deobfuscate_string(value, patterns[key])
            else:
                deobfuscate_data(value, patterns)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            deobfuscate_data(value, patterns)
    return data
