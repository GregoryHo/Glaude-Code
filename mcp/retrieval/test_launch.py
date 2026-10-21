import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from launch import LANGUAGES, language_for, plan, workspace


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='retrieval-launcher-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'project with spaces'
        self.root.mkdir()
        self.tool = self.base / 'fake-tool'
        self.tool.write_text('#!/bin/sh\nexit 0\n')
        self.tool.chmod(0o700)
        self.config = {'bridge': str(self.tool), 'servers': {
            name: {'command': str(self.tool), 'args': ['--stdio']} for name in LANGUAGES}}

    def test_codex_uses_exact_cwd_not_claude_env(self):
        self.assertEqual(workspace(None, 'codex', self.root, {'CLAUDE_PROJECT_DIR': '/wrong'})[0], self.root)

    def test_claude_prefers_project_env(self):
        self.assertEqual(workspace(None, 'claude', Path('/'), {'CLAUDE_PROJECT_DIR': str(self.root)})[0], self.root)

    def test_claude_missing_env_fails(self):
        with self.assertRaisesRegex(ValueError, 'did not provide'):
            workspace(None, 'claude', self.root, {})

    def test_explicit_wins(self):
        self.assertEqual(workspace(str(self.root), 'claude', Path('/'), {})[1], 'explicit')

    def test_reject_broad_or_relative_root(self):
        for value in ('/', str(Path.home()), 'relative'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                workspace(value, 'codex', self.root, {})

    def test_symlink_canonicalized(self):
        link = self.base / 'alias'
        link.symlink_to(self.root, target_is_directory=True)
        self.assertEqual(workspace(str(link), 'codex', self.root, {})[0], self.root)

    def test_no_parent_escalation(self):
        (self.base / '.git').mkdir()
        self.assertEqual(workspace(None, 'codex', self.root, {})[0], self.root)

    def test_auto_single_family(self):
        (self.root / 'package.json').write_text('{}\n')
        self.assertEqual(language_for(self.root, 'auto'), 'typescript')

    def test_auto_unknown_or_ambiguous(self):
        with self.assertRaises(ValueError):
            language_for(self.root, 'auto')
        (self.root / 'package.json').write_text('{}\n')
        (self.root / 'Cargo.toml').write_text('\n')
        with self.assertRaises(ValueError):
            language_for(self.root, 'auto')

    def test_all_explicit_families_and_argv(self):
        for name in LANGUAGES:
            result = plan(self.config, self.root, language_for(self.root, name), 'explicit')
            self.assertEqual(result['argv'], [str(self.tool), '--workspace', str(self.root),
                                             '--lsp', str(self.tool), '--', '--stdio'])

    def test_reject_project_executable_and_symlink(self):
        tool = self.root / 'untrusted'
        tool.write_text('#!/bin/sh\n')
        tool.chmod(0o700)
        alias = self.base / 'outside-alias'
        alias.symlink_to(tool)
        for value in (tool, alias):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'target workspace'):
                plan({**self.config, 'bridge': str(value)}, self.root, 'python', 'explicit')

    def test_lazy_is_opt_in_and_precedes_lsp_separator(self):
        eager = plan(self.config, self.root, 'python', 'explicit')
        lazy = plan(self.config, self.root, 'python', 'explicit', lazy=True)
        self.assertNotIn('--lazy', eager['argv'])
        self.assertEqual(lazy['argv'][-3:], ['--lazy', '--', '--stdio'])

    def test_invalid_server(self):
        for entry in ({}, {'command': 'python'}, {'command': str(self.tool), 'args': 'shell command'}):
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                plan({**self.config, 'servers': {'python': entry}}, self.root, 'python', 'explicit')

    def test_dry_run_does_not_execute(self):
        self.tool.write_text('#!/bin/sh\nexit 99\n')
        config_path = self.base / 'servers.json'
        config_path.write_text(json.dumps(self.config))
        args = [sys.executable, str(Path(__file__).with_name('launch.py')), '--host', 'codex',
                '--language', 'python', '--config', str(config_path)]
        dry = subprocess.run([*args, '--dry-run'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual(json.loads(dry.stdout)['workspace'], str(self.root))
        real = subprocess.run(args, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(real.returncode, 99)
        self.assertEqual(real.stdout, '')

    def test_cross_workspace_plans_do_not_share_roots(self):
        other = self.base / 'second'
        other.mkdir()
        one = plan(self.config, self.root, 'typescript', 'process-cwd')
        two = plan(self.config, other, 'typescript', 'process-cwd')
        self.assertNotEqual(one['workspace'], two['workspace'])


if __name__ == '__main__':
    unittest.main()
