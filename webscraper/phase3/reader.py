import pandas as pd
import json

def load_and_explore(file_path, output_file):
    # Load JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Try to normalize nested JSON data, else convert directly to DataFrame
    try:
        if isinstance(data, list):
            # Normalize if data is a list of records
            df = pd.json_normalize(data)
        else:
            # If data is a dictionary, convert directly to DataFrame
            df = pd.DataFrame([data])
    except Exception as e:
        with open(output_file, 'w') as f:
            f.write(f"Error processing file {file_path}: {e}\n")
        return

    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Write basic information
        f.write(f"Data from {file_path}:\n")
        f.write("First 20 rows:\n")
        f.write(str(df.head(20)) + '\n')
        f.write("\nSummary Statistics:\n")
        f.write(str(df.describe(include='all')) + '\n')
        f.write("\nData Types:\n")
        f.write(str(df.dtypes) + '\n')
        f.write("\nMissing Values:\n")
        f.write(str(df.isnull().sum()) + '\n')
        f.write("\n")

# Paths to the JSON files and output files remain the same

# Explore each dataset and save the result to a file
seo_path = "phase3\\seo_status_data.json"
seo_output = "phase3\\seo_output.txt"
load_time_path = "phase3\\load_time_data.json"
load_time_output = "phase3\\load_time_output.txt"
design_status_path = "phase3\\design_status_data.json"
design_status_output = "phase3\\design_status_output.txt"
pwa_features_status_path = "clientes\\www.estudiomalagueta.com.br\\pwa_features_status.json"
pwa_features_status_output = "phase3\\pwa_features_status_output.txt"

load_and_explore(seo_path, seo_output)
load_and_explore(load_time_path, load_time_output)
load_and_explore(design_status_path, design_status_output)
load_and_explore(pwa_features_status_path, pwa_features_status_output)
load_and_explore(pwa_features_status_path, pwa_features_status_output)


