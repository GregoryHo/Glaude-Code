# Validation — 2026-10-21

Fixed-source installation and direct MCP checks passed locally. Second-Mac
acceptance is still pending access to that machine.

Pinned source: `69d8aaa8c9ddb1301dcffef7f1677f205167b3e1`, available in the
GregoryHo fork on `feat/position-based-lsp-tools`.

| Check | Observed result |
| --- | --- |
| Installer and imported launcher tests | 29 passed |
| Policy synchronization | Repository Claude/Codex templates and live user instruction sections match ROUTING.md |
| Shell / Python / JSON validation | Passed |
| Bridge root/internal tests and Go vet | Passed |
| Bridge root/LSP/tools race tests | Passed before the version-only metadata change |
| TypeScript saved-file synchronization integration test | Passed |
| Native executable/launcher plans | All six families resolved on this Apple Silicon Mac |
| Actual installed MCP definition queries | TypeScript L1:C1–L1:C60 and Python L1:C1–L2:C21 matched; server reports 0.2.0 |
| Fixed-SHA fetch/build/install and repeated install | Passed using the committed local source and then GitHub; repeated install reused matching artifacts |
| Live host configure dry run | Parsed and planned both existing configurations successfully; runtime host settings were not replaced |
| Second Mac / Intel hardware | Not run |

The candidate probe and pinned-source installer used temporary installation and
fixture directories. Live instruction sections were synchronized, but runtime
LSP configuration was not replaced. Local evidence is retained in the handover
evaluation directory `evaluation/mac-install-20261021/`; paths/logs stay local.

The bridge commit retains the existing SSH signature; no signing setting or
commit hook was bypassed. On the second Mac run doctor/install/configure and the
same two definition checks; do not repeat a seven-language benchmark. The local
checks establish installation/MCP plumbing, not fresh model-driven routing or
complete seven-language semantic compatibility.
