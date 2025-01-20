from fastapi import APIRouter, HTTPException
from crawl4ai import AsyncWebCrawler
from app.models.requests import ContentCrawlRequest

# Add a description for the router
router = APIRouter(
    prefix="/content",  # This makes the endpoint /crawl/content
    tags=["content"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")  # Changed from "/content" to "/"
async def content_crawl(request: ContentCrawlRequest):
    """
    Advanced content-focused crawling with comprehensive filtering and selection options
    """
    try:
        # Basic crawler options - only include non-None values
        crawler_options = {
            "headless": request.headless,
            "viewport_width": request.viewport_width,
            "viewport_height": request.viewport_height
        }
        
        # Add optional crawler parameters only if they are not None
        if request.user_agent is not None:
            crawler_options["user_agent"] = request.user_agent
        if request.proxy_server is not None:
            crawler_options["proxy_server"] = request.proxy_server

        # Content selection and filtering options - only include non-None values
        content_options = {}
        
        # Add optional content parameters only if they are not None
        if request.css_selector is not None:
            content_options["css_selector"] = request.css_selector
        if request.word_count_threshold is not None:
            content_options["word_count_threshold"] = request.word_count_threshold
        if request.excluded_tags is not None:
            content_options["excluded_tags"] = request.excluded_tags
        if request.exclude_external_links is not None:
            content_options["exclude_external_links"] = request.exclude_external_links
        if request.exclude_social_media_links is not None:
            content_options["exclude_social_media_links"] = request.exclude_social_media_links
        if request.exclude_domains is not None:
            content_options["exclude_domains"] = request.exclude_domains
        if request.exclude_social_media_domains is not None:
            content_options["exclude_social_media_domains"] = request.exclude_social_media_domains
        if request.exclude_external_images is not None:
            content_options["exclude_external_images"] = request.exclude_external_images
        if request.process_iframes is not None:
            content_options["process_iframes"] = request.process_iframes
        if request.remove_overlay_elements is not None:
            content_options["remove_overlay_elements"] = request.remove_overlay_elements
        if request.selectors_include is not None:
            content_options["selectors_include"] = request.selectors_include
        if request.selectors_exclude is not None:
            content_options["selectors_exclude"] = request.selectors_exclude
        if request.remove_selectors is not None:
            content_options["remove_selectors"] = request.remove_selectors

        async with AsyncWebCrawler(**crawler_options) as crawler:
            result = await crawler.arun(
                url=str(request.url),
                **content_options
            )
            
            return {
                "url": str(request.url),
                "markdown": result.markdown,
                "content_only": True,
                "cleaned_html_length": len(result.cleaned_html) if hasattr(result, 'cleaned_html') else None,
                "status": "success"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 