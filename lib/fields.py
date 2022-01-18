#!/usr/bin/env python3

import yaml
import textwrap


# case_hear_date_s -- Дата слушания
# case_hear_m2_search -- Слушания по делу
# case_common_court_i -- Суд (мировой судья) первой инстанции
# u2_33_case_court_i -- Районный суд
# case_user_court_i -- Передано из


known_fields = yaml.safe_load(textwrap.dedent('''
    case_common_doc_court:
        desc: Наименование суда
        isDictionary: true

    case_common_doc_entry_date:
        desc: Дата поступления
        value: dateValue

    case_common_doc_number:
        desc: Номер дела (материала)

    case_common_doc_number_rewrite:
        duplicate: case_common_doc_number

    case_common_doc_result:
        desc: Результат
        isDictionary: true

    case_common_doc_result_date:
        desc: Дата решения
        value: dateValue

    case_common_document_article:
        desc: Статья УК РФ
        skip: true
        comment: Иногда отсутствует. В case_document_articles более полная информация.

    case_common_document_num:
        value: longValue

    case_common_document_type:
        isDictionary: true
        desc: Тип документа

    case_common_doc_validity_date:
        value: dateValue

    case_common_entry_date:
        desc: Дата поступления
        value: dateValue
        duplicate: case_common_doc_entry_date

    case_common_event_m2:
        desc: Движение дела
        isArray: true

    case_common_event_m2_search:
        isArray: true
        skip: true
        comment: Вся информация есть в case_common_event_m2

    case_common_event_date:
        value: dateValue
        isArray: true
        skip: true
        comment: Вся информация есть в case_common_event_m2

    case_common_event_name:
        isArray: true
        skip: true
        comment: Вся информация есть в case_common_event_m2

    case_common_event_result:
        isArray: true
        skip: true
        comment: Вся информация есть в case_common_event_m2

    case_common_judge:
        desc: Судья
        isDictionary: true

    case_common_parts_m2_search:
        isArray: true
        comment: Заменяет собой поля case_common_parts_type и case_common_parts_name

    case_common_parts_name:
        isArray: true
        skip: true

    case_common_parts_type:
        isArray: true
        skip: true

    case_common_type:
        isDictionary: true

    case_court_type:
        desc: Уровень суда
        isDictionary: true

    case_court_type_cat:
        desc: Уровень суда
        duplicate: case_court_type

    case_doc_district_rf:
        desc: Округ РФ
        isDictionary: true

    case_doc_instance:
        desc: Инстанция
        isDictionary: true

    case_doc_kind:
        desc: Вид судопроизводства
        isDictionary: true
        const: Уголовное дело

    case_doc_kind_prefix:
        skip: true
        desc: Однозначно соответствует case_doc_kind??

    case_doc_kind_short:
        skip: true
        desc: Однозначно соответствует case_doc_kind??

    case_doc_load_date:
        desc: Дата загрузки дела
        value: dateValue

    case_doc_source:
        desc: Источник
        const: Обезличенная БД СОЮ

    case_doc_source_table:
        desc: Источник (префикс таблиц)
        skip: true

    case_doc_subject_number:
        skip: true
        desc: Код субъекта РФ

    case_doc_subject_rf:
        skip: true
        desc: Субъект РФ

    case_doc_subject_rf_code:
        isDictionary: true
        desc: Субъект РФ (с кодом)

    case_document_articles:
        desc: Статьи закона
        isArray: true

    case_document_category_article:
        desc: Статья или категория
        isArray: true
        skip: true
        comment: Дублирует case_document_articles немного в другом формате

    case_document_id: {}

    case_document_load_date:
        desc: Дата загрузки дела
        value: dateValue
        # duplicate: case_doc_load_date

    case_document_num_build:
        value: longValue

    case_document_publ_date:
        value: dateValue

    case_document_result:
        desc: Результат
        isDictionary: true

    case_document_result_date:
        value: dateValue
        # duplicate: case_common_doc_result_date

    case_document_results:
        desc: Результат
        isDictionary: true
        duplicate: case_document_result

    case_document_types:
        duplicate: case_common_document_type

    case_doc_vnkod:
        desc: Код суда

    case_id:
        desc: Идентификатор дела

    case_id_region:
        desc: Идентификатор дела в субъекте

    case_regbasenum:
        value: longValue
        desc: Уровень по субъекту

    case_short_number:
        desc: Порядковый номер дела

    case_user_doc_court:
        desc: Наименование суда
        value: linkName
        const: null

    case_user_doc_entry_date:
        value: dateValue
        duplicate: case_common_doc_entry_date

    case_user_doc_number:
        desc: Номер дела (материала)

    case_user_doc_number_rewrite:
        duplicate: case_user_doc_number

    case_user_doc_result:
        duplicate: case_common_doc_result

    case_user_doc_result_date:
        value: dateValue
        duplicate: case_common_doc_result_date

    case_user_document_num:
        value: longValue
        comment: Количество документов в деле?

    case_user_document_text_tag: {}

    case_user_document_type:
        duplicate: case_common_document_type

    case_user_doc_validity_date:
        desc: Дата вступления в силу
        value: dateValue

    case_user_entry_date:
        value: dateValue
        duplicate: case_common_doc_entry_date

    case_user_judge:
        duplicate: case_common_judge

    case_user_type: {}

    case_year_entry:
        desc: Год поступления дела
        value: longValue

    case_year:
        desc: Год регистрации дела
        value: longValue

    case_year_result:
        desc: Год решения по делу
        value: longValue

    court_deside:
        desc: Дела с решением
        skip: true

    name:
        desc: Название

    timestamp:
        value: dateValue
        desc: Дата индексирования

    txt_exist:
        desc: Наличие текста
        skip: true

    u_case_common_article:
        desc: Статья УК РФ
        skip: true
        comment: Дублирует 

    u_case_user_article:
        duplicate: u_case_common_article

    u_common_case_defendant_m:
        isArray: true
        desc: ФИО, статья, результат дела?

    u_common_case_defendant_m_search:
        isArray: true
        duplicate: u_common_case_defendant_m

    u_common_case_defendant_name:
        desc: ФИО защитника
        isArray: true
        skip: true
        comment: В u_common_case_defendant_m более полная информация
'''))


def name_value(fld):
    name = fld['name']
    val = fld[known_fields[name].get('value', 'value')]
    if isinstance(val, str):
        val = val.strip()
    return (name, val)
