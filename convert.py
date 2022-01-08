#!/usr/bin/env python3

import os
import sys
import csv
import json
import yaml
import tarfile
import logging
import argparse

import data_iterator
from fields import known_fields, name_value


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    stream=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument('--format', type=str, choices=['yaml', 'psql-tsv'],
                    default='yaml',
                    help='Output format. Default is "yaml".')
group = parser.add_mutually_exclusive_group()
group.add_argument('--except', type=str, dest='except_',
                    help='Comma-separated list of fields to exclude.')
group.add_argument('--only', type=str,
                    help='Comma-separated list of fields to include.')


def main():
    args = parser.parse_args()

    fields = known_fields.keys()
    if args.except_:
        except_fields = args.except_.split(',')
        fields = set(filter(lambda f: f not in except_fields, fields))
    if args.only:
        only_fields = args.only.split(',')
        fields = set(filter(lambda f: f in only_fields, fields))

    files = sys.stdin.readlines()

    if args.format == 'yaml':
        for raw_doc in data_iterator.read_docs(files):
            doc = build_doc(raw_doc, fields)
            dump_yaml({raw_doc['id']: doc}, sys.stdout)
    elif args.format == 'psql-tsv':
        tsv_writer = csv.writer(sys.stdout, dialect='tsv')
        for raw_doc in data_iterator.read_docs(files):
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


def dump_yaml(doc, file):
    yaml_str = yaml.safe_dump(doc, allow_unicode=True)
    file.write(yaml_str)


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
