import re
import os

# Directory containing BLOCK files
block_dir = "./BLOCKS"  # Replace with the actual path to your BLOCK files directory
output_file = "catalog_objects_sorted.txt"

# Regular expression to identify catalog objects
catalog_pattern = re.compile(r"(\d+)\s0\sobj")

def identify_and_sort_catalog_objects():
    results = []

    # Iterate through all files in the directory
    for file_name in sorted(os.listdir(block_dir)):
        file_path = os.path.join(block_dir, file_name)

        # Ensure it's a file (not a directory)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                content = file.read().decode(errors='ignore')  # Decode to string, ignore errors

                # Find all catalog objects in the content
                matches = catalog_pattern.findall(content)

                # Append results with catalog object first
                for match in matches:
                    results.append((int(match), f"{match} 0 obj: {file_name}"))

    # Sort results by catalog object number
    results.sort(key=lambda x: x[0])

    # Write results to the output file
    with open(output_file, "w") as out_file:
        for _, line in results:
            out_file.write(line + "\n")

    print(f"Catalog objects identified, sorted, and saved to '{output_file}'")

# Run the function
identify_and_sort_catalog_objects()
