import os, json, secrets, time

KEY_FILE = ".logfuscate.key"

def get_or_create_key():
    """Get or create the obfuscation key."""
    # Check if the key file exists
    if not os.path.exists(KEY_FILE):
        # Generate a random key
        key = secrets.token_hex(16)
        
        # Save the key to the key file
        with open(KEY_FILE, 'w') as f:
            f.write(key)
        
        print("Warning: A new obfuscation key has been generated and saved in .logfuscate.key. Do NOT delete this file if you wish to deobfuscate data in the future.")
        return key
    
    # If the key file exists, read and return the key
    with open(KEY_FILE, 'r') as f:
        return f.read().strip()

def save_results(data, table_name=None, source_filename=None, obfuscated=True):
    """
    Save the results in a JSON file inside the 'results' directory.
    
    The filename will be a combination of table_name, current timestamp, and if it's obfuscated or deobfuscated.

    Args:
    - data (dict): The data to be saved.
    - source_filename (str, optional): The filename of the source file being deobfuscated. Required if obfuscated is False.
    - obfuscated (bool, optional): If the data is obfuscated or not. Defaults to True.

    Returns:
    - str: The path to the saved file.
    """

    # Ensure the 'results' directory exists
    if not os.path.exists("results"):
        os.mkdir("results")

    """Save the obfuscated or deobfuscated data to a file."""
    if obfuscated:
        output_filename = f"results/{table_name}_{int(time.time() * 1000)}_obfuscated.json"
    else:
        output_filename = f"results/{source_filename.split('/')[-1].split('_')[0]}_{int(time.time() * 1000)}_deobfuscated.json"

    with open(output_filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {output_filename}")
