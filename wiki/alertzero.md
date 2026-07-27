---
type: Concept
title: "AlertZero"
description: "Accurate framing for AlertZero as a SOC operating goal supported by Attack Discovery, Alert Analysis, and human judgment."
tags: [elastic, security, alertzero, attack-discovery, soc, alert-fatigue]
timestamp: 2026-07-27T10:58:00+01:00
---

# Core explanation

AlertZero is Elastic's name for a goal, not a standalone product or a promise of zero alerts. It is the SOC equivalent of inbox zero: agents and analysts work a raw alert queue down to the potential attacks that deserve human attention.

Attack Discovery is the main product capability positioned as moving teams toward this goal.

# Existing Attack Discovery model

Public documentation describes Attack Discovery as LLM-assisted analysis that groups related security alerts into a potential attack narrative. A discovery can identify implicated users and hosts, connect activity to MITRE ATT&CK tactics, and provide context for analyst triage.

Attack Discovery findings remain hypotheses. Analysts should validate the generated narrative and underlying evidence before acting.

# 9.5 draft additions

The pre-publication 9.5 announcement says Attack Discovery can go beyond its initial alerts by:

- Threat-hunting raw events.
- Checking entity risk.
- Seeking corroborating evidence before labeling activity as an attack.
- Drafting an ES|QL detection rule when it finds a coverage gap.
- Requiring analyst approval before saving the drafted rule.

The draft also says manual, scheduled, and Workflow-triggered runs use the same investigation. A separate Alert Analysis workflow classifies true and false positives, reducing the low-fidelity alert set that Attack Discovery must inspect.

# Human role

The defensible value proposition is not autonomous incident confirmation. AI performs repetitive triage, gathers context, and proposes a next action. Analysts validate whether the threat is real, apply institutional context, approve rule changes, and decide the response.

# Video guidance

- Define AlertZero before discussing product mechanics.
- Explicitly say it does not mean zero alerts or replacing analysts.
- Show the funnel from raw alerts and events to a short list of attack narratives.
- Distinguish Alert Analysis, which reduces low-fidelity alert noise, from Attack Discovery, which investigates potential attacks.
- Describe generated findings as evidence-backed hypotheses rather than validated incidents unless the final product language establishes a stronger meaning.

# Validation gate

Before publication, confirm the final 9.5 availability, licensing, workflow names, raw-event investigation scope, rule-drafting flow, and analyst approval behavior.

# Sources

- [Draft: Elastic 9.5 All-Up Release Announcement](../sources/elastic-9-5-release-blog-draft.md)
- [Attack Discovery documentation](https://www.elastic.co/docs/solutions/security/ai/attack-discovery)
- [Triage Attack Discovery findings](https://www.elastic.co/docs/solutions/security/ai/triage-attack-discovery-findings)
