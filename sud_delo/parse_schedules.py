#!/usr/bin/env python3

import sys
import orjson

import parsel
import formats.F1 as F1
import formats.F2 as F2
from formats.commons import Ok, Err

ERR_MSG_1 = 'Информация временно недоступна. Приносим свои извинения. Попробуйте обратиться позже или обратитесь непосредственно в суд.'

ERR_MSG_2 = 'Не определен ни один сервер, на котором расположен модуль сопряжения с БД'

def parse(obj):
    if 'err' in obj:
        return Err(obj['err'])

    if obj['status'] != 200:
        return Err('bad status')

    body = obj['body']
    if body.find(ERR_MSG_1) != -1:
        return Err('try again')

    if body.find(ERR_MSG_2) != -1:
        return Err('DB err')

    if body.find('дел не назначено') != -1:
        return Ok([])

    errs = []
    selector = parsel.Selector(text=body)
    for p in [F1.parse_cases, F2.parse_cases]:
        res = p(selector)
        if isinstance(res, Ok):
            return Ok(res.value)
        elif isinstance(res, Err):
            errs.append(res.value)
        else:
            errs.append(('unexpected parser result', res))
    return Err(errs)

def main():
    for ln in sys.stdin:
        obj = orjson.loads(ln)
        res = parse(obj)
        if isinstance(res, Ok):
            sch = {
                'sud': obj['sud'],
                'date': obj['date'],
                't': obj['t'],
                'cases': res.value
            }
            print(orjson.dumps(sch).decode('utf-8'))
        else:
            del obj['body']
            obj['err'] = res.value
            print(orjson.dumps(obj).decode('utf-8'), file=sys.stderr)

main()
