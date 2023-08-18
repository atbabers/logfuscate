import argparse, datetime, json, time
from config import load_config
from utils.utils import save_results
from get_schemas import fetch_and_save_schemas
from data_load import fetch_data
from obfuscation import obfuscate_data
from deobfuscation import deobfuscate_data
from regexes import PATTERNS



# def banner():
# BANNER & DEV INFO


def main():
    # Load the Panther API configurations
    config = load_config()
    patterns = PATTERNS
    
    parser = argparse.ArgumentParser(description="Obfuscate and deobfuscate logs pulled from Panther's API.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--sql_query", type=str, help="The SQL query to fetch data from Panther's API.")
    group.add_argument("-d", "--deobfuscate", type=str, help="Path to the file to deobfuscate.")
    args = parser.parse_args()



    # If we're deobfuscating
    if args.deobfuscate:
        with open(args.deobfuscate, 'r') as f:  # Filepath
            data_to_deobfuscate = json.load(f)
        deobfuscated_data = deobfuscate_data(data_to_deobfuscate, patterns)
        schema_name = data_to_deobfuscate.get('p_log_type', 'unknown')
        current_timestamp = int(time.time() * 1000)  # Epoch time in milliseconds
        save_results(deobfuscated_data, schema_name, args.deobfuscate, False)
    else:
        # Fetch the data
        results = fetch_data(args.sql_query, config)
        
        # Ensure results is a list for uniform processing
        if not isinstance(results, list):
            results = [results]

        # Process each result
        for result in results:
            schema_name = result.get('p_log_type', 'unknown')
            obfuscated_data = obfuscate_data(result, patterns)
            current_timestamp = int(time.time() * 1000)  # Epoch time in milliseconds
            filename = f"{schema_name}_{current_timestamp}_obfuscated.json"
            save_results(obfuscated_data, schema_name, None, True)

if __name__ == "__main__":
    main()