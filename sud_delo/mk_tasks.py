#!/usr/bin/env python3

import sys
import json
from datetime import datetime, timedelta

start_date = datetime.fromisoformat(sys.argv[1])
end_date = datetime.fromisoformat(sys.argv[2])
urls = sys.argv[3]

global tasks
with open(urls) as f:
    tasks = json.load(f)

date = start_date
while date < end_date:
    date_str = date.strftime('%d.%m.%Y')
    for sud in tasks:
        task = {
            'date': date.strftime('%Y-%m-%d'),
            'sud': sud['id'],
            'q': (
                f'https://{sud["url"]}/modules.php'
                f'?name=sud_delo&srv_num=1'
                f'&H_date={date_str}')
            }
        print(json.dumps(task, ensure_ascii=False))

    date += timedelta(days=1)
