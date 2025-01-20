from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import markdown2

router = APIRouter()

# Convert markdown files to HTML
def get_markdown_content():
    docs = {
        "overview": """# Crawl4AI API Documentation

Welcome to the Crawl4AI API documentation! This guide will help you understand and use our web crawling API effectively.

## Getting Started

Crawl4AI provides a powerful HTTP API for web crawling and data extraction. The API is built using FastAPI and supports various features like browser automation, content extraction, and caching.

### Base URL
```
http://localhost:8000/api/v1
```

### Prerequisites
- Python 3.9+
- FastAPI
- Crawl4AI library

### Installation
```bash
pip install -r requirements.txt
```

### Running the API
```bash
uvicorn app.main:app --reload
```
""",
        "endpoints": """# API Endpoints

## Basic Crawling
**Endpoint**: `POST /api/v1/crawl/basic`

Performs a basic crawl of a webpage, returning HTML content and metadata.

### Request
```json
{
  "url": "https://example.com",
  "headless": true,
  "viewport_width": 1280,
  "viewport_height": 800
}
```

### Response
```json
{
  "status": "success",
  "url": "https://example.com",
  "html": "...",
  "markdown": "...",
  "cleaned_html": "...",
  "links": ["..."]
}
```

## Content Extraction
**Endpoint**: `POST /api/v1/crawl/content`

Extracts specific content from a webpage using CSS selectors.

### Request
```json
{
  "url": "https://quotes.toscrape.com",
  "selectors_include": [".quote"],
  "selectors_exclude": [".footer"],
  "remove_selectors": [".tags"]
}
```

### Response
```json
{
  "status": "success",
  "url": "https://quotes.toscrape.com",
  "content": {
    "extracted_content": "...",
    "matched_elements": 10
  }
}
```

## Structured Data Extraction
**Endpoint**: `POST /api/v1/crawl/extraction/structured`

Extracts structured data from a webpage using a defined schema.

### Request
```json
{
  "url": "https://quotes.toscrape.com",
  "schema": {
    "name": "Quotes",
    "base_selector": ".quote",
    "fields": [
      {
        "name": "text",
        "selector": ".text",
        "type": "text"
      },
      {
        "name": "author",
        "selector": ".author",
        "type": "text"
      },
      {
        "name": "tags",
        "selector": ".tag",
        "type": "text",
        "is_collection": true
      }
    ]
  }
}
```

## Multi-URL Crawling
**Endpoint**: `POST /api/v1/crawl/multi`

Crawls multiple URLs in parallel or sequentially.

### Request
```json
{
  "urls": [
    "https://quotes.toscrape.com",
    "https://books.toscrape.com"
  ],
  "mode": "parallel",
  "max_concurrent": 2,
  "headless": true,
  "session_reuse": true
}
```

## Cache Management
**Endpoint**: `POST /api/v1/crawl/cached`

Performs crawling with caching support.

### Request
```json
{
  "url": "https://quotes.toscrape.com",
  "cache_mode": "enabled",
  "headless": true,
  "viewport_width": 1280,
  "viewport_height": 800
}
```

### Cache Modes
- `enabled`: Use cache if available, otherwise crawl and cache
- `disabled`: Never use cache, always crawl
- `read_only`: Only use cache, fail if not cached
- `write_only`: Always crawl and update cache
- `bypass`: Ignore cache completely
""",
        "best_practices": """# Best Practices & Error Handling

## Best Practices

### 1. Rate Limiting
- Implement appropriate delays between requests
- Use the cache feature for frequently accessed pages
- Consider using the multi-URL crawler with session_reuse: true for better performance

### 2. Selector Optimization
- Use specific CSS selectors to target exact elements
- Combine selectors_include and selectors_exclude for precise content extraction
- Test selectors in browser dev tools before using them in API calls

### 3. Browser Configuration
- Use headless: true for better performance when visual rendering isn't needed
- Set appropriate viewport dimensions for responsive websites
- Enable stealth mode when crawling sites with bot detection

### 4. Cache Strategy
Choose the appropriate cache mode based on your needs:
- Use enabled for general purpose crawling
- Use read_only for analytics and reporting
- Use write_only for content monitoring
- Use bypass for real-time data needs

### 5. Error Handling
- Always check the response status
- Implement retry logic for failed requests
- Handle timeouts gracefully
- Validate input parameters before making requests

## Common Error Codes

| Status Code | Description           | Solution                                 |
|------------|----------------------|------------------------------------------|
| 400        | Bad Request          | Check request parameters and format      |
| 401        | Unauthorized         | Verify authentication credentials        |
| 403        | Forbidden            | Check if the target site allows crawling |
| 404        | Not Found            | Verify the URL is correct and accessible |
| 429        | Too Many Requests    | Implement rate limiting and use caching  |
""",
        "examples": """# Quick Start Guide

## Basic Usage Examples

### 1. Basic Web Crawling
```bash
curl -X POST "http://localhost:8000/api/v1/crawl/basic" \\
     -H "Content-Type: application/json" \\
     -d '{
         "url": "https://quotes.toscrape.com",
         "headless": true,
         "viewport_width": 1280,
         "viewport_height": 800
     }'
```

### 2. Extract Specific Content
```bash
curl -X POST "http://localhost:8000/api/v1/crawl/content" \\
     -H "Content-Type: application/json" \\
     -d '{
         "url": "https://quotes.toscrape.com",
         "selectors_include": [".quote"],
         "selectors_exclude": [".footer"],
         "remove_selectors": [".tags"]
     }'
```

### 3. Structured Data Extraction
```bash
curl -X POST "http://localhost:8000/api/v1/crawl/extraction/structured" \\
     -H "Content-Type: application/json" \\
     -d '{
         "url": "https://news.ycombinator.com",
         "schema": {
             "name": "HackerNews",
             "base_selector": ".athing",
             "fields": [
                 {
                     "name": "title",
                     "selector": ".titleline > a",
                     "type": "text"
                 },
                 {
                     "name": "url",
                     "selector": ".titleline > a",
                     "type": "attribute",
                     "attribute": "href"
                 },
                 {
                     "name": "score",
                     "selector": "score",
                     "type": "text"
                 }
             ]
         }
     }'
```

### 4. Multi-URL Crawling
```bash
curl -X POST "http://localhost:8000/api/v1/crawl/multi" \\
     -H "Content-Type: application/json" \\
     -d '{
         "urls": [
             "https://quotes.toscrape.com",
             "https://books.toscrape.com"
         ],
         "mode": "parallel",
         "max_concurrent": 2,
         "headless": true,
         "session_reuse": true
     }'
```

### 5. Cached Crawling
```bash
curl -X POST "http://localhost:8000/api/v1/crawl/cached" \\
     -H "Content-Type: application/json" \\
     -d '{
         "url": "https://quotes.toscrape.com",
         "cache_mode": "enabled",
         "headless": true,
         "viewport_width": 1280,
         "viewport_height": 800
     }'
```

## Python Examples

### Basic Crawling
```python
import requests

def crawl_page(url):
    response = requests.post(
        "http://localhost:8000/api/v1/crawl/basic",
        json={
            "url": url,
            "headless": True
        }
    )
    return response.json()

result = crawl_page("https://quotes.toscrape.com")
print(result["markdown"])
```

### Structured Data Extraction
```python
import requests

def extract_data(url, schema):
    response = requests.post(
        "http://localhost:8000/api/v1/crawl/extraction/structured",
        json={
            "url": url,
            "schema": schema
        }
    )
    return response.json()

schema = {
    "name": "Quotes",
    "base_selector": ".quote",
    "fields": [
        {"name": "text", "selector": ".text", "type": "text"},
        {"name": "author", "selector": ".author", "type": "text"},
        {"name": "tags", "selector": ".tag", "type": "text", "is_collection": True}
    ]
}

result = extract_data("https://quotes.toscrape.com", schema)
for quote in result["data"]:
    print(f"Quote: {quote['text']}")
    print(f"Author: {quote['author']}")
    print(f"Tags: {', '.join(quote['tags'])}")
```
"""
    }
    return docs

@router.get("/human/docs", response_class=HTMLResponse, tags=["documentation"])
async def get_human_documentation():
    """
    Get the complete human-readable API documentation in HTML format.
    """
    docs = get_markdown_content()
    html_content = ""
    for section in docs.values():
        html_content += markdown2.markdown(section, extras=["tables", "fenced-code-blocks"])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crawl4AI API Documentation</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
                color: #333;
            }}
            pre {{
                background-color: #f6f8fa;
                padding: 1rem;
                border-radius: 6px;
                overflow-x: auto;
            }}
            code {{
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                font-size: 0.9em;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1rem 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 0.5rem;
                text-align: left;
            }}
            th {{
                background-color: #f6f8fa;
            }}
            h1, h2, h3, h4 {{
                color: #24292e;
                margin-top: 2rem;
            }}
            a {{
                color: #0366d6;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .container {{
                background-color: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
                border-radius: 8px;
                padding: 2rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_content}
        </div>
    </body>
    </html>
    """

@router.get("/human/docs/{section}", response_class=HTMLResponse, tags=["documentation"])
async def get_human_documentation_section(section: str):
    """
    Get a specific section of the human-readable API documentation in HTML format.
    Available sections: overview, endpoints, best_practices, examples
    """
    docs = get_markdown_content()
    if section not in docs:
        return HTMLResponse(
            content=f"""
            <h1>Error: Section Not Found</h1>
            <p>Documentation section '{section}' not found.</p>
            <p>Available sections: {', '.join(docs.keys())}</p>
            """,
            status_code=404
        )
    
    html_content = markdown2.markdown(docs[section], extras=["tables", "fenced-code-blocks"])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crawl4AI API Documentation - {section.title()}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
                color: #333;
            }}
            pre {{
                background-color: #f6f8fa;
                padding: 1rem;
                border-radius: 6px;
                overflow-x: auto;
            }}
            code {{
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
                font-size: 0.9em;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1rem 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 0.5rem;
                text-align: left;
            }}
            th {{
                background-color: #f6f8fa;
            }}
            h1, h2, h3, h4 {{
                color: #24292e;
                margin-top: 2rem;
            }}
            a {{
                color: #0366d6;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .container {{
                background-color: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
                border-radius: 8px;
                padding: 2rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_content}
        </div>
    </body>
    </html>
    """ 