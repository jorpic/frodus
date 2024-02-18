#!/usr/bin/env python3

import sys
import json
import yaml


def main():
    with open(sys.argv[1]) as f:
        global known_fields
        known_fields = yaml.safe_load(f)

    for ln in sys.stdin:
        jsn = json.loads(ln)
        for raw_doc in jsn['searchResult']['documents']:
            doc = build_doc(raw_doc)
            doc['id'] = raw_doc['id']
            print(json.dumps(doc, ensure_ascii=False))


def field_info(fld):
    name = fld['name']
    spec = known_fields[name]
    val = fld[spec.get('value', 'value')]
    if isinstance(val, str):
        val = val.strip()
    return (name, val, spec)


def build_doc(raw_doc):
    doc = {}
    for fld in raw_doc['additionalFields']:
        (name, val, spec) = field_info(fld)
        skip = 'skip' in spec or 'duplicate' in spec or 'const' in spec
        if not skip:
            if 'isArray' not in spec:
                doc[name] = val
            else:
                if name in doc:
                    doc[name].append(val)
                else:
                    doc[name] = [val]
    return doc



if __name__ == '__main__':
    main()
