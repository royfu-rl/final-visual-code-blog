#!/usr/bin/env python3
"""博客的静态服务 + 划词备注接口。

正文只放结论，长解释挂在备注里：页面上划词 → 写备注 → 存进 data/notes.json。
用别的静态服务打开时页面只读（用 build 时嵌进去的那份备注）。

    GET  /api/notes                                      → {"notes": [...]}
    POST /api/notes  {"op": "add" | "update" | "delete", "note": {...}}

    python3 scripts/serve_notes.py --port 8977
"""
import argparse
import json
import os
import threading
import time
import uuid
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES = os.path.join(ROOT, 'data', 'notes.json')
FIELDS = ('doc', 'view', 'quote', 'prefix', 'suffix', 'body')
LOCK = threading.Lock()


def load():
    try:
        return json.load(open(NOTES, encoding='utf-8'))['notes']
    except FileNotFoundError:
        return []


def save(notes):
    tmp = NOTES + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({'notes': notes}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, NOTES)


def apply(op, note):
    notes = load()
    now = time.strftime('%Y-%m-%d %H:%M')
    if op == 'add':
        notes.append({**{k: str(note.get(k, '')) for k in FIELDS}, 'id': uuid.uuid4().hex[:8], 'ts': now})
    elif op == 'update':
        for n in notes:
            if n['id'] == note.get('id'):
                n.update(body=str(note.get('body', '')), ts=now)
    elif op == 'delete':
        notes = [n for n in notes if n['id'] != note.get('id')]
    else:
        raise ValueError(f'unknown op: {op}')
    save(notes)
    return notes


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        # 重新 build 后刷新即见新页面
        if self.path.split('?')[0].endswith(('.html', '/')):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def reply(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split('?')[0] == '/api/notes':
            return self.reply(200, {'notes': load()})
        super().do_GET()

    def do_POST(self):
        if self.path.split('?')[0] != '/api/notes':
            return self.reply(404, {'error': 'not found'})
        size = int(self.headers.get('Content-Length') or 0)
        if size > 1 << 20:
            return self.reply(413, {'error': 'too large'})
        try:
            req = json.loads(self.rfile.read(size))
            with LOCK:
                notes = apply(req.get('op'), req.get('note') or {})
        except ValueError as e:
            return self.reply(400, {'error': str(e)})
        self.reply(200, {'notes': notes})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8977)
    a = ap.parse_args()
    srv = ThreadingHTTPServer(('127.0.0.1', a.port), partial(Handler, directory=ROOT))
    print(f'serving {ROOT} on :{a.port}  (notes → {NOTES})', flush=True)
    srv.serve_forever()


if __name__ == '__main__':
    main()

