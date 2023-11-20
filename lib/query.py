import yaml
import json
import textwrap
import time
from datetime import datetime, timedelta

LIMIT = 20

def case_user_doc_result_date(from_date, to_date):
    query = yaml.safe_load(textwrap.dedent(f'''
        mode: EXTENDED
        typeRequests:
            - fieldRequests:
                - name: case_user_doc_result_date
                  operator: B
                  query: '{from_date.isoformat()}'
                  sQuery: '{to_date.isoformat()}'
                  fieldName: case_user_doc_result_date
              mode: AND
              name: common
              typesMode: AND
        '''
    ))
    return json.dumps(query, ensure_ascii=False)

def search(group, from_date, to_date, offset=0):
    date_query = case_user_doc_result_date(from_date, to_date)

    if group == 'ugo':
        queryId = '7f9e8ff8-4bc8-46aa-bcbd-f2b3ed5f159f'
        groups = ['Уголовные дела']
        additionalFields = additionalFields_ugo
    elif group == 'adm':
        groups = ['Дела об АП']
        queryId = '1f074cdd-f56a-4089-b901-df7a05b3a5c8'
        additionalFields = additionalFields_adm

    query = yaml.safe_load(textwrap.dedent(f'''
        doNotSaveHistory: true
        request:
          start: {offset}
          rows: {LIMIT}
          groups: []
          sorts:
            - field: score
              order: desc
          type: MULTIQUERY
          multiqueryRequest:
            queryRequests:
              - type: Q
                request: |
                    {date_query}
                operator: AND
                queryRequestRole: CATEGORIES
              - type: SQ
                queryId: '{queryId}'
                operator: AND
          simpleSearchFieldsBundle: null
          noOrpho: true
          facet:
            field:
              - type
          facetLimit: 21
          hlFragSize: 1000
          groupLimit: 3
          woBoost: false
          additionalFields: []
        '''))

    query['request']['groups'] = groups
    query['request']['additionalFields'] = additionalFields
    return query

'''
request:
  groups:
    - Дела об АП
  type: MULTIQUERY
  multiqueryRequest:
    queryRequests:
      - type: Q
        request: {request}
        operator: AND
        queryRequestRole: CATEGORIES
      - type: SQ
        queryId: 1f074cdd-f56a-4089-b901-df7a05b3a5c8
        operator: AND
  sorts:
    - field: score
      order: desc
  simpleSearchFieldsBundle: null
  start: 0
  rows: 10
  uid: d6a383f3-b91d-4058-9688-a52be634584c
  noOrpho: false
  facet:
    field:
      - type
  facetLimit: 21
  additionalFields:
    - case_user_doc_number
    - case_user_document_type
    - case_common_parts_law_article
    - case_user_entry_date
    - case_user_doc_result_date
    - case_doc_subject_rf
    - case_user_doc_court
    - adm_case_user_name
    - case_user_doc_result
  hlFragSize: 1000
  groupLimit: 3
  woBoost: false
doNotSaveHistory: false
'''


additionalFields_ugo = [
    'case_common_doc_court',            'case_common_doc_entry_date',
    'case_common_doc_number',           'case_common_doc_number_rewrite',
    'case_common_doc_result',           'case_common_doc_result_date',
    'case_common_document_article',     'case_common_document_num',
    'case_common_document_type',        'case_common_doc_validity_date',
    'case_common_entry_date',           'case_common_event_m2',
    'case_common_judge',                'case_common_parts_m2_search',
    'case_common_parts_name',           'case_common_parts_type',
    'case_common_type',                 'case_court_type',
    'case_court_type_cat',              'case_doc_district_rf',
    'case_doc_instance',                'case_doc_kind',
    'case_doc_kind_prefix',             'case_doc_kind_short',
    'case_doc_load_date',               'case_doc_source',
    'case_doc_source_table',            'case_doc_subject_number',
    'case_doc_subject_rf',              'case_doc_subject_rf_code',
    'case_document_articles',           'case_document_category_article',
    'case_document_id',                 'case_document_load_date',
    'case_document_num_build',          'case_document_publ_date',
    'case_document_result',             'case_document_result_date',
    'case_document_results',            'case_document_types',
    'case_doc_vnkod',                   'case_id',
    'case_id_region',                   'case_regbasenum',
    'case_short_number',                'case_user_doc_court',
    'case_user_doc_entry_date',         'case_user_doc_number',
    'case_user_doc_number_rewrite',     'case_user_doc_result',
    'case_user_doc_result_date',        'case_user_document_num',
    'case_user_document_text_tag',      'case_user_document_type',
    'case_user_doc_validity_date',      'case_user_entry_date',
    'case_user_judge',                  'case_user_type',
    'case_year',                        'case_year_entry',
    'case_year_result',                 'court_deside',
    'name',                             'timestamp',
    'txt_exist',                        'u_case_common_article',
    'u_case_user_article',              'u_common_case_defendant_m',
    'u_common_case_defendant_m_search', 'u_common_case_defendant_name'
    ]


additionalFields_adm = [
  'adm_case_common_article',        'adm_case_common_name',
  'adm_case_id',                    'adm_case_result',
  'adm_case_user_name',             'case_common_doc_court',
  'case_common_doc_entry_date',     'case_common_doc_number',
  'case_common_doc_number_rewrite', 'case_common_doc_result',
  'case_common_doc_result_date',    'case_common_document_num',
  'case_common_document_type',      'case_common_doc_validity_date',
  'case_common_entry_date',         'case_common_event_date',
  'case_common_event_m2',           'case_common_event_m2_search',
  'case_common_event_name',         'case_common_judge',
  'case_common_parts_breaking_law', 'case_common_parts_law_article',
  'case_common_parts_m2_search',    'case_common_parts_name',
  'case_common_parts_type',         'case_court_type',
  'case_court_type_cat',            'case_doc_district_rf',
  'case_doc_instance',              'case_doc_kind',
  'case_doc_kind_prefix',           'case_doc_kind_short',
  'case_doc_load_date',             'case_doc_source',
  'case_doc_source_table',          'case_doc_subject_number',
  'case_doc_subject_rf',            'case_doc_subject_rf_code',
  'case_document_articles',         'case_document_category_article',
  'case_document_id',               'case_document_load_date',
  'case_document_num_build',        'case_document_publ_date',
  'case_document_result_date',      'case_document_types',
  'case_doc_vnkod',                 'case_hear_date',
  'case_hear_date_s',               'case_hear_m2',
  'case_hear_m2_search',            'case_id',
  'case_id_region',                 'case_regbasenum',
  'case_short_number',              'case_user_doc_court',
  'case_user_doc_entry_date',       'case_user_doc_number',
  'case_user_doc_number_rewrite',   'case_user_doc_result',
  'case_user_doc_result_date',      'case_user_document_num',
  'case_user_document_text_tag',    'case_user_document_type',
  'case_user_doc_validity_date',    'case_user_entry_date',
  'case_user_judge',                'case_year',
  'case_year_entry',                'case_year_result',
  'court_deside',                   'name',
  'timestamp',                      'txt_exist',
  ]
