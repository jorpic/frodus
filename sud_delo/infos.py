#!/usr/bin/env python3

import sys
import orjson

import parsel
from formats.commons import Ok, Err
import formats.info

ERR_MSG_1 = 'Информация временно недоступна.'
ERR_MSG_2 = 'Не определен ни один сервер, на котором расположен модуль сопряжения с БД'
ERR_MSG_3 = 'Обратитесь к странице позже'
ERR_MSG_4 = 'НЕВЕРНЫЙ ФОРМАТ ЗАПРОСА'
ERR_MSG_5 = 'Trying to access array offset on value of type null'

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

    if ERR_MSG_4 in body:
        return Err('invalid query format')

    if ERR_MSG_5 in body:
        return Err('PHP bug')

    errs = []
    selector = parsel.Selector(text=body)
    try:
        return Ok(formats.info.parse(selector))
    except Exception as e:
        return Err(('parse error', str(e)))

def main():
    for ln in sys.stdin:
        obj = orjson.loads(ln)
        res = parse(obj)
        if isinstance(res, Ok):
            inf = {
                't': obj['t'],
                'url': obj['url'],
            }
            inf.update(res.value)
            print(orjson.dumps(inf).decode('utf-8'))
        else:
            if 'body' in obj:
                del obj['body']
            obj['err'] = res.value
            print(orjson.dumps(obj).decode('utf-8'), file=sys.stderr)

main()
