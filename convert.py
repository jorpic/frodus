#!/usr/bin/env python3

import os
import sys
import csv
import json
import yaml
import tarfile
import logging
import argparse

import lib.data_iterator as data_iterator
from lib.fields import known_fields, name_value


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    stream=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument('--format', type=str, choices=['yaml', 'tsv'],
                    default='yaml',
                    help='Output format. Default is "yaml".')
group = parser.add_mutually_exclusive_group()
group.add_argument('--except', type=str, dest='except_',
                    help='Comma-separated list of fields to exclude.')
group.add_argument('--only', type=str,
                    help='Comma-separated list of fields to include.')
parser.add_argument('files', type=str, nargs='+',
                    help='Input data files.')


def main():
    args = parser.parse_args()

    fields = known_fields.keys()
    if args.except_:
        except_fields = args.except_.split(',')
        fields = set(filter(lambda f: f not in except_fields, fields))
    elif args.only:
        only_fields = args.only.split(',')
        fields = set(filter(lambda f: f in only_fields, fields))

    if args.format == 'yaml':
        for raw_doc, _  in data_iterator.read_docs(args.files):
            doc = build_doc(raw_doc, fields)
            doc = {raw_doc['id']: doc}
            yaml.dump(
                doc,
                sys.stdout,
                allow_unicode=True,
                Dumper=yaml.CDumper)

    elif args.format == 'tsv':
        tsv_writer = csv.writer(sys.stdout, dialect='tsv')
        for raw_doc, _ in data_iterator.read_docs(args.files):
            doc = build_doc(raw_doc, fields)
            jsn = json.dumps(doc, ensure_ascii=False)
            tsv_writer.writerow([raw_doc['id'], jsn])


def build_doc(raw_doc, fields_to_extract):
    doc = {}
    for fld in raw_doc['additionalFields']:
        if fld['name'] in fields_to_extract:
            (name, val) = name_value(fld)
            spec = known_fields[name]
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

class tsv(csv.Dialect):
    delimiter = '\t'
    quotechar = "'"
    doublequote = True
    escapechar = '\\'
    skipinitialspace = True
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE

csv.register_dialect('tsv', tsv)


if __name__ == '__main__':
    main()
