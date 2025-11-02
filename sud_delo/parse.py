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

def main():
    for ln in sys.stdin:
        js = json.loads(ln)
        if 'err' in js:
            print(js.get('sud'), js['err'], file=sys.stderr)
            continue

        if js['status'] != 200:
            print(js.get('sud'), 'err: status', file=sys.stderr)
            continue

        body = js['body']
        if body.find(ERR_MSG_1) != -1:
            print(js.get('sud'), 'err: try again', file=sys.stderr)
            continue

        if body.find(ERR_MSG_2) != -1:
            print(js.get('sud'), 'err: DB', file=sys.stderr)
            continue

        res = parse(body)
        if isinstance(res, Ok):
            for case in res.value:
                case['sud'] = js['sud']
                case['date'] = js['date']
                print(json.dumps(case, ensure_ascii=False))
        else:
            print(js.get('sud'), res.value, file=sys.stderr)

main()
