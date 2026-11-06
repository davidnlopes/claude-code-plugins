---
name: writing-effective-rules
description: Use before creating or changing Claude Code rules, and when reviewing them, including files in `.claude/rules/` and `~/.claude/rules/`.
---

# Writing effective rules

A rule changes what Claude does in a specific situation. Give each rule the shape its content needs: a one-line convention stays one line, and a boundary with a tempting violation gets an example. Rule files have no standard template.

## Get an explicit request first

Create or change a rule file only when the user explicitly asks for that change. Neither of these counts as a request:

- A useful fact that you discover during a task
- Text that Claude drafted, such as a plan or an issue

If a change makes a rule false, or you find knowledge that might belong in a rule, leave the file unchanged. Tell the user, and propose the exact edit.

## Choose where the instruction belongs

Name the repeated mistake or ambiguity the instruction prevents. If you cannot name one, raise that with the user instead of writing the rule.

Then pick the home that fits. Write a rule only if none of these apply:

- **Multi-step procedure or occasional task:** a skill, which loads only when relevant.
- **Action that must always be blocked or enforced:** a hook or a permission. Claude treats rules as context, not as enforced configuration.
- **Behaviour a linter, formatter, type checker, or test already enforces:** that tool. Mention the command at most.
- **Fact Claude can find by reading a config file or running a command:** nowhere. Keep the unwritten convention, the reason behind a choice, and the gotcha that nothing else reveals.

## Include the instruction, scope, and reason

Every rule conveys three things, with or without headings.

**Instruction.** Open the file with it. State the target behaviour rather than only the banned one. Match the wording to the real strictness:

- For an invariant, use `must`, and give no exceptions.
- For a default, say so and name the exceptions.

**Scope.** Use `paths` frontmatter when the scope is file-based:

```md
---
paths:
  - "src/api/**/*.ts"
  - "lib/**/*.ts"
---
```

- A rule with `paths` loads when Claude reads or edits a matching file. If the rule must shape a decision made before Claude touches such a file, leave out `paths`.
- A rule without `paths` loads every session and costs context every session, so reserve this for instructions that apply to most work.
- `paths` is the only frontmatter field Claude Code reads from a rule. If the YAML does not parse, the rule loads as if it had no `paths`.
- For a scope that is not file-based, state it in the opening sentence: "When you add a public HTTP endpoint, ...".

**Reason.** Say what goes wrong without the rule, so Claude can handle cases the rule does not foresee. Omit the reason only when it is self-evident.

## Add other devices only when the rule needs them

Each device below is optional. Most rules need one at most.

| Device | Use when | Skip when |
| --- | --- | --- |
| Example | The correct shape is hard to describe in words | One sentence states the shape exactly |
| Wrong and right contrast | Claude is likely to choose a specific wrong approach | The wrong approach only negates the instruction |
| Ordered steps | The order matters and there are a few steps | The procedure is long enough to be a skill |
| Checklist | Several separate conditions must be verified | The rule has one condition |
| Headings | The rule has several parts to navigate | The rule fits on one screen |

Prefer a short copied snippet for an example, cut to the smallest size that shows the shape. Use a file reference when the example is too long to copy, and remember that references break when files move.

Write checklist items that a reviewer can answer yes or no by inspecting imports, files, behaviour, commands, or tests:

```md
- [ ] The service does not import from `adapters`.
- [ ] HTTP integration tests use `testutil.NewIntegrationTestServer`.
```

Items such as "Code is clean" or "Tests are enough" cannot be verified, so rewrite them or delete them.

## Sample rules of different shapes

These samples show the range. They are not templates.

A single convention:

```md
---
paths:
  - "db/migrations/**"
---
Name migrations `YYYYMMDD_description.sql`. The deploy job applies them in filename order, so any other format runs out of sequence.
```

A boundary with a tempting violation:

````md
---
paths:
  - "internal/services/**"
---
Services must depend on interfaces in `internal/ports`. Tests replace adapters through these interfaces, so a direct import forces the test to run against a real database.

```go
// Wrong
import "app/internal/adapters/postgres"

// Right
func NewBilling(store ports.InvoiceStore) *Billing
```
````

A scope that is not file-based, with several conditions to verify:

```md
When you add a public HTTP endpoint, describe it in the OpenAPI spec. CI generates client SDKs from the spec, so customers cannot call an endpoint that it omits.

- [ ] `api/openapi.yaml` describes the endpoint and its error responses.
- [ ] `make generate-sdk` ran, and its output is committed.
- [ ] An integration test calls the endpoint through `testutil.NewIntegrationTestServer`.
```

## Keep each rule to one concern

Split a rule when it covers more than one concern. Give the file a descriptive name, such as `api-design.md`. Delete any line Claude already follows by default, and any line that does not prevent a likely mistake.

## Write or revise a rule

1. Confirm that the user explicitly asked for this change. Then name the mistake the rule prevents, and confirm a rule is the right home.
2. Read the existing rules and `CLAUDE.md`. Match local conventions, and resolve any conflict, because Claude can follow either side of a contradiction.
3. Write the instruction, scope, and reason.
4. Add a device only where the table in "Add other devices only when the rule needs them" calls for it.
5. Check the draft:
   - [ ] The rule covers one concern.
   - [ ] Its wording matches how strict the rule really is.
   - [ ] Every line changes what Claude does, compared with its default.
   - [ ] Its scope loads the rule before Claude needs it, and not more often.
6. Return only the Markdown for the rule file, unless the user asks for an explanation. When you revise a rule, also summarise the meaningful changes.
