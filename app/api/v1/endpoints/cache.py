from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import Optional

router = APIRouter()

class CacheMode(str, Enum):
    ENABLED = "enabled"    # Normal caching (read/write)
    DISABLED = "disabled"  # No caching at all
    READ_ONLY = "read_only"    # Only read from cache
    WRITE_ONLY = "write_only"  # Only write to cache
    BYPASS = "bypass"      # Skip cache for this operation

class CrawlRequest(BaseModel):
    url: HttpUrl
    cache_mode: CacheMode = CacheMode.ENABLED
    headless: bool = True
    viewport_width: int = 1280
    viewport_height: int = 800

@router.post("/cached")
async def cached_crawl(request: CrawlRequest):
    """
    Crawl a webpage with the new caching system (Crawl4AI 0.5.0+).
    Cache modes:
    - ENABLED: Normal caching (read/write)
    - DISABLED: No caching at all
    - READ_ONLY: Only read from cache
    - WRITE_ONLY: Only write to cache
    - BYPASS: Skip cache for this operation
    """
    try:
        from crawl4ai import AsyncWebCrawler, CacheMode as Crawl4AICacheMode

        # Map our API cache mode to Crawl4AI cache mode
        cache_mode_mapping = {
            CacheMode.ENABLED: Crawl4AICacheMode.ENABLED,
            CacheMode.DISABLED: Crawl4AICacheMode.DISABLED,
            CacheMode.READ_ONLY: Crawl4AICacheMode.READ_ONLY,
            CacheMode.WRITE_ONLY: Crawl4AICacheMode.WRITE_ONLY,
            CacheMode.BYPASS: Crawl4AICacheMode.BYPASS
        }

        # Create crawler with configuration
        crawler_options = {
            "headless": request.headless,
            "viewport_width": request.viewport_width,
            "viewport_height": request.viewport_height
        }

        # Add optional parameters if they exist
        if hasattr(request, 'user_agent') and request.user_agent is not None:
            crawler_options["user_agent"] = request.user_agent
        if hasattr(request, 'proxy_server') and request.proxy_server is not None:
            crawler_options["proxy_server"] = request.proxy_server

        # Use async context manager to ensure proper browser initialization and cleanup
        async with AsyncWebCrawler(**crawler_options) as crawler:
            # Perform crawl with cache mode
            result = await crawler.arun(
                url=str(request.url),
                cache_mode=cache_mode_mapping[request.cache_mode]  # Pass cache mode directly
            )

            if not hasattr(result, 'success') or not result.success:
                error_msg = getattr(result, 'error_message', 'Unknown error occurred')
                raise HTTPException(status_code=500, detail=error_msg)

            # Build response with available attributes
            response = {
                "status": "success",
                "cache_mode": request.cache_mode,
                "data": {}
            }

            # Add available attributes to response
            if hasattr(result, 'cache_hit'):
                response["cache_hit"] = result.cache_hit
            if hasattr(result, 'html') and result.html:  # Only add if not empty
                response["data"]["html"] = result.html
            if hasattr(result, 'markdown') and result.markdown:  # Only add if not empty
                response["data"]["markdown"] = result.markdown
            if hasattr(result, 'cleaned_html') and result.cleaned_html:  # Only add if not empty
                response["data"]["cleaned_html"] = result.cleaned_html
            if hasattr(result, 'content') and result.content:  # Only add if not empty
                response["data"]["content"] = result.content
            if hasattr(result, 'links') and result.links:  # Only add if not empty
                response["data"]["links"] = result.links

            # Check if we got any actual data
            if not any(response["data"].values()):
                raise HTTPException(
                    status_code=500, 
                    detail="Crawl completed but no content was retrieved. This might be due to page loading issues or content blocking."
                )

            return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 