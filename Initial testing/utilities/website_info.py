import requests
from time import time
from uuid import uuid3, NAMESPACE_URL

class Website:
    def __init__(self, url) -> None:
        self.url = url
        self.last_update = time()  # Call time() to get the current time
        self.sitemap = False
        self.access = 0
        self.ID = uuid3(NAMESPACE_URL, url)
        self.language = "None"
    
    def create_XML(self):
        

        
def get_title(url):
    pass

def get_robot_instructions(url):
    """
    Retrieves and prints the contents of the robots.txt file from the given URL.
    
    Args:
    url (str): The base URL of the website (without 'robots.txt').
    
    Returns:
    str: The content of the robots.txt file or an error message.
    """
    try:
        # Ensure the URL ends with a '/'
        if not url.endswith('/'):
            url += '/'
        
        # Construct the URL for robots.txt
        robots_url = url + "robots.txt"
        
        # Send a GET request to retrieve robots.txt
        response = requests.get(robots_url)
        response.raise_for_status()  # Check if the request was successful
        
        return response.text
    
    except requests.RequestException as e:
        # Print the error message
        print(f"Failed to retrieve robots.txt: {e}")
        return None