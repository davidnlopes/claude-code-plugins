<!--
---
scope:
  paths:
    - .github/workflows/**
    - renovate.json
  summary: "Build, test, and development workflow"
last_updated: 2026-05-12T23:21:35Z
---
-->

# Development

## Prerequisites

- A GitHub account with write access to the repository
- Familiarity with [Conventional Commits](https://www.conventionalcommits.org/) — PRs that don't comply are blocked

## Setup

No local tooling required. There is no build step. All you need is a text editor and git.

## Contributing a Plugin

1. Create a new directory at the repo root using `kebab-case` — this becomes the plugin name.
2. Add `<plugin>/.claude-plugin/plugin.json` declaring `name` (must match directory), `description`, `version`, and `author`.
3. Add skills, agents, commands, and scripts under `<plugin>/skills/`, `<plugin>/agents/`, `<plugin>/commands/`, and `<plugin>/scripts/` as appropriate.
4. Register the plugin in `.claude-plugin/marketplace.json` with the same version declared in `plugin.json`.
5. Open a PR with a conventional commit title (e.g., `feat: add <plugin> plugin`).

## Modifying an Existing Plugin

Every change to a plugin's contents requires a version bump in two places:

- `<plugin>/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

Both must carry the same version. Bump type: `patch` for fixes, `minor` for new capabilities, `major` for breaking changes.

Exception: vendored-skill sync PRs opened by `sync-vendored-skills.yaml` apply the bump automatically — contributors do not need to bump manually on those PRs.

## Release Process

Releases are fully automated. On merge to `main`, `semantic-release` reads the conventional commit messages to determine the bump type, creates a GitHub release and tag, and publishes a changelog. No manual version management is needed at the repository level — only the manifest files require manual bumping.

## CI Checks

All PRs must pass:

- **Conventional commit check** (organisation-wide `Semantic PR` workflow) — enforces commit message format; determines release version.
- **Security scan** (organisation-wide `Trivy` workflow) — Trivy scans for known vulnerabilities in referenced content.

There is no automated test suite for manifest correctness or skill syntax. Structural validation is human-reviewed.

## Vendored Skills

To vendor a skill from an external repository:

1. Copy the skill files into the appropriate plugin directory.
2. Add an entry to `.github/vendored-skills.yaml` with `name`, `dest`, `plugin`, and a nested `source` block (`repo`, `ref`, `path`).
3. Create a `.upstream` provenance file alongside the vendored skill. The sync workflow writes `commit` and `synced_at` into this file on each run — contributors do not need to supply them up-front.

The `sync-vendored-skills.yaml` workflow fetches from upstream periodically and opens a PR when changes are detected. The PR includes the dual-manifest patch version bump (both `<plugin>/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`) automatically — no manual bump is needed. Do not edit vendored skill files directly — changes will be overwritten on the next sync.

## Dependency Updates

Renovate is configured to open automated PRs for dependency updates (e.g., GitHub Actions versions). Review and merge these PRs as part of routine maintenance.
