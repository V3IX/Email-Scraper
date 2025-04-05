import json

def is_contact_valid(contact):
    return bool(contact.get("email")) or bool(contact.get("phone"))

def clean_contact_data(input_file="data/contact_data.json", output_file="cleaned_contact_data.json"):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_data = {}

    for main_url, info in data.items():
        main_contact = info.get("contact", {})
        sub_contacts = info.get("sub_links_contact", [])

        # Filter out empty sub-links
        valid_sub_contacts = [
            entry for entry in sub_contacts
            if is_contact_valid(entry.get("contact", {}))
        ]

        # Only keep main_url if it has valid contact or any valid sub-links
        if is_contact_valid(main_contact) or valid_sub_contacts:
            cleaned_data[main_url] = {
                "contact": main_contact if is_contact_valid(main_contact) else {},
                "sub_links_contact": valid_sub_contacts
            }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print(f"Cleaned data saved to '{output_file}'")

# Run the cleaner
if __name__ == "__main__":
    clean_contact_data()
