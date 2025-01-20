from fastapi import APIRouter, HTTPException
from crawl4ai import AsyncWebCrawler
from app.models.requests import BaseCrawlRequest

# Add a description for the router
router = APIRouter(
    prefix="/basic",  # This makes the endpoint /crawl/basic
    tags=["basic"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")  # Changed from "/basic" to "/"
async def basic_crawl(request: BaseCrawlRequest):
    """
    Basic crawling endpoint with configurable settings
    """
    try:
        # Only include non-None options
        crawler_options = {
            "headless": request.headless,
            "viewport_width": request.viewport_width,
            "viewport_height": request.viewport_height
        }
        
        # Add optional parameters only if they are not None
        if request.user_agent is not None:
            crawler_options["user_agent"] = request.user_agent
        if request.proxy_server is not None:
            crawler_options["proxy_server"] = request.proxy_server

        async with AsyncWebCrawler(**crawler_options) as crawler:
            result = await crawler.arun(url=str(request.url))
            
            return {
                "url": str(request.url),
                "markdown": result.markdown,
                "status": "success"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 