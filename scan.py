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


    for archive in files:
        archive = archive.strip()
        with tarfile.open(archive, 'r|bz2') as tar:
            for json_file in tar:
                with tar.extractfile(json_file) as json_text:
                    logging.info(f'reading {json_file}')
                    jsn = json.load(json_text)
                    res = jsn['searchResult']

                    for doc in res['documents']:
                        check_duplicate_fields(doc)
                        check_for_double_doc(doc)
                        build_dictionaries(doc, dictionaries)

    dump_dictionaries('dictionaries', dictionaries)


def check_duplicate_fields(doc):
    values = {}
    for fld in doc['additionalFields']:
        (name, val) = name_value(fld)
        values[name] = val

    for name, spec in known_fields.items():
        if 'duplicate' in spec:
            main_name = spec['duplicate']
            if main_name not in values and name in values:
                logging.warning(
                    f'duplicate {name} without main field in {doc["id"]}')
                continue

            if name in values and main_name in values:
                if values[name] != values[main_name]:
                    logging.warning(
                        f'''false duplicate in {doc['id']}
                            {main_name}: {values[main_name]}
                            {name}: {values[name]}
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
        return True
    return False


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


# TODO: count docs?
# TODO: check for array fields (single value only if not isArray)

if __name__ == "__main__":
    main()
