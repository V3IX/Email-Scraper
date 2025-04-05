import requests
from bs4 import BeautifulSoup
import re
import json
import time

# Function to extract contact data from a webpage
def extract_contact_data(url):
    contact_data = {
        "email": [],
        "phone": [],
    }

    print(f"  [*] Scraping: {url}")
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find emails from mailto links
            email_links = soup.find_all('a', href=re.compile(r'mailto:'))
            for link in email_links:
                email = link['href'][7:].split('?')[0]  # remove any '?subject=' etc.
                if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) and email not in contact_data["email"]:
                    contact_data["email"].append(email)

            # Regex-based emails in text
            emails_in_text = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            for email in emails_in_text:
                if email not in contact_data["email"]:
                    contact_data["email"].append(email)

            # Phone numbers from tel: links
            phone_links = soup.find_all('a', href=re.compile(r'tel:'))
            for link in phone_links:
                phone = link['href'][4:]
                cleaned = re.sub(r'\D', '', phone)
                if len(cleaned) >= 9 and cleaned not in contact_data["phone"]:
                    contact_data["phone"].append(cleaned)

            # Regex-based phones in text
            phone_regex = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}'
            raw_phones = re.findall(phone_regex, response.text)
            for match in raw_phones:
                flat = ''.join(match)
                cleaned = re.sub(r'\D', '', flat)
                if len(cleaned) >= 9 and cleaned not in contact_data["phone"]:
                    contact_data["phone"].append(cleaned)

        else:
            print(f"  [!] Failed to load: {url} (Status {response.status_code})")
    
    except Exception as e:
        print(f"  [!] Error scraping {url}: {e}")

    print(f"    → Found {len(contact_data['email'])} emails, {len(contact_data['phone'])} valid phones")
    return contact_data

# Function to search for contact data in a list of websites
def search_contact_data(main_to_sublinks):
    contact_info = {}
    total_main = len(main_to_sublinks)
    main_counter = 0
    
    for main_url, sub_links in main_to_sublinks.items():
        main_counter += 1
        print(f"\n[MAIN {main_counter}/{total_main}] Scraping main URL: {main_url}")

        main_contact = extract_contact_data(main_url)
        contact_info[main_url] = {
            "contact": main_contact,
            "sub_links_contact": []
        }

        total_sub = len(sub_links)
        for i, sub_link in enumerate(sub_links, 1):
            print(f"  [SUB {i}/{total_sub}]")
            sub_contact = extract_contact_data(sub_link)
            contact_info[main_url]["sub_links_contact"].append({
                "url": sub_link,
                "contact": sub_contact
            })

            # Optional: sleep a little to reduce load / prevent blocking
            # time.sleep(0.5)

    return contact_info

# Function to save the contact data to a JSON file
def save_contact_data_to_json(contact_data, filename="data/contact_data.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(contact_data, f, ensure_ascii=False, indent=4)
    print(f"\nContact data has been saved to '{filename}'.")

# Example usage
if __name__ == "__main__":
    with open('data/deduplicated_sublinks_result.json', 'r', encoding='utf-8') as f:
        main_to_sublinks = json.load(f)

    print(f"🔍 Starting scraping on {len(main_to_sublinks)} main websites...\n")
    contact_data = search_contact_data(main_to_sublinks)
    save_contact_data_to_json(contact_data)
