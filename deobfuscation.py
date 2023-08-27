import os, yaml, secrets, re, logging
from utils.utils import get_or_create_key

# Initialize the logger
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
VERBOSE = False

# Get or create the obfuscation key
OBFUSCATION_KEY = get_or_create_key()

def xor_with_key(input_string, key):
    """
    XORs a given string with a key.

    Parameters:
        input_string (str): The string to be XORed.
        key (str): The key to XOR with.

    Returns:
        str: The result of the XOR operation.
    """
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, key * len(input_string)))

def deobfuscate_string(value, pattern):
    """
    Deobfuscate a string.

    Parameters:
        value (str): The string to be deobfuscated.
        pattern (str): The pattern to match.

    Returns:
        str: The deobfuscated string if it matches the pattern, otherwise the original string.
    """
    try:
        # Extract the random key from the value
        random_key = value[-len(value)//2:]
        # Extract the obfuscated hexadecimal value
        obfuscated_hex = value[:-len(value)//2]
        # Convert the obfuscated hexadecimal value to string
        obfuscated = bytes.fromhex(obfuscated_hex).decode('utf-8')
        result = xor_with_key(obfuscated, random_key)
        if VERBOSE:
            logger.info(f'Deobfuscated {value} to {result}')
        return result
    except:
        # If decoding fails or the value wasn't obfuscated, return the original value
        return value

def deobfuscate_data(data, patterns):
    """
    Recursive function to deobfuscate data.

    Parameters:
        data (dict or list): The data to be deobfuscated.
        patterns (dict): The patterns to match.

    Returns:
        dict or list: The deobfuscated data.
    """
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
