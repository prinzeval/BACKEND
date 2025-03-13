# 6. scrapper/Url_Info.py - Refactored to use utility functions
from datetime import datetime, timedelta
from typing import List
from database import get_supabase_client
from scrapper.utils import is_in_whitelist, is_in_blacklist, fetch_page
from scrapper.media import extract_media_links

def bring_data(urls: List[str], whitelist: List[str], blacklist: List[str]):
    """Fetch data from URLs and save to the database."""
    supabase = get_supabase_client()
    
    for url in urls:
        if not is_in_whitelist(url, whitelist) or is_in_blacklist(url, blacklist):
            continue
            
        # Check if data already exists
        existing_data = supabase.table("scrapperDB").select("*").eq("url", url).execute()
        if existing_data.data:
            continue
        
        try:
            page_source = fetch_page(url)
            
            # Clean the page
            for tag in page_source.find_all(['a', 'script', 'style', 'aside', 'footer', 'header', 'nav']):
                tag.decompose()
            
            # Extract title
            title_element = page_source.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title'])
            title = title_element.text if title_element else "No title found"
            
            # Extract body text
            body_text = page_source.get_text(separator=' ').strip()
            body_text = '.\n'.join(' '.join(body_text.split()).split('. '))
            
            # Extract media links
            media_links = extract_media_links(page_source, url)
            media_links_str = ', '.join(media_links)
            
            # Save to database
            created_at = datetime.utcnow() - timedelta(hours=2)
            supabase.table("scrapperDB").insert({
                "created_at": str(created_at),
                "title": title,
                "content": body_text,
                "media_links": media_links_str,
                "url": url
            }).execute()
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
