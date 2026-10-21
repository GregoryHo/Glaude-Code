"""Keep the shared policy in the two host instruction files without other edits."""
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
POLICY = Path(__file__).with_name('ROUTING.md')


def replace_policy(text, policy):
    # Replace only the routing and adjoining LSP sections; preserve other content.
    start = text.find('## Retrieval routing\n')
    if start < 0:
        return text.rstrip() + '\n\n' + policy
    tail = text[start:]
    headings = list(re.finditer(r'^## (.+)$', tail, re.M))
    end = next((m.start() for m in headings[1:]
                if m.group(1) != 'LSP navigation'), len(tail))
    return text[:start] + policy + ('\n' if end < len(tail) else '') + tail[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--deploy', action='store_true', help='Also sync live user instructions')
    args = parser.parse_args()
    paths = [ROOT/'core/CLAUDE.md', ROOT/'core/codex/AGENTS.md']
    if args.deploy:
        paths += [Path.home()/'.claude/CLAUDE.md', Path.home()/'.codex/AGENTS.md']
    mismatches = []
    for path in paths:
        original = path.read_text()
        updated = replace_policy(original, POLICY.read_text())
        if original != updated:
            if args.write:
                path.write_text(updated)
                print(f'Updated routing: {path}')
            else:
                mismatches.append(str(path))
    if mismatches:
        raise SystemExit('Routing differs; run sync_policy.py --write: ' + ', '.join(mismatches))


if __name__ == '__main__':
    main()
