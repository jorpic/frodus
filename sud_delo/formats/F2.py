import parsel
from formats.commons import Ok, Err, all_text


def parse_cases(html):
    p = parsel.Selector(text=html)
    table = p.xpath('//div[@id="resultTable"]/table')

    if len(table) == 0:
        if html.find('дел не назначено') != -1:
            return Ok([])
        else:
            return Err('unusual html')

    rows = table.xpath('.//tr')
    if len(rows) == 0:
        return Err('no rows in tablcont')

    header = [
        ' '.join(col.xpath('.//text()').getall())
        for col in rows[0].xpath('.//td')]
    if not is_valid_header(header):
        return Err(('unusual table header', header))

    category = None
    cases = []
    for row in rows[1:]:
        new_cat = row.xpath('.//td[@colspan="9"]//text()').get()
        if new_cat:
            category = new_cat
            continue

        td = row.xpath('.//td')
        cases.append({
            'cat':    category,
            'num':    all_text(td[1]),
            'url':    td[1].xpath('.//a/@href').get(),
            'time':   all_text(td[2]),
            'event':  all_text(td[3]),
            'place':  all_text(td[4]),
            'info':   all_text(td[5]),
            'judge':  all_text(td[6]),
            'result': all_text(td[7]),
            'docs':   td[8].xpath('.//@href').getall()})
    return Ok(cases)

def is_valid_header(header):
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
