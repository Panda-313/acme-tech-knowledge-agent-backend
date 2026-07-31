# API Design Standards

## General Principles

- RESTful where it fits, pragmatic where it doesn’t
- Consistent naming and response shapes
- Explicit versioning
- Good error messages that help the client

## URL Structure

```
https://api.acmetech.example/v1/resources
https://api.acmetech.example/v1/resources/{id}
https://api.acmetech.example/v1/resources/{id}/sub-resources
```

- Use kebab-case for multi-word path segments
- Prefer plural nouns for collections
- Version in the path (`/v1/`, `/v2/`)

## HTTP Methods

| Method | Usage                              |
|--------|------------------------------------|
| GET    | Read (safe, idempotent)            |
| POST   | Create or non-idempotent actions   |
| PUT    | Full replacement                   |
| PATCH  | Partial update                     |
| DELETE | Remove                             |

## Request & Response

- JSON only (unless streaming or file download)
- Request bodies validated with Pydantic models
- Success responses: appropriate 2xx status + JSON body
- Collections should support pagination (`limit`, `cursor` or `offset`)

### Standard Success Envelope (optional but recommended for new endpoints)

```json
{
  "data": { ... },
  "meta": {
    "request_id": "..."
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "validation_error",
    "message": "Human readable message",
    "details": [ ... ]
  },
  "meta": {
    "request_id": "..."
  }
}
```

Use consistent error codes across services.

## Authentication

- Bearer token (JWT or opaque) in the `Authorization` header
- Service-to-service: mTLS or signed internal tokens (details in security docs)

## Pagination

Prefer cursor-based pagination for large or frequently changing collections:

```
GET /v1/items?limit=20&cursor=eyJ...
```

## Streaming

For LLM responses we use Server-Sent Events (SSE) or chunked transfer encoding.  
Document the exact format in the endpoint docstring.

## Documentation

- Every public endpoint must have an OpenAPI entry (FastAPI handles most of this)
- Keep descriptions up to date
- Breaking changes require a new major version and a migration guide

## Deprecation

- Announce deprecations at least 90 days in advance for external APIs
- Internal APIs can move faster but still need communication in `#engineering`
