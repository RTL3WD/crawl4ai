# Quick Start Guide

This guide will help you get started with the Crawl4AI API using practical examples.

## Basic Usage

### 1. Basic Web Crawling

Crawl a webpage and get its content:

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/basic" \
     -H "Content-Type: application/json" \
     -d '{
         "url": "https://quotes.toscrape.com",
         "headless": true,
         "viewport_width": 1280,
         "viewport_height": 800
     }'
```

### 2. Extract Specific Content

Extract quotes from a webpage:

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/content" \
     -H "Content-Type: application/json" \
     -d '{
         "url": "https://quotes.toscrape.com",
         "selectors_include": [".quote"],
         "selectors_exclude": [".footer"],
         "remove_selectors": [".tags"]
     }'
```

### 3. Structured Data Extraction

Extract structured data from Hacker News:

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/extraction/structured" \
     -H "Content-Type: application/json" \
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

Crawl multiple URLs in parallel:

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/multi" \
     -H "Content-Type: application/json" \
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

Use caching for better performance:

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/cached" \
     -H "Content-Type: application/json" \
     -d '{
         "url": "https://quotes.toscrape.com",
         "cache_mode": "enabled",
         "headless": true,
         "viewport_width": 1280,
         "viewport_height": 800
     }'
```

## Common Use Cases

### 1. News Article Extraction

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/content" \
     -H "Content-Type: application/json" \
     -d '{
         "url": "https://example-news.com/article",
         "selectors_include": [
             "article",
             ".article-content",
             ".article-header"
         ],
         "selectors_exclude": [
             ".advertisements",
             ".related-articles",
             ".comments"
         ]
     }'
```

### 2. E-commerce Product Details

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/extraction/structured" \
     -H "Content-Type: application/json" \
     -d '{
         "url": "https://books.toscrape.com",
         "schema": {
             "name": "Products",
             "base_selector": "article.product_pod",
             "fields": [
                 {
                     "name": "title",
                     "selector": "h3 a",
                     "type": "text"
                 },
                 {
                     "name": "price",
                     "selector": ".price_color",
                     "type": "text"
                 },
                 {
                     "name": "availability",
                     "selector": ".availability",
                     "type": "text"
                 }
             ]
         }
     }'
```

### 3. Monitor Website Changes

```bash
curl -X POST "http://localhost:8000/api/v1/crawl/cached" \
     -H "Content-Type: application/json" \
     -d '{
         "url": "https://example.com",
         "cache_mode": "write_only",
         "selectors_include": [".content-to-monitor"],
         "compare_with_previous": true
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
    print(f"Tags: {', '.join(quote['tags'])}\n")
```
