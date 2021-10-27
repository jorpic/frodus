#!/usr/bin/env python3

import os
import sys
import json
import yaml
import textwrap
import tarfile
import psycopg2



'''
create table processed_files(
    ctime timestamp with time zone not null default now(),
    file_name text not null unique
);
'''

known_fields = yaml.safe_load(textwrap.dedent('''
    case_common_doc_court:
        duplicate: case_user_doc_court
        isDictionary: true

    case_common_doc_entry_date:
        value: dateValue

    case_common_doc_number: {}
    case_common_doc_number_rewrite: {}
    case_common_doc_result: {}
    case_common_doc_result_date:
        value: dateValue
    case_common_document_article: {}

    case_common_document_num:
        value: longValue

    case_common_document_type:
        isDictionary: true
        desc: Тип документа
        duplicate: case_user_document_type

    case_common_doc_validity_date:
        value: dateValue
    case_common_entry_date:
        value: dateValue
    case_common_event_date:
        value: dateValue
        isArray: true
    case_common_event_m2_search:
        isArray: true
    case_common_event_m2:
        isArray: true
    case_common_event_name:
        isArray: true
    case_common_event_result:
        isArray: true

    case_common_judge:
        duplicate: case_user_judge

    case_common_parts_m2_search:
        isArray: true
    case_common_parts_name:
        isArray: true
    case_common_parts_type:
        isArray: true

    case_common_type: {}

    case_court_type: {}

    case_court_type_cat:
        skip: true
        duplicate: case_court_type

    case_doc_district_rf:
        isDictionary: true

    case_doc_instance: {}

    case_doc_kind:
        isDictionary: true

    case_doc_kind_prefix:
        skip: true
        desc: Однозначно соответствует case_doc_kind??

    case_doc_kind_short:
        skip: true
        desc: Однозначно соответствует case_doc_kind??

    case_doc_load_date:
        value: dateValue

    case_doc_source:
        isDictionary: true

    case_doc_source_table:
        skip: true

    case_doc_subject_number:
        skip: true
        desc: Код субъекта РФ

    case_doc_subject_rf:
        skip: true
        desc: Название субъекта РФ

    case_doc_subject_rf_code:
        isDictionary: true
        desc: Код и название субъекта РФ

    case_document_articles:
        isArray: true

    case_document_category_article:
        isArray: true

    case_document_id: {}

    case_document_load_date:
        value: dateValue

    case_document_num_build:
        value: longValue

    case_document_publ_date:
        value: dateValue

    case_document_result: {}

    case_document_result_date:
        value: dateValue

    case_document_results:
        skip: true
        duplicate: case_document_result

    case_document_types:
        skip: true
        duplicate: case_common_document_type

    case_doc_vnkod: {}
    case_id: {}
    case_id_region: {}
    case_regbasenum:
        value: longValue
    case_short_number: {}
    case_user_doc_court:
        value: linkName
        duplicate: case_common_doc_court

    case_user_doc_entry_date:
        value: dateValue
    case_user_doc_number: {}
    case_user_doc_number_rewrite: {}
    case_user_doc_result:
        isDictionary: true
    case_user_doc_result_date:
        value: dateValue
    case_user_document_num:
        value: longValue
    case_user_document_text_tag: {}

    case_user_document_type:
        skip: true
        duplicate: case_common_document_type

    case_user_doc_validity_date:
        value: dateValue

    case_user_entry_date:
        value: dateValue

    case_user_judge:
        skip: true
        duplicate: case_common_judge

    case_user_type: {}

    case_year_entry:
        value: longValue

    case_year:
        value: longValue

    case_year_result:
        value: longValue

    court_deside: {}

    name: {}

    timestamp:
        value: dateValue
        desc: Дата загрузки документа на sudrf??

    txt_exist:
        skip: true

    u_case_common_article:
        desc: статья

    u_case_user_article:
        skip: true
        duplicate: u_case_common_article

    u_common_case_defendant_m:
        desc: ФИО, статья, результат дела?

    u_common_case_defendant_m_search:
        skip: true
        duplicate: u_common_case_defendant_m

    u_common_case_defendant_name:
        desc: ФИО защитника
        isDictionary: true
    '''))


def process_doc(doc):
    # if exists and not is_array and val1 != val2:
    #       stop & report
    # at the end of the loop remove duplicates from all array_fields

    doc_hash = doc['id']
    print(doc_hash)
    new_doc = {}
    for f in doc['additionalFields']:
        name = f['name']
        if name in known_fields:
            f_desc = known_fields[name]
            val = f[f_desc.get('value', 'value')]
            if f_desc.get('isArray', False):
                if name not in new_doc:
                    new_doc[name] = []
                new_doc[name].append(val)
            else:
                if name in new_doc and new_doc[name] != val:
                    print(f'Conflicting field values {name=} {val=} {new_doc[name]=}')
                else:
                    new_doc[name] = val
        else:
            print(f'Unknown field {name=} {f}')

    # check duplicates

    # delete skipped
    for name in known_fields:
        if name in new_doc:
            if known_fields[name].get('skip', False):
                del new_doc[name] # FIXME: k.get('new_name', name)
            else:
                print(name, str(new_doc[name])[:120])


def process_all(x):
    for doc in x['searchResult']['documents']:
        process_doc(doc)


def already_processed(file_name):
    cur.execute(
        "select true from processed_files where file_name = %s",
        (file_name,))
    return cur.fetchall() != []


def mark_as_processed(file_name):
    pass
    # cur.execute(
    #     "insert into processed_files(file_name) values (%s)", 
    #     (file_name,))


pg = psycopg2.connect(dbname='frodus')
pg.autocommit = True
cur = pg.cursor()

files = sys.stdin.readlines()

for file_name in files:
    file_name = file_name.strip()
    if already_processed(file_name):
        continue
    print(file_name)
    with tarfile.open(file_name, 'r|bz2') as tar:
        for f in tar:
            with tar.extractfile(f) as g:
                if already_processed(f.name):
                    continue
                # try:
                process_all(json.load(g))
                # except Exception as e:
                #    print(e)
                mark_as_processed(f.name)
    mark_as_processed(file_name)
