# claude-code-plugins

This repository is a Claude Code plugin marketplace. It holds the source of every published plugin and the registry that lists them. There is no application code to build or test: a change here edits skills, agents, commands, hooks, and JSON manifests that Claude Code loads from the plugin directories.

## How the repository fits together

Each top-level plugin directory is a self-contained unit. It carries its own `.claude-plugin/plugin.json` and the skills, agents, commands, or hooks it ships. Plugins do not depend on each other, so a plugin must not reference files in another plugin's directory.

`.claude-plugin/marketplace.json` is the registry. It maps each plugin name to its directory and repeats the plugin's version and description. Claude Code installs from the registry, so a plugin that is missing from it is not published.

## What must stay true

- A plugin's version in `.claude-plugin/marketplace.json` equals the version in its own `plugin.json`. Change both in the same commit that changes the plugin. Installed copies update only when the version changes, so a content change without a bump never reaches users.
- Vendored skills are read-only copies. A skill that has an `.upstream` file is declared in `.github/vendored-skills.yaml`, and a scheduled workflow deletes and re-creates it from the upstream repository. Fix such a skill upstream, or the next sync discards your edit.
- Every plugin directory is listed in the root `README.md` plugin table, because the table is the only inventory that readers browse. Add or remove the row when you add or remove a plugin.
- The repository is public. Skills, descriptions, and docs must make sense to any user, without references to one person's machine, accounts, or private tooling.

## Releases

A semantic-release workflow on `main` derives releases from Conventional Commit messages, so commit and pull request titles must follow that format. The release rules in `.releaserc.yaml` decide which types produce a release.
