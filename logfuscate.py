import argparse, json, time, logging, yaml
from yaml_processor import process_yaml_file
from config import load_config
from utils.utils import save_results
import get_schemas, data_load, obfuscation, deobfuscation
from regexes import PATTERNS

# Initialize the logger
logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def banner():
    print("""#    _                 __                      _        
#   | |    ___  __ _  / _| _  _  ___ __  __ _ | |_  ___ 
#   | |__ / _ \\/ _` ||  _|| || |(_-</ _|/ _` ||  _|/ -_)
#   |____|\\___/\\__, ||_|   \\_,_|/__/\\__|\\__,_| \\__|\\___|
#              |___/                                    """)
    print("Developer: Asante Babers | Version: 0.9")
    print("Description: Obfuscate and deobfuscate events for Panther." + "\\n")


def main():
    # Load the Panther API configurations
    banner()

    config = load_config()
    patterns = PATTERNS
    
    parser = argparse.ArgumentParser(description="Obfuscate and deobfuscate logs pulled from Panther's API.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--sql_query", type=str, help="The SQL query to fetch data from Panther's API.")
    group.add_argument("-d", "--deobfuscate", type=str, help="Path to the file to deobfuscate.")
    group.add_argument("-f", "--file", help="Path to YAML file to encryptthe Tests key", type=str)
    group.add_argument("-fd", "--file-deobfuscation", help="Path to YAML file to decrypt the Tests key", type=str)

    args = parser.parse_args()

    # Set the verbose mode
    if args.verbose:
        obfuscation.VERBOSE = True
        deobfuscation.VERBOSE = True
        logger.setLevel(logging.DEBUG)
    
    #If file is the input
    if args.file:
        process_yaml_file(args.file, "obfuscation", patterns)
        return
    if args.file_deobfuscation:
        process_yaml_file(args.file_deobfuscation, "deobfuscation", patterns)
        return

    # If we're deobfuscating
    if args.deobfuscate:
        with open(args.deobfuscate, 'r') as f:  # Filepath
            data_to_deobfuscate = json.load(f)
        deobfuscated_data = deobfuscation.deobfuscate_data(data_to_deobfuscate, patterns)
        schema_name = data_to_deobfuscate.get('p_log_type', 'unknown')
        current_timestamp = int(time.time() * 1000)  # Epoch time in milliseconds
        save_results(deobfuscated_data, schema_name, args.deobfuscate, False)
    else:
        # Fetch the data
        results = data_load.fetch_data(args.sql_query, config)
        
        # Ensure results is a list for uniform processing
        if not isinstance(results, list):
            results = [results]

        # Process each result
        for result in results:
            schema_name = result.get('p_log_type', 'unknown')
            obfuscated_data = obfuscation.obfuscate_data(result, patterns)
            current_timestamp = int(time.time() * 1000)  # Epoch time in milliseconds
            filename = f"{schema_name}_{current_timestamp}_obfuscated.json"
            save_results(obfuscated_data, schema_name, None, True)

if __name__ == "__main__":
    main()
