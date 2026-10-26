#!/usr/bin/env python3
"""Check self-contained SVG structure; does not certify anatomy or art quality."""
import argparse,json,re
from pathlib import Path
import xml.etree.ElementTree as ET


def check(path):
    raw=path.read_text();errors=[]
    if len(raw)>2_000_000:return ['SVG exceeds2MB inspection budget']
    if re.search(r'<!DOCTYPE|<!ENTITY',raw,re.I):return ['External/entity declarations are not allowed']
    root=ET.fromstring(raw)
    if root.tag!='{http://www.w3.org/2000/svg}svg':errors.append('SVG namespace/root required')
    if not root.get('viewBox'):errors.append('Explicit viewBox required')
    ids=set();references=[]
    for e in root.iter():
        tag=e.tag.split('}')[-1]
        if tag in {'script','foreignObject','image'}:errors.append('No script/HTML/raster embeds: '+tag)
        if e.get('id'):
            if e.get('id') in ids:errors.append('Duplicate layer ID')
            ids.add(e.get('id'))
        for key,value in e.attrib.items():
            k=key.split('}')[-1]
            if k.lower().startswith('on'):errors.append('Event handlers are not allowed')
            if k=='href':
                if not value.startswith('#'):errors.append('External href is not allowed')
                else:references.append(value[1:])
            for target in re.findall(r'url\(([^)]+)\)',value):
                target=target.strip('\"\' ')
                if not target.startswith('#'):errors.append('External URL paint is not allowed')
                else:references.append(target[1:])
        if tag=='style' and re.search(r'@import|@font-face|https?://|data:',e.text or '',re.I):errors.append('External/embedded CSS dependency')
    for target in references:
        if target not in ids:errors.append('Missing local SVG reference: '+target)
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('svg',type=Path);a=p.parse_args()
    try:errors=check(a.svg)
    except (OSError,ET.ParseError) as e:p.exit(2,f'Cannot inspect SVG: {e}\n')
    print(json.dumps({'ok':not errors,'errors':errors,'limit':'Structure/self-containment only; visually inspect complete scene, anatomy, contact and motion.'},indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
