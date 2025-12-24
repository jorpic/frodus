from formats.parser import x

def parse(sel):
    rows = None
    try:
        rows = x(
            sel,
            '1n//div[@id="content"]//table[@id="tablcont"]',
            '+n.//tr')
    except Exception as e:
        pass

    if rows:
        return parse1(rows)

    try:
        rows = x(
            sel,
            '1n//div[@id="resultTable"]/table',
            '+n.//tr')
    except Exception as e:
        pass

    if rows:
        return parse2(rows)

    raise Exception("can't parse")

def parse1(rows):
    header = x(rows[0], '8n.//td', '+s.//text()')
    if not is_valid_header1(header):
        raise Exception(header)

    category = None
    cases = []
    for row in rows[1:]:
        # There may be no text inside, so we use `string(.)` to convert.
        new_cat = x(row, '?n.//td[@colspan="8"]', '?sstring(.)')
        if new_cat:
            category = new_cat
            continue

        td = x(row, '8n.//td')
        cases.append({
            'cat':    category,
            'num':    x(td[1], '+s.//text()'),
            'url':    x(td[1], '1t.//a/@href'),
            'time':   x(td[2], '*s.//text()'),
            'place':  x(td[3], '*s.//text()'),
            'info':   x(td[4], '+S.//text()'),
            'judge':  x(td[5], '*s.//text()'),
            'result': x(td[6], '*s.//text()'),
            'docs':   x(td[7], '*t.//@href')})
    return cases

def parse2(rows):
    header = x(rows[0], '9n.//td', '+s.//text()')
    if not is_valid_header2(header):
        raise Exception(header)

    category = None
    cases = []
    for row in rows[1:]:
        # There may be no text inside, so we use `string(.)` to convert.
        new_cat = x(row, '?n.//td[@colspan="9"]', '?sstring(.)')
        if new_cat:
            category = new_cat
            continue

        td = x(row, '9n.//td')
        cases.append({
            'cat':    category,
            'num':    x(td[1], '+s.//text()'),
            'url':    x(td[1], '1t.//a/@href'),
            'time':   x(td[2], '*s.//text()'),
            'event':  x(td[3], '*s.//text()'),
            'place':  x(td[4], '*s.//text()'),
            'info':   x(td[5], '+S.//text()'),
            'judge':  x(td[6], '*s.//text()'),
            'result': x(td[7], '*s.//text()'),
            'docs':   x(td[8], '*t.//@href')})
    return cases

def is_valid_header1(header):
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

def is_valid_header2(header):
    expected_header1 = [
        '№ п/п',
        'Номер дела',
        'Время слушания',
        'Событие',
        'Место проведения',
        'Информация по делу',
        'Судья',
        'Результат слушания',
        'Судебные акты']
    expected_header2 = [
        '№ п/п',
        'Номер дела',
        'Время слушания',
        'Событие',
        'Место проведения (Зал судебного заседания)',
        'Информация по делу',
        'Судья',
        'Результат слушания',
        'Судебные акты']

    return header == expected_header1 \
        or header == expected_header2
