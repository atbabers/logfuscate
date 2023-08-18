import os, yaml, secrets, re, base64
from utils.utils import get_or_create_key

OBFUSCATION_KEY = get_or_create_key()

def xor_with_key(input_string, key):
    """ XORs a given string with a key """
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, key * len(input_string)))

def obfuscate_string(value, pattern):
    """ Obfuscate a string if it matches the pattern """
    if re.search(pattern, value):
        obfuscated = xor_with_key(value, OBFUSCATION_KEY)
        # Base64 encode the obfuscated value
        return base64.b64encode(obfuscated.encode()).decode()
    return value

def obfuscate_data(data, patterns):
    """ Recursive function to obfuscate data """
    if isinstance(data, dict):
        for key, value in data.items():
            if key in patterns:
                data[key] = obfuscate_string(value, patterns[key])
            else:
                obfuscate_data(value, patterns)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            obfuscate_data(value, patterns)
    return data
