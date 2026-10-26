from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def send_head(self):
  self.byte_range=None
  path=Path(self.translate_path(self.path))
  if path.is_file() and self.headers.get('Range'):
   size=path.stat().st_size;m=re.fullmatch(r'bytes=(\d*)-(\d*)',self.headers['Range'])
   if not m:return super().send_head()
   if m[1]:start=int(m[1]);end=min(int(m[2]) if m[2] else size-1,size-1)
   else:start=max(0,size-int(m[2]));end=size-1
   if start>=size or start>end:self.send_error(416);return None
   f=path.open('rb');f.seek(start);self.byte_range=(start,end)
   self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Content-Length',str(end-start+1));self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Accept-Ranges','bytes');self.end_headers();return f
  return super().send_head()
 def end_headers(self):
  self.send_header('Accept-Ranges','bytes');self.send_header('Cache-Control','no-cache');super().end_headers()
 def copyfile(self,src,dst):
  if self.byte_range:
   remaining=self.byte_range[1]-self.byte_range[0]+1
   while remaining:
    data=src.read(min(65536,remaining))
    if not data:break
    dst.write(data);remaining-=len(data)
  else:super().copyfile(src,dst)
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4183);args=parser.parse_args()
 print(f'Film player: http://localhost:{args.port}/',flush=True)
 ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
