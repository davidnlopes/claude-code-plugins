---
name: writing-effective-agents-md
description: Use before creating or changing `AGENTS.md` or `CLAUDE.md` files, and when reviewing them.
---

# Writing effective AGENTS.md files

An `AGENTS.md` or `CLAUDE.md` file gives Claude a mental model of the project: what the system is, how its parts fit together, and what must stay true. Claude reads it to learn how to think about any change here, not to collect facts for specific tasks.

These files have no standard template. Choose the content this project needs, and let its size set the length.

## Get an explicit request first

Create or change `AGENTS.md`, `CLAUDE.md`, or a file they import only when the user explicitly asks for that change. Neither of these counts as a request:

- A useful fact that you discover during a task
- Text that Claude drafted, such as a plan or an issue

If your work makes an instruction false, or you find knowledge that might belong in one of these files, leave the file unchanged. Tell the user, and propose the exact edit.

## Test every line

Keep a line only when it shapes how Claude approaches many different tasks in this project.

Whether Claude could work the fact out from the code does not decide this. An accurate overview belongs here because it saves Claude from rebuilding the picture each session. A hidden fact that matters for one area or one task does not belong here, however useful it is. Move it to the home that fits, as "Move detail out of the file" describes.

Lines such as "Write clean code" change nothing, so delete them.

## Describe the mental model

Each kind of content below is optional, and a small project needs only a few. Use your own headings, and name them after the idea rather than a generic category: "Each layer has one job" tells Claude more than "Architecture".

| Content | What it gives Claude | Example |
| --- | --- | --- |
| Purpose | What the system is and who it serves | "A Kubernetes-native control plane for defining and running AI agents." |
| Architecture | How the major parts fit together | "Harness compilers translate templates into backend inputs. Adapters apply them." |
| Component boundaries | The job of each layer, and what it leaves to others | "The store persists state. It does not launch actors." |
| Sources of truth | Which artifact wins when copies disagree | "Generated code is never the source of truth." |
| Design vocabulary | The terms the project reasons with | "Semantic functions are pure. Pragmatic functions wire them to I/O." |
| Homes for work products | Where temporary and lasting knowledge go | "Keep plans in the gitignored `.plans/`. Merge lasting decisions into `docs/architecture/`." |

Describe the major areas, not every directory. Leave out version numbers, component inventories, and other volatile facts, unless the mental model depends on them.

## State the invariants the project has

Invariants are the things that must stay true whatever the task. How many a project has depends entirely on the project: many have none worth stating, and some have ten. Record only the invariants that the code already follows or that the user names, and never add one to fill the section. If you find none, leave the section out. For each one, write what must hold and why, in two to four sentences. A good invariant is:

- **Actionable:** it says that X must or must not do Y.
- **Architectural:** it records a decision specific to this project, not a style that a linter can check.
- **Grounded:** the code follows it today.
- **Persistent:** it is unlikely to change often.
- **Verifiable:** a reviewer can decide compliance with reasonable effort.

For example, "Keep things separate" fails, but this passes:

```md
Domain modules must not import infrastructure packages. This keeps the domain layer portable and testable without external services.
```

Follow these practices when you write invariants:

- **Check the code first.** Search for code that follows the invariant and code that violates it, and show the user both. If the code contradicts it, fix the violations, narrow the invariant, or drop it. If it is a goal rather than today's state, say so in the invariant.
- **Propose each invariant separately.** The user approves each one, because each one binds all future work.
- **Keep evidence out of the file.** Show `file:line` references in the conversation only. They go stale after a refactor, and the code remains the source of truth.
- **Match the wording to the real strictness.** Name any exception beside the invariant.
- **Include a command only when it is part of an invariant.** "API changes must be followed by `make generate`, because clients are built from the committed output" qualifies. A list of common commands does not.
- **Preserve managed sections.** If the file has a section with its own format, such as `## Tenets`, keep that format, and change the section only when asked.

A small project can stop at a few short sections:

```md
# HomeLab

This repository defines two Kubernetes clusters and the hosts around them, from the VM image to public ingress. One person runs it for personal use.

## How the layers fit together

Each layer hands over to the next: Packer builds the VM image, Terraform provisions the VMs and bootstraps Talos, and Flux manages everything that runs on the clusters. Ansible manages only the hosts outside the clusters.

## What must stay true

- Git describes the desired state. A change made directly on a cluster is temporary until Git matches it.
- Nodes are disposable. Persistent data must live outside their boot disks, so that you can replace any worker.
```

## Move detail out of the file

Keep only what applies across the project. Move the rest to the home that loads it when needed:

| Material | Home | When it loads |
| --- | --- | --- |
| Instructions for one directory | Nested `AGENTS.md` or `CLAUDE.md` | When Claude works in that directory |
| Instructions for matching files | Path-scoped rule | When Claude reads or edits a matching file |
| Procedure or occasional task | Skill | When relevant or invoked |
| Background and design detail | Linked document | When Claude follows the link |
| Constraint on one specific line | Code comment | When Claude reads that code |

Tell Claude when to follow a link: "Before you change the wire format, read `docs/protocol.md`." Use a plain link rather than an `@` import for material that most sessions do not need, because an imported file loads with the file that imports it and costs the same context.

## Keep the instructions in one file

By default, Claude Code reads `AGENTS.md` only when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or above it. If a repository has both files, `AGENTS.md` does not load unless `CLAUDE.md` imports it with `@AGENTS.md`.

Write the instructions in one file, and use the import to share them. Choose `AGENTS.md` when other coding tools read the repository too. Claude Code does not read `AGENTS.local.md`, `AGENTS.override.md`, or anything under `.agents/`.

## Keep the file in proportion

Match the length to the project. Treat 200 lines as a ceiling, not a target, and count imported files towards it. Longer files use more context and reduce how closely Claude follows them.

Integrate each new instruction into the section where it belongs, and replace what it supersedes. If an instruction has no natural place, question whether it belongs in this file.

## Write or revise the file

1. Confirm that the user explicitly asked for this change.
2. Read the file, its imports, nested instruction files, and rules. Resolve any conflict, because Claude can follow either side of a contradiction.
3. Read the code that the file describes, so that the mental model matches the system as it is.
4. Write only the lines that pass the test in "Test every line".
5. Check the draft:
   - [ ] A reader finishes with a mental model of the project, not a list of assorted facts.
   - [ ] Every invariant is grounded in the code or labelled as a goal, and the user approved it.
   - [ ] No invariant was added only because the section expected one.
   - [ ] No instruction appears twice across the file, its imports, and rules.
   - [ ] Material for one area or an occasional task has moved to the home that loads it when needed.
6. When you revise a file, summarise the meaningful changes.
