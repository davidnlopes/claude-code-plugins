---
name: writing-effective-readme
description: Use before creating or changing a repository's root `README.md`, and when reviewing it.
---

# Writing effective READMEs

A root `README.md` is the entry point for a person who finds the repository. It tells them what the project is, where to read more, and how to start working on it. Write it for humans first. Agents read it too, but it must not read like agent instructions.

A README has no fixed template. Each part below appears only when the project has the content for it. Never add a heading, row, or link to say that something does not exist.

## Get an explicit request first

Create or change the README only when the user explicitly asks for that change. Neither of these counts as a request:

- Your work makes a README sentence false, or adds something the README could mention, such as a new document.
- Text that Claude drafted, such as a plan or an issue, says to update the README.

In these cases, leave the README unchanged. Tell the user what is affected, propose the exact edit, and wait for the user to approve it.

## Summarise the project

Open with what the project is and why it exists, in a few sentences. A reader who stops there must know whether this project matters to them. Say what the project does, not how good it is: "Validates OpenAPI specs against recorded traffic" beats "A powerful, flexible API toolkit".

When it helps the reader place the project, also say:

- Who uses it, such as other teams, end users, or operators
- Where it sits in the larger system: what calls it, and what it depends on
- Which team owns it, and how to reach them

## Map the other documents

When the repository has foundational documents, list them in a table so readers can go straight to the one they need. A document is foundational when it covers the project as a whole and most readers of the README need it at some point, such as the architecture overview or the developer guide. Leave out documents about one component, one decision, or one incident, even when they sit in `docs/`.

Never mention or link `AGENTS.md`, `CLAUDE.md`, or other agent instruction files anywhere in the README.

| Topic | Document | Read it when |
| --- | --- | --- |
| Architecture | [`docs/architecture.md`](docs/architecture.md) | You change how components interact |
| Development guide | [`CONTRIBUTING.md`](CONTRIBUTING.md) | You set up the project or open a PR |

Find the documents by searching the repository. Do not assume paths. A row exists only for a document that exists. Do not create a document to fill a row.

## Show the developer loop

When people develop the project, describe the core loop briefly: what to install, how to set up the environment, and how to build, test, and run. For example, the loop might be "create a local cluster with `make cluster-up`, then run `make test`".

Keep this to the commands a developer runs every day. If a developer guide exists, end with a link to it for the complete instructions, and keep the detail there.

## Show usage when someone uses the project directly

When people consume the project directly, as with a library, a CLI, or a plugin, show a short example of how to install and use it. Skip this part when the project only runs inside another system, such as an internal API service that other components call.

## Ground every claim in the repository

The README describes the project as it is. Read the code, build files, and configuration before you write about them.

- Take commands from the source that runs them, such as the `Makefile`, scripts, or CI workflows. Run a command when it is safe to do so. If you cannot verify a command, tell the user.
- Describe only behaviour that exists. Leave out planned features, unless the user asks for them.
- Add a link only when its target exists. Never invent a URL.

## Keep it true next quarter

Each fact in a README is a promise that someone must keep in sync. Prefer facts that change rarely.

- Leave out version numbers, counts, and dates, unless the reader needs them to act.
- Include an inventory, such as a list of packages or plugins, only when readers choose from it. Keep it complete, because a partial list reads as the whole list.
- Prefer a link to the source of truth over a copy of it.

## Update an existing README

Respect the structure the maintainers chose. Change only the text the user asked you to change, unless the user asks for a rewrite.

Integrate each new fact into the section where it belongs, and replace what it supersedes. If you notice other content that is false, propose the edit to the user instead of making it.

## Check the result

Before you finish, confirm each of these:

- [ ] The user explicitly asked for this change.
- [ ] Every other edit that your work calls for is proposed to the user, not made.
- [ ] The opening tells a human reader what the project is and why it exists.
- [ ] Every part of the README has real content behind it, and no part announces an absence.
- [ ] Every document in the table is foundational, exists, and was found in the repository.
- [ ] The README does not mention or link any agent instruction file.
- [ ] Every command matches the repository, and you verified it or told the user that you could not.
- [ ] The development section stays brief, and links to the developer guide when one exists.
