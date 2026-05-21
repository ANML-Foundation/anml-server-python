"""Tests for anml_server."""
from anml_server import AnmlDocumentBuilder, to_json, to_xml, negotiate_content_type, serialize


def test_builder_basic():
    doc = (
        AnmlDocumentBuilder()
        .title("Test Service")
        .ttl(600)
        .build()
    )
    assert doc.head.title.text == "Test Service"
    assert doc.ttl == 600


def test_builder_full():
    doc = (
        AnmlDocumentBuilder()
        .title("Checkout")
        .ttl(300)
        .disclosure("email", requires="explicit-consent")
        .flow([{"id": "cart", "label": "Cart", "status": "completed"},
               {"id": "pay", "label": "Pay", "status": "current", "action": "submit"}])
        .action("submit", method="POST", endpoint="/api/pay", auth="required", confirm=True)
        .inform("Free shipping over $50.", ttl=3600)
        .ask("email", action="submit", required=True, purpose="receipt")
        .persona(tone="helpful", instructions="Be concise.", brand_color="#4F46E5")
        .body("Widget x1 - $25.00")
        .rights("cache")
        .build()
    )
    assert doc.constraints.disclosures[0].field == "email"
    assert doc.state.flow.steps[1].status.value == "current"
    assert doc.interact.actions[0].confirm is True
    assert doc.knowledge.inform[0].content == "Free shipping over $50."
    assert doc.persona.brand_color == "#4F46E5"
    assert doc.rights.usage.value == "cache"


def test_to_json():
    doc = AnmlDocumentBuilder().title("Test").build()
    j = to_json(doc)
    assert '"anml": "1.0"' in j
    assert '"title": "Test"' in j


def test_to_xml():
    doc = AnmlDocumentBuilder().title("Test").build()
    x = to_xml(doc)
    assert "<title>Test</title>" in x
    assert "urn:ietf:params:xml:ns:anml:1.0" in x


def test_negotiate_json():
    assert negotiate_content_type("application/json") == "application/anml+json"
    assert negotiate_content_type(None) == "application/anml+json"


def test_negotiate_xml():
    assert negotiate_content_type("application/xml") == "application/anml+xml"
    assert negotiate_content_type("application/anml+xml") == "application/anml+xml"


def test_serialize_dispatches():
    doc = AnmlDocumentBuilder().title("X").build()
    assert '"anml"' in serialize(doc, "application/anml+json")
    assert "<anml" in serialize(doc, "application/anml+xml")
