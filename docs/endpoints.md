# API Endpoints

## Basic Crawling

Endpoint: `POST /api/v1/crawl/basic`

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

Endpoint: `POST /api/v1/crawl/content`

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

Endpoint: `POST /api/v1/crawl/extraction/structured`

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

### Response

```json
{
  "status": "success",
  "data": [
    {
      "text": "...",
      "author": "...",
      "tags": ["...", "..."]
    }
  ]
}
```

## Multi-URL Crawling

Endpoint: `POST /api/v1/crawl/multi`

Crawls multiple URLs in parallel or sequentially.

### Request

```json
{
  "urls": ["https://example1.com", "https://example2.com"],
  "mode": "parallel",
  "max_concurrent": 3,
  "headless": true,
  "session_reuse": true
}
```

### Response

```json
{
    "status": "success",
    "mode": "parallel",
    "summary": {
        "total_urls": 2,
        "successful": 2,
        "failed": 0
    },
    "results": [
        {
            "url": "https://example1.com",
            "success": true,
            "data": {...}
        },
        {
            "url": "https://example2.com",
            "success": true,
            "data": {...}
        }
    ]
}
```

## Cache Management

Endpoint: `POST /api/v1/crawl/cached`

Performs crawling with caching support.

### Request

```json
{
  "url": "https://example.com",
  "cache_mode": "enabled",
  "headless": true,
  "viewport_width": 1280,
  "viewport_height": 800
}
```

### Response

```json
{
  "status": "success",
  "cache_hit": true,
  "data": {
    "html": "...",
    "markdown": "...",
    "cleaned_html": "...",
    "links": ["..."]
  }
}
```

### Cache Modes

- `enabled`: Use cache if available, otherwise crawl and cache
- `disabled`: Never use cache, always crawl
- `read_only`: Only use cache, fail if not cached
- `write_only`: Always crawl and update cache
- `bypass`: Ignore cache completely
