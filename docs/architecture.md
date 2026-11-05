<!--
---
scope:
  paths:
    - .claude-plugin/**
    - "*/.claude-plugin/**"
    - .github/workflows/**
  summary: "System architecture and component relationships"
last_updated: 2026-05-12T23:21:35Z
---
-->

# Architecture

## Overview

This repository is a plugin marketplace for Claude Code: a collection of independently versioned plugins, each a self-contained bundle of skills, agents, and commands. The marketplace itself is declaratively defined in a root-level registry file, and each plugin carries its own manifest. There is no build step — the "release" is a semantic-release-driven GitHub tag that updates the registry.

## Components

### Marketplace Registry
**Lives in:** `.claude-plugin/marketplace.json`
**Owns:** The authoritative, consumer-facing index of all available plugins — their names, versions, and source paths. Claude Code reads this file when resolving what to install.
**Interacts with:** Each plugin's manifest (`<plugin>/.claude-plugin/plugin.json`) — both must carry the same version for any given plugin. Drift between these two is a silent correctness bug.

### Plugin
**Lives in:** `<plugin>/` (one directory per plugin at the repo root)
**Owns:** All skills, agents, commands, hooks, and scripts for a single capability domain. A plugin is the unit of installation — Claude Code installs and loads a plugin as a whole.
**Interacts with:** The marketplace registry for version indexing. A plugin must never reference components in another plugin; all `<plugin>:<name>` references must resolve internally.

### Plugin Manifest
**Lives in:** `<plugin>/.claude-plugin/plugin.json`
**Owns:** The plugin's declared identity: name, description, version, author. The `name` field must equal the parent directory name — this is the contract that keeps path-based and manifest-based references consistent.
**Interacts with:** The marketplace registry, which mirrors the version. Both must be bumped in lockstep on every change.

### Skills
**Lives in:** `<plugin>/skills/`
**Owns:** Specialized instruction sets loaded into Claude Code sessions on demand. Each skill is a markdown file (`SKILL.md`) describing a focused workflow. Skills may reference scripts within the same plugin but never in sibling plugins.
**Interacts with:** Agents and commands within the same plugin when a workflow requires orchestration.

### Agents
**Lives in:** `<plugin>/agents/`
**Owns:** Named agent definitions invoked by skills or commands within the same plugin. Agents encapsulate a specific sub-task (e.g., codebase exploration, doc generation) and are not shared across plugins.
**Interacts with:** Skills that delegate sub-tasks to them; scripts in the same plugin's `scripts/` directory.

### Scripts
**Lives in:** `<plugin>/scripts/`
**Owns:** Bash utilities that support skill or agent execution — file discovery, data transformation, or external tool integration. Scripts are implementation details of the plugin, not independently consumable.
**Interacts with:** Called by agents or skills within the same plugin; never imported by other plugins.

### Hooks
**Lives in:** `<plugin>/hooks/`
**Owns:** Event-driven scripts triggered by Claude Code tool-lifecycle events (e.g., `PostToolUse`). A hook is registered via a `hooks.json` manifest at the hook directory root and is invoked by the Claude Code runtime — not by skills, agents, or commands.
**Interacts with:** The Claude Code runtime, which dispatches lifecycle events; remains plugin-scoped, like every other component type.

### CI/CD Workflows
**Lives in:** `.github/workflows/`
**Owns:** The automated quality and release pipeline. Key workflows: the organisation-wide `Semantic PR` (enforces conventional commits) and `Trivy` (security scanning) workflows, `release.yaml` (semantic-release on push to `main`), `sync-vendored-skills.yaml` (upstream skill synchronization).
**Interacts with:** The marketplace registry and plugin manifests — semantic-release is responsible for creating GitHub releases but does NOT automatically bump version numbers inside manifest files. Version bumps in manifests are a manual contributor responsibility.

### Vendored Skills Registry
**Lives in:** `.github/vendored-skills.yaml`
**Owns:** The declarative list of skills copied from external repositories, including the upstream repo, ref, path, and commit. This is the source of truth for the sync workflow.
**Interacts with:** `sync-vendored-skills.yaml` workflow, which reads this file and fetches from upstream. Each vendored skill directory also carries a `.upstream` provenance file — these two must always be consistent.

## Invariants

- A plugin's version in `<plugin>/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` must always be identical. There is no runtime enforcement — this is a contributor invariant.
- The `curator` plugin is self-hosting: it provides the skills and agents used to generate and update this repository's own documentation. Modifications to `curator` affect future documentation generation runs.
- Vendored skills are overwritten on every sync run. Local edits to vendored skill files will be silently lost.
- No cross-plugin references are permitted. The modular distribution model depends on every plugin being independently installable.
