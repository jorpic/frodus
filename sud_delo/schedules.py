#!/usr/bin/env python3

import sys
import orjson

import parsel
from formats.commons import Ok, Err
import formats.schedule

ERR_MSG_1 = 'Информация временно недоступна. Приносим свои извинения. Попробуйте обратиться позже или обратитесь непосредственно в суд.'
ERR_MSG_2 = 'Не определен ни один сервер, на котором расположен модуль сопряжения с БД'

ERR_MSG_3 = 'Обратитесь к странице позже'

def parse(obj):
    if 'err' in obj:
        return Err(obj['err'])

    if obj['status'] != 200:
        return Err('bad status')

    body = obj['body']
    if ERR_MSG_1 in body:
        return Err('try again')

    if ERR_MSG_2 in body:
        return Err('DB err')

    if ERR_MSG_3 in body:
        return Err('try later')

    if 'дел не назначено' in body:
        return Ok([])

    selector = parsel.Selector(text=body)
    try:
        return Ok(formats.schedule.parse(selector))
    except Exception as e:
        return Err(('parse error', str(e)))

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
            if 'body' in obj:
                del obj['body']
            obj['err'] = res.value
            print(orjson.dumps(obj).decode('utf-8'), file=sys.stderr)

main()
