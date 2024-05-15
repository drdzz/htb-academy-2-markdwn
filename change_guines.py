import os
import re

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    prev_line_empty = False

    for line in lines:
        if re.match(r'^-+$', line.strip()):  # Match lines containing dashes
            if not prev_line_empty and not line.startswith('## '):
                modified_lines[-1] = '## ' + modified_lines[-1]
                modified_lines.append(line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)

        prev_line_empty = not line.strip()

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                process_file(file_path)

# Specify your directory here
