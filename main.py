#!/usr/bin/env python3
import os
import sys
import bz2
import time
import logging
import requests
from datetime import datetime, timedelta

from api import API
import query

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
if not os.path.exists(DATA_DIR):
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
while True:
    date = query_date.date().isoformat()
    while True:
        response = api.search(query.search(query_date, offset))

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

        time.sleep(delay)

        offset += docs
        if offset >= total:
            break

    logging.info(f'Compress day results {date=}')
    os.system(f'tar --remove-files -cjf {DATA_DIR}/{date}.tar.bz2 {DATA_DIR}/{date}.*.response')

    offset = 0
    prev_date = query_date
    query_date += timedelta(days=1)
    if query_date.year > prev_date.year:
        break

logging.info('Done!')
