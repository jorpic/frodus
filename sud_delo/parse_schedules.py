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


ERR_MSG_1 = 'Информация временно недоступна. Приносим свои извинения. Попробуйте обратиться позже или обратитесь непосредственно в суд.'

ERR_MSG_2 = 'Не определен ни один сервер, на котором расположен модуль сопряжения с БД'

def get_err(obj):
    if 'err' in obj:
        return obj['err']

    if obj['status'] != 200:
        return 'bad status'

    body = obj['body']
    if body.find(ERR_MSG_1) != -1:
        return 'try again'

    if body.find(ERR_MSG_2) != -1:
        return 'DB err'


def main():
    for ln in sys.stdin:
        obj = json.loads(ln)
        err = get_err(obj)
        if err:
            obj['err'] = err
            print(json.dumps(obj, ensure_ascii=False), file=sys.stderr)
            continue

        res = parse(obj['body'])
        if isinstance(res, Ok):
            sch = {
                'sud': obj['sud'],
                'date': obj['date'],
                't': obj['t'],
                'cases': res.value
            }
            print(json.dumps(sch, ensure_ascii=False))
        else:
            obj['err'] = res.value
            print(json.dumps(obj, ensure_ascii=False), file=sys.stderr)

main()
