## Retrieval routing

Choose the tool by the evidence needed, not a fixed pipeline. If the file or
range is already known, read it directly rather than repeating discovery.

| Question or clue | Preferred operation |
| --- | --- |
| Known identifier, literal, filename, or path | Scoped `rg`, then read the relevant range |
| Unknown feature, intent, or business behavior | On an approved repository, prefer mgrep to find candidates; do not first cycle through guessed grep terms |
| Syntax shape, repeated call pattern, or repeated codemod | `ast-grep` when the language/parser is available |
| Symbol identity, definition, references, type, or diagnostics | An actual LSP client/tool for the candidate's language |
| Security pattern, policy violation, or source-to-sink question | Local Semgrep CE with an explicit local rule; CE analysis does not establish cross-file taint coverage |

Read current source to validate candidates. Text matches are not semantic
references; mgrep relevance is not proof of behavior. Use Git history/diff for
questions about when behavior changed. Edit single sites with the normal editor;
use structural codemods for repeated shapes, then inspect the diff and run the
project's relevant tests/type-check/lint (plus Semgrep when relevant).

Each search should answer a specific missing question. Narrow noisy results by
directory, file type, or structure. Stop when evidence is sufficient; switch
tools when the remaining question calls for different evidence. Do not repeat
broad grep scans or force every tool into every task.

### mgrep eligibility

Remote indexing is opt-in per repository. Approval must come from the user;
record it in that repository's agent instructions, identifying the repository,
allowed directories, and permission for remote indexing/data handling. An agent
must not grant itself approval. Within that scope, use on-demand semantic
queries without asking again. Existing indexing or a public repository alone is
not approval. Check the index/store belongs to the approved scope and is usable;
if synchronization is needed, stay within that same approved scope.

Never automatically enable the mgrep plugin/MCP, start `mgrep watch`, or index
adjacent repositories. Missing approval, an unusable/stale index, or a failed
query requires a disclosed fallback to local filenames/directories and scoped
keyword search. Empty semantic output does not establish absence. Recheck
candidate snippets against current local source.

### Local Semgrep

Use `semgrep scan --oss-only --metrics off --config <approved-local-rule>`.
Do not use `--config auto`, log in to Cloud, or register a Semgrep MCP without
explicit authorization. Set `SEMGREP_ENABLE_VERSION_CHECK=0` and put
logs/settings/temp files in dedicated writable scratch space. On macOS, if TLS
verification fails, use `SSL_CERT_FILE=/etc/ssl/cert.pem` when that bundle exists.
Never disable TLS verification or relax source permissions to run a scan.
Findings and clean results are limited by the rules, language, and CE engine.

## LSP navigation

- Discover exposed LSP tools (including deferred tools or a built-in client)
  before declaring LSP unavailable. Native server installation alone is not a
  client connection.
- Locate a candidate with scoped lexical, semantic, or structural search unless
  its position is already known. Use definition/references/hover/diagnostics for
  the remaining semantic question. Read the tool's coordinate convention; this
  bridge uses 1-based UTF-8 byte columns, which are not editor display columns.
- Empty or partial output does not prove absence. Results cover the server's
  project model, not necessarily a whole monorepo. Disclose unsupported features,
  initialization failures, and incomplete coverage; supplement with scoped
  lexical inspection and project-native verification.
- Keep queries read-only and make edits with normal editor tools. Instances
  start their native server on first use and retain their startup workspace;
  start a new session when switching projects. Kotlin and Xcode project support
  remain limited. Native servers are not sandboxed by the bridge.
