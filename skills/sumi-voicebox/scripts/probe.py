#!/usr/bin/env python3
"""Read-only local Voicebox model/API metadata. Never downloads or generates."""
import argparse,json,urllib.request

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def probe(port=17493):
    if not isinstance(port,int) or not 1<=port<=65535:raise ValueError('Invalid loopback port')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    result={'url':f'http://127.0.0.1:{port}','status':'unknown_or_not_running','models':[],'generation_or_download_started':False}
    for path in ['/models/status','/openapi.json']:
        try:
            with opener.open(result['url']+path,timeout=2) as response:raw=response.read(2_000_001)
            if len(raw)>2_000_000:raise ValueError('Oversized local metadata')
            data=json.loads(raw)
            if path=='/models/status':
                if not isinstance(data,dict) or not isinstance(data.get('models'),list):raise ValueError('Unknown model schema')
                result['status']='responding'
                result['models']=[{k:x.get(k) for k in ['model_name','display_name','engine','downloaded','loaded','size_mb']} for x in data['models'] if isinstance(x,dict)]
            else:result['documented_paths']=sorted(data.get('paths',{}))
        except (OSError,ValueError,TypeError):result[path]='not_verified'
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=17493);a=p.parse_args()
    try:print(json.dumps(probe(a.port),indent=2))
    except ValueError as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
