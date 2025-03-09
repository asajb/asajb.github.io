import re
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

def create_opening_subpage(title):
    #search_query = f'{title} chess opening'
    search_query = f'{title}'
    search_query = search_query.lower()
    results = ""
    try:
        results = DDGS().chat(f'give 3 links for {search_query}')
        print(f"Successfully searched for {repr(search_query)}")
    except DuckDuckGoSearchException:
        print(f"Failed to search for {repr(search_query)}")
    
    answer = f'## {title}\n\n + ChatGPT search results for {title} chess opening:\n\n'
    answer += results
    with open(f'openings/{title.replace(" ", "-").lower()}.md', 'w') as f:
        f.write(answer)

def add_a_bit(text):
    #opening_pattern = r'## .*\n'

    #title = re.search(opening_pattern, text).group(0)
    title = text[3:-1]

    create_opening_subpage(title)
    
    result = f'## [{title}](openings/{title.replace(" ", "-").lower()}.md)\n'
    return result
    
with open("index.md", "r") as f:
    text = f.read()

pattern = r'(?<![#])## .*\n'

text = re.sub(pattern, lambda m: add_a_bit(m.group(0)), text)

with open("index.md", "w") as f:
    f.write(text)
