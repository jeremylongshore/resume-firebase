# Beads Storage Model

## Authority

Beads 1.x uses Dolt as its only database backend. Dolt provides SQL tables plus
Git-like database history and merging.

- Embedded mode is the default for a standalone, single-writer workspace.
- Server mode supports multiple concurrent clients through `dolt sql-server`.
- Normal issue writes can create Dolt commits according to the configured
  auto-commit policy.
- `bd vc status`, `bd vc log`, and `bd diff` inspect database history and changes.

SQLite is legacy. `.beads/issues.jsonl` is a passive export for viewers,
interchange, and migration; it is not the source of truth or a full backup.

## Remote synchronization

Use explicit Dolt operations:

```bash
bd dolt remote list
bd dolt pull
bd dolt push
```

When a Git repository is used as the Dolt remote, issue data is stored under
`refs/dolt/data`, separate from `refs/heads/*` and `refs/tags/*`. A normal
`git push` does not replace `bd dolt push`, and a Dolt push does not publish code
commits.

DoltHub is one optional remote-hosting service for a Dolt database. Beads also
supports compatible Git, S3, GCS, and filesystem remotes. “DoltLite” is not a
Beads backend term. A project or product named Freshie is separate from the
Beads storage model unless that project's own architecture explicitly connects
them.

## Initialization and bootstrap

- Use `bd init` for a new workspace.
- Use `bd bootstrap` in a clone that may already have `refs/dolt/data` or another
  configured remote.
- Use `bd init --stealth` when task data must remain locally invisible to Git,
  while recognizing that stealth does not itself create a remote backup.
- Never use reinitialization or remote-discard flags without explicit operator
  authorization and a verified target.

## Credentials

Remote authentication belongs in the supported Git, SSH, cloud, or Dolt
credential mechanism. Never put passwords in a bead, command argument, tracked
file, or skill transcript.

## Authoritative references

- [Beads repository and current storage overview](https://github.com/gastownhall/beads)
- [Dolt architecture and remotes](https://github.com/gastownhall/beads/blob/main/docs/architecture/dolt.md)
- [Dolt backend guide](https://github.com/gastownhall/beads/blob/main/docs/DOLT.md)
