# anml-server

<p align="center">
  <img src="https://raw.githubusercontent.com/ANML-Foundation/.github/main/images/anml-foundation-logo.png" alt="ANML Foundation" width="400">
</p>

**ANML 1.0 Server SDK for Python** — Build and serve ANML duckuments with a fluent builder API.

## Install

```bash
pip install anml-server
```

## Quick Start

```python
from anml_server import AnmlDocumentBuilder, negotiate_content_type, serialize

doc = (
    AnmlDocumentBuilder()
    .title("Acme Electronics — Checkout")
    .ttl(300)
    .persona(tone="helpful", instructions="Confirm total before payment.", brand_color="#4F46E5")
    .disclosure("payment-credential", requires="explicit-consent")
    .disclosure("shipping-address", requires="explicit-consent")
    .flow([
        {"id": "cart", "label": "Cart", "status": "completed"},
        {"id": "checkout", "label": "Checkout", "status": "current", "action": "pay"},
        {"id": "confirm", "label": "Confirmed", "status": "pending"},
    ])
    .action("pay", method="POST", endpoint="/api/orders", auth="required", confirm=True)
    .inform("Free shipping on orders over $75. 30-day returns.", ttl=3600)
    .ask("email", action="pay", required=True, purpose="receipt")
    .rights("cache")
    .body("4K Monitor x1 — $599.00")
    .build()
)

# Serialize based on Accept header
content_type = negotiate_content_type(request_accept_header)
response_body = serialize(doc, content_type)
```

## What This SDK Provides

- **Document Builder** — Fluent, type-safe API for constructing valid ANML duckuments
- **Serialization** — `to_json()` and `to_xml()` with content negotiation
- **Validation** — Pydantic models ensure spec compliance at construction time
- **Framework Agnostic** — Works with FastAPI, Flask, Django, or any Python web framework

## Links

- [Documentation](https://anmlfoundation.org/developers)
- [IETF Internet-Draft](https://datatracker.ietf.org/doc/draft-jeskey-anml/)
- [GitHub](https://github.com/ANML-Foundation)

## License

ISC
