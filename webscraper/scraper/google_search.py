import json
import random
from urllib.parse import urlparse, urlunparse
from cachetools import TTLCache
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import requests

sys.path.append(str(Path(__file__).parent.parent))
from config import GOOGLE_API_KEY, SEARCH_ENGINE_ID

BLOCK_LIST = "-site:apple.com -site:samsung.com -site:facebook.com -site:instagram.com -site:pinterest.com -site:linkedin.com -site:twitter.com -site:.gov -site:.gov.br -site:wikipedia.org -filetype:pdf -filetype:html -site:google.com -site:youtube.com -site:amazon.com -site:amazon.com.br -site:ebay.com -site:walmart.com -site:aliexpress.com -site:play.google.com -site:apps.apple.com -site:mercadolivre.com.br"

# Configure logger for Google search operations
def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Cache setup
cache = TTLCache(maxsize=1000, ttl=3600)

def get_main_page_url(url):
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

# In your perform_google_search function, use the BLOCK_LIST:
def perform_google_search(query, start_index=1, num_results=10):
    logger = setup_logger('search_logger', 'google_search.log')
    logger.info(f"Performing search for query: {query}")

    results = []
    total_results_fetched = 0
    url = 'https://www.googleapis.com/customsearch/v1'
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Add more user agents here
    ]

    with requests.Session() as session:
        while total_results_fetched < num_results:
            headers = {
                'User-Agent': random.choice(user_agents)
            }
            params = {
                'q': f"{query} {BLOCK_LIST}",
                'key': GOOGLE_API_KEY,
                'cx': SEARCH_ENGINE_ID,
                'start': start_index,
                'gl': 'br',
                'lr': 'lang_pt',
            }

            try:
                response = session.get(url, headers=headers, params=params)
                response.raise_for_status()
                search_data = response.json()
                search_results = search_data.get('items', [])

                for item in search_results:
                    page_url = get_main_page_url(item['link'])
                    if page_url not in cache:  # Check if URL is not in cache
                        results.append({
                            'link': page_url,
                            'title': item.get('title'),
                            'snippet': item.get('snippet')
                        })
                        cache[page_url] = True  # Add URL to cache
                        total_results_fetched += 1
                        if total_results_fetched == num_results:
                            break

                start_index += len(search_results)

            except (HTTPError, ConnectionError, Timeout, RequestException) as err:
                logger.error(f"Error during Google Search: {err}")
                break

    return results

# Example usage
if __name__ == "__main__":
    query = "example query"
    results = perform_google_search(query, 10)
    print(json.dumps(results, indent=2))
