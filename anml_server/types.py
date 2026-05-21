"""ANML 1.0 document types for server-side construction."""
from __future__ import annotations
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field

class StepStatus(str, Enum):
    PENDING = "pending"
    CURRENT = "current"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class DisclosureRequirement(str, Enum):
    NONE = "none"
    LEGITIMATE_INTEREST = "legitimate-interest"
    EXPLICIT_CONSENT = "explicit-consent"

class UsageRight(str, Enum):
    NONE = "none"
    DISPLAY = "display"
    CACHE = "cache"
    STORE = "store"
    TRAIN = "train"

class Confidentiality(str, Enum):
    PUBLIC = "public"
    AGENT_ONLY = "agent-only"
    USER_ONLY = "user-only"

class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class AnmlMeta(BaseModel):
    name: str
    value: str

class AnmlTitle(BaseModel):
    text: str

class AnmlHead(BaseModel):
    title: Optional[AnmlTitle] = None
    meta: list[AnmlMeta] = Field(default_factory=list)

class AnmlDisclosure(BaseModel):
    field: str
    requires: DisclosureRequirement = DisclosureRequirement.NONE

class AnmlConstraints(BaseModel):
    disclosures: list[AnmlDisclosure] = Field(default_factory=list)

class AnmlStep(BaseModel):
    id: str
    label: Optional[str] = None
    status: StepStatus = StepStatus.PENDING
    action: Optional[str] = None
    required: Optional[bool] = None

class AnmlFlow(BaseModel):
    steps: list[AnmlStep] = Field(default_factory=list)

class AnmlContext(BaseModel):
    step: str

class AnmlState(BaseModel):
    flow: Optional[AnmlFlow] = None
    context: Optional[AnmlContext] = None

class AnmlParam(BaseModel):
    name: str
    type: str = "string"
    required: bool = False

class AnmlAction(BaseModel):
    id: str
    method: HttpMethod = HttpMethod.POST
    endpoint: str
    enctype: Optional[str] = None
    auth: Optional[str] = None
    confirm: Optional[bool] = None
    params: list[AnmlParam] = Field(default_factory=list)

class AnmlInteract(BaseModel):
    actions: list[AnmlAction] = Field(default_factory=list)

class AnmlInform(BaseModel):
    content: str
    confidentiality: Confidentiality = Confidentiality.PUBLIC
    ttl: Optional[int] = None

class AnmlAsk(BaseModel):
    field: str
    action: Optional[str] = None
    required: Optional[bool] = None
    purpose: Optional[str] = None

class AnmlKnowledge(BaseModel):
    inform: list[AnmlInform] = Field(default_factory=list)
    ask: list[AnmlAsk] = Field(default_factory=list)

class AnmlTone(BaseModel):
    value: str

class AnmlPersona(BaseModel):
    tone: Optional[AnmlTone] = None
    instructions: Optional[str] = None
    brand_color: Optional[str] = None
    logo_url: Optional[str] = None

class AnmlMedia(BaseModel):
    src: str
    type: Optional[str] = None
    alt: Optional[str] = None

class AnmlBody(BaseModel):
    content: str = ""
    media: list[AnmlMedia] = Field(default_factory=list)

class AnmlRights(BaseModel):
    usage: UsageRight = UsageRight.DISPLAY

class AnmlDocument(BaseModel):
    version: str = "1.0"
    ttl: int = 300
    head: AnmlHead = Field(default_factory=AnmlHead)
    constraints: Optional[AnmlConstraints] = None
    state: Optional[AnmlState] = None
    interact: Optional[AnmlInteract] = None
    knowledge: Optional[AnmlKnowledge] = None
    persona: Optional[AnmlPersona] = None
    body: Optional[AnmlBody] = None
    rights: Optional[AnmlRights] = None
