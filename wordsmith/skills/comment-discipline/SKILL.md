---
name: comment-discipline
description: Use when writing, editing, or reviewing code or config in any language, including IaC and manifests, to decide whether a comment belongs and how to word it.
user-invocable: false
---

# Comment discipline

Default to no comments. A file that reads clean from start to finish is the expected result, not a gap to fill.

## Apply one test

Add a comment only when both conditions are true:

1. **The fact is hidden.** Names, the surrounding code, and what a competent practitioner in this stack already knows do not reveal it.
2. **Missing it has a concrete cost.** A competent practitioner would break something, "fix" it into a regression, or lose real time chasing an external fact. A moment of pause does not count.

"Competent" is the calibration: not a novice, and not someone new to this tool. A true, well-written sentence that teaches this reader what they already know fails the test. So does "a reader might appreciate this", because nearly anything clears that bar.

Comments that pass usually record one of these:

- A constraint the code must satisfy but does not display
- An invariant that types, names, and specs do not show
- A workaround for a named external bug, platform quirk, or version gap
- An incident or measured failure that recurs if someone "fixes" the code
- Behaviour that looks wrong for a reason specific to this system
- A cross-file or cross-system link that nothing in the file surfaces, such as the service that consumes a value

When you are unsure, cut the comment. A reader sent to `git blame` now and then costs less than a codebase where every comment must be evaluated for whether it is worth reading.

## Word the comment

- State the fact and its consequence, not the action the next line performs.
- Keep it to one or two lines. Put longer rationale in the commit message or an existing document.
- Name the specifics: the bug ID, the version, the incident, the measured number. Cite what happened, not a hypothetical. These are external facts that the code cannot show.
- Do not restate what the code holds, such as its values, defaults, or the current list of callers. The code changes, the comment does not, and the reader then trusts the wrong one.
- Say it once, where a reader lands first, such as the shared module. Other instances get nothing, or at most a one-clause pointer.

## Compare near-miss pairs

Each pair below shows a comment that sounds useful but fails, and one that passes. The failing comment states general knowledge or restates the code. The passing comment states a fact specific to this system.

```hcl
# Fails: Pin deliberately; check the registry before bumping.
# Passes: 3.2.5 breaks OIDC token refresh (upstream #4812).
image_tag = "v3.2.4"
```

```yaml
# Fails: 2 replicas gives failover if one pod goes down.
# Passes: Max 2. Each replica holds 200 connections, and the database allows 400.
replicas: 2
```

```ts
// Fails: Use a transaction to ensure atomicity.
// Passes: The reconciliation job flags a ledger row with no balance update as fraud.
await db.transaction(writeLedgerAndBalance);
```

```ts
// Fails: Retry with backoff to handle transient failures.
// Passes: The vendor returns 429 for up to 30 s after a burst, so retries must outlast that.
await retry(sendInvoice, { maxElapsedMs: 45_000 });
```

```python
# Fails: Start the retry count at 1.
# Passes: Upstream treats 0 as "infinite retries".
retry_count = 1
```

```hcl
# Fails: writeback improves write performance.
# Passes: A crash-looping pod under cache=none generated 23 TB of disk reads and wedged the node (k8s-prod-wrk-2 incident).
cache = "writeback"
```

```yaml
# Fails: Address of the NFS server.
# Passes: Must be the IP. The CSI controller mounts from a pod, and cluster DNS never sees the nodes' /etc/hosts entry.
NFS_SERVER: "10.0.0.5"
```

```js
// Fails: Fix for PROJ-123, as requested in review.
// Passes: Works around acme-http #2114, which drops the body on redirect.
const res = await fetch(url, { redirect: "manual" });
```

An external bug that explains the code belongs in the comment. The ticket, review, or conversation that produced the change belongs in the commit message or PR description.

## Write nothing for these habits

These habits fail the test, however reasonable each comment looks:

```ts
/** @param userId The ID of the user */
// --- Helpers ---
// Arrange
// Changed to a Set for O(1) lookup
```

```yaml
# Let's Encrypt account email
ACME_EMAIL: "ops@example.com"
```

```hcl
# A separate Terraform root gives this its own state file.
module "storage" { ... }
```

- **Decision records.** "We chose Redis here" helps only if not knowing it breaks something. In that case, comment the consequence. Put the decision itself in the commit message or an existing document.
- **Repeated rationale.** The same explanation above every namespace, policy, or environment has become habitual coverage.
- **Blanket coverage.** Every function, block, or resource does not need a comment. Judge the file's comment-to-code ratio as well as each comment.

## Handle cases outside the test

- **Comments a tool or language needs**, such as `# noqa`, `//go:build`, or license headers: write them when required. Apply the test to any reason you add beside them.
- **Public API documentation that the language or repo expects**, such as Go doc comments: write them, and spend the words on what the signature hides, such as errors, units, and ownership.
- **Existing comments:** update or delete any that your change makes false. Leave unrelated comments alone, unless you are asked to review them.
- **Commented-out code:** leave it out, because version control keeps it.
- **`TODO` comments:** write one only with a tracked issue or a specific condition for doing the work. Otherwise, tell the user about the gap.
- **A user who explicitly asks for comments:** write them, and use the wording guidance above.

## Review comments in a diff or file

Apply the test to each comment, then check the whole file:

1. Flag a comment that fails the test, including one written as a full, well-phrased sentence.
2. Flag a reference to this PR, the fix, the discussion, or the user's request.
3. Flag rationale repeated across sibling files, namespaces, or resources.
4. Flag a file whose comment volume is out of proportion to its code, even if no single comment fails.
5. Flag a missing comment only where a hidden constraint, incident, or cross-system link exists and nothing in the file surfaces it.
