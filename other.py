import os
import re
from alive_progress import alive_bar

def is_full_link(link):
    """Check if a link is a full link starting with 'http://'"""
    return link.startswith("http://")

def parse_file(file_path):
    """Parse a file and replace links as described"""
    temp_file_path = file_path + ".tmp"
    with open(file_path, "r") as file:
        with open(temp_file_path, "w") as temp_file:
            for line in file:
                # Search for links in the format ![text](link)
                while re.search(r'!\[(.*?)\]\((.*?)\)', line):
                    match = re.search(r'!\[(.*?)\]\((.*?)\)', line)
                    text = match.group(1)
                    link = match.group(2)
                    # Check if the link is not a full link
                    if not is_full_link(link):
                        # Extract filename from link
                        filename = os.path.basename(link)
                        # Replace link with desired format
                        new_link = "![[pics/" + filename + "]]"
                        # Replace the link in the line
                        line = line.replace(f"![{text}]({link})", f"![{text}]({new_link})")
                temp_file.write(line)
    os.replace(temp_file_path, file_path)

def parse_directory(directory):
    """Recursively parse files in a directory"""
    file_count = sum(len(files) for _, _, files in os.walk(directory))
    with alive_bar(file_count, title="Processing files") as bar:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                parse_file(file_path)
                bar()
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    parse_directory(directory)
