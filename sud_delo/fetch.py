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

for ln in sys.stdin:
    task = json.loads(ln)
    task['t'] = datetime.now().isoformat()
    start_time = time.perf_counter()

    try:
        rq.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': ua.random
        })

        rsp = rq.get(url=task['url'], verify=False, timeout=90)
        task['status'] = rsp.status_code
        task['body'] = rsp.text
    except Exception as err:
        task['err'] = repr(err)

    task['d'] = f'{time.perf_counter() - start_time:.6f}'
    print(json.dumps(task, ensure_ascii=False))
