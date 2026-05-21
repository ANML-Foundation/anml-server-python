"""Fluent builder for constructing ANML documents."""
from __future__ import annotations
from typing import Optional
from .types import (
    AnmlDocument, AnmlHead, AnmlTitle, AnmlMeta, AnmlConstraints, AnmlDisclosure,
    AnmlState, AnmlFlow, AnmlStep, AnmlContext, AnmlInteract, AnmlAction, AnmlParam,
    AnmlKnowledge, AnmlInform, AnmlAsk, AnmlPersona, AnmlTone, AnmlBody, AnmlMedia,
    AnmlRights, DisclosureRequirement, UsageRight, Confidentiality, HttpMethod, StepStatus,
)


class AnmlDocumentBuilder:
    """Fluent builder for ANML documents."""

    def __init__(self) -> None:
        self._ttl: int = 300
        self._title: Optional[str] = None
        self._meta: list[AnmlMeta] = []
        self._disclosures: list[AnmlDisclosure] = []
        self._steps: list[AnmlStep] = []
        self._context_step: Optional[str] = None
        self._actions: list[AnmlAction] = []
        self._informs: list[AnmlInform] = []
        self._asks: list[AnmlAsk] = []
        self._persona: AnmlPersona | None = None
        self._body_content: str = ""
        self._media: list[AnmlMedia] = []
        self._rights: UsageRight | None = None

    def title(self, title: str) -> "AnmlDocumentBuilder":
        self._title = title
        return self

    def ttl(self, ttl: int) -> "AnmlDocumentBuilder":
        self._ttl = ttl
        return self

    def meta(self, name: str, value: str) -> "AnmlDocumentBuilder":
        self._meta.append(AnmlMeta(name=name, value=value))
        return self

    def disclosure(self, field: str, *, requires: str = "none") -> "AnmlDocumentBuilder":
        self._disclosures.append(AnmlDisclosure(
            field=field, requires=DisclosureRequirement(requires)
        ))
        return self

    def flow(self, steps: list[AnmlStep | dict]) -> "AnmlDocumentBuilder":
        for s in steps:
            if isinstance(s, dict):
                self._steps.append(AnmlStep(**s))
            else:
                self._steps.append(s)
        return self

    def context(self, step: str) -> "AnmlDocumentBuilder":
        self._context_step = step
        return self

    def action(
        self, id: str, *, method: str = "POST", endpoint: str,
        auth: Optional[str] = None, confirm: Optional[bool] = None,
        enctype: Optional[str] = None, params: Optional[list[dict]] = None,
    ) -> "AnmlDocumentBuilder":
        action_params = [AnmlParam(**p) for p in params] if params else []
        self._actions.append(AnmlAction(
            id=id, method=HttpMethod(method), endpoint=endpoint,
            auth=auth, confirm=confirm, enctype=enctype, params=action_params,
        ))
        return self

    def inform(
        self, content: str, *, confidentiality: str = "public", ttl: Optional[int] = None,
    ) -> "AnmlDocumentBuilder":
        self._informs.append(AnmlInform(
            content=content, confidentiality=Confidentiality(confidentiality), ttl=ttl,
        ))
        return self

    def ask(
        self, field: str, *, action: Optional[str] = None,
        required: Optional[bool] = None, purpose: Optional[str] = None,
    ) -> "AnmlDocumentBuilder":
        self._asks.append(AnmlAsk(
            field=field, action=action, required=required, purpose=purpose,
        ))
        return self

    def persona(
        self, *, tone: Optional[str] = None, instructions: Optional[str] = None,
        brand_color: Optional[str] = None, logo_url: Optional[str] = None,
    ) -> "AnmlDocumentBuilder":
        self._persona = AnmlPersona(
            tone=AnmlTone(value=tone) if tone else None,
            instructions=instructions,
            brand_color=brand_color,
            logo_url=logo_url,
        )
        return self

    def body(self, content: str) -> "AnmlDocumentBuilder":
        self._body_content = content
        return self

    def media(self, src: str, *, type: Optional[str] = None, alt: Optional[str] = None) -> "AnmlDocumentBuilder":
        self._media.append(AnmlMedia(src=src, type=type, alt=alt))
        return self

    def rights(self, usage: str) -> "AnmlDocumentBuilder":
        self._rights = UsageRight(usage)
        return self

    def build(self) -> AnmlDocument:
        head = AnmlHead(
            title=AnmlTitle(text=self._title) if self._title else None,
            meta=self._meta,
        )
        constraints = AnmlConstraints(disclosures=self._disclosures) if self._disclosures else None
        state = None
        if self._steps:
            flow = AnmlFlow(steps=self._steps)
            ctx = AnmlContext(step=self._context_step) if self._context_step else None
            if not ctx:
                for s in self._steps:
                    if s.status == StepStatus.CURRENT:
                        ctx = AnmlContext(step=s.id)
                        break
            state = AnmlState(flow=flow, context=ctx)
        interact = AnmlInteract(actions=self._actions) if self._actions else None
        knowledge = None
        if self._informs or self._asks:
            knowledge = AnmlKnowledge(inform=self._informs, ask=self._asks)
        body = None
        if self._body_content or self._media:
            body = AnmlBody(content=self._body_content, media=self._media)
        rights_obj = AnmlRights(usage=self._rights) if self._rights else None

        return AnmlDocument(
            ttl=self._ttl, head=head, constraints=constraints,
            state=state, interact=interact, knowledge=knowledge,
            persona=self._persona, body=body, rights=rights_obj,
        )
