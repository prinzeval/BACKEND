from supabase import Client
from database import get_supabase_client
from typing import List, Dict, Union

def fetch_data(url: str) -> Dict:
    """Fetch data for a single URL from the database."""
    supabase: Client = get_supabase_client()   

    try:
        print(f"Fetching data for URL: {url}")
        response = supabase.table("scrapperDB").select("*").eq("url", url).execute()

        if not response.data:
            print("No data found for the given URL.")
            return {"error": "No data found for the given URL."}

        print(f"Data fetched successfully: {response.data}")
        return {"data": response.data}
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": str(e)}

def fetch_multiple_data(urls: List[str]) -> Dict[str, Union[List, Dict]]:
    """Fetch data for multiple URLs from the database."""
    supabase: Client = get_supabase_client()
    
    result_data = []
    errors = {}
    
    try:
        print(f"Fetching data for URLs: {urls}")
        
        # Query the database for all URLs at once using the 'in' filter
        response = supabase.table("scrapperDB").select("*").in_("url", urls).execute()
        
        # Create a dictionary to quickly look up which URLs were found
        found_urls = {item["url"]: item for item in response.data}
        
        # Process each requested URL
        for url in urls:
            if url in found_urls:
                result_data.append(found_urls[url])
            else:
                errors[url] = "No data found for this URL"
        
        print(f"Data fetched successfully for {len(result_data)} URLs")
        return {
            "data": result_data,
            "errors": errors,
            "total_found": len(result_data),
            "total_requested": len(urls)
        }
    except Exception as e:
        error_message = str(e)
        print(f"Exception occurred: {error_message}")
        return {
            "error": error_message,
            "data": result_data,
            "errors": errors
        }