<!--
---
scope:
  paths:
    - README.md
    - .claude-plugin/marketplace.json
  summary: "Project overview and installation"
last_updated: 2026-08-21T00:00:00Z
---
-->

# claude-code-plugins

A personal marketplace of Claude Code plugins — self-contained bundles of skills, agents, and slash commands that extend Claude Code's capabilities for AI-assisted development workflows.

## Summary

This repository is both the plugin source and the marketplace registry it publishes from. Each plugin is an independently versioned, self-contained unit that Claude Code can install directly. Plugins extend Claude Code with purpose-built workflows for git, code review, documentation, UI development, backend development, and architectural governance.

## Installation

Install a plugin from this marketplace by pointing Claude Code at this repo's marketplace registry:

```bash
# Add this marketplace to Claude Code
claude plugins marketplace add https://github.com/davidnlopes/claude-code-plugins
```

Then install individual plugins:

```bash
claude plugins install curator
claude plugins install git-workflow
claude plugins install governor
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `curator` | Repository documentation for AI agents, with git-based staleness tracking |
| `git-workflow` | Git and GitHub workflow commands for commits and pull requests |
| `governor` | Project tenets management via user-invocable skills: bootstrap, manage, and verify architectural constraints in AGENTS.md |
| `review-toolkit` | Multi-agent code review toolkit with specialized reviewers |
| `ui-dev` | UI development toolkit with headless browser automation and shadcn/ui |
| `backend-dev` | Backend development toolkit with database and API best practices |
| `status-line` | Custom Claude Code status line showing context window usage, cost, and model |

## Documentation

- [Architecture](docs/architecture.md) — System design and component relationships
- [Patterns](docs/patterns.md) — Plugin conventions and invariants
- [Development](docs/development.md) — Contributing and release workflow
