from pydantic import BaseModel, Field
from typing import List, Optional

class ScrapedBaseUrl(BaseModel):
    url: str
    whitelist: Optional[List[str]] = []
    blacklist: Optional[List[str]] = []
    link_limit: Optional[int] = 100  # Default limit of 100, but user can override

class Output(BaseModel):
    all_links: List[str] = []

class MultipleFetchRequest(BaseModel):
    urls: List[str]