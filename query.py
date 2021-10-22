import uuid
import yaml
import json
import textwrap
import time
from datetime import datetime, timedelta

LIMIT = 20

def case_user_doc_result_date(date):
    query = yaml.safe_load(textwrap.dedent(f'''
        mode: EXTENDED
        typeRequests:
            - fieldRequests:
                - name: case_user_doc_result_date
                  operator: B
                  query: '{date.isoformat()}'
                  sQuery: '{(date + timedelta(days=1)).isoformat()}'
                  fieldName: case_user_doc_result_date
              mode: AND
              name: common
              typesMode: AND
        '''
    ))
    return json.dumps(query, ensure_ascii=False)


query_id = uuid.uuid4()

def search(day, offset=0):
    date_query = case_user_doc_result_date(day)

    query = yaml.safe_load(textwrap.dedent(f'''
        doNotSaveHistory: true
        request:
          start: {offset}
          rows: {LIMIT}
          groups:
            - Уголовные дела
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
                queryId: 7f9e8ff8-4bc8-46aa-bcbd-f2b3ed5f159f
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
          additionalFields:
              - case_common_doc_court
              - case_common_doc_entry_date
              - case_common_doc_number
              - case_common_doc_number_rewrite
              - case_common_doc_result
              - case_common_doc_result_date
              - case_common_document_article
              - case_common_document_num
              - case_common_document_type
              - case_common_doc_validity_date
              - case_common_entry_date
              - case_common_event_m2
              - case_common_judge
              - case_common_parts_m2_search
              - case_common_parts_name
              - case_common_parts_type
              - case_common_type
              - case_court_type
              - case_court_type_cat
              - case_doc_district_rf
              - case_doc_instance
              - case_doc_kind
              - case_doc_kind_prefix
              - case_doc_kind_short
              - case_doc_load_date
              - case_doc_source
              - case_doc_source_table
              - case_doc_subject_number
              - case_doc_subject_rf
              - case_doc_subject_rf_code
              - case_document_articles
              - case_document_category_article
              - case_document_id
              - case_document_load_date
              - case_document_num_build
              - case_document_publ_date
              - case_document_result
              - case_document_result_date
              - case_document_results
              - case_document_types
              - case_doc_vnkod
              - case_id
              - case_id_region
              - case_regbasenum
              - case_short_number
              - case_user_doc_court
              - case_user_doc_entry_date
              - case_user_doc_number
              - case_user_doc_number_rewrite
              - case_user_doc_result
              - case_user_doc_result_date
              - case_user_document_num
              - case_user_document_text_tag
              - case_user_document_type
              - case_user_doc_validity_date
              - case_user_entry_date
              - case_user_judge
              - case_user_type
              - case_year
              - case_year_entry
              - case_year_result
              - court_deside
              - name
              - timestamp
              - txt_exist
              - u_case_common_article
              - u_case_user_article
              - u_common_case_defendant_m
              - u_common_case_defendant_m_search
              - u_common_case_defendant_name
        '''))
    return query

