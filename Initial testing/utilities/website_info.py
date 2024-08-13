import requests
from time import time
from uuid import uuid3, NAMESPACE_URL

class Website:
    def __init__(self, url) -> None:
        self.url = url
        self.last_update = time()  # Call time() to get the current time
        self.sitemapURL, self.sitemap = self.get_sitemap_urls(url)
        self.access = 0
        self.ID = uuid3(NAMESPACE_URL, url)
        self.language = "None"
        self.disallowed = self.get_robot_instructions(url)
    
    def create_XML(self):
        pass

    def get_sitemap_urls(self,url):
        """
        Retrieves sitemap URLs from the robots.txt file of the given URL.
        
        Args:
        url (str): The base URL of the website (without 'robots.txt').
        
        Returns:
        list: A list of sitemap URLs, or an empty list if none are found.
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
            
            # Split the contents into lines
            lines = response.text.splitlines()
            
            # List to store the sitemap URLs
            sitemap_urls = []
            
            for line in lines:
                # Strip whitespace and ignore comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Check if the line starts with 'Sitemap:'
                if line.lower().startswith('sitemap:'):
                    # Extract the sitemap URL and add it to the list
                    sitemap_url = line.split(':', 1)[1].strip()
                    if sitemap_url:  # Only add if the URL is not empty
                        sitemap_urls.append(sitemap_url)
            
            return sitemap_urls, True
        
        except requests.RequestException as e:
            # Print the error message
            print(f"Failed to retrieve robots.txt: {e}")
            return [], False

    def get_robot_instructions(self, url):
        """
        Retrieves the disallowed paths for user-agent '*' from the robots.txt file of the given URL.
        
        Args:
        url (str): The base URL of the website (without 'robots.txt').
        
        Returns:
        list: A list of disallowed paths for the user-agent '*', or an empty list if none are found.
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
            
            # Split the contents into lines
            lines = response.text.splitlines()
            
            # Variables to track the user-agent and disallowed paths
            disallowed_paths = []
            in_user_agent_section = False
            
            for line in lines:
                # Strip whitespace and ignore comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse the line to check if it's a user-agent or a disallow rule
                if line.lower().startswith('user-agent:'):
                    # Check if this user-agent is '*'
                    in_user_agent_section = line.split(':', 1)[1].strip() == '*'
                elif in_user_agent_section and line.lower().startswith('disallow:'):
                    # Extract the disallowed path and add it to the list
                    disallow_path = line.split(':', 1)[1].strip()
                    if disallow_path:  # Only add if the path is not empty
                        disallowed_paths.append(disallow_path)
            
            return disallowed_paths
        
        except requests.RequestException as e:
            # Print the error message
            print(f"Failed to retrieve robots.txt: {e}")
            return []

# Example usage
vg = Website('https://vg.no')
print(vg.sitemapURL)