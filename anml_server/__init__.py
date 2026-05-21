"""ANML 1.0 Server SDK for Python."""
from .types import (
    AnmlDocument, AnmlHead, AnmlTitle, AnmlMeta, AnmlConstraints, AnmlDisclosure,
    AnmlState, AnmlFlow, AnmlStep, AnmlContext, AnmlInteract, AnmlAction, AnmlParam,
    AnmlKnowledge, AnmlInform, AnmlAsk, AnmlPersona, AnmlTone, AnmlBody, AnmlMedia,
    AnmlRights, StepStatus, DisclosureRequirement, UsageRight, Confidentiality, HttpMethod,
)
from .builder import AnmlDocumentBuilder
from .serializer import to_json, to_xml, negotiate_content_type, serialize

# Convenience: attach builder classmethod to AnmlDocument
AnmlDocument.builder = classmethod(lambda cls: AnmlDocumentBuilder())  # type: ignore[attr-defined]

__all__ = [
    "AnmlDocument", "AnmlDocumentBuilder", "AnmlHead", "AnmlTitle", "AnmlMeta",
    "AnmlConstraints", "AnmlDisclosure", "AnmlState", "AnmlFlow", "AnmlStep",
    "AnmlContext", "AnmlInteract", "AnmlAction", "AnmlParam", "AnmlKnowledge",
    "AnmlInform", "AnmlAsk", "AnmlPersona", "AnmlTone", "AnmlBody", "AnmlMedia",
    "AnmlRights", "StepStatus", "DisclosureRequirement", "UsageRight",
    "Confidentiality", "HttpMethod", "to_json", "to_xml",
    "negotiate_content_type", "serialize",
]
