import subprocess
from collections import Counter
import math
import os

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

def entropy_from_file(file_path):
    """Calculate entropy of a file based on its xxd output."""
    hex_data = get_hex_data(file_path)
    return calculate_entropy(hex_data)

def calculate_entropy_for_folder(folder_path, output_file):
    """Calculate entropy for all files in a folder and save the results."""
    with open(output_file, 'w') as f:
        f.write("Filename,Entropy\n")  # Header for CSV output
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):  # Only process files, not subdirectories
                entropy = entropy_from_file(file_path)
                f.write(f"{filename},{entropy:.4f}\n")
                print(f"Processed {filename}: Entropy = {entropy:.4f}")

# Usage
folder_path = '.'  # Current directory
output_file = 'entropy_results.csv'
calculate_entropy_for_folder(folder_path, output_file)
print(f"Entropy results saved to {output_file}")
