# Claude Code Plugins

A personal marketplace of Claude Code plugins — self-contained bundles of skills, agents, and slash commands that extend Claude Code for AI-assisted development workflows. The repo is both the plugin source and the marketplace registry it publishes from.

## Quick Start

No build step. To contribute a plugin, author the required files and bump versions — see [Development](docs/development.md).

## Documentation

@docs/architecture.md
@docs/patterns.md
@docs/development.md

- [Architecture](docs/architecture.md) — System design and component relationships
- [Patterns](docs/patterns.md) — Plugin conventions and invariants
- [Development](docs/development.md) — Release workflow and contribution guidelines

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `.claude-plugin/` | Marketplace registry (`marketplace.json`) — authoritative plugin index |
| `<plugin>/` | Each plugin's self-contained source (skills, agents, commands, hooks, scripts) |
| `<plugin>/.claude-plugin/` | Per-plugin manifest (`plugin.json`) — name, description, version, author |
| `.github/workflows/` | CI/CD: semantic-release, PR checks, security scans, vendored-skill sync |

## Tenets

CRITICAL: These tenets are MANDATORY and MUST be followed in all work on this codebase.

### T1. Plugin manifests must declare name, description, version, and author, with name matching the directory

Every plugin must contain `<plugin>/.claude-plugin/plugin.json` declaring at minimum `name`, `description`, `version`, and `author`. The `name` field must equal the parent directory name so that path-based references and manifest-based references stay consistent.

**Severity:** critical

### T2. Plugin version bumps must touch both manifest files in lockstep, and every plugin change must include a bump

Any change to a plugin's contents must include a version bump in both `<plugin>/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. The two files store the same version fact and must never drift. The bump type (major / minor / patch) must reflect the nature of the change. Before opening a PR or merging a side branch into main, verify the bump exists and matches the change set.

**Severity:** critical

### T3. Plugins must be self-contained — no cross-plugin skill or agent references

A plugin's skills, agents, commands, and hooks must only reference other components within the same plugin. `<plugin>:<name>` references must always resolve inside the source plugin. Cross-plugin dependencies would couple release cycles and break the marketplace's modular distribution model.

**Severity:** high

### T4. Vendored skills must carry a `.upstream` marker and be declared in `.github/vendored-skills.yaml`

Skills copied from upstream repositories must be tracked declaratively in `.github/vendored-skills.yaml` (with `name`, `dest`, `plugin`, and a nested `source` block declaring `repo`, `ref`, and `path`) and must carry a `.upstream` provenance file. The sync workflow writes the resolved `commit` and `synced_at` into `.upstream`; contributors do not supply those fields. Local edits to vendored skills are not allowed — the sync workflow will overwrite them. First-party skills must not appear in the vendored manifest or carry a `.upstream` marker.

**Severity:** high

## Tenet Exceptions

Approved exceptions to tenets. Each must have justification.

| File | Tenet | Reason | Approved |
|------|-------|--------|----------|
| (none) | | | |
