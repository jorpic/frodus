#!/usr/bin/env python3

import sys
import csv
import json
import logging
import argparse

import lib.data_iterator as data_iterator
from lib.fields import known_fields, name_value


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    stream=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument('--props', type=str, required=True,
                    help='File to save props in TSV format.')
parser.add_argument('--texts', type=str, required=True,
                    help='File to save texts in TSV format.')
parser.add_argument('files', type=str, nargs='+',
                    help='Input data files.')

TEXT_FIELD = 'case_user_document_text_tag'


def main():
    args = parser.parse_args()

    hashes = set()

    with open(args.props, 'w') as props_file:
        with open(args.texts, 'w') as texts_file:
            props_writer = csv.writer(props_file, dialect='tsv')
            texts_writer = csv.writer(texts_file, dialect='tsv')

            for raw_doc, _ in data_iterator.read_docs(args.files):
                doc_id = raw_doc['id']
                if doc_id in hashes:
                    continue

                hashes.add(doc_id)
                doc = build_doc(raw_doc)

                if TEXT_FIELD in doc:
                    jsn = json.dumps(doc[TEXT_FIELD], ensure_ascii=False)
                    texts_writer.writerow([doc_id, jsn])
                    del doc[TEXT_FIELD]

                jsn = json.dumps(doc, ensure_ascii=False)
                props_writer.writerow([doc_id, jsn])


def build_doc(raw_doc):
    doc = {}
    for fld in raw_doc['additionalFields']:
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
