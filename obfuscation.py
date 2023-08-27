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

def obfuscate_string(value, pattern):
    if VERBOSE:
        logger.setLevel(logging.DEBUG)
    """
    Obfuscate a string if it matches the pattern.

    Parameters:
        value (str): The string to be obfuscated.
        pattern (str): The pattern to match.

    Returns:
        str: The obfuscated string if it matches the pattern, otherwise the original string.
    """
    if re.search(pattern, value):
        # Generate a random key for this obfuscation
        random_key = secrets.token_hex(len(value))
        obfuscated = xor_with_key(value, random_key)
        # Convert the obfuscated value to hexadecimal
        obfuscated_hex = obfuscated.encode('utf-8').hex()
        # Append the random key to the obfuscated value
        result = obfuscated_hex + random_key
        if VERBOSE:
            logger.debug(f'Obfuscating {value} to {result}')
        return result
    return value

def obfuscate_data(data, patterns):
    if VERBOSE:
        logger.setLevel(logging.DEBUG)
    """
    Recursive function to obfuscate data.

    Parameters:
        data (dict or list): The data to be obfuscated.
        patterns (dict): The patterns to match.

    Returns:
        dict or list: The obfuscated data.
    """
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
