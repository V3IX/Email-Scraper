import json

# Function to remove duplicate sub-links from the JSON data
def remove_duplicates(input_filename="sublinks_results.json", output_filename="cleaned_sublinks_results.json"):
    # Load the data from the original JSON file
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create a new dictionary to store the cleaned data
    cleaned_data = {}

    for main_link, sub_links in data.items():
        # Remove duplicates by converting the list of sub-links to a set
        cleaned_sub_links = list(set(sub_links))
        cleaned_data[main_link] = cleaned_sub_links

    # Save the cleaned data to a new JSON file
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print(f"Duplicates removed. Cleaned data has been saved to '{output_filename}'.")

# Example usage:
remove_duplicates(input_filename="data/sublinks_results.json", output_filename="data/cleaned_sublinks_results.json")
