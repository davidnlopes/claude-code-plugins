# claude-code-plugins

A Claude Code plugin marketplace. It publishes plugins that add skills, agents, and slash commands to Claude Code for code review, documentation, UI and backend development, project management, and architecture decision records.

The repository holds both the plugin sources and the marketplace registry, `.claude-plugin/marketplace.json`. Each plugin is a directory at the repository root and installs on its own.

## Install a plugin

To add the marketplace, run this in Claude Code:

```text
/plugin marketplace add davidnlopes/claude-code-plugins
```

Then install any plugin from it:

```text
/plugin install review-toolkit@dnlopes
```

## Plugins

| Plugin | What it adds |
| --- | --- |
| [`review-toolkit`](review-toolkit) | A multi-agent pull request review with reviewers for bugs, security, quality, contracts, tests, and history |
| [`ui-dev`](ui-dev) | Skills for browser automation, shadcn/ui, React, web design, and Hugo |
| [`backend-dev`](backend-dev) | Postgres best practices |
| [`quartermaster`](quartermaster) | Skills that turn plans into tickets and move issues through triage |
| [`status-line`](status-line) | A status line showing context window usage, cost, and model |
| [`wordsmith`](wordsmith) | Skills for writing documentation, READMEs, `AGENTS.md` files, rules, and code comments |
| [`adr-template`](adr-template) | A skill that records architecture decisions in a consistent format |

## Contribute

Each plugin directory holds its own `.claude-plugin/plugin.json` and its skills, agents, or commands. To add a plugin, create the directory and register it in `.claude-plugin/marketplace.json`. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit and pull request titles, because the release workflow reads them.
