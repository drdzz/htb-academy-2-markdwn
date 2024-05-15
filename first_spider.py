import requests, re, os, time
from bs4 import BeautifulSoup as bs4
from markdownify import markdownify as md
import change_guines
from tqdm import tqdm

# vars
url = "https://academy.hackthebox.com/modules/unlocked"
directory = '/Users/marc.ponce/Documents/Obsidian Vault/Training/Hack the Box'
headers = {
            "Host": "academy.hackthebox.com",
            "Cookie": "_gcl_au=1.1.580230637.1715171948; ajs_anonymous_id=486b6ba2-c4fc-4034-85ba-33711676067a; _fbp=fb.1.1715171948152.1793348649; ps_mode=trackingV1; hubspotutk=83fc464dca33ad6af7079c03e9e6237a; intercom-id-awwxrc0h=e2cec2ba-529a-42c4-b93f-42197b18855e; intercom-device-id-awwxrc0h=ef37ce1a-4215-4a05-857e-61ae180dbae4; ajs_user_id=e2738a126c8a97b2dc5670d9428ba43c; tracking-preferences={%22version%22:1%2C%22destinations%22:{%22Actions%20Google%20Analytic%204%22:true%2C%22Google%20Analytics%22:true%2C%22Intercom%22:true%2C%22LinkedIn%20Insight%20Tag%22:false%2C%22Twitter%20Ads%22:false}%2C%22custom%22:{%22functional%22:true%2C%22marketingAndAnalytics%22:true%2C%22advertising%22:false}}; __cf_bm=aEtGBHWRbWTt4frx9ljVz_Pz8WVSiBKzue3VQxCIhUE-1715781136-1.0.1.1-Pl_g9AsTNB0W1d.bjooaV8LKs7pDwciQ908rOFJZ45aUSmkh_z60uL8AvqgRnj5MmhLfzc5eU8RbgTMolUQvfA; _gid=GA1.2.1693809428.1715781138; _gat_UA-93577176-12=1; _gat=1; __hstc=186608822.83fc464dca33ad6af7079c03e9e6237a.1715171949032.1715245750743.1715781139013.4; __hssrc=1; XSRF-TOKEN=eyJpdiI6InFxd2t3QTYzRU9UbjZyZFBYa21yb2c9PSIsInZhbHVlIjoiMVRqdFhMNk0vRjUrbndIM1hpUTNGMXlJZHMyZEx6Y1JXL3QwbGhsSlM2QUJVUVJ1T0c4TXNvUmgxNlh3ZUNjZk43V1RsQjB4UVR3aFFyc2Z3OGkvRk1wQ0c0bDA0MHcwSmxHUWliMFNIcXhvTTJLWUFtWTFrbnVuZk5TU0xtVTYiLCJtYWMiOiIwOTI3Y2MyM2ZmZDY4MDJlZmE3ZDU1OWRlYjg4OGQwNjkxYTg4ZTAxMmM2NDYxYmQzYjBiMjQ4Y2UwNTVkNDdmIiwidGFnIjoiIn0%3D; htb_academy_session=eyJpdiI6ImZDY3dmREJkSkpXZng2NEZ2cXpxZ2c9PSIsInZhbHVlIjoiTkw1Y3o1TXJhaGk5OC93YmZRQi9tVmc3cnlSSXIwYlAyYmpweGM0UUZxYWlRaHJwRklVZHl1SHRZTXFVTmN2MGJZQUh0OW0rc2wrNm5NUklmZ0w5djVnODg5ZTE4N3p4dUQxRis1WlBOcGNKOXZLZDlyaTdvY1BDUHU3ZnhmMlMiLCJtYWMiOiI5Y2Y1MjM2ZGY1MTU1NzhmMDk3OWIyMWQzNWJhYWIxYjFhYTg5YzU2M2YwM2FmOWJiZjg3YmM3Yzk2YjU0ODdhIiwidGFnIjoiIn0%3D; __gtm_referrer=https%3A%2F%2Faccount.hackthebox.com%2F; _ga_TKKV7WGJ6V=GS1.1.1715781138.6.1.1715781166.0.0.0; _ga=GA1.2.1428039496.1715171948; _ga_BFR4KR7D60=GS1.2.1715781138.4.1.1715781166.32.0.0; __hssc=186608822.4.1715781139013; intercom-session-awwxrc0h=U3F4OGIyaVl4TnlxSjVWdU50RGJaV0RPbVdvV0lOTEtiZ28yZThQdzJLS1Y5YnVqd0ttUUp4bjZTRU5MZzFhNC0teXhvei9PK0tqNGpwWm9NbjNMUDhLZz09--862cdf3bb27812c0957ecf27f03254f2b7115c4b",
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
change_guines.process_directory(directory)