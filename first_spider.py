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
            "Cookie": "_gcl_au=1.1.580230637.1715171948; ajs_anonymous_id=486b6ba2-c4fc-4034-85ba-33711676067a; _fbp=fb.1.1715171948152.1793348649; ps_mode=trackingV1; hubspotutk=83fc464dca33ad6af7079c03e9e6237a; intercom-id-awwxrc0h=e2cec2ba-529a-42c4-b93f-42197b18855e; intercom-device-id-awwxrc0h=ef37ce1a-4215-4a05-857e-61ae180dbae4; ajs_user_id=e2738a126c8a97b2dc5670d9428ba43c; tracking-preferences={%22version%22:1%2C%22destinations%22:{%22Actions%20Google%20Analytic%204%22:true%2C%22Google%20Analytics%22:true%2C%22Intercom%22:true%2C%22LinkedIn%20Insight%20Tag%22:false%2C%22Twitter%20Ads%22:false}%2C%22custom%22:{%22functional%22:true%2C%22marketingAndAnalytics%22:true%2C%22advertising%22:false}}; __cf_bm=Duil5lw_9jhS5m6M9PejqUDYIEA9L3_Wv1aNuSFJwK0-1717430417-1.0.1.1-pR1NlNtjhHNM_vTj5uIqJ_TOaYqGS3dZ5xjyMFG9UNmuAqkDXZIRIJu0pF4f6p4rfnwMdxw58YTSvLaM7DecVw; _gid=GA1.2.82511626.1717430421; _gat_UA-93577176-12=1; _gat=1; __hstc=186608822.83fc464dca33ad6af7079c03e9e6237a.1715171949032.1715781139013.1717430421510.5; __hssrc=1; XSRF-TOKEN=eyJpdiI6Im5SK0VDTTJEZHVhM3VpMVZ4amhFUEE9PSIsInZhbHVlIjoiN1ZnTGdLVlRQOFM2U1Z3eXZMaTAxcUZ4cEdYQjlYdnJXN1V0cytnTVh2NjdMYnl0YWt2aGhEZWRtYUpyTkcrd05LUzZjNW44Qk9OcUg2YWduM0RMeXVLZjZoUDdQbXBraEZJa0ZKdEdUcWVlaTQ1d2lvY3VrNEE1OFBZanhVeUsiLCJtYWMiOiI1ZGNkODU0NWUzNTdmNTZjNjg4OWEyMDEwMWZlNGZkNWVhODgwZjAzNTU3ZjZlMTU5YTU0YjM5ZmM4YTM5MzJkIiwidGFnIjoiIn0%3D; htb_academy_session=eyJpdiI6ImRoQ3F4aFB2UFp6V1RYMEJMT0JDSVE9PSIsInZhbHVlIjoiUmFkOUhtVWg3Z3YvVUxvbVg2RHJKbWVOQmVmMUlZZmpzdzJoK2pPejh3N3JDNlp2VnBsdmNHcldKclAxbUpnTEVqZkxUdGxMbm1EUUJIQUQzQWg4OG9MeVFBVUFMeWNTYUlyOEkwTGhKd1kxWUtxbVQvUXFrb1hxMyt6VHNDOS8iLCJtYWMiOiIyZTVkMTEyNWYwZjI1NmM5YWM2MjdlNmU2OGZhNGEyNjBhODgyYmM0ZDA4Y2YxNWU4NjhiOGJjM2EwMzg1MDEyIiwidGFnIjoiIn0%3D; __gtm_referrer=https%3A%2F%2Faccount.hackthebox.com%2F; _ga_TKKV7WGJ6V=GS1.1.1717430420.8.1.1717430438.0.0.0; _ga=GA1.2.1428039496.1715171948; _ga_BFR4KR7D60=GS1.2.1717430421.5.1.1717430440.41.0.0; __hssc=186608822.2.1717430421510"
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
    for module in modules[:1]:
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