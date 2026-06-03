---
name: architecture-diagramming
description: Create, explain, or review technical/system architecture diagrams that show logical components, responsibilities, dependencies, data flow, synchronous/asynchronous calls, layers, domains, and production support concerns. Use when the user asks how to draw architecture diagrams, system architecture, technical architecture, logical architecture, application architecture, architecture review diagrams, Mermaid/PlantUML architecture output, or wants an existing diagram evaluated and improved.
---

# Architecture Diagramming

## Overview

Produce architecture diagrams that reduce communication cost and guide engineering decisions. Avoid component piles: every diagram must clarify responsibilities, relationships, abstraction level, and intended audience.

## First Decide The Diagram Level

Choose one level before drawing. If the user has not specified the level, infer it from the audience and purpose, then state the assumption briefly.

1. Overall technical architecture
   - Audience: CTO, tech leads, product managers, new team members.
   - Show systems, applications, services, major platforms, and high-level data flow.
   - Do not include classes, controllers, repositories, tables, or framework annotations.

2. Domain or subsystem architecture
   - Audience: domain architects, senior engineers, cross-team reviewers.
   - Show the logical components inside one business domain and the contracts to neighboring domains.
   - Emphasize domain autonomy, boundaries, shared services, and integration points.

3. Application-level architecture
   - Audience: developers and testers.
   - Show internal modules, layers, interfaces, middleware, storage, and implementation-level technology choices.
   - Keep this separate from the overall diagram to avoid mixing abstraction levels.

## Six-Step Drawing Workflow

1. Derive the technical skeleton from the business architecture.
   - Map business capabilities to services or modules.
   - Add pure technical modules that the business view does not mention, such as gateway, auth, tracing, config, and scheduling.
   - Keep module granularity aligned with business granularity.

2. Derive non-functional modules from key scenarios.
   - High read traffic implies cache, CDN, read replicas, or prewarming.
   - Inter-service communication implies discovery, load balancing, contracts, and failure handling.
   - Async side effects imply message queues, event topics, consumers, retries, and idempotency.
   - Strong consistency or money movement implies transaction strategy, reconciliation, audit, and idempotency.
   - Spikes or flash sales imply rate limiting, queueing, degradation, and capacity controls.

3. Extract horizontal layers.
   - Separate access, application, domain, infrastructure, and data layers when appropriate.
   - Keep the domain layer framework-independent and central.
   - Move observability, configuration, security, and operations into a support plane instead of letting them clutter the main business flow.

4. Extract vertical reusable modules.
   - Move reusable platform services downward or sideways: auth center, message platform, ID generation, shared libraries, notification service, file service.
   - Use this to reduce direct service-to-service lines and reveal intended reuse.

5. Add stability and production support modules.
   - Include metrics, logs, tracing, alerts, health checks, circuit breakers, rate limiters, degradation, config center, registry, audit, encryption, and WAF when relevant.
   - Draw these with lighter emphasis so they are visible but do not dominate the business flow.

6. Produce a layered and sliced logical architecture.
   - Layer by responsibility from user-facing access down to data and infrastructure.
   - Slice by business domain or subsystem horizontally.
   - Label critical arrows with protocol, sync/async semantics, data type, and rough volume when known.

## Diagram Grammar

Use a small, consistent vocabulary:

- Boxes: bounded components such as services, applications, modules, platforms, databases, queues, and external systems.
- Solid arrows: synchronous calls such as HTTP, RPC, or direct request/response dependency.
- Dashed arrows: asynchronous messages, events, jobs, or weak runtime coupling.
- Bidirectional arrows: bidirectional communication such as WebSocket or duplex protocol.
- Dashed lines without arrows: compile-time, configuration, or non-runtime dependencies.
- Groups or swimlanes: domains, layers, teams, or deployment zones.

Color should carry meaning, not decoration. Use at most five semantic groups:

- Business or logical components.
- Infrastructure such as databases, caches, queues, and storage.
- Boundary components such as gateway, auth, and external interfaces.
- Observability and operations.
- Shared or common support.

## Layout Rules

- Put user-facing or upstream systems above or to the left.
- Put lower-level dependencies, data, and infrastructure below.
- Use left-to-right flow for request and data movement when possible.
- Put boundary components on the edge and core business modules near the center.
- Group related modules with light containers or swimlanes.
- If more than five lines cross, reconsider layering, grouping, or whether a mediator/platform component is missing.

## Review Checklist

Before finishing, check:

- Audience: Is the diagram level right for who will read it?
- Responsibility: Does every component say what it owns?
- Relationship: Can readers tell who depends on whom and how data moves?
- Semantics: Are sync, async, strong dependency, weak dependency, and support dependencies distinguishable?
- Business mapping: Can each major business capability map to a technical component?
- Stability: Are production concerns represented where relevant?
- Simplicity: Is this one diagram trying to answer only one main question?
- Maintainability: Can the diagram be versioned or regenerated with Mermaid, PlantUML, or source-controlled text?

## Pitfalls To Avoid

- Do not draw framework classes, controllers, repositories, annotations, or database tables in an overall architecture diagram.
- Do not turn the diagram into a technology stack inventory.
- Do not use many colors without semantic meaning.
- Do not create a fully connected mesh of services; introduce domains, platforms, mediators, or async events when the model is too tangled.
- Do not omit labels on important arrows.
- Do not give executives implementation detail or give developers a diagram too abstract to build from.
- Do not treat architecture diagrams as one-time artifacts; keep them aligned with code and architecture decisions.

## Output Defaults

When asked to create a diagram, provide:

1. A short assumption about audience and diagram level.
2. A component inventory with responsibilities.
3. A relationship inventory with sync/async semantics.
4. A diagram, preferably Mermaid when suitable.
5. A short review checklist and next refinements.

Respond in Chinese by default unless the user requests another language.

