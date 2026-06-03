# Architecture Diagramming Skill

Codex skill for creating and reviewing clear technical/system architecture diagrams.

- [中文说明](README.zh-CN.md)
- [English README](README.en.md)

## Quick Install

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\architecture-diagramming "$env:USERPROFILE\.codex\skills\architecture-diagramming"
```

Then ask Codex:

```text
Use $architecture-diagramming to design a technical architecture diagram for my system.
```

## Publish Automation

This repository includes a standard-library Python publisher:

```powershell
python .\scripts\publish_skill_to_github.py `
  --skill-path .\skills\architecture-diagramming `
  --repo-name architecture-diagramming-skill `
  --description "Codex skill for creating and reviewing clear technical/system architecture diagrams."
```

It reads `GITHUB_TOKEN` from the environment, creates or reuses the GitHub repository, creates a local commit, and uploads files through the GitHub Contents API. Run with `--dry-run` to verify the local packaging flow without calling GitHub.

## What It Helps With

- Selecting the right diagram level for the audience.
- Mapping business capabilities to technical components.
- Showing responsibilities, dependencies, sync/async relationships, data flow, and production support concerns.
- Producing reviewable Mermaid or text-based architecture diagrams.
