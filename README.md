# The public archiving of this repository is due to the integration of logfuscate features into the Panther Analysis Tool (PAT). The PR can be found [here](https://github.com/panther-labs/panther_analysis_tool/pull/354).

---
###### Logfuscate

Logfuscate is a tool designed for obfuscating and deobfuscating logs pulled from [Panther's API](https://docs.panther.com/panther-developer-workflows/api/operations/data-lake-queries). Panther is a platform that helps you detect threats with log data, improve cloud security posture, and perform advanced data analysis. This tool will help you to obfuscate the logs before sharing them with others and deobfuscate them when needed.

---

###### Developer

- Name: [Asante Babers](https://atbabers.com/)
- Version: 0.9

---

###### How It Works

The tool fetches the data from Panther's API using the provided SQL query. The data is then processed, and each log is obfuscated. The obfuscation is done by replacing the values of certain fields with a fixed string or a random value. The fields to be obfuscated and the replacement values are defined in the `regexes.py` file.

The deobfuscation is done by replacing the obfuscated values with the original values. The original values are stored in a separate file during the obfuscation process.

---

###### Installation

1. Clone the repository or download the source code.
2. Install the required packages by running `pip install -r requirements.txt`.

---
######  Usage
```
usage: logfuscate.py [-h] [-v] (-s SQL_QUERY | -d DEOBFUSCATE | -f OBFUSCATE | -fd FILE_DEOBFUSCATE)
```

###### Options
- `-h`, `--help`  
  Show this help message and exit.
- `-v`, `--verbose`  
  Enable verbose mode.
- `-s SQL_QUERY`, `--sql_query SQL_QUERY`  
  The SQL query to fetch data from Panther's API.
- `-d DEOBFUSCATE`, `--deobfuscate DEOBFUSCATE`  
  Path to the file to deobfuscate.
- `-f FILE_OBFUSCATE`, `--file FILE_OBFUSCATE`  
  Path to the file to deobfuscate.
- `-fd FILE_DEOBFUSCATE`, `--file-deobfuscate FILE_DEOBFUSCATE`  
  Path to the file to deobfuscate.

---

###### Obfuscation

To obfuscate the logs, you need to fetch the data from Panther's API using an SQL query and then obfuscate the data.

```bash
python logfuscate.py -s "<SQL_QUERY>"
```

Replace `<SQL_QUERY>` with the actual SQL query. The SQL Query does need to be enclosed in single or double quotes.

```bash
python logfuscate.py -f "/path/to/file"
```

Replace `/path/to/file` with the actual path to the obfuscated file.
---

###### Deobfuscation

To deobfuscate the logs, you need to have a file with the obfuscated data.

```bash
python logfuscate.py -d "<PATH_TO_OBFUSCATED_FILE>"
```

Replace `<PATH_TO_OBFUSCATED_FILE>` with the actual path to the obfuscated file.

```bash
python logfuscate.py -fd "/path/to/file"
```

Replace `/path/to/file` with the actual path to the obfuscated file.
---

