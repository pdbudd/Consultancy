import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from utilities.website_info import get_robot_instructions

from bs4 import BeautifulSoup
import requests

url = "https://vg.no"

get_robot_instructions(url)