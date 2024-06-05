import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        modified_lines = []

        for line in lines:
            stripped_line = line.strip()
            
            if stripped_line.startswith('#'):
                # Check if there are multiple sets of hashes separated by spaces
                if re.match(r'^#+(\s#+)+', stripped_line):
                    # Split the line into parts, keep the first set of hashes, and clean the rest
                    first_hash_set = re.match(r'^#+', stripped_line).group(0)
                    rest_of_line = re.sub(r'#', '', stripped_line[len(first_hash_set):]).strip()
                    cleaned_line = first_hash_set + ' ' + rest_of_line
                    modified_lines.append(cleaned_line + '\n')
                else:
                    # Leave lines like '#hello' as is
                    modified_lines.append(line)
            else:
                modified_lines.append(line)

        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                process_file(file_path)

# Example usage:
directory = "/Users/marc.ponce/Documents/Obsidian Vault/Training/Hack the Box/SQLMap Essentials/"
process_directory(directory)
