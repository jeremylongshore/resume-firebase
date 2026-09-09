---
name: beads-expert
description: |
  Manage durable engineering work with the current bd CLI and Dolt-backed
  Beads database. Use when work spans sessions, needs dependency tracking, or
  must survive context compaction. Trigger with requests to create, claim,
  update, link, close, diagnose, or synchronize Beads issues.
allowed-tools: "Bash(bd:*),Read"
argument-hint: "[issue-id or task description]"
version: "2.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
compatibility: "Requires bd 1.x with its Dolt backend. Git is required for source-code operations; network and configured remote credentials are required only for bd dolt pull/push."
tags: [task-management, issue-tracking, dependencies, dolt, durable-memory]
model: inherit
effort: medium
---

# Beads Expert

## Overview

Use Beads as the durable work graph and Git as the separate source-code history.
Beads stores issues in a versioned Dolt database rather than SQLite or JSONL, so
read the [storage model](references/storage-model.md) before diagnosing
synchronization or migration problems.

## Prerequisites

- `bd version` reports a 1.x release.
- The current repository is the intended target.
- Repository instructions such as `AGENTS.md` have been read with `Read`.
- A Beads workspace exists, or the operator has authorized initialization.

## Safety boundary

- Run `bd where` or `bd context --json` before any write.
- Prefer `bd bootstrap` when a clone may already have a Dolt data ref or remote.
- Use `bd init` only for a genuinely new workspace. Never reinitialize or discard
  remote history without explicit authorization and the required destroy token.
- Do not edit `.beads/` database files directly.
- Never print remote passwords or credential-file contents.
- Keep Git commits/pushes and Dolt commits/pushes conceptually separate.

## Workflow

1. Load context:
   ```bash
   bd prime
   bd ready
   bd list --status in_progress
   ```
2. Select exactly one issue and inspect it:
   ```bash
   bd show ISSUE_ID
   bd update ISSUE_ID --claim
   ```
3. Record material findings while working:
   ```bash
   bd comments add ISSUE_ID "Evidence, decision, or handoff detail"
   bd update ISSUE_ID --append-notes "Current state and next step"
   ```
4. Add discovered work with provenance instead of expanding scope silently:
   ```bash
   bd create "Follow-up" --deps discovered-from:ISSUE_ID --description "Why it exists"
   ```
5. Re-run acceptance gates. Close only when the issue outcome is genuinely
   complete:
   ```bash
   bd close ISSUE_ID --reason "Outcome and verification receipt"
   ```
6. Synchronize issue data only when a remote is configured:
   ```bash
   bd dolt remote list
   bd dolt pull
   bd dolt push
   bd vc status
   ```
7. Synchronize source code separately with normal Git commands and repository
   policy.

## Dependencies and hierarchy

- `bd dep add CHILD PARENT --type blocks` creates a readiness blocker.
- `bd create "Child" --parent EPIC_ID` creates hierarchy, not a blocker.
- `related` records an informational relationship.
- `discovered-from` preserves why follow-up work was created.

Check the installed CLI help before relying on a remembered flag:

```bash
bd COMMAND --help
```

## Output

Return a compact receipt containing:

- workspace and Dolt mode;
- issue ID, title, status, and assignee;
- dependency or hierarchy changes;
- evidence added and acceptance gates run;
- close reason when completed;
- Dolt remote pull/push result when synchronization was requested;
- reminder that source-code Git synchronization is a separate workflow when
  source changes were requested.

## Error Handling

- **No workspace:** run `bd where`, then use `bd bootstrap`; offer `bd init` only
  when no remote or prior workspace exists.
- **Unknown `bd sync`:** replace it with explicit `bd dolt pull` or
  `bd dolt push`; the legacy command was removed.
- **Remote divergence:** inspect `bd vc status`, `bd vc log`, and remote settings;
  do not discard either history automatically.
- **Database health failure:** run `bd doctor` and `bd info --json`, then report
  findings before any repair.
- **Claim conflict:** do not overwrite another assignee; select other ready work
  or coordinate explicitly.
- **Push failure:** keep the issue open or in progress, preserve the error, and
  retry only after resolving authentication, connectivity, or divergence.

## Examples

Resume durable work:

```bash
bd prime
bd list --status in_progress
bd show ISSUE_ID
```

Create a dependency-aware task:

```bash
bd create "Verify production receipt" --priority 1 --type task \
  --deps blocks:RELEASE_ID --description "Required before release closure"
```

## Resources

- [Beads storage, remotes, and terminology](references/storage-model.md)
- [Current Beads repository](https://github.com/gastownhall/beads)
- Built-in command truth: `bd --help` and `bd COMMAND --help`
