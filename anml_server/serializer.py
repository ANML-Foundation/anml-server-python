"""Serialize ANML documents to XML and JSON."""
from __future__ import annotations
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from .types import AnmlDocument, StepStatus


def to_json(doc: AnmlDocument) -> str:
    """Serialize an ANML document to JSON."""
    data: dict = {"anml": doc.version, "ttl": doc.ttl}
    if doc.head and doc.head.title:
        data["head"] = {"title": doc.head.title.text}
        if doc.head.meta:
            data["head"]["meta"] = [{"name": m.name, "value": m.value} for m in doc.head.meta]
    if doc.constraints and doc.constraints.disclosures:
        data["constraints"] = {
            "disclosure": [{"field": d.field, "requires": d.requires.value} for d in doc.constraints.disclosures]
        }
    if doc.state:
        state: dict = {}
        if doc.state.flow:
            state["flow"] = {"step": []}
            for s in doc.state.flow.steps:
                step_d: dict = {"id": s.id, "status": s.status.value}
                if s.label:
                    step_d["label"] = s.label
                if s.action:
                    step_d["action"] = s.action
                if s.required is not None:
                    step_d["required"] = s.required
                state["flow"]["step"].append(step_d)
        if doc.state.context:
            state["context"] = {"step": doc.state.context.step}
        data["state"] = state
    if doc.interact and doc.interact.actions:
        data["interact"] = {"action": []}
        for a in doc.interact.actions:
            act: dict = {"id": a.id, "method": a.method.value, "endpoint": a.endpoint}
            if a.auth:
                act["auth"] = a.auth
            if a.confirm is not None:
                act["confirm"] = a.confirm
            if a.enctype:
                act["enctype"] = a.enctype
            data["interact"]["action"].append(act)
    if doc.knowledge:
        know: dict = {}
        if doc.knowledge.inform:
            know["inform"] = []
            for i in doc.knowledge.inform:
                inf: dict = {"content": i.content, "confidentiality": i.confidentiality.value}
                if i.ttl is not None:
                    inf["ttl"] = i.ttl
                know["inform"].append(inf)
        if doc.knowledge.ask:
            know["ask"] = []
            for a in doc.knowledge.ask:
                ask_d: dict = {"field": a.field}
                if a.action:
                    ask_d["action"] = a.action
                if a.required is not None:
                    ask_d["required"] = a.required
                if a.purpose:
                    ask_d["purpose"] = a.purpose
                know["ask"].append(ask_d)
        data["knowledge"] = know
    if doc.persona:
        p: dict = {}
        if doc.persona.tone:
            p["tone"] = {"value": doc.persona.tone.value}
        if doc.persona.instructions:
            p["instructions"] = doc.persona.instructions
        if doc.persona.brand_color:
            p["brand_color"] = doc.persona.brand_color
        if doc.persona.logo_url:
            p["logo_url"] = doc.persona.logo_url
        data["persona"] = p
    if doc.body:
        body_d: dict = {}
        if doc.body.content:
            body_d["content"] = doc.body.content
        if doc.body.media:
            body_d["media"] = [{"src": m.src, "type": m.type, "alt": m.alt} for m in doc.body.media]
        data["body"] = body_d
    if doc.rights:
        data["rights"] = {"usage": doc.rights.usage.value}
    return json.dumps(data, indent=2)


def to_xml(doc: AnmlDocument) -> str:
    """Serialize an ANML document to XML."""
    root = ET.Element("anml")
    root.set("xmlns", "urn:ietf:params:xml:ns:anml:1.0")
    root.set("ttl", str(doc.ttl))
    if doc.head:
        head_el = ET.SubElement(root, "head")
        if doc.head.title:
            t = ET.SubElement(head_el, "title")
            t.text = doc.head.title.text
        for m in doc.head.meta:
            meta_el = ET.SubElement(head_el, "meta")
            meta_el.set("name", m.name)
            meta_el.set("value", m.value)
    if doc.constraints and doc.constraints.disclosures:
        cons_el = ET.SubElement(root, "constraints")
        for d in doc.constraints.disclosures:
            disc_el = ET.SubElement(cons_el, "disclosure")
            disc_el.set("field", d.field)
            disc_el.set("requires", d.requires.value)
    if doc.state:
        state_el = ET.SubElement(root, "state")
        if doc.state.context:
            ctx_el = ET.SubElement(state_el, "context")
            step_el = ET.SubElement(ctx_el, "step")
            step_el.text = doc.state.context.step
        if doc.state.flow:
            flow_el = ET.SubElement(state_el, "flow")
            for s in doc.state.flow.steps:
                s_el = ET.SubElement(flow_el, "step")
                s_el.set("id", s.id)
                s_el.set("status", s.status.value)
                if s.label:
                    s_el.set("label", s.label)
                if s.action:
                    s_el.set("action", s.action)
                if s.required is not None:
                    s_el.set("required", str(s.required).lower())
    if doc.interact and doc.interact.actions:
        int_el = ET.SubElement(root, "interact")
        for a in doc.interact.actions:
            a_el = ET.SubElement(int_el, "action")
            a_el.set("id", a.id)
            a_el.set("method", a.method.value)
            a_el.set("endpoint", a.endpoint)
            if a.auth:
                a_el.set("auth", a.auth)
            if a.confirm is not None:
                a_el.set("confirm", str(a.confirm).lower())
    if doc.knowledge:
        k_el = ET.SubElement(root, "knowledge")
        for i in doc.knowledge.inform:
            i_el = ET.SubElement(k_el, "inform")
            i_el.set("confidentiality", i.confidentiality.value)
            if i.ttl is not None:
                i_el.set("ttl", str(i.ttl))
            i_el.text = i.content
        for a in doc.knowledge.ask:
            a_el = ET.SubElement(k_el, "ask")
            a_el.set("field", a.field)
            if a.action:
                a_el.set("action", a.action)
            if a.required is not None:
                a_el.set("required", str(a.required).lower())
            if a.purpose:
                a_el.set("purpose", a.purpose)
    if doc.persona:
        p_el = ET.SubElement(root, "persona")
        if doc.persona.tone:
            t_el = ET.SubElement(p_el, "tone")
            t_el.set("value", doc.persona.tone.value)
        if doc.persona.instructions:
            ins_el = ET.SubElement(p_el, "instructions")
            ins_el.text = doc.persona.instructions
        if doc.persona.brand_color:
            bc_el = ET.SubElement(p_el, "brand-color")
            bc_el.text = doc.persona.brand_color
        if doc.persona.logo_url:
            logo_el = ET.SubElement(p_el, "logo")
            logo_el.set("src", doc.persona.logo_url)
    if doc.body:
        b_el = ET.SubElement(root, "body")
        if doc.body.content:
            b_el.text = doc.body.content
        for m in doc.body.media:
            m_el = ET.SubElement(b_el, "media")
            m_el.set("src", m.src)
            if m.type:
                m_el.set("type", m.type)
            if m.alt:
                m_el.set("alt", m.alt)
    if doc.rights:
        r_el = ET.SubElement(root, "rights")
        r_el.set("usage", doc.rights.usage.value)
    rough = ET.tostring(root, encoding="unicode", xml_declaration=True)
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent="  ", encoding=None)


def negotiate_content_type(accept: str | None) -> str:
    """Determine response content type from Accept header."""
    if not accept:
        return "application/anml+json"
    accept_lower = accept.lower()
    if "xml" in accept_lower or "application/anml+xml" in accept_lower:
        return "application/anml+xml"
    return "application/anml+json"


def serialize(doc: AnmlDocument, content_type: str) -> str:
    """Serialize document based on content type."""
    if "xml" in content_type:
        return to_xml(doc)
    return to_json(doc)
