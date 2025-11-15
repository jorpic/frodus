from formats.commons import Ok, Err, all_text

# kaliazinsky--twr.sudrf.ru and others

def parse_cases(sel):
    table = sel.xpath('//div[@id="content"]//table[@id="tablcont"]')

    if len(table) == 0:
        return Err('no table found')

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
    try:
        for row in rows[1:]:
            new_cat = row.xpath('.//td[@colspan="8"]')
            if new_cat:
                # There could be no text inside, so we use
                # `string(.)` to convert.
                category = new_cat.xpath('string(.)').get()
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
    except Exception as err:
        return Err(('parse error', repr(err)))
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
