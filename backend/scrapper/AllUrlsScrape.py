# 7. scrapper/AllUrlsScrape.py - Refactored
from collections import deque
from typing import List, Dict
from scrapper.utils import is_valid_url, is_valid_link, is_in_whitelist, is_in_blacklist, fetch_page
from scrapper.Url_Info import bring_data
from urllib.parse import urljoin

class ScraperKING:
    def __init__(self, link_limit=100):
        self.all_links = set()
        self.visited_links = set()
        self.link_limit = link_limit
    
    def get_links_only(self, base_url: str, whitelist: List[str], blacklist: List[str]) -> Dict:
        """Scrape website for links without processing content."""
        # Ensure base URL starts with http
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
            
        # Initialize with base URL
        self.all_links.add(base_url)
        link_queue = deque([base_url])
        links_scraped = 0
        
        try:
            while link_queue and links_scraped < self.link_limit:
                url = link_queue.popleft()
                
                # Skip if already visited or invalid
                if url in self.visited_links or not is_valid_url(url, base_url):
                    continue
                    
                # Check whitelist/blacklist
                if is_in_whitelist(url, whitelist) and not is_in_blacklist(url, blacklist):
                    try:
                        page_source = fetch_page(url)
                        
                        # Find all links on the page
                        new_links = {
                            urljoin(url, a['href']) for a in page_source.find_all('a', href=True)
                            if is_valid_url(urljoin(url, a['href']), base_url) and 
                            is_valid_link(a['href']) and 
                            not (a['href'].startswith('#') or 
                                 a['href'].startswith('mailto:') or 
                                 a['href'].startswith('javascript:'))
                        }
                        
                        # Remove self-references
                        new_links = {link for link in new_links if link.rstrip('/') != url.rstrip('/')}
                        
                        # Update tracking
                        self.all_links.update(new_links)
                        link_queue.extend(new_links)
                        self.visited_links.add(url)
                        links_scraped += 1
                        
                    except Exception as e:
                        print(f"Error fetching {url}: {e}")
                
            # Standardize to https
            all_links = {link.replace('http://', 'https://') if link.startswith('http://') else link 
                         for link in self.all_links}
            
            # Return links without processing with bring_data
            return {'all_links': list(all_links)}
            
        except Exception as e:
            return {"error": f"Error scraping {base_url}: {str(e)}"}
    
    def scrape_website_links(self, base_url: str, whitelist: List[str], blacklist: List[str]) -> Dict:
        """Scrape website for links within constraints and process content."""
        # Ensure base URL starts with http
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url
            
        # Initialize with base URL
        self.all_links.add(base_url)
        link_queue = deque([base_url])
        links_scraped = 0
        
        try:
            while link_queue and links_scraped < self.link_limit:
                url = link_queue.popleft()
                
                # Skip if already visited or invalid
                if url in self.visited_links or not is_valid_url(url, base_url):
                    continue
                    
                # Check whitelist/blacklist
                if is_in_whitelist(url, whitelist) and not is_in_blacklist(url, blacklist):
                    try:
                        page_source = fetch_page(url)
                        
                        # Find all links on the page
                        new_links = {
                            urljoin(url, a['href']) for a in page_source.find_all('a', href=True)
                            if is_valid_url(urljoin(url, a['href']), base_url) and 
                            is_valid_link(a['href']) and 
                            not (a['href'].startswith('#') or 
                                 a['href'].startswith('mailto:') or 
                                 a['href'].startswith('javascript:'))
                        }
                        
                        # Remove self-references
                        new_links = {link for link in new_links if link.rstrip('/') != url.rstrip('/')}
                        
                        # Update tracking
                        self.all_links.update(new_links)
                        link_queue.extend(new_links)
                        self.visited_links.add(url)
                        links_scraped += 1
                        
                    except Exception as e:
                        print(f"Error fetching {url}: {e}")
                
            # Standardize to https
            all_links = {link.replace('http://', 'https://') if link.startswith('http://') else link 
                         for link in self.all_links}
            
            output_data = {'all_links': list(all_links)}
            
            # Process links
            bring_data(output_data['all_links'], whitelist, blacklist)
            
            return output_data
            
        except Exception as e:
            return {"error": f"Error scraping {base_url}: {str(e)}"}