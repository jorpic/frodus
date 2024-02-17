#!/usr/bin/env python3

import sys
import json
import parsel
import requests
import queue
import threading
import fake_useragent

from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta

num_threads = int(sys.argv[1])
start_date = datetime.fromisoformat(sys.argv[2])

urls = []
with open('urls.txt') as f:
    for url in f:
        urls.append(url.strip())


jobs = queue.Queue(num_threads*2)
results = queue.Queue()

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def output():
    while True:
        obj = results.get()
        print(json.dumps(obj, ensure_ascii=False))


def worker():
    ua = fake_useragent.UserAgent()
    rq = requests.Session()
    rq.headers.update({
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
            rq.headers.update({'User-Agent': ua.random})
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
        except Exception as err:
            res['error'] = {'msg': repr(err)}

        results.put(res)


threading.Thread(target=output).start()
for _ in range(0, num_threads):
    threading.Thread(target=worker).start()


while True:
    print(start_date.date(), datetime.now(), file=sys.stderr)
    for url in urls:
        jobs.put((url, start_date))
    start_date += timedelta(days=1)
