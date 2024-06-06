import requests, re, os, json
from bs4 import BeautifulSoup as bs4
from markdownify import markdownify as md
import change_guines
from tqdm import tqdm

# vars
url = "https://academy.hackthebox.com/modules/unlocked"
directory = '/Users/marc.ponce/Documents/Obsidian Vault/Training/Hack the Box'
headers = {
            "Cookie": "htb_academy_session=eyJpdiI6IlJCcGV4cTlkNUtkV09zWkd2c3ByRlE9PSIsInZhbHVlIjoiL1lKM2xKL0pmT3hxb3pIaFhibk9SVWFhL1l6aEVMQStJUVlLdGdma2c3NEJBNjh1U045TkFMaEdsL1IwdzJFYklFTW5VQlFYUmc3L3U2TnJZY1NVSWszRHlaUkQ2alhsQnJiTFRBUy9LSTZKMGYvSFY3V2luZFFhSjFaVUM1S2EiLCJtYWMiOiJjMDY4NWQ1MTRlYTNiMjVhNzc5ZGIzNjc1YWY4Njk5NzlmNDgyZGVkMWU5OWNmNTc3YjUyOGZlOTNkYTBhOWZiIiwidGFnIjoiIn0%3D"
            }

def get_session(cookie):
    cookie_string = cookie
    cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookie_string.split("; ")}
    s = requests.Session()
    s.cookies.update(cookies)
    return s
def get_moduleNames(s):
    r = s.get(url)
    soup = bs4(r.text, "html.parser")
    modules = soup.find_all("div", class_="card")
    module_names = {}
    for module in modules[:]:
        module_name = module.find("img", alt=True)["alt"]
        module_names[module_name] = []
    return modules, module_names
def get_moduleLinks(modules, headers):
    hrefs = []
    for module in modules[:]:
        link = module.find("a")
        if link:
            hrefs.append(link.get("href"))
    # Get redirects links (and content pages, it has logic behind. SO its weird)
    redirect_info = []
    for link in tqdm(hrefs, desc=f"Getting links for each module:"):
        if link == "https://academy.hackthebox.com/module/details/67":
            module = link.split("/")[-1]
            stripped_link = link.split("/details")[0] + link.split("/details")[1]
            response = requests.get(stripped_link, headers=headers)
            r = bs4(response.text, "html.parser")
            table_contents = r.find("div", {'class': 'card', 'id': 'TOC'})
            redirect = table_contents.find_all("a")
            for r in redirect:
                a = r.get("href")
                if "/section/" in a:
                    redirect_info.append(a)
            else:continue
    module_links = {}
    for link in redirect_info:
        module_number = link.split("/")[-3]
        # Append response content to the appropriate list based on the module number
        if module_number not in module_links:
            module_links[module_number] = []
        module_links[module_number].append(link)
    return module_links
def get_content(module_links):
    content = {}
    os.system("clear")
    with tqdm(total=sum(len(value_list) for value_list in module_links.values()), desc="Getting contents for each module") as pbar1:
        for key, value_list in module_links.items():
            content[key] = []
            for value in value_list:
                r = requests.get(value, headers=headers)
                s = bs4(r.text, "html.parser")
                moduletext = s.find("div", class_="training-module")
                content[key].append(moduletext)
                pbar1.update(1)
    # put the contents into the dictionary with the key as the module name 
    for i, (content, value1) in enumerate(content.items()):
        if i < len(module_names):
            key2 = list(module_names.keys())[i]
            module_names[key2].extend(value1)
    return module_names
def to_markdown(module_names):
    os.system('clear')
    with tqdm(total=len(module_names.items()), desc="Processing data for each module:") as outer_bar:
        for key, value_list in module_names.items():
            for i, text in enumerate(value_list):
                html_to_md = md(str(text))
                processed_text = re.sub(r'\n{3,}', '\n\n', html_to_md)
                value_list[i] = processed_text
            outer_bar.update()
    return module_names
def write_to_files(module_names):
    os.system('clear')
    # Initialize the outer tqdm progress bar for module names
    with tqdm(total=len(module_names.items()), desc="\rWriting files to system:") as outer_bar:
        # Iterate over module names
        for key, value_list in module_names.items():
            # Create a folder with the name of the key
            folder_path = "/Users/marc.ponce/Documents/Obsidian Vault/Training/Hack the Box/" + key + "/"
            if os.path.exists(folder_path):
                # Skip if the folder already exists
                outer_bar.update(1)
                continue
            
            os.makedirs(folder_path, exist_ok=True)
            # Initialize the inner tqdm progress bar for loading files to the module folder
            i = 0
            # Iterate over the processed list of values
            for value in value_list:
                lines = value.split('\n')
                start_index = next((i for i, line in enumerate(lines[1:], start=1) if re.search(r'\w', line)), None)
                if start_index is not None:
                    file = lines[start_index].strip().replace("/", "-")
                    # Use the first line containing a word as the filename
                    filename = os.path.join(folder_path, f"{i}. {file}.md")
                    # Increment index for the next file
                    i += 1
                    lines.insert(3, "#hacktheboxacademy #theory")
                    # Check if the file already exists
                    if not os.path.exists(filename):
                        # Write the value starting from the line with a word to a Markdown file inside the folder
                        with open(filename, 'w') as f:
                            f.write('\n'.join(lines[3:]))
            # Update the outer progress bar
            outer_bar.update(1)

# execution flow
s = get_session(headers["Cookie"])
modules, module_names = get_moduleNames(s)
module_links = get_moduleLinks(modules, headers)
module_names = get_content(module_links)
markdowned = to_markdown(module_names)
write_to_files(markdowned)
change_guines.process_directory(directory)