#!/usr/bin/env python3

import sys
import orjson

def dump(stash):
    for key in stash:
        with open(f'{key}.jsonl', 'a') as file:
            for ln in stash[key]:
                print(ln, file=file)
        stash[key].clear()

key_name = sys.argv[1]
stash = {}

for ln in sys.stdin:
    obj = orjson.loads(ln)
    key = obj[key_name]
    stash.setdefault(key, []).append(ln)
    if len(stash[key]) > 16:
        dump(stash)

dump(stash)
