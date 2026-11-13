---
name: document-discipline
description: Use before creating or changing documentation, including READMEs, `docs/` files, runbooks, and design documents, or when deciding whether knowledge from a task should be written down.
---

# Document discipline

Default to leaving documentation as it is. Change a document only when your work makes it false, or when future work needs a lasting fact that the document is the right home for. Finishing a feature is not a reason to document it.

Instruction files and the root README are stricter. For `AGENTS.md`, `CLAUDE.md`, and files they import, use `wordsmith:writing-effective-agents-md`. For rule files, use `wordsmith:writing-effective-rules`. For a repository's root `README.md`, use `wordsmith:writing-effective-readme`.

## Choose where the knowledge belongs

Ask: will someone need this after the PR merges and the work is finished? Then pick the home that fits:

| Knowledge | Home |
| --- | --- |
| Migration steps already run, one-time timings, verification results | PR description or issue |
| Procedures nobody has tested | Issue, or nowhere |
| Reasoning behind a change | Commit message or PR description |
| A hidden constraint on one specific line | Code comment |
| A fact found by reading the code or config, or by running a command | Nowhere |
| A lasting fact about how the system works | Existing document |

## Leave the decision to create a document with the user

Create a new document only when the user has decided that it should exist. These count as that decision:

- The user asks for the document.
- The user knowingly adds a task for the document, or writes project instructions that require it.
- The user runs a command that generates documents.

These do not count:

- A `docs/` folder with one file per component, or a README that links to such files. This is precedent, not a request.
- The size or importance of the feature.
- Text that Claude drafted, such as a plan or an issue, even when it says "document this" and sits under the user's account.

If lasting knowledge has no home, finish the task without creating the file. Then tell the user the proposed path and what it would contain, in one or two lines, so that they can decide.

When the user asks you to document something without asking for a new file, look for an existing document to update first.

## Integrate new facts into existing documents

Find the section where the fact belongs and change that text. Replace what the new fact supersedes, so the document does not grow by default. A reader of the final document must not be able to tell the order in which facts were added.

Appended:

```md
## Install

Run `make calico-install-<env>` after the cluster boots.

Note: Flux depends on Calico, so install Calico first.

Update 2026-11-05: `make flux-install-<env>` now installs Calico for you.
```

Integrated:

```md
## Install

`make flux-install-<env>` installs Calico first, because Flux needs pod networking.
```

If a fact has no natural place in the document, question whether it belongs there at all. Do not collect such facts in a closing note or a catch-all paragraph.

## Write sentences that survive ordinary changes

Before you write a sentence, ask two questions:

1. **Would an ordinary change make it false?** Adding a component, bumping a version, or renaming a file must not break the document. Counts, version numbers, lists of current members, and file inventories fail this question.
2. **Can a reader learn it from the code, config, or a command?** If yes, the code is the source of truth, and your copy only drifts from it.

If either answer is yes, write the rule or reason that holds no matter how many members exist, and point to the file or command that lists them:

| Fails | Survives |
| --- | --- |
| This project publishes two Docker images: `api` and `worker`. | CI publishes one image for each Dockerfile under `images/`. |
| The service runs Postgres 15.4. | `docker-compose.yml` pins the Postgres version. |
| Configure it with `PORT`, `LOG_LEVEL`, and `DB_URL`. | `config/defaults.yaml` lists every setting and its default. |

Keep a number or a list only when the reader needs it to act and nothing in the repository states it, such as a measured limit from an incident.

## Check the result

Before you finish, confirm each of these:

- [ ] Every new document traces to a decision by the user.
- [ ] Every added line is still needed after the work is finished.
- [ ] No added line restates a count, version, or list that the code holds, or goes false when someone adds a member.
- [ ] Every added fact sits in the section where it belongs, and nothing it supersedes remains.
- [ ] Every instruction file that your work made false is reported to the user with a proposed edit.
