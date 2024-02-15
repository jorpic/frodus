#!/usr/bin/env python3

import sys
import json

seen = {}

for ln in sys.stdin:
    js = json.loads(ln)
    id = js['id']
    hs = hash(js.get('case_user_document_text_tag'))

    if id in seen:
        print('duplicate:', id, file=sys.stderr)
        if hs not in seen[id]:
            print('new text:', hs, file=sys.stderr)
            seen[id].append(hs)
    else:
        seen[id] = [hs]
        print(ln)
