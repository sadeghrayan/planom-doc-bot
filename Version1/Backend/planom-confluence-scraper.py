import requests
import pickle

def get_confluence_page_content(base_url, page_id, username, password):
    # Construct the URL for fetching page content
    url = f"{base_url}/rest/api/content/{page_id}?expand=body.storage"

    # Send a GET request with basic authentication
    response = requests.get(url, auth=(username, password))

    print("Response status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200:
        try:
            data = response.json()  # This line properly parses the JSON response
            if 'body' in data:
                content = data['body']['storage']['value']
                return content
        except ValueError as e:
            print("Error parsing JSON:", e)
            return None
    else:
        print("Failed to fetch Confluence page content.")
        return None

def save_data_as_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def split_content(content, max_length):
    split_content_list = []
    for i in range(0, len(content), max_length):
        split_content_list.append(content[i:i+max_length])
    return split_content_list

if __name__ == "__main__":
    # Confluence base URL
    base_url = 'https://planom.atlassian.net/wiki'

    # Confluence page ID
    page_id = '98308'

    # Credentials for basic authentication
    username = 'sadeghrayan'
    password = 'Sadegh9.com!'

    # Fetch content from Confluence page
    content = get_confluence_page_content(base_url, page_id, username, password)

    if content:
        # Split content into chunks of 256 characters
        split_content_list = split_content(content, 512)

        # Create a dictionary to store the scraped data
        scraped_data = {}
        for i, chunk in enumerate(split_content_list):
            scraped_data[f'content_{i+1}'] = chunk

        # Save the scraped data as a pickle dictionary file
        save_data_as_pickle(scraped_data, 'tom.pickle')
        print("Scraped data saved successfully.")
    else:
        print("Failed to scrape data from the Confluence page.")
