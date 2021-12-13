#!/usr/bin/env python3

import os
import sys
import json
import yaml
import textwrap
import tarfile
import logging

from fields import known_fields, name_value


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename='scan.log')


def main():
    files = sys.stdin.readlines()

    dictionaries = {k: set()
        for k,v in known_fields.items()
        if 'isDictionary' in v}

    count = 0
    count_texts = 0

    for archive in files:
        archive = archive.strip()
        logging.info(f'reading {archive}')
        with tarfile.open(archive, 'r|bz2') as tar:
            for json_file in tar:
                with tar.extractfile(json_file) as json_text:
                    jsn = json.load(json_text)
                    res = jsn['searchResult']

                    for raw_doc in res['documents']:
                        doc = build_doc(raw_doc)
                        count += 1
                        if 'case_user_document_text_tag' in doc:
                            count_texts += 1
                        check_duplicate_fields(doc)
                        if check_for_double_doc(raw_doc):
                            check_array_fields(raw_doc)
                        build_dictionaries(raw_doc, dictionaries)

    logging.info(f'{count} docs scanned')
    logging.info(f'{count_texts} texts found')
    dump_dictionaries('dictionaries', dictionaries)


def build_doc(raw_doc):
    doc = {}
    for fld in raw_doc['additionalFields']:
        (name, val) = name_value(fld)
        doc[name] = val
    return doc


def check_duplicate_fields(doc):
    for name, spec in known_fields.items():
        if 'duplicate' in spec:
            main_name = spec['duplicate']
            if main_name not in doc and name in doc:
                logging.warning(f'duplicate {name} without main field')
                continue

            if name in doc and main_name in doc:
                if doc[name] != doc[main_name]:
                    logging.warning(
                        f'''false duplicate
                            {main_name}: {doc[main_name]}
                            {name}: {doc[name]}
                        ''')


def check_for_double_doc(doc):
    count_case_id = 0
    count_case_document_load_date = 0

    for f in doc['additionalFields']:
        if f['name'] == 'case_id':
            count_case_id += 1
        if f['name'] == 'case_document_load_date':
            count_case_document_load_date += 1

    if count_case_id > 1 or count_case_document_load_date > 1:
        count = max(count_case_id, count_case_document_load_date)
        logging.warning(f'double document in {doc["id"]}: {count}')
        return False
    return True


def check_array_fields(doc):
    seen_fields = {}
    for f in doc['additionalFields']:
        name = f['name']
        if name in seen_fields:
            seen_fields[name] += 1
        else:
            seen_fields[name] = 1

    for name, count in seen_fields.items():
        if count > 1:
            if 'isArray' not in known_fields[name]:
                logging.warning(f'possible array field {name}:{count}')


def build_dictionaries(doc, dictionaries):
    for fld in doc['additionalFields']:
        (name, val) = name_value(fld)
        if name in dictionaries:
            dictionaries[name].add(val)


def dump_dictionaries(path, dictionaries):
    if not os.path.isdir(path):
        os.makedirs(path)

    for name, vals in dictionaries.items():
        logging.info(f'dumping dictionary {name}: {len(vals)}')
        with open(f'{path}/{name}.yaml', 'w') as f:
            yaml.dump(sorted(vals), f, allow_unicode = True)


# TODO: check for array fields (single value only if not isArray)

if __name__ == "__main__":
    main()
