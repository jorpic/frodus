#!/usr/bin/env python3

import sys
import json
import tarfile
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    stream=sys.stderr)


def read_docs(files):
    for archive in files:
        archive = archive.strip()
        logging.info(f'reading {archive}')

        with tarfile.open(archive, 'r:xz') as tar:
            for json_file in tar:
                with tar.extractfile(json_file) as json_text:
                    try:
                        jsn = json.load(json_text)
                        res = jsn['searchResult']
                    except json.decoder.JSONDecodeError as e:
                        logging.error(f'in {json_file}: {e}')
                    else:
                        for doc in res['documents']:
                            yield (doc, json_file.name)
