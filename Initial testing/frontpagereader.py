import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_titles_and_urls(url, before):
    """Fetches titles (headings) and associated URLs from a webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        soup = BeautifulSoup(response.content, 'html.parser')

        # Dictionary to store titles and associated URLs
        titles_and_urls = {}

        # Extract headings and their links if present
        for level in range(1, 7):  # h1 to h6
            headings = soup.find_all(f'h{level}')
            for heading in headings:
                # Extract text from the heading
                heading_text = heading.get_text(strip=True)
                
                # Find the closest <a> tag within the heading or after it
                if before:
                    link = heading.find_previous('a', href=True)
                else:
                    link = heading.find_next('a',href=True)
                link_url = urljoin(url,link['href'] if link else 'No URL found')
                
                # Store the heading text and URL
                titles_and_urls[heading_text] = link_url

        # Print the results
        for title, link in titles_and_urls.items():
            print(f"Title: {title}")
            print(f"URL: {link}\n")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

# Example usage
url = 'https://timesofoman.com/'
get_titles_and_urls(url, False)