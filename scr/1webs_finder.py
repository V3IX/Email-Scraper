import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urlparse, urljoin

# Function to get the sublinks from a page
def get_sublinks(main_url):
    sub_links = []
    try:
        response = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all <a> tags that have 'href' attributes
            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href']
                # Make sure the link is a valid URL and it's an internal sub-link
                full_url = urljoin(main_url, href)
                parsed_url = urlparse(full_url)

                # Ensure the link is within the same domain (subwebsites)
                if parsed_url.netloc == urlparse(main_url).netloc:
                    sub_links.append(full_url)
    except Exception as e:
        print(f"Error scraping {main_url}: {e}")

    return sub_links

# Function to get Bing search results
def get_bing_search_results(query, num_results=100):
    search_url = "https://www.bing.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # List to hold the URLs
    all_urls = []
    offset = 0

    while len(all_urls) < num_results:
        params = {
            "q": query,
            "first": offset  # Pagination offset for Bing search results
        }

        # Send a GET request to Bing search
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            # Parse the search results using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all the search result links
            result_links = soup.find_all('a', {'href': True})

            # Extract the URLs from the links
            for link in result_links:
                url = link['href']
                if url.startswith('http'):
                    all_urls.append(url)
                    print(f"Found URL: {url}")

            # Move to the next page of results
            offset += 10  # Bing shows 10 results per page

        else:
            print(f"Error: Unable to fetch search results (Status code: {response.status_code})")
            break

        # Wait a bit to avoid hitting Bing too quickly (optional but recommended)
        time.sleep(2)

    # Return the first 'num_results' URLs
    return all_urls[:num_results]

# Function to get a dictionary of main link -> sub links
def get_main_to_sublinks(query, num_results):
    main_to_sublinks = {}
    main_links = get_bing_search_results(query, num_results)

    for main_link in main_links:
        sub_links = get_sublinks(main_link)
        main_to_sublinks[main_link] = sub_links
        time.sleep(2)  # Sleep between requests to avoid getting blocked

    return main_to_sublinks

# Function to save the dictionary to a JSON file
def save_to_json(data, filename="data/sublinks_results.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Example usage:
search_phrase = str(input("Enter the search phrase: "))
results = int(input("Enter the number of results to fetch: "))
result_dict = get_main_to_sublinks(search_phrase, results)

# Save the dictionary to a JSON file
save_to_json(result_dict)

print("Data has been saved to 'sublinks_results.json'")
