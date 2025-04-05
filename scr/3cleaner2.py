import json

def deduplicate_sublinks_across_mains(input_file="data/sublinks_results.json", output_file="data/deduplicated_sublinks_result.json"):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    seen_sublinks = set()
    cleaned_data = {}

    for main_url, sub_links in data.items():
        unique_sub_links = []
        for link in sub_links:
            if link not in seen_sublinks:
                seen_sublinks.add(link)
                unique_sub_links.append(link)
            else:
                print(f"Duplicate sublink skipped: {link}")

        if unique_sub_links:
            cleaned_data[main_url] = unique_sub_links

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print(f"Deduplicated sub-links saved to '{output_file}'")

if __name__ == "__main__":
    deduplicate_sublinks_across_mains()
