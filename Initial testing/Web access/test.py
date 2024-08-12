import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

def scrape_links(base_url):
    """Scrapes all HTTPS links from a single URL, converts relative links to absolute, and returns a list of them."""
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Check for HTTP request errors

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all links from <a> tags
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Convert relative links to absolute and filter to include only links that start with 'https'
        https_links = []
        for link in links:
            # Print debug information
            print(f"Original link: {link}")

            # Convert relative URLs to absolute URLs
            absolute_link = urljoin(base_url, link)

            # Print debug information
            print(f"Absolute link: {absolute_link}")

            # Ensure the link is an HTTPS link
            if absolute_link.startswith('https'):
                https_links.append(absolute_link)

        return https_links

    except requests.RequestException as e:
        print(f"Request failed for {base_url}: {e}")
        return []

def create_xml(links_by_url, output_filename):
    """Creates an XML file from a dictionary of links grouped by URL."""
    root = ET.Element("root")

    for url, links in links_by_url.items():
        url_element = ET.SubElement(root, "url", {"value": url})
        for link in links:
            link_element = ET.SubElement(url_element, "link")
            link_element.text = link

    tree = ET.ElementTree(root)
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)

def scrape_websites_to_xml(input_filename, output_filename):
    """Reads URLs from the input file, scrapes HTTPS links, and writes them to an XML file."""
    links_by_url = {}

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]

            for url in urls:
                links = scrape_links(url)
                if links:
                    links_by_url[url] = links

    except FileNotFoundError:
        print(f"File {input_filename} not found.")

    create_xml(links_by_url, output_filename)

# Specify the input and output filenames
input_filename = "Websites.txt"
output_filename = "links.xml"

# Scrape the websites and create the XML file
scrape_websites_to_xml(input_filename, output_filename)
