"""Serve only this delivery folder on loopback, with seeking and real downloads."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
import re

ROOT = Path(__file__).resolve().parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_head(self):
        self.byte_range = None
        path = Path(self.translate_path(self.path)).resolve()
        if not path.is_relative_to(ROOT):
            self.send_error(403)
            return None
        if not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        start, end = 0, size - 1
        request_range = self.headers.get('Range')
        if request_range:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', request_range)
            if not match or not any(match.groups()) or size == 0:
                self.send_error(416)
                return None
            if match[1]:
                start = int(match[1])
                end = min(int(match[2]) if match[2] else size - 1, size - 1)
            else:
                start = max(0, size - int(match[2]))
            if start > end or start >= size:
                self.send_error(416)
                return None
            self.byte_range = (start, end)
        file = path.open('rb')
        file.seek(start)
        self.send_response(206 if request_range else 200)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Content-Length', str(max(0, end - start + 1)))
        if request_range:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        if parse_qs(urlsplit(self.path).query).get('download') == ['1']:
            name = re.sub(r'[^A-Za-z0-9._-]', '_', path.name)
            self.send_header('Content-Disposition', f'attachment; filename="{name}"')
        self.end_headers()
        return file

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def copyfile(self, source, output):
        if self.byte_range is None:
            return super().copyfile(source, output)
        remaining = self.byte_range[1] - self.byte_range[0] + 1
        while remaining:
            block = source.read(min(65536, remaining))
            if not block:
                break
            output.write(block)
            remaining -= len(block)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4260)
    args = parser.parse_args()
    print(f'Beyondsumi: http://127.0.0.1:{args.port}/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
