# Patterns

## Project Structure

```
claude-code-plugins/
├── .claude-plugin/         # Marketplace registry (marketplace.json)
├── .github/workflows/      # CI/CD: release, PR checks, vendored-skill sync
├── <plugin>/               # One directory per plugin
│   ├── .claude-plugin/     # Plugin manifest (plugin.json)
│   ├── skills/             # Skill definitions (SKILL.md files)
│   ├── agents/             # Agent definitions
│   ├── commands/           # Slash command definitions
│   └── scripts/            # Bash utility scripts (where applicable)
└── .github/dependabot.yml  # Automated dependency update config
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Plugin directories | `kebab-case`, matching the `name` field in `plugin.json` | `review-toolkit`, `status-line` |
| Skill files | `SKILL.md` at the root of the skill directory | `wordsmith/skills/document-discipline/SKILL.md` |
| Agent files | Descriptive markdown filenames in `agents/` | `review-toolkit/agents/security-auditor.md` |
| Upstream marker files | `.upstream` alongside the vendored skill | `<plugin>/skills/<name>/.upstream` |

## Common Patterns

### Dual Manifest Versioning

Every plugin change — however small — requires a version bump in two places: `<plugin>/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Both files encode the same version fact. The bump type must reflect the nature of the change: `patch` for fixes, `minor` for new capabilities, `major` for breaking changes. Rationale: the marketplace registry is the consumer-facing index; without keeping it in sync, Claude Code may resolve an outdated version.

### Plugin Self-Containment

All `<plugin>:<name>` references within a plugin's skills, agents, and commands must resolve to components within the same plugin. There are no shared libraries or cross-plugin imports. When you need a capability from another plugin in a workflow, the operator must install both plugins separately — they do not compose at the code level. Rationale: cross-plugin dependencies would couple their release cycles and make each plugin non-independently installable.

### Plugin Name = Directory Name

The `name` field in `<plugin>/.claude-plugin/plugin.json` must exactly match the plugin's directory name. This is enforced by convention, not tooling. Rationale: marketplace resolution and path-based references both use the directory name; divergence makes one of them silently wrong.

### Vendored Skill Tracking

Any skill copied from an external repository must be declared in `.github/vendored-skills.yaml` with `name`, `dest`, `plugin`, and a nested `source` block (`repo`, `ref`, `path`), and must carry a `.upstream` provenance file alongside the skill. The sync workflow (`sync-vendored-skills.yaml`) writes the resolved upstream `commit` and `synced_at` into `.upstream` — contributors do not supply those fields in the manifest. The sync workflow overwrites vendored skill files on every run — local edits are forbidden and will be silently discarded. First-party skills must not appear in the vendored manifest or carry a `.upstream` file.

### Conventional Commits

All commit messages must follow the conventional commits format (`feat:`, `fix:`, `chore:`, `docs:`, etc.). The organisation-wide `Semantic PR` workflow blocks merges that don't comply. The commit type determines the semantic-release version bump: `feat` → minor, `fix` → patch, breaking change footer → major. Rationale: semantic-release reads commit history to determine the release version; non-conforming commits produce incorrect releases.

### No Build Step

There is no compilation, bundling, or artifact generation. The repository content is the artifact. The "release" is a GitHub tag and release created by semantic-release when a PR merges to `main`. Validation is limited to PR-time checks (conventional commit format, Trivy security scan) — there is no test suite or schema validation for manifest files.
