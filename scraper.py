import requests
from bs4 import BeautifulSoup
import re
from duckduckgo_search import DDGS
import time
from duckduckgo_search.exceptions import DuckDuckGoSearchException

url = 'https://www.thechesswebsite.com/chess-openings/'

r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')

content = soup.find_all('div', id='cb-container')[1]

content_string = str(content)

text = content_string.replace("<span>MEMBERS ONLY</span>", "")
text = re.sub(r'\n\s*\n', '\n', text)

def convert_chess_opening_to_markdown(html):
    # Extract the URL, image source, and title using regex
    url_pattern = r'<a href="([^"]+)">'
    img_pattern = r'<img src="([^"]+)"/>'
    title_pattern = r'<h5>([^<]+)</h5>'
    
    url = re.search(url_pattern, html).group(1)
    img = re.search(img_pattern, html).group(1)
    title = re.search(title_pattern, html).group(1)
    
    # Search for the chess opening
    search_query = f"{title} chess opening"
    results = ""
    try:
        results = DDGS().chat(search_query)
        print(f"Successfully searched for {search_query}")
    except DuckDuckGoSearchException:
        print(f"Failed to search for {search_query}")
        
    # Extract a brief description if results found
    description = results
    
    # Create Markdown format:
    # ## Title
    # [![Title](image_url)](link_url)
    markdown = f"## {title}\n\n[![{title}]({img})]({url})\n\n"

    if description:
        markdown += f"{description}\n\n"

    return markdown

text = re.sub(
    r'<a href="[^"]+">\s*<img[^>]+/>\s*<h5>[^<]+</h5>\s*</a>',
    lambda m: convert_chess_opening_to_markdown(m.group(0)),
    text
)

text = re.sub(r'<div id="cb-container">', "# Chess Openings\n\n", text)
text = re.sub(r'</div>', "", text)

with open("output.md", "w", encoding="utf-8") as f:
        f.write(text)