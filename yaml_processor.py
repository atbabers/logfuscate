import yaml
import obfuscation, deobfuscation


def process_yaml_file(file_path, operation, patterns):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    if "Tests" in data:
        if operation == "obfuscation":
            for test in data["Tests"]:
                if "Log" in test:
                    log_data = test["Log"]
                    encrypted_data = obfuscation.obfuscate_data(log_data, patterns)
                    test["Log"] = encrypted_data
        elif operation == "deobfuscation":
            for test in data["Tests"]:
                if "Log" in test:
                    encrypted_data = test["Log"]
                    decrypted_data = deobfuscation.deobfuscate_data(encrypted_data, patterns)
                    test["Log"] = decrypted_data

    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f)
    print(f'{operation} has been completed.')
