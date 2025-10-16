#!/usr/bin/env python3

import sys
import json
from datetime import datetime
import time

import fake_useragent
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

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

for ln in sys.stdin:
    task = json.loads(ln)
    res = {
        'date': task['date'],
        'sud': task['sud'],
        'q': task['q'],
        't': datetime.now().isoformat(),
        }

    start_time = time.perf_counter()

    try:
        rq.headers.update({'User-Agent': ua.random})
        rsp = rq.get(url=task['q'], verify=False, timeout=90)
        res['status'] = rsp.status_code
        res['body'] = rsp.text
    except Exception as err:
        res['err'] = repr(err)

    res['d'] = f'{time.perf_counter() - start_time:.6f}'
    print(json.dumps(res, ensure_ascii=False))
