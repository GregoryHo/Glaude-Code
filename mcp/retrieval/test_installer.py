import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import installer as i
import sync_policy


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='retrieval test ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_server_map_is_local_to_each_machine(self):
        for prefix in ('opt/homebrew','usr/local'):
            tools = {}
            for name in ('node','typescript-language-server','tsc','pyright-langserver'):
                p = self.root/prefix/'bin'/name
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text('#!/usr/bin/env node\n')
                p.chmod(0o755)
                tools[name] = str(p)
            with patch.object(i,'resolve_binary',side_effect=tools.get), patch.object(i,'output',return_value=None):
                found,missing=i.discover()
            self.assertEqual(found['typescript']['command'],tools['node'])
            self.assertEqual(found['typescript']['args'],[tools['typescript-language-server'],'--stdio'])
            self.assertEqual(found['python']['command'],tools['node'])
            self.assertIn('swift',missing)

    def test_missing_node_is_explicit(self):
        server=self.root/'pyright-langserver'
        server.write_text('#!/usr/bin/env node\n')
        with patch.object(i,'resolve_binary',side_effect=lambda n:str(server) if n=='pyright-langserver' else None), patch.object(i,'output',return_value=None):
            found,missing=i.discover()
        self.assertNotIn('python',found)
        self.assertIn('Node.js',missing['python'])

    def test_rustup_proxy_resolves_actual_toolchain(self):
        actual=self.root/'toolchain/rust-analyzer'
        actual.parent.mkdir()
        actual.write_text('binary')
        actual.chmod(0o755)
        proxy=self.root/'rust-analyzer'
        proxy.symlink_to(self.root/'rustup')
        (self.root/'rustup').touch()
        with patch.object(i.shutil,'which',return_value=str(proxy)), patch.object(i,'output',return_value=str(actual)):
            self.assertEqual(i.resolve_binary('rust-analyzer'),str(actual.resolve()))

    def test_missing_and_ambiguous_language_selection(self):
        self.assertEqual(i.selected_languages(None,{'python':{}}),['python'])
        self.assertEqual(i.selected_languages('typescript,python',{}),['typescript','python'])
        with self.assertRaises(ValueError):
            i.selected_languages(None,{})
        with self.assertRaises(ValueError):
            i.selected_languages('javascript',{})

    def test_toml_merge_preserves_unrelated_tables_and_comments(self):
        original=('# existing comment\nmodel="sample"\n[mcp_servers.other]\ncommand="keep"\n'
                  '[mcp_servers."lsp_python"]\ncommand="old"\n'
                  '[mcp_servers.lsp_python.env]\nSAMPLE="value"\n'
                  '[projects."/a path"]\ntrust_level="trusted"\n')
        entries={'lsp_python':{'command':'/a path/python','args':['--stdio'],'enabled':True}}
        result=i.merge_codex(original,entries)
        expected=tomllib.loads(original)
        expected['mcp_servers'].update(entries)
        self.assertEqual(tomllib.loads(result),expected)
        self.assertIn('# existing comment',result)
        self.assertEqual(i.merge_codex(result,entries),result)

    def test_toml_unrecognized_layout_fails_before_writing(self):
        with self.assertRaises(ValueError):
            i.merge_codex('mcp_servers = {lsp_python = {command="old"}}\n',
                          {'lsp_python':{'command':'new'}})

    def test_conflicts_noninteractive_and_yes(self):
        old={'lsp_python':{'command':'old','env':{'PASSWORD':'do-not-print'}}}
        new={'lsp_python':{'command':'new','args':[]}}
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured), patch('sys.stdin.isatty',return_value=False):
            with self.assertRaises(ValueError):
                i.approve_conflicts(old,new,False)
            i.approve_conflicts(old,new,True)
        self.assertNotIn('do-not-print',captured.getvalue())

    def test_atomic_backup_noop_and_concurrent_change(self):
        p=self.root/'settings.json'
        p.write_text('old')
        i.atomic_write(p,'new',expected='old')
        backups=list((self.root/'.retrieval-backups').iterdir())
        self.assertEqual(backups[0].read_text(),'old')
        self.assertEqual(backups[0].stat().st_mode & 0o777,0o600)
        i.atomic_write(p,'new',expected='new')
        self.assertEqual(len(list((self.root/'.retrieval-backups').iterdir())),1)
        with self.assertRaises(ValueError):
            i.atomic_write(p,'overwrite',expected='stale')
        self.assertEqual(p.read_text(),'new')

    def test_configuration_is_idempotent_and_preserves_other_settings(self):
        home=self.root/'another user'
        home.mkdir()
        (home/'.claude').mkdir()
        (home/'.claude.json').write_text(json.dumps({'projects':{'keep':{}},'mcpServers':{'other':{'command':'keep'}}}))
        (home/'.claude/settings.json').write_text(json.dumps({'hooks':{'SessionStart':[]},'permissions':{'allow':['Read']}}))
        receipt={'release':str(self.root/'install with spaces'),'languages':['typescript','python'],
                 'python':str(self.root/'python3')}
        args=argparse.Namespace(root=self.root,host='both',languages=None,yes=False,dry_run=False)
        with patch.object(i,'read_receipt',return_value=receipt):
            i.configure(args,home)
            paths=[home/'.claude.json',home/'.claude/settings.json',home/'.codex/config.toml']
            before=[p.read_bytes() for p in paths]
            i.configure(args,home)
        self.assertEqual(before,[p.read_bytes() for p in paths])
        claude=json.loads(paths[0].read_text())
        self.assertEqual(claude['mcpServers']['other'],{'command':'keep'})
        self.assertEqual(claude['projects'],{'keep':{}})
        settings=json.loads(paths[1].read_text())
        self.assertEqual(settings['hooks'],{'SessionStart':[]})
        self.assertIn('Read',settings['permissions']['allow'])
        self.assertFalse(settings['enabledPlugins']['mgrep@Mixedbread-Grep'])
        self.assertEqual(len(settings['permissions']['deny']),8)
        codex=tomllib.loads(paths[2].read_text())
        self.assertEqual(codex['mcp_servers']['lsp_python']['enabled_tools'],list(i.TOOLS))
        self.assertNotIn('cwd',codex['mcp_servers']['lsp_python'])

    def test_dry_run_writes_nothing(self):
        args=argparse.Namespace(root=self.root,host='both',languages=None,yes=False,dry_run=True)
        receipt={'release':str(self.root/'install'),'languages':['python'],'python':'/python'}
        home=self.root/'not-created'
        with patch.object(i,'read_receipt',return_value=receipt):
            i.configure(args,home)
        self.assertFalse(home.exists())

    def test_install_fixed_revision_repeat_and_bad_fetch(self):
        source=self.root/'installer-source'
        source.mkdir()
        commit='a'*40
        (source/'manifest.json').write_text(json.dumps({'version':'0.2.0',
            'bridge_repository':'https://example.invalid/bridge.git','bridge_commit':commit}))
        (source/'launch.py').write_text('launcher\n')
        tool=self.root/'native-server'
        tool.write_text('#!/bin/sh\nexit 0\n')
        tool.chmod(0o755)
        detected={'python':{'command':str(tool),'args':['--stdio']}}
        args=argparse.Namespace(root=self.root/'installed',languages='python',
                                install_missing=False,source=None)
        calls=[]
        def fake_run(argv,**kwargs):
            calls.append([str(x) for x in argv])
            if argv[:2]==['go','build']:
                Path(argv[argv.index('-o')+1]).write_text('#!/bin/sh\necho --lazy\n')
                Path(argv[argv.index('-o')+1]).chmod(0o755)
        def fake_output(argv,**kwargs):
            return commit if 'rev-parse' in argv else 'test-version'
        with patch.object(i,'HERE',source), patch.object(i.platform,'system',return_value='Darwin'), \
             patch.object(i,'discover',return_value=(detected,{})), \
             patch.object(i.shutil,'which',return_value='/tool'), \
             patch.object(i,'run',side_effect=fake_run), patch.object(i,'output',side_effect=fake_output):
            i.install(args)
            first=i.read_receipt(args.root)
            i.install(args)
            self.assertEqual(i.read_receipt(args.root)['release'],first['release'])
            self.assertTrue(any('fetch' in c and c[-1]==commit for c in calls))
            self.assertEqual(first['bridge_commit'],commit)
            with patch.object(i,'output',return_value='b'*40):
                with self.assertRaisesRegex(ValueError,'revision mismatch'):
                    i.install(args)

    def test_missing_selected_dependency_does_not_fetch_or_write(self):
        source=self.root/'source'
        source.mkdir()
        (source/'manifest.json').write_text(json.dumps({'bridge_commit':'a'*40}))
        args=argparse.Namespace(root=self.root/'not-created',languages='python',
                                install_missing=False,source=None)
        with patch.object(i,'HERE',source), patch.object(i.platform,'system',return_value='Darwin'), \
             patch.object(i,'discover',return_value=({}, {'python':'pyright-langserver missing'})), \
             patch.object(i,'run') as execute:
            with self.assertRaisesRegex(ValueError,'dependencies are missing'):
                i.install(args)
        execute.assert_not_called()
        self.assertFalse(args.root.exists())

    def test_doctor_reads_only(self):
        args=argparse.Namespace(root=self.root,languages=None)
        with patch.object(i,'discover',return_value=({'python':{}},{n:'not found' for n in i.LANGUAGES if n!='python'})), contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(i.doctor(args),1)
        self.assertIn('not found',stream.getvalue())
        self.assertFalse((self.root/'installation.json').exists())

    def test_policy_replaces_duplicates_preserving_other_sections(self):
        original='# Other\nkeep\n## Retrieval routing\nold\n## LSP navigation\nold\n## LSP navigation\nold2\n## Unrelated\nkeep2\n'
        policy=(Path(__file__).parent/'ROUTING.md').read_text()
        result=sync_policy.replace_policy(original,policy)
        self.assertEqual(result.count('## LSP navigation'),1)
        self.assertTrue(result.endswith('## Unrelated\nkeep2\n'))
        self.assertEqual(sync_policy.replace_policy(result,policy),result)


if __name__=='__main__':
    unittest.main()
