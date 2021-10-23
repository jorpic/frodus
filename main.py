#!/usr/bin/env python3
import os
import sys
import bz2
import time
import logging
from datetime import datetime, timedelta

from api import API
import query

query_date = sys.argv[1]

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename=f'{query_date}.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
logging.getLogger('').addHandler(console)


DATA_DIR = 'results'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

query_date = datetime.strptime(sys.argv[1], '%Y-%m-%d')
logging.info(f'Starting from {query_date.date().isoformat()}')

api = API()
logging.info(f'With {api.uid=}')

delay = 9
while True:
    offset = 0
    while True:
        response = api.search(query.search(query_date, offset))

        date = query_date.date().isoformat()
        ts = int(datetime.now().timestamp())
        file_name = f'{DATA_DIR}/{date}.{offset}.{ts}.bz2'

        with bz2.open(file_name, "wb") as f:
            f.write(response.content)
        logging.debug(f'Written to {file_name=} {len(response.content)=}')

        r = response.json()
        docs = len(r['searchResult']['documents'])
        total = r['searchResult']['numFounds']
        logging.info(f'Query result {date=} {total=} {offset=} {docs=}')

        time.sleep(delay)

        offset += docs
        if offset >= total:
            break

    query_date += timedelta(days=1)
