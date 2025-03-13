# 3. fetch_db.py - Consolidated database operations
from typing import List, Dict, Union
from database import get_supabase_client

def fetch_data(url: str) -> Dict:
    """Fetch data for a single URL from the database."""
    supabase = get_supabase_client()   
    
    try:
        response = supabase.table("scrapperDB").select("*").eq("url", url).execute()
        return {"data": response.data} if response.data else {"error": "No data found"}
    except Exception as e:
        return {"error": str(e)}

def fetch_multiple_data(urls: List[str]) -> Dict[str, Union[List, Dict]]:
    """Fetch data for multiple URLs from the database."""
    supabase = get_supabase_client()
    
    result_data = []
    errors = {}
    
    try:
        response = supabase.table("scrapperDB").select("*").in_("url", urls).execute()
        found_urls = {item["url"]: item for item in response.data}
        
        for url in urls:
            if url in found_urls:
                result_data.append(found_urls[url])
            else:
                errors[url] = "No data found for this URL"
        
        return {
            "data": result_data,
            "errors": errors,
            "total_found": len(result_data),
            "total_requested": len(urls)
        }
    except Exception as e:
        return {
            "error": str(e),
            "data": result_data,
            "errors": errors
        }
