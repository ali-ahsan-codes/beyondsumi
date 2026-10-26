#!/usr/bin/env python3
"""Serve only Sumi's portable lab/references locally; no installation or network upload."""
import argparse, functools, http.server
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=4198);a=p.parse_args()
root=Path(__file__).resolve().parents[1]
server=http.server.ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root)))
print(f'Open in Chrome: http://127.0.0.1:{a.port}/assets/director-lab/',flush=True)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
