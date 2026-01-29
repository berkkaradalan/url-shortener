# URL Shortener

A URL shortening service implementing the hash + collision resolution approach from *System Design Interview* by Alex Xu.

## Features

- Shorten long URLs to 7-character codes using base62 encoding
- Automatic collision resolution
- 301/302 redirect support
- Supports up to 3.5 trillion unique URLs (62^7)

## How It Works

### Hash Function

The system uses SHA-256 to hash long URLs, then converts the result to a base62 string (characters `[0-9, a-z, A-Z]`).

**Why 7 characters?**

| Length (n) | Possible URLs (62^n) |
|------------|----------------------|
| 6          | ~57 billion          |
| 7          | ~3.5 trillion        |
| 8          | ~218 trillion        |

7 characters provides enough capacity for 365 billion URLs with room to spare.

### Collision Resolution

When two different URLs produce the same hash:

1. Detect collision by checking the database
2. Append a counter to the original URL
3. Rehash and retry
4. Repeat until a unique hash is found

```
URL A: "https://example.com/page1" → hash → "abc1234" → saved ✓
URL B: "https://example.com/page2" → hash → "abc1234" → collision!
       "https://example.com/page21" → hash → "xyz7890" → saved ✓
```

## API Endpoints

### Create Short URL

```
POST /shorten
Content-Type: application/json

{
  "url": "https://example.com/very/long/url/here"
}
```

**Response:**

```json
{
  "short_url": "http://localhost:8000/abc1234",
  "url_id": "abc1234",
  "original_url": "https://example.com/very/long/url/here"
}
```

### Redirect

```
GET /{url_id}
```

Returns `301 Moved Permanently` or `302 Found` with `Location` header pointing to the original URL.

## Reference

This implementation is based on Chapter 8 of:

> **System Design Interview – An Insider's Guide**  
> by Alex Xu  
> ISBN: 979-8664653403

The book covers two approaches for URL shortening:

1. **Hash + Collision Resolution** (implemented here)
2. **Base62 Conversion** using auto-increment IDs

## License

MIT