from formats.parser import x, select

def parse(sel):
    return select(sel,
        (['1n//div[@id="content"]//table[@id="tablcont"]', '+n.//tr'], parse1),
        (['1n//div[@id="resultTable"]/table', '+n.//tr'], parse2)
    )

def parse1(rows):
    header = x(rows[0], '8t.//td')
    if not is_valid_header1(header):
        raise Exception(f'Invalid header: {header}')

    category = None
    cases = []
    for row in rows[1:]:
        # NB. There may be a category with empty title.
        new_cat = x(row, '?n.//td[@colspan="8"]', '!t.')
        if new_cat != None:
            category = new_cat
            continue

        td = x(row, '8n.//td')
        cases.append({
            'cat':    category,
            'num':    x(td[1], '?t.'),
            'url':    x(td[1], '1s.//a/@href'),
            'time':   x(td[2], '?t.'),
            'place':  x(td[3], '?t.'),
            'info':   x(td[4], '?T.'),
            'judge':  x(td[5], '?t.'),
            'result': x(td[6], '?t.'),
            'docs':   x(td[7], '*s.//a/@href')})
    return cases

def parse2(rows):
    header = x(rows[0], '9t.//td')
    if not is_valid_header2(header):
        raise Exception(f'Invalid header: {header}')

    category = None
    cases = []
    for row in rows[1:]:
        # NB. There may be a category with empty title.
        new_cat = x(row, '?n.//td[@colspan="9"]', '!t.')
        if new_cat:
            category = new_cat
            continue

        td = x(row, '9n.//td')
        cases.append({
            'cat':    category,
            'num':    x(td[1], '?t.'),
            'url':    x(td[1], '1s.//a/@href'),
            'time':   x(td[2], '?t.'),
            'event':  x(td[3], '?t.'),
            'place':  x(td[4], '?t.'),
            'info':   x(td[5], '?T.'),
            'judge':  x(td[6], '?t.'),
            'result': x(td[7], '?t.'),
            'docs':   x(td[8], '*s.//a/@href')})
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
