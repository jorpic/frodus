#!/usr/bin/env python3
import os
import sys
import time
import logging
import requests
from datetime import datetime, timedelta

from lib.api import API
import lib.query as query

year = sys.argv[1]

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename=f'{year}.log',
    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
logging.getLogger('').addHandler(console)


DATA_DIR = 'results'
if not os.path.isdir(DATA_DIR):
    os.makedirs(DATA_DIR)

query_date = datetime.strptime(year, '%Y')
logging.info(f'Starting from {query_date.date().isoformat()}')

ip_addr = requests.get("https://ipinfo.io/ip").text
logging.info(f'Fetching via {ip_addr=}')

api = API()
logging.info(f'With {api.uid=}')

offset = 0
if os.path.isfile(f'{year}.savepoint'):
    with open(f'{year}.savepoint', 'r') as f:
        [date, total, offset] = f.read().strip().split('.')
        query_date = datetime.strptime(date, '%Y-%m-%d')
        total = int(total)
        offset = int(offset)
        logging.info(f'Continue from {date=} {offset=}')

delay = 9
while query_date.year == int(year):
    date = query_date.date().isoformat()
    next_date = query_date + timedelta(weeks=1)
    while True:
        response = api.search(
            query.search(
                query_date,
                next_date,
                offset))
        # response = api.search(query.search1('Республика Башкортостан', query_date, offset))

        file_name = f'{DATA_DIR}/{date}.{offset}.response'

        with open(file_name, 'wb') as f:
            f.write(response.content)
        logging.debug(f'Written to {file_name=} {len(response.content)=}')

        r = response.json()
        docs = len(r['searchResult']['documents'])
        total = r['searchResult']['numFounds']
        logging.info(f'Query result {date=} {total=} {offset=} {docs=}')

        with open(f'{year}.savepoint', 'w') as f:
            f.write(f'{date}.{total}.{offset}')

        offset += docs
        if offset >= total:
            break

        time.sleep(delay)

    logging.info(f'Compress day results {date=}')
    os.system(f'tar --remove-files -cJf {DATA_DIR}/{date}.tar.xz {DATA_DIR}/{date}.*.response')

    offset = 0
    query_date = next_date

logging.info('Done!')
