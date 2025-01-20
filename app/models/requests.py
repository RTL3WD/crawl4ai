from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Set, Dict, Any

class BaseCrawlRequest(BaseModel):
    url: HttpUrl
    # Crawler configuration
    headless: Optional[bool] = True
    viewport_width: Optional[int] = 1280
    viewport_height: Optional[int] = 800
    user_agent: Optional[str] = None
    proxy_server: Optional[str] = None

class ContentCrawlRequest(BaseCrawlRequest):
    # CSS Selection
    css_selector: Optional[str] = None
    
    # Content Filtering
    word_count_threshold: Optional[int] = 10
    excluded_tags: Optional[List[str]] = Field(default_factory=lambda: ["form", "header", "footer", "nav"])
    
    # Link Filtering
    exclude_external_links: Optional[bool] = False
    exclude_social_media_links: Optional[bool] = False
    exclude_domains: Optional[List[str]] = None
    exclude_social_media_domains: Optional[List[str]] = None
    
    # Media Filtering
    exclude_external_images: Optional[bool] = False
    
    # Iframe Handling
    process_iframes: Optional[bool] = False
    remove_overlay_elements: Optional[bool] = False
    
    # Content Selection
    selectors_include: Optional[List[str]] = None
    selectors_exclude: Optional[List[str]] = None
    remove_selectors: Optional[List[str]] = None 

class ExtractionSchema(BaseModel):
    name: str
    baseSelector: str
    fields: List[Dict[str, Any]]
    baseFields: Optional[List[Dict[str, Any]]] = None

class ExtractionRequest(BaseCrawlRequest):
    schema: ExtractionSchema 