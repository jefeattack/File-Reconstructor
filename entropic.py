import os
import subprocess
import math
import csv
import shutil
from collections import Counter

# Define entropy ranges and corresponding target folders
RANGES_AND_FOLDERS = {
    (2.48, 3.32): "adobo",
    (4.14, 4.99): "doctor",
    (7.46, 8.39): "jeepy"
}

# Ensure target folders exist
for folder in RANGES_AND_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

def calculate_entropy(data):
    """Calculate the Shannon entropy of data."""
    if len(data) == 0:
        return 0
    frequency = Counter(data)
    data_len = len(data)
    entropy = -sum((freq / data_len) * math.log2(freq / data_len) for freq in frequency.values())
    return entropy

def get_hex_data(file_path):
    """Get hex data from a file using xxd."""
    result = subprocess.run(['xxd', '-p', file_path], stdout=subprocess.PIPE)
    hex_data = result.stdout.decode().replace("\n", "")
    data = bytes.fromhex(hex_data)
    return data

def move_file_based_on_entropy(file_path, entropy):
    """Move file to the appropriate folder based on its entropy."""
    for (low, high), folder in RANGES_AND_FOLDERS.items():
        if low <= entropy <= high:
            shutil.move(file_path, os.path.join(folder, os.path.basename(file_path)))
            print(f"Moved {file_path} to {folder} (Entropy={round(entropy, 4)})")
            return  # Exit after moving to prevent multiple moves

def analyze_files_in_folder(folder_path, output_file):
    """Analyze all files in a folder, output entropy results to CSV, and move based on entropy."""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'Entropy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # Calculate entropy for the file
                data = get_hex_data(file_path)
                entropy = calculate_entropy(data)
                
                # Write the result to CSV
                writer.writerow({
                    'Filename': filename,
                    'Entropy': round(entropy, 4)
                })
                
                # Move file if entropy falls within specified ranges
                move_file_based_on_entropy(file_path, entropy)

# Usage
folder_path = '.'  # Set to the directory containing the files
output_file = 'entropy_results.csv'
analyze_files_in_folder(folder_path, output_file)
print(f"Entropy results saved to {output_file}")
