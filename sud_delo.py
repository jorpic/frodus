#!/usr/bin/env python3

import sys
import json
import parsel
import requests
import queue
import threading

from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta

start_date = datetime.fromisoformat(sys.argv[1])
progress = {}

urls = []
with open('urls.txt') as f:
    for url in f:
        urls.append(url.strip())


jobs = queue.Queue(100)
results = queue.Queue()

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def output():
    while True:
        obj = results.get()
        print(json.dumps(obj, ensure_ascii=False))


def worker():
    rq = requests.Session()
    rq.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://bsr.sudrf.ru',
        'Referer': 'https://bsr.sudrf.ru/bigs/portal.html',
    })

    while True:
        (url, date) = jobs.get()

        query = 'https://' + url \
            + '/modules.php?name=sud_delo&srv_num=1&H_date=' \
            + date.strftime('%d.%m.%Y')

        res = {'url': url,
               'date': date.strftime('%Y-%m-%d'),
               'ts': datetime.now().isoformat()
               }
        try:
            response = rq.get(url=query, verify=False)
            if response.status_code == 200:
                p = parsel.Selector(body=response.content, encoding='windows-1251')

                table = p.xpath('//div[@id="content"]').get()
                if table:
                    res['html'] = table
                else:
                    res['error'] = {'msg': 'no #content tag'}
            else:
                res['error'] = {'msg': 'unexpected http status',
                                'code': response.status_code}
        except ConnectionError as err:
            res['error'] = {'msg': repr(err)}

        results.put(res)


threading.Thread(target=output).start()
for _ in range(0, 10):
    threading.Thread(target=worker).start()


while True:
    print(start_date.date(), datetime.now(), file=sys.stderr)
    for url in urls:
        jobs.put((url, start_date))
    start_date += timedelta(days=1)
