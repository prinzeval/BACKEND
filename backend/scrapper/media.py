# 5. scrapper/media.py - Simplified
from urllib.parse import urljoin
from scrapper.utils import UNWANTED_PREFIXES, is_valid_url

def extract_media_links(page_source, base_url):
    """Extract media links from the page source."""
    media_links = []
    
    # Helper to process tags with src/href attributes
    def process_tag(tag, attr):
        src = tag.get(attr)
        if src and not any(src.startswith(p) for p in UNWANTED_PREFIXES) and is_valid_url(src):
            media_links.append(urljoin(base_url, src))
    
    # Process different media types
    for img in page_source.find_all('img', src=True):
        process_tag(img, 'src')
    
    for video in page_source.find_all('video', src=True):
        process_tag(video, 'src')
        
    for audio in page_source.find_all('audio', src=True):
        process_tag(audio, 'src')
    
    # Extract PDFs from links
    for a in page_source.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.pdf'):
            process_tag(a, 'href')
    
    return list(set(media_links))  # Remove duplicates
