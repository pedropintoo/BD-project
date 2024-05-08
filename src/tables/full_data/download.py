import requests
import os


def get_fullData_links(dataset, release = "latest"):
    # Define the API endpoint URL
    url = f'https://api.semanticscholar.org/datasets/v1/release/{release}/dataset/{dataset}'

    api_key = os.getenv('API_KEY_SEMANTICSCHOLAR')  # API key

    # Define headers with API key
    headers = {'x-api-key': api_key}

    # Send the API request
    response = requests.get(url, headers=headers)
    links = None

    # Check response status
    if response.status_code == 200:
        response_data = response.json()
        # Process and print the response data as needed
        
        links = response_data['files']
        
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

    return links

if __name__ == '__main__':
    link = get_fullData_links("authors","2024-04-02")[0]

    print(link)

    # author_links = get_fullData_links("tables\\full_data\\authors")
    # urllib.request.urlretrieve(author_links[0], "author0.jsonl.gz")