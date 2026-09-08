#!/usr/bin/env bash
# PostToolUse gate: lint Traditional Chinese in files Claude just wrote.
# Exits 2 with the report on stderr so Claude reads it and fixes the file.
# Silent no-op when zhtw-mcp is absent, the path is not prose, the file is
# mostly English (an English doc quoting Chinese), or the file is clean.
set -uo pipefail

PATH="$HOME/.local/bin:$PATH"
command -v zhtw-mcp >/dev/null 2>&1 || exit 0

file=$(python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get("tool_input", {}).get("file_path", ""))
' 2>/dev/null) || exit 0

case "$file" in
  *.md|*.markdown|*.txt) ;;
  *) exit 0 ;;
esac

[ -f "$file" ] || exit 0

# Skip files under 10% CJK: an English document citing Chinese terms trips the
# mixed-script punctuation rules without being Chinese prose.
python3 -c '
import sys
try:
    t = open(sys.argv[1], encoding="utf-8").read()
except Exception:
    sys.exit(1)
cjk = sum(1 for c in t if "一" <= c <= "鿿")
sys.exit(0 if t and cjk / len(t) >= 0.10 else 1)
' "$file" 2>/dev/null || exit 0

report=$(zhtw-mcp lint --max-warnings 0 --max-errors 0 "$file" 2>&1)
[ $? -eq 0 ] && exit 0

printf 'zhtw-mcp gate failed on %s\n\n%s\n\nFix with the zhtw MCP tool (fix_mode: lexical_safe) and write the file again. If a finding is a false positive (a quoted mainland source, a proper noun, a term of art), say so in one line and move on — do not rewrite the same file more than twice for this gate.\n' \
  "$file" "$report" >&2
exit 2
