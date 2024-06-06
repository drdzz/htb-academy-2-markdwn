import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        modified_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()  # Remove trailing whitespace
            stripped_line = line.strip()

            # Check if the current line is a valid title (words) and the next line is dashes
            if stripped_line and not stripped_line.startswith("##") and re.match(r'^\w+', stripped_line) and i + 1 < len(lines) and re.match(r'^\s*-{3,}\s*$', lines[i + 1].strip()):
                # Transform the title into a Markdown heading
                modified_lines.append(f'## {stripped_line}\n')
                modified_lines.append(lines[i + 1])  # Add the line with dashes
                i += 2  # Skip the next line (already processed)
                continue

            # Leave lines like '#hashtag' intact
            if re.match(r'^#[A-Za-z0-9]', stripped_line):
                modified_lines.append(line + '\n')
                i += 1
                continue
            
            # Match lines that are just hashes and replace them with empty lines
            if re.match(r'^#+$', stripped_line):
                modified_lines.append('\n')
                i += 1
                continue

            # Match lines that start with multiple sets of hashes
            if re.match(r'^#+(\s#+)+', stripped_line):
                first_hash_set = re.match(r'^#+', stripped_line).group(0)
                rest_of_line = re.sub(r'#', '', stripped_line[len(first_hash_set):]).strip()
                cleaned_line = first_hash_set + ' ' + rest_of_line
                modified_lines.append(cleaned_line + '\n')
            else:
                modified_lines.append(line + '\n')

            i += 1

        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                process_file(file_path)

# Example usage:
directory = "/Users/marc.ponce/Documents/Obsidian Vault/Training/Hack the Box/"
process_directory(directory)
