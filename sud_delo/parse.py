#!/usr/bin/env python3

import sys
import json

import formats.F1 as F1
import formats.F2 as F2
from formats.commons import Ok, Err

def parse(body):
    errs = []
    for p in [F1.parse_cases, F2.parse_cases]:
        res = p(body)
        if isinstance(res, Ok):
            return Ok(res.value)
        elif isinstance(res, Err):
            errs.append(res.value)
        else:
            errs.append(('unexpected parser result', res))
    return Err(errs)


def main():
    for ln in sys.stdin:
        js = json.loads(ln)
        body = js['body']

        if js['status'] != 200:
            continue

        msg = 'Информация временно недоступна. Приносим свои извинения. Попробуйте обратиться позже или обратитесь непосредственно в суд.'
        if body.find(msg) != -1:
            # print(js.get('q'), 'try later', file=sys.stderr)
            continue

        msg = 'Не определен ни один сервер, на котором расположен модуль сопряжения с БД'
        if body.find(msg) != -1:
            # print(js.get('q'), 'check this err!!', file=sys.stderr)
            continue

        res = parse(body)
        if isinstance(res, Ok):
            del js['body']
            js['cases'] = res.value
            print(json.dumps(js, ensure_ascii=False))
        else:
            print(js.get('q'), res.value, file=sys.stderr)

main()
