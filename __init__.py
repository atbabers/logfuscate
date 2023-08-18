# regexes/__init__.py
import os
import json

PATTERNS = {}

# For each JSON file in the regexes directory
for file_name in os.listdir(os.path.dirname(__file__)):
    if file_name.endswith('.json'):
        with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
            # Load the JSON content and update the PATTERNS dictionary
            PATTERNS.update(json.load(f))