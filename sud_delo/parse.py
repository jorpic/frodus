#!/usr/bin/env python3

import sys
import json
import parsel

class Err:
    def __init__(self, val):
        self.value = val

class Ok:
    def __init__(self, val):
        self.value = val

def parse_cases(html):
    p = parsel.Selector(text=html)
    table = p.xpath('//table[@id="tablcont"]')

    if len(table) == 0:
        if html.find('дел не назначено') == -1:
            return Err(('unusual html', ln))

    rows = table.xpath('//tr')

    header = [
        ' '.join(col.xpath('.//text()').getall())
        for col in rows[0].xpath('.//td')]
    if not is_valid_header(header):
        return Err(('unusual table header', header))

    category = None
    cases = []
    for row in rows[1:]:
        new_cat = row.xpath('.//td[@colspan="8"]//text()').get()
        if new_cat:
            category = new_cat
            continue

        td = row.xpath('.//td')
        cases.append({
            'cat':    category,
            'num':    all_text(td[1]),
            'url':    td[1].xpath('.//a/@href').get(),
            'time':   all_text(td[2]),
            'place':  all_text(td[3]),
            'info':   all_text(td[4]),
            'judge':  all_text(td[5]),
            'result': all_text(td[6]),
            'docs':   td[7].xpath('.//@href').getall()})
    return Ok(cases)


def is_valid_header(header):
    expected_header = [
        '№ п/п',
        'Номер дела',
        'Время слушания',
        'Место проведения (Зал судебного заседания)',
        'Информация по делу',
        'Судья',
        'Результат слушания',
        'Судебные акты']
    return header == expected_header


def all_text(selector, separator='\n'):
    return separator.join(
        [s.strip() for s in selector.xpath('.//text()').getall()])


def main():
    for ln in sys.stdin:
        js = json.loads(ln)
        if 'html' not in js:
            print(ln, end='')
            continue

        res = parse_cases(js['html'])
        if isinstance(res, Ok):
            del js['html']
            js['cases'] = res.value
            print(json.dumps(js, ensure_ascii=False))
        elif isinstance(res, Err):
            print(res.value, file=sys.stderr)
        else:
            print('unexpected result from get_cases', res, file=sys.stderr)

main()
