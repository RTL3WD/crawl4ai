from fastapi import APIRouter, HTTPException
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import json

router = APIRouter(
    prefix="/extraction",
    tags=["extraction"],
    responses={404: {"description": "Not found"}},
)

class ExtractionField(BaseModel):
    name: str
    selector: str
    type: str = "text"
    attribute: Optional[str] = None
    is_collection: bool = False

class ExtractionSchema(BaseModel):
    name: str
    base_selector: str
    fields: List[ExtractionField]

class ExtractionRequest(BaseModel):
    url: str
    schema: ExtractionSchema
    headless: bool = True
    viewport_width: int = 1280
    viewport_height: int = 800
    wait_time: Optional[int] = 2

@router.post("/structured")
async def structured_extraction(request: ExtractionRequest):
    """
    Extract structured data using CSS selectors without LLM
    """
    try:
        # Convert schema to dictionary format
        schema_dict = {
            "name": request.schema.name,
            "baseSelector": request.schema.base_selector,
            "fields": [
                {
                    "name": field.name,
                    "selector": field.selector,
                    "type": field.type,
                    "isCollection": field.is_collection,
                    **({"attribute": field.attribute} if field.attribute else {})
                }
                for field in request.schema.fields
            ]
        }

        # Create extraction strategy
        extraction_strategy = JsonCssExtractionStrategy(
            schema=schema_dict,
            verbose=True
        )

        # Basic crawler options
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

        async with AsyncWebCrawler(**crawler_options) as crawler:
            result = await crawler.arun(
                url=str(request.url),
                extraction_strategy=extraction_strategy,
                wait_for=request.schema.base_selector,
                wait_time=request.wait_time or 2
            )
            
            if not result.success:
                raise HTTPException(status_code=500, detail=result.error_message)

            try:
                # Parse the extracted content
                extracted_data = json.loads(result.extracted_content) if result.extracted_content else None
                
                # Return the items directly if they exist
                items = []
                if extracted_data and isinstance(extracted_data, list):
                    items = extracted_data
                elif extracted_data and isinstance(extracted_data, dict) and "items" in extracted_data:
                    items = extracted_data["items"]
                
                return {
                    "url": str(request.url),
                    "data": items,
                    "status": "success",
                    "total_items": len(items)
                }
                
            except json.JSONDecodeError as e:
                return {
                    "url": str(request.url),
                    "data": None,
                    "status": "error",
                    "error": f"JSON decode error: {str(e)}",
                    "raw_content": result.extracted_content
                }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 