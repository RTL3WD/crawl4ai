# Best Practices & Error Handling

## Best Practices

### 1. Rate Limiting

- Implement appropriate delays between requests
- Use the cache feature for frequently accessed pages
- Consider using the multi-URL crawler with `session_reuse: true` for better performance

### 2. Selector Optimization

- Use specific CSS selectors to target exact elements
- Combine `selectors_include` and `selectors_exclude` for precise content extraction
- Test selectors in browser dev tools before using them in API calls

### 3. Browser Configuration

- Use `headless: true` for better performance when visual rendering isn't needed
- Set appropriate viewport dimensions for responsive websites
- Enable stealth mode when crawling sites with bot detection

### 4. Cache Strategy

Choose the appropriate cache mode based on your needs:

- Use `enabled` for general purpose crawling
- Use `read_only` for analytics and reporting
- Use `write_only` for content monitoring
- Use `bypass` for real-time data needs

### 5. Error Handling

- Always check the response status
- Implement retry logic for failed requests
- Handle timeouts gracefully
- Validate input parameters before making requests

## Error Handling

### Common Error Codes

| Status Code | Description           | Solution                                 |
| ----------- | --------------------- | ---------------------------------------- |
| 400         | Bad Request           | Check request parameters and format      |
| 401         | Unauthorized          | Verify authentication credentials        |
| 403         | Forbidden             | Check if the target site allows crawling |
| 404         | Not Found             | Verify the URL is correct and accessible |
| 429         | Too Many Requests     | Implement rate limiting and use caching  |
| 500         | Internal Server Error | Contact support or check server logs     |

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Detailed error message",
    "details": {
      "field": "Additional error context"
    }
  }
}
```

### Common Error Scenarios

1. **Invalid Selectors**

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_SELECTOR",
    "message": "The provided CSS selector '.invalid!!!' is not valid",
    "details": {
      "selector": ".invalid!!!",
      "reason": "Invalid CSS syntax"
    }
  }
}
```

2. **Rate Limiting**

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests to target domain",
    "details": {
      "retry_after": 60,
      "limit": "100 requests per minute"
    }
  }
}
```

3. **Cache Errors**

```json
{
  "status": "error",
  "error": {
    "code": "CACHE_ERROR",
    "message": "Content not found in cache (read_only mode)",
    "details": {
      "url": "https://example.com",
      "cache_mode": "read_only"
    }
  }
}
```

## Troubleshooting Tips

1. **Connection Issues**

   - Check network connectivity
   - Verify proxy configuration if used
   - Ensure target site is accessible

2. **Performance Issues**

   - Use appropriate cache modes
   - Optimize selector patterns
   - Consider using multi-URL crawling with parallel mode

3. **Content Extraction Problems**

   - Verify selectors in browser dev tools
   - Check if content is dynamically loaded
   - Enable browser debugging for detailed logs

4. **Cache-Related Issues**
   - Verify cache configuration
   - Check storage capacity
   - Monitor cache hit rates
