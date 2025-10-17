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
    sud = task['sud']
    date = task['date']
    date_str = datetime.fromisoformat(date).strftime("%d.%m.%Y")
    query = (
        f'https://{sud}/modules.php'
        f'?name=sud_delo&srv_num=1&H_date={date_str}')

    res = {
        'date': date,
        'sud': sud,
        't': datetime.now().isoformat(),
        }

    start_time = time.perf_counter()

    try:
        rq.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=utf-8',
            'Origin': f'https://{sud}',
            'Referer': f'https://{sud}',
            'User-Agent': ua.random
        })

        rsp = rq.get(url=query, verify=False, timeout=90)
        res['status'] = rsp.status_code
        res['body'] = rsp.text
    except Exception as err:
        res['err'] = repr(err)

    res['d'] = f'{time.perf_counter() - start_time:.6f}'
    print(json.dumps(res, ensure_ascii=False))
