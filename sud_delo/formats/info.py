from formats.parser import x, select

def parse(sel):
    return select(sel,
        (['1n//div[@id="modSdpContent"]/div[@id="content"]'], parse1),
        (['1n//div[@id="modSdpContent"]//div[@id="search_results"]'], parse2)
    )

def parse1(info):
    res = {
        'cat': x(info, '1t./div[@class="title"]'),
        'num': x(info, '1t./div[@class="casenumber"]'),
    }
    tabs = info.xpath('./div[@class="contentt"]')
    tab_names = x(info, '+n./ul[@class="tabs"]/li', ('1s./@id', '1t.'))
    for (tab_id, tab_name) in tab_names:
        if tab_name not in known_tabs1:
            raise Exception(f'1: Unknown tab {tab_name}')
        tab_id = tab_id.replace('tab', 'cont') # tab1 -> cont1
        res[tab_name] = known_tabs1[tab_name](tabs, tab_id, tab_name)
    return res

def parse2(info):
    res = {
        'cat': x(info, '1t.//div[@class="name-instanse"]'),
        'num': x(info, '1t.//div/div[@class="case-num"]'),
        'pub': x(info, '*t.//div/div[contains(@class, "publishInfo")]'),
    }
    tab_names = x(info, '+n.//ul[@id="case_bookmarks"]/li', ('1s./@id', '1t.'))
    for (tab_id, tab_name) in tab_names:
        if tab_name not in known_tabs2:
            raise Exception(f'2: Unknown tab {tab_name}')
        tab_id = tab_id.replace('tab_id', 'tab_content')
        res[tab_name] = known_tabs2[tab_name](info, tab_id, tab_name)
    return res

def table1_1(tabs, tab_id, tab_name):
    return x(
        tabs,
        f'1n./div[@id="{tab_id}"]/table',
        '+n./tr[position() > 1]',
        '*n./td', '1t.')

def table1_n(tabs, tab_id, tab_name):
    return x(
        tabs,
        f'1n./div[@id="{tab_id}"]/table',
        '+n./tr[position() > 1]',
        '+n./td', '1t.')

def docs1(tabs, tab_id, tab_name):
    doc_names = x(
        tabs,
        f'1n./div[@id="{tab_id}"]',
        '*n./ul[@class="tabs"]/li',
        ('1s./@id', '1t.'))
    doc_conts = tabs.xpath(
        f'./div[@id="{tab_id}"]/div[@class="contentt"]')

    res = []
    for (doc_id, doc_name) in doc_names:
        doc_id = doc_id.replace('tab', 'cont')
        doc = x(doc_conts, f'1n./div[@id="{doc_id}"]', '?T.')
        res.append({doc_name: doc})
    return res

def claim(tabs, tab_id, tab_name):
    return x(
        tabs,
        f'1n.//div[@id="{tab_id}"]',
        '+n./table',
        '+n./tr',
        lambda tr: select(tr,
            (['1n./td/table', '+n.//tr', '*t./td'], lambda x: x),
            (['+t./td'], lambda x: x),
            (['+t./th'], lambda x: x),
        )
    )


def table2_1(tabs, tab_id, tab_name):
    return x(
        tabs,
        f'1n.//div[@id="{tab_id}"]/table',
        '+n./tr',
        '*n./td', '1t.')

def table2_n(tabs, tab_id, tab_name):
    return x(
        tabs,
        f'1n.//div[@id="{tab_id}"]/table',
        '+n.//tr',
        '+n./td', '1t.')

def docs2(tabs, tab_id, tab_name):
    doc_names = x(
        tabs,
        f'1n.//div[@class="lawcase-tab-content" and @id="{tab_id}"]',
        '*n.//ul[@id="doc_bookmarks"]/li',
        ('1s./@id', '1t.'))

    res = []
    for (doc_id, doc_name) in doc_names:
        doc_id = doc_id.replace('doctab_id', 'doctab_content')
        doc = x(tabs, f'1n.//div[@id="{doc_id}"]', '1T.')
        res.append({doc_name: doc})
    return res

def inline_doc2(tabs, tab_id, tab_name):
    return x(tabs, f'1n.//div[@id="{tab_id}"]/table', '1T.')

def not_implemented(tabs, tab_id, tab_name):
    tab = x(
        tabs,
        f'*s.//div[@id="{tab_id}"]')
    raise Exception((tab_name, tab))

known_tabs1 = {
    'ДВИЖЕНИЕ ДЕЛА': table1_n,
    'ДВИЖЕНИЕ МАТЕРИАЛА': table1_n,
    'ДЕЛО': table1_1,
    'ЖАЛОБЫ': table1_n,
    'ИСПОЛНИТЕЛЬНЫЕ ЛИСТЫ': table1_n,
    'ЛИЦА': table1_n,
    'ОБЖАЛОВАНИЕ ОПРЕДЕЛЕНИЙ КАССАЦИОННОЙ ИНСТАНЦИИ': table1_1,
    'ОБЖАЛОВАНИЕ ПРИГОВОРОВ ОПРЕДЕЛЕНИЙ (ПОСТ.)': claim,
    'ОБЖАЛОВАНИЕ РЕШЕНИЙ, ОПРЕДЕЛЕНИЙ (ПОСТ.)': claim,
    'ОГРАНИЧЕНИЯ ДОСТУПА': table1_1,
    'ПРОИЗВОДСТВО': table1_1,
    'РАССМОТРЕНИЕ В НИЖЕСТОЯЩЕМ СУДЕ': table1_1,
    'СЛУШАНИЯ': table1_n,
    'СТОРОНЫ': table1_n,
    'СТОРОНЫ ПО ДЕЛУ': table1_n,
    'СТОРОНЫ ПО ДЕЛУ (ТРЕТЬИ ЛИЦА)': table1_n,
    'СУДЕБНЫЕ АКТЫ': docs1,
    'УЧАСТНИКИ': table1_n,
}

known_tabs2 = {
    'Движение дела': table2_n,
    'Движение материала': table2_n,
    'Дело': table2_1,
    'Исполнительные листы': table2_n,
    'Лица': table2_n,
    'Материал': table2_1,
    'Обжалования': claim,
    'Рассмотрение в нижестоящем суде': table2_1,
    'Стороны': table2_n,
    'Судебные акты': docs2,
    'Судебный акт #1 ()': inline_doc2,
    'Судебный акт #1 (Определение)': inline_doc2,
    'Судебный акт #1 (Приговор)': inline_doc2,
    'Судебный акт #1 (Приговоры)': inline_doc2,
    'Судебный акт #1 (Постановление)': inline_doc2,
}
