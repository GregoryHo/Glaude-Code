"""Two real MCP/LSP definition checks; no model calls or host config writes."""
import argparse
import json
import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import tempfile
import threading

from installer import DEFAULT_ROOT, host_entries, read_receipt


def query(entry, workspace, language):
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen([entry['command'], *entry['args']], cwd=workspace,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=errors, start_new_session=True)
        messages = queue.Queue()
        def receive():
            for line in process.stdout:
                messages.put(line)
            messages.put(None)
        reader = threading.Thread(target=receive, daemon=True)
        reader.start()
        def send(message):
            process.stdin.write((json.dumps(message)+'\n').encode())
            process.stdin.flush()
        def response(identifier):
            while True:
                line = messages.get(timeout=100)
                if line is None:
                    errors.seek(0)
                    raise RuntimeError('Bridge exited: '+errors.read().decode(errors='replace')[-2000:])
                value = json.loads(line)
                if value.get('id') == identifier:
                    if 'error' in value:
                        raise RuntimeError(str(value['error']))
                    return value['result']
        try:
            send({'jsonrpc':'2.0','id':1,'method':'initialize','params':{
                'protocolVersion':'2024-11-05','capabilities':{},
                'clientInfo':{'name':'retrieval-smoke','version':'0.2.0'}}})
            init = response(1)
            send({'jsonrpc':'2.0','method':'notifications/initialized'})
            file,line,column,span = (('main.ts',2,16,'L1:C1 - L1:C60') if language=='typescript'
                                     else ('main.py',3,10,'L1:C1 - L2:C21'))
            send({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{
                'name':'definition_at','arguments':{'filePath':file,'line':line,'column':column}}})
            result = response(2)
            text = '\n'.join(c.get('text','') for c in result.get('content',[]))
            if result.get('isError') or str(workspace/file) not in text or span not in text:
                raise RuntimeError(f'{language} returned unexpected definition: {text}')
            return {'language':language,'status':'passed','server':init['serverInfo'],
                    'definition':text,'arguments':{'filePath':file,'line':line,'column':column}}
        finally:
            process.stdin.close()
            try:
                process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL)
                    process.wait()
            reader.join(timeout=2)
            process.stdout.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=DEFAULT_ROOT)
    parser.add_argument('--keep-fixture',action='store_true')
    args=parser.parse_args()
    receipt=read_receipt(args.root.expanduser().resolve())
    if not {'typescript','python'} <= set(receipt['languages']):
        raise SystemExit('Install typescript and python first')
    workspace=Path(tempfile.mkdtemp(prefix='retrieval-fixture-')).resolve()
    try:
        (workspace/'main.ts').write_text('export function double(value: number) { return value * 2; }\nconst result = double(3);\n')
        (workspace/'main.py').write_text('def double(value: int) -> int:\n    return value * 2\nresult = double(3)\n')
        (workspace/'tsconfig.json').write_text('{"compilerOptions":{"strict":true},"include":["*.ts"]}\n')
        (workspace/'pyrightconfig.json').write_text('{"include":["main.py"]}\n')
        entries=host_entries(receipt,'codex',['typescript','python'])
        results=[query(entries['lsp_'+language],workspace,language) for language in ('typescript','python')]
        print(json.dumps({'bridge_commit':receipt['bridge_commit'],'workspace':str(workspace),
                          'fixture_retained':args.keep_fixture,'results':results},indent=2))
    finally:
        if not args.keep_fixture:
            shutil.rmtree(workspace)


if __name__=='__main__':
    main()
