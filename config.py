import os

CONFIG_FILE = ".config"

def configure():
    """ Prompt the user for configuration details and save them. """
    api_url = input("Enter the PANTHER API URL: ")
    api_token = input("Enter the PANTHER API TOKEN: ")

    with open(CONFIG_FILE, 'w') as f:
        f.write(f"API_URL={api_url}\n")
        f.write(f"API_TOKEN={api_token}\n")

    print("Configuration saved.")

def load_config():
    """ Load the configuration from the .config file. """
    if not os.path.exists(CONFIG_FILE):
        print("Configuration not found. Setting up...")
        configure()

    config = {}
    with open(CONFIG_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            config[key] = value

    return config

# For testing purposes
# config = load_config()
# print(config)
