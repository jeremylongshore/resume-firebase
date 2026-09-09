# Changelog

## [2.0.0] - 2026-09-09

- Replace obsolete SQLite/JSONL authority claims with the Dolt-backed Beads 1.x
  storage model.
- Replace removed `bd sync`, `bd stats`, and daemon-era guidance with current
  `bd dolt`, `bd status`, and embedded/server workflows.
- Correct the upstream repository from `steveyegge/beads` to
  `gastownhall/beads`.
- Add initialization, remote-divergence, credential, and destructive-operation
  safety boundaries.
- Clarify that DoltHub is an optional Dolt remote host, “DoltLite” is not a Beads
  backend, and Freshie is a separate project concept unless explicitly wired.

## [1.0.0]

- Initial Beads workflow skill.
