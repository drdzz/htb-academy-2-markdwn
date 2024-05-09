import requests
from bs4 import BeautifulSoup as bs4
from markdownify import markdownify as md
import re
import os
from tqdm import tqdm

# vars
url = "https://academy.hackthebox.com/modules/unlocked"
headers = {
            "Host": "academy.hackthebox.com",
            "Cookie": "_gcl_au=1.1.580230637.1715171948; ajs_anonymous_id=486b6ba2-c4fc-4034-85ba-33711676067a; _gid=GA1.2.1199292335.1715171948; _fbp=fb.1.1715171948152.1793348649; ps_mode=trackingV1; hubspotutk=83fc464dca33ad6af7079c03e9e6237a; intercom-id-awwxrc0h=e2cec2ba-529a-42c4-b93f-42197b18855e; intercom-device-id-awwxrc0h=ef37ce1a-4215-4a05-857e-61ae180dbae4; ajs_user_id=e2738a126c8a97b2dc5670d9428ba43c; tracking-preferences={%22version%22:1%2C%22destinations%22:{%22Actions%20Google%20Analytic%204%22:true%2C%22Google%20Analytics%22:true%2C%22Intercom%22:true%2C%22LinkedIn%20Insight%20Tag%22:false%2C%22Twitter%20Ads%22:false}%2C%22custom%22:{%22functional%22:true%2C%22marketingAndAnalytics%22:true%2C%22advertising%22:false}}; __cf_bm=8INSe9xEIXegQuWMnV6Yi0zeHw09LGqTnH5AP.H988k-1715245749-1.0.1.1-AhCeprsF544wlkXWc5gqqawAMASH0A.oUwB5sJWG8eFREZZwDkCLYHyifKjFpymr7TgF_OKmS_ub9czHNXHQ9Q; _ga=GA1.2.1428039496.1715171948; _gat_UA-93577176-12=1; _gat=1; _ga_BFR4KR7D60=GS1.2.1715245750.3.0.1715245750.60.0.0; __hstc=186608822.83fc464dca33ad6af7079c03e9e6237a.1715171949032.1715182172129.1715245750743.3; __hssrc=1; __hssc=186608822.1.1715245750743; _ga_TKKV7WGJ6V=GS1.1.1715245749.4.0.1715245755.0.0.0; XSRF-TOKEN=eyJpdiI6IjJOdTBDc3Y4NTFKbUJTTXlRYmZyTlE9PSIsInZhbHVlIjoicE1mbkFJM0lVN2U4M1VmWGh1RFR2L3hSYUhmZ0tidjQ3N25qZmVYekNLd3BJZkFjNUU4VW5MUTlNM09ZQnB6YVdBNzJvWGkybnJ6UVdFMG03SWRaYm96dmhsUWdReDRLRjdRdkJ2SUsyQkhMcVpLMXhzRUxuUDk2YlFMZi8zVUUiLCJtYWMiOiI4ZDA3MGU3ZTI1MTUxNjA1NDc4YWE5OGY3ZTA4MDNkMjVmNGQxYjljNWYzM2IxOWYyYzFmNmFjMTI1ZGRiY2I3IiwidGFnIjoiIn0%3D; htb_academy_session=eyJpdiI6IkZNeUNnMDBZY3Izdjl6bW02bWlwQVE9PSIsInZhbHVlIjoibkRqMURoUnloMGFIa1ppcytGWW5lSEcxRy81dm1FMDIwa25jTkovbThVQ3NXR1VGZ3g0QUpWcDVuSDZ2M25TeGxHSStYYmxrOXdvSFpweG9qb0xNb0JVc3FweWpyellrWjRYakQxOHlPbVNuRllaSngyR0JCY1JJN0d6NjFBVjIiLCJtYWMiOiJjN2QyNWQ4YmI4YjBiMWQ2NjM4Y2U1ZGRmNGNlNjZkMGIwODY3ZTQ1MDI4M2E4MmM0MjEzYjczZjk1ZDU5N2YzIiwidGFnIjoiIn0%3D; intercom-session-awwxrc0h=RDNzSTlGUmRhZzFLK0dUOW5uaFpwblNBTkIxVTQyVC9XeDJHTEUveWNkL2VRcjZORjdicXlleloyMWVucWlMSy0tMWl4WE9PcjQyUkRWV05BVXFPeXpqUT09--ee2c8f2606e4586cfefd53e1aff6de3b3f832ca6",
            "Sec-Ch-Ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"macOS\"",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://academy.hackthebox.com/module/details/41",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Priority": "u=0, i"
        }

# methods
def get_session(cookie):
    # Define the intercepted cookie string
    cookie_string = cookie
    # Parse the cookie string into a dictionary
    cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookie_string.split("; ")}
    # Open the session 
    s = requests.Session()
    s.cookies.update(cookies)
    return s
def get_moduleNames(s):
    r = s.get(url)
    # Make the bs4 object
    soup = bs4(r.text, "html.parser")
    modules = soup.find_all("div", class_="card")
    module_names = {}
    for module in modules[0:7]:
        module_name = module.find("img", alt=True)["alt"]
        module_names[module_name] = []
    return modules, module_names
def get_moduleLinks(modules, headers):
    hrefs = []
    for module in modules[:7]:
        link = module.find("a")
        if link:
            hrefs.append(link.get("href"))
    # Get redirects links (and content pages, it has logic behind. SO its weird)
    redirect_info = []
    for link in tqdm(hrefs, desc=f"Getting links for each module:"):
        module = link.split("/")[-1]
        stripped_link = link.split("/details")[0] + link.split("/details")[1]
        response = requests.get(stripped_link, headers=headers)
        r = bs4(response.text, "html.parser")
        redirect = r.find_all("a")
        for r in redirect:
            a = r.get("href")
            if "/section/" in a:
                redirect_info.append(a)
        #os.system("clear")
    #better presentation as a list of lists
    #redirects = sorted(set(redirect_info))
    module_links = {}
    for link in redirect_info:
        module_number = link.split("/")[-3]
        # Append response content to the appropriate list based on the module number
        if module_number not in module_links:
            module_links[module_number] = []
        module_links[module_number].append(link)

    sorted_dict = {}

    for key, value in module_links.items():
        # Remove duplicates and sort based on the last number after a "/"
        sorted_values = sorted(set(value), key=lambda x: int(re.search(r'/(\d+)$', x).group(1)))
        sorted_dict[key] = sorted_values
    return sorted_dict
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
    # Initialize the outer tqdm progress bar for module names
    with tqdm(total=len(module_names.items()), desc="Processing data for each module:") as outer_bar:
        # Iterate over module names
        for key, value_list in module_names.items():
            # Initialize the inner tqdm progress bar for each value list
                # Iterate over values in the list
            for i, text in enumerate(value_list):
                html_to_md = md(str(text))
                processed_text = re.sub(r'\n{3,}', '\n\n', html_to_md)
                value_list[i] = processed_text
                # Update both progress bars
            outer_bar.update()
    return module_names
def write_to_files(module_names):
    os.system('clear')
    # Initialize the outer tqdm progress bar for module names
    with tqdm(total=len(module_names.items()), desc="\rWriting files to system:") as outer_bar:
        # Iterate over module names
        for key, value_list in module_names.items():
            # Create a folder with the name of the key
            #key = key.replace("/", "\/")
            folder_path = "/Users/marc.ponce/Documents/Obsidian Vault/Training/Hack the Box/" + key + "/"
            os.makedirs(folder_path, exist_ok=True)
            # Initialize the inner tqdm progress bar for loading files to the module folder
            i = 0
            # Iterate over the processed list of values
            for value in value_list:
                lines = value.split('\n')
                start_index = next((i for i, line in enumerate(lines[1:], start=1) if re.search(r'\w', line)), None)
                if start_index is not None:
                    file = lines[start_index].strip()
                    file = file.replace("/","-")
                        # Use the first line containing a word as the filename
                    filename = os.path.join(folder_path + str(i) + ". " + file + ".md")
                        # Increment index for the next file
                    i += 1
                    lines.insert(3, "#hacktheboxacademy #theory")
                        # Write the value starting from the line with a word to a Markdown file inside the folder
                    with open(filename, 'w') as f:
                        f.write('\n'.join(lines[3:]))
            outer_bar.update()  # Update the outer progress bar

# execution flow
s = get_session(headers["Cookie"])
modules, module_names = get_moduleNames(s)
module_links = get_moduleLinks(modules, headers)
module_names = get_content(module_links)
markdowned = to_markdown(module_names)
write_to_files(markdowned)