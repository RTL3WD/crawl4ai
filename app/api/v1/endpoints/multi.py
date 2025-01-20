from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import List, Optional
import asyncio

router = APIRouter()

class CrawlMode(str, Enum):
    SEQUENTIAL = "sequential"  # Crawl URLs one by one with session reuse
    PARALLEL = "parallel"      # Crawl URLs in parallel with browser reuse

class MultiCrawlRequest(BaseModel):
    urls: List[HttpUrl]
    mode: CrawlMode = CrawlMode.SEQUENTIAL
    max_concurrent: Optional[int] = 3  # For parallel mode
    headless: bool = True
    viewport_width: int = 1280
    viewport_height: int = 800
    session_reuse: bool = True  # Whether to reuse session across URLs

@router.post("/multi")
async def multi_crawl(request: MultiCrawlRequest):
    """
    Crawl multiple URLs either sequentially or in parallel.
    Uses browser reuse for better performance and resource management.
    """
    try:
        from crawl4ai import AsyncWebCrawler

        results = []
        # Use async context manager for automatic cleanup
        async with AsyncWebCrawler(
            headless=request.headless,
            viewport_width=request.viewport_width,
            viewport_height=request.viewport_height,
            extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"]
        ) as crawler:
            
            if request.mode == CrawlMode.SEQUENTIAL:
                # Sequential crawling with session reuse
                session_id = "shared_session" if request.session_reuse else None
                for url in request.urls:
                    result = await crawler.arun(
                        url=str(url),
                        session_id=session_id
                    )
                    results.append({
                        "url": str(url),
                        "success": result.success if hasattr(result, 'success') else True,
                        "data": {
                            "html": result.html if hasattr(result, 'html') else None,
                            "markdown": result.markdown if hasattr(result, 'markdown') else None,
                            "cleaned_html": result.cleaned_html if hasattr(result, 'cleaned_html') else None,
                            "links": result.links if hasattr(result, 'links') else None
                        }
                    })
            else:  # Parallel mode
                # Process URLs in batches
                for i in range(0, len(request.urls), request.max_concurrent):
                    batch = request.urls[i:i + request.max_concurrent]
                    tasks = []
                    
                    for j, url in enumerate(batch):
                        # Create unique session ID for each URL unless session reuse is enabled
                        session_id = "shared_session" if request.session_reuse else f"session_{i + j}"
                        task = crawler.arun(
                            url=str(url),
                            session_id=session_id
                        )
                        tasks.append(task)
                    
                    # Wait for batch to complete
                    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Process batch results
                    for url, result in zip(batch, batch_results):
                        if isinstance(result, Exception):
                            results.append({
                                "url": str(url),
                                "success": False,
                                "error": str(result)
                            })
                        else:
                            results.append({
                                "url": str(url),
                                "success": result.success if hasattr(result, 'success') else True,
                                "data": {
                                    "html": result.html if hasattr(result, 'html') else None,
                                    "markdown": result.markdown if hasattr(result, 'markdown') else None,
                                    "cleaned_html": result.cleaned_html if hasattr(result, 'cleaned_html') else None,
                                    "links": result.links if hasattr(result, 'links') else None
                                }
                            })

        # Prepare summary
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful

        return {
            "status": "success",
            "mode": request.mode,
            "summary": {
                "total_urls": len(request.urls),
                "successful": successful,
                "failed": failed
            },
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 