# 8. tools.py - Refactored to use the utilities
from scrapper.AllUrlsScrape import ScraperKING
from scrapper.Url_Info import bring_data
from scrapper.media import extract_media_links
from scrapper.utils import fetch_page, is_in_whitelist, is_in_blacklist
from models import ScrapedBaseUrl, Output
from urllib.parse import urljoin, urlparse
from collections import deque
from typing import Dict, List

# Helper to convert comma-separated string to list
def parse_list_param(param_str):
    return [item.strip() for item in param_str.split(",") if item.strip()] if param_str else []

# Reusable scraping functions
async def web_scraper(url: str, whitelist: str = "", blacklist: str = "", link_limit: int = 100, memory: Dict = {}):
    try:
        whitelist_list = parse_list_param(whitelist)
        blacklist_list = parse_list_param(blacklist)
        
        scraper = ScraperKING(link_limit=link_limit)
        result = scraper.scrape_website_links(url, whitelist_list, blacklist_list)
        
        memory["scrapedLinks"] = result.get("all_links", [])
        return {
            "responseString": f"Scraped {len(memory['scrapedLinks'])} links with limit {link_limit}.",
            "memory": memory
        }
    except Exception as e:
        return {
            "responseString": f"Error: {str(e)}",
            "memory": memory
        }

async def scrape_single_page(url: str, memory: Dict = {}):
    try:
        bring_data([url], [url], [])
        memory["scrapedContent"] = "Content from the single page scrape is now available."
        return {
            "responseString": f"Scraped content from {url}.",
            "memory": memory
        }
    except Exception as e:
        return {
            "responseString": f"Error: {str(e)}",
            "memory": memory
        }

async def extract_media_from_single_page(url: str, memory: Dict = {}):
    try:
        page_source = fetch_page(url)
        media_links = extract_media_links(page_source, url)
        
        memory["mediaLinks"] = media_links
        return {
            "responseString": f"Extracted {len(media_links)} media links from {url}.",
            "memory": memory
        }
    except Exception as e:
        return {
            "responseString": f"Error: {str(e)}",
            "memory": memory
        }

async def multiple_page_media(url: str, whitelist: str = "", blacklist: str = "", link_limit: int = 100, memory: Dict = {}):
    try:
        # First get all links without scraping content
        whitelist_list = parse_list_param(whitelist)
        blacklist_list = parse_list_param(blacklist)
        
        scraper = ScraperKING(link_limit=link_limit)
        # We'll modify this to not call bring_data
        result = scraper.get_links_only(url, whitelist_list, blacklist_list)
        all_links = result.get("all_links", [])
        
        # Then extract media from each link
        media_links = []
        for link in all_links:
            try:
                page_source = fetch_page(link)
                media_links.extend(extract_media_links(page_source, link))
            except Exception:
                continue
        
        memory["mediaLinks"] = media_links
        return {
            "responseString": f"Extracted {len(media_links)} media links from {len(all_links)} pages.",
            "memory": memory
        }
    except Exception as e:
        return {
            "responseString": f"Error: {str(e)}",
            "memory": memory
        }

async def extract_links_only(url: str, whitelist=None, blacklist=None):
    try:
        page_source = fetch_page(url)
        
        links = set()
        for a_tag in page_source.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            
            if (not whitelist or any(w in full_url for w in whitelist)) and \
               (not blacklist or not any(b in full_url for b in blacklist)):
                links.add(full_url)
        
        return {"links": list(links)}
    except Exception as e:
        return {"error": str(e)}

async def extract_related_links(url: str, whitelist=None, blacklist=None, link_limit: int = 10):
    try:
        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc
        
        queue = deque([url])
        visited = set()
        related_links = set()
        
        while queue and len(related_links) < link_limit:
            current_url = queue.popleft()
            if current_url in visited:
                continue
                
            visited.add(current_url)
            
            try:
                page_source = fetch_page(current_url)
                
                for a_tag in page_source.find_all('a', href=True):
                    href = a_tag['href']
                    full_url = urljoin(current_url, href)
                    parsed_full_url = urlparse(full_url)
                    
                    if parsed_full_url.netloc == base_domain and full_url not in visited:
                        if (not whitelist or any(w in full_url for w in whitelist)) and \
                           (not blacklist or not any(b in full_url for b in blacklist)):
                            related_links.add(full_url)
                            queue.append(full_url)
            except Exception:
                continue
                
        return {"related_links": list(related_links)}
    except Exception as e:
        return {"error": str(e)}
