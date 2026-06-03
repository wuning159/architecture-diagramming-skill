# Architecture Diagramming Skill

A Codex skill for creating, explaining, and reviewing technical/system architecture diagrams.

It captures a practical architecture diagramming method: choose the audience and diagram level first, then derive components from business capabilities, key scenarios, non-functional requirements, horizontal layers, reusable vertical modules, and production support concerns. The goal is to avoid technology-component piles and produce diagrams that guide decisions.

## When To Use

- You need an overall technical architecture diagram, system architecture diagram, or logical architecture diagram.
- You need to map business capabilities into technical components.
- You need to show responsibilities, dependencies, data flow, and synchronous/asynchronous calls.
- You want Mermaid or PlantUML architecture output.
- You want to review an existing diagram for mixed abstraction levels, unclear lines, component piles, missing stability concerns, or weak visual semantics.

## Installation

Copy the skill folder into your global Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\architecture-diagramming "$env:USERPROFILE\.codex\skills\architecture-diagramming"
```

If the target directory already exists, back up the old version before replacing it.

## Usage

Example:

```text
Use $architecture-diagramming to design a technical architecture diagram for an e-commerce order system.
```

Codex will default to:

1. Stating the assumed audience and diagram level.
2. Listing components and responsibilities.
3. Listing relationships with sync/async semantics.
4. Producing a Mermaid diagram when suitable.
5. Providing a short review checklist and refinement suggestions.

## Publish Automation

This repository includes a Python publisher:

```powershell
python .\scripts\publish_skill_to_github.py `
  --skill-path .\skills\architecture-diagramming `
  --repo-name architecture-diagramming-skill `
  --description "Codex skill for creating and reviewing clear technical/system architecture diagrams."
```

The script:

1. Reads `GITHUB_TOKEN` from the environment.
2. Packages the skill into a standard repository layout.
3. Creates or reuses the GitHub repository.
4. Initializes git, commits, and pushes.

It never writes the token to disk. Add `--dry-run` to verify local packaging without calling GitHub.

## Core Method

### 1. Choose The Diagram Level

- Overall technical architecture: for CTOs, tech leads, product managers, and new team members.
- Domain or subsystem architecture: for domain architects, senior engineers, and cross-team reviews.
- Application-level architecture: for developers and testers, including internal modules, layers, interfaces, and implementation details.

### 2. Six-Step Workflow

1. Derive the technical skeleton from the business architecture.
2. Derive technical modules from key scenarios and non-functional requirements.
3. Extract horizontal layers.
4. Extract reusable vertical modules.
5. Add stability and production support modules.
6. Produce a layered and sliced logical architecture.

### 3. Diagram Semantics

- Boxes: services, applications, modules, platforms, databases, queues, and external systems.
- Solid arrows: synchronous calls such as HTTP/RPC.
- Dashed arrows: asynchronous messages, events, or jobs.
- Bidirectional arrows: bidirectional communication such as WebSocket.
- Dashed lines without arrows: compile-time, configuration, or non-runtime dependencies.

## Maintenance Ideas

This repository can grow with:

- Mermaid templates for common business domains.
- Architecture review examples.
- Bilingual example prompts.
- Reusable architecture patterns extracted from real projects.
