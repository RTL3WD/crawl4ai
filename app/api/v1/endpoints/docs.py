from fastapi import APIRouter

router = APIRouter(
    prefix="/docs",
    tags=["documentation"],
    responses={404: {"description": "Not found"}},
)

@router.get("/extraction")
async def get_extraction_docs():
    """
    Get documentation for the extraction API
    """
    return {
        "title": "Crawl4AI Extraction Guide",
        "sections": [
            {
                "name": "Available Methods",
                "methods": [
                    {
                        "name": "Basic Crawl",
                        "endpoint": "/api/v1/crawl/basic",
                        "description": "Simple webpage crawling with browser configuration",
                        "best_for": [
                            "Single page content capture",
                            "Simple HTML structure",
                            "When full page content is needed",
                            "Testing site accessibility"
                        ],
                        "example": {
                            "url": "https://quotes.toscrape.com",
                            "headless": True,
                            "viewport_width": 1280,
                            "viewport_height": 800
                        }
                    },
                    {
                        "name": "Content Crawl",
                        "endpoint": "/api/v1/crawl/content",
                        "description": "Selective content extraction with CSS selectors",
                        "best_for": [
                            "Specific content sections",
                            "Excluding unwanted elements",
                            "Cleaning up page structure",
                            "When specific DOM elements are targeted"
                        ],
                        "example": {
                            "url": "https://quotes.toscrape.com",
                            "selectors_include": [".quote"],
                            "selectors_exclude": [".footer"],
                            "remove_selectors": [".tags"]
                        }
                    },
                    {
                        "name": "Structured Extraction",
                        "endpoint": "/api/v1/crawl/extraction/structured",
                        "description": "Schema-based data extraction with pagination support",
                        "best_for": [
                            "Repeated content patterns",
                            "Multi-page data collection",
                            "Structured data needs",
                            "When specific data fields are required"
                        ],
                        "features": [
                            "CSS selector-based extraction",
                            "Pagination support",
                            "Field type handling (text, attributes)",
                            "Collection extraction",
                            "Wait time configuration"
                        ],
                        "example": {
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
                                        "selector": ".tags .tag",
                                        "type": "text",
                                        "is_collection": True
                                    }
                                ],
                                "pagination": {
                                    "next_page_selector": ".pager .next a",
                                    "max_pages": 3,
                                    "wait_between_pages": 1
                                }
                            }
                        }
                    },
                    {
                        "name": "Cached Crawl",
                        "endpoint": "/api/v1/crawl/cached",
                        "description": "Crawl with caching support to improve performance and reduce load on target sites",
                        "best_for": [
                            "Frequent crawling of the same pages",
                            "Performance optimization",
                            "Reducing load on target sites",
                            "Offline access to content"
                        ],
                        "cache_modes": [
                            {
                                "mode": "enabled",
                                "description": "Normal caching (read/write)",
                                "use_case": "Default mode, balances performance and freshness"
                            },
                            {
                                "mode": "disabled",
                                "description": "No caching at all",
                                "use_case": "When you need guaranteed fresh content"
                            },
                            {
                                "mode": "read_only",
                                "description": "Only read from cache",
                                "use_case": "When you want to avoid hitting the target site"
                            },
                            {
                                "mode": "write_only",
                                "description": "Only write to cache",
                                "use_case": "When you want to update the cache without using it"
                            },
                            {
                                "mode": "bypass",
                                "description": "Skip cache for this operation",
                                "use_case": "When you need to temporarily ignore caching"
                            }
                        ],
                        "example": {
                            "url": "https://quotes.toscrape.com",
                            "cache_mode": "enabled",
                            "headless": True,
                            "viewport_width": 1280,
                            "viewport_height": 800
                        }
                    },
                    {
                        "name": "Multi-URL Crawl",
                        "endpoint": "/api/v1/crawl/multi",
                        "description": "Crawl multiple URLs efficiently with browser and session reuse",
                        "best_for": [
                            "Batch processing multiple URLs",
                            "Crawling entire websites",
                            "Parallel data collection",
                            "Performance optimization"
                        ],
                        "modes": [
                            {
                                "mode": "sequential",
                                "description": "Crawl URLs one by one with session reuse",
                                "use_case": "When order matters or for memory-constrained environments"
                            },
                            {
                                "mode": "parallel",
                                "description": "Crawl URLs concurrently in batches",
                                "use_case": "When speed is priority and resources are available"
                            }
                        ],
                        "features": [
                            "Browser reuse across all URLs",
                            "Optional session sharing",
                            "Configurable concurrency",
                            "Batch processing",
                            "Detailed results per URL"
                        ],
                        "example": {
                            "urls": [
                                "https://quotes.toscrape.com",
                                "https://books.toscrape.com",
                                "https://news.ycombinator.com"
                            ],
                            "mode": "parallel",
                            "max_concurrent": 2,
                            "headless": True,
                            "viewport_width": 1280,
                            "viewport_height": 800,
                            "session_reuse": True
                        }
                    }
                ]
            },
            {
                "name": "Decision Making Guide",
                "scenarios": [
                    {
                        "scenario": "Single Page Content",
                        "recommended_method": "Basic Crawl",
                        "when_to_use": [
                            "Need full page content",
                            "Simple webpage structure",
                            "No specific data structure needed",
                            "Testing crawl configuration"
                        ]
                    },
                    {
                        "scenario": "Specific Content Sections",
                        "recommended_method": "Content Crawl",
                        "when_to_use": [
                            "Need to focus on specific page sections",
                            "Want to exclude certain elements",
                            "Clean up page structure",
                            "Remove unwanted content"
                        ]
                    },
                    {
                        "scenario": "Data Extraction",
                        "recommended_method": "Structured Extraction",
                        "when_to_use": [
                            "Need specific data fields",
                            "Have repeated content patterns",
                            "Multiple pages to process",
                            "Want structured JSON output"
                        ]
                    },
                    {
                        "scenario": "Performance Optimization",
                        "recommended_method": "Cached Crawl",
                        "when_to_use": [
                            "Frequent crawling of the same pages",
                            "Need to reduce load on target sites",
                            "Want to improve response times",
                            "Need offline access to previously crawled content"
                        ]
                    },
                    {
                        "scenario": "Batch Processing",
                        "recommended_method": "Multi-URL Crawl",
                        "when_to_use": [
                            "Need to crawl multiple URLs efficiently",
                            "Want to optimize browser resource usage",
                            "Need parallel processing capability",
                            "Want to maintain session state across URLs"
                        ]
                    }
                ]
            },
            {
                "name": "Common Use Cases",
                "examples": [
                    {
                        "case": "News Article Extraction",
                        "recommended_method": "Content Crawl",
                        "example": {
                            "url": "https://news.ycombinator.com",
                            "selectors_include": [".athing", ".subtext"],
                            "selectors_exclude": [".hnmore"],
                            "remove_selectors": [".rank"]
                        }
                    },
                    {
                        "case": "Product Catalog",
                        "recommended_method": "Structured Extraction",
                        "example": {
                            "url": "https://books.toscrape.com",
                            "schema": {
                                "name": "Books",
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
                                ],
                                "pagination": {
                                    "next_page_selector": ".next a",
                                    "max_pages": 5,
                                    "wait_between_pages": 1
                                }
                            }
                        }
                    },
                    {
                        "case": "News Feed Caching",
                        "recommended_method": "Cached Crawl",
                        "example": {
                            "url": "https://news.ycombinator.com",
                            "cache_mode": "enabled",
                            "headless": True,
                            "viewport_width": 1280,
                            "viewport_height": 800
                        },
                        "description": "Cache news feed content to reduce load and improve response times"
                    }
                ]
            },
            {
                "name": "Best Practices",
                "categories": [
                    {
                        "name": "Performance Optimization",
                        "tips": [
                            "Use caching when crawling the same pages frequently",
                            "Enable headless mode when possible",
                            "Set appropriate viewport sizes",
                            "Use pagination limits for large datasets"
                        ]
                    },
                    {
                        "name": "Error Prevention",
                        "tips": [
                            "Test selectors before deployment",
                            "Handle missing content gracefully",
                            "Set reasonable timeouts",
                            "Consider site structure changes"
                        ]
                    },
                    {
                        "name": "Ethical Crawling",
                        "tips": [
                            "Respect robots.txt",
                            "Use appropriate delays between requests",
                            "Don't overload servers",
                            "Consider site terms of service"
                        ]
                    },
                    {
                        "name": "Cache Management",
                        "tips": [
                            "Use read_only mode for frequently accessed static content",
                            "Use write_only mode to update cache without affecting current request",
                            "Use bypass mode for time-sensitive data",
                            "Consider cache invalidation strategies"
                        ]
                    }
                ]
            }
        ]
    } 