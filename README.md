
```bash
export HTTPS_PROXY="http://51.250.41.21:1080"
ssh -i ~/.ssh/dnl -N -D 1080 51.250.41.21 &
while [[ 1 ]] ; do ./download.py adm 2021 ; sleep 329 ; done
```

```fish
set KEYS '"adm_case_common_article","adm_case_common_name","adm_case_id","adm_case_result","adm_case_user_name","case_common_doc_court","case_common_doc_entry_date","case_common_doc_number","case_common_doc_result","case_common_doc_result_date","case_common_doc_validity_date","case_common_document_num","case_common_document_type","case_common_event_date","case_common_event_m2","case_common_event_m2_search","case_common_event_name","case_common_judge","case_common_parts_breaking_law","case_common_parts_law_article","case_common_parts_m2_search","case_court_type","case_doc_district_rf","case_doc_instance","case_doc_load_date","case_doc_subject_rf_code","case_document_articles","case_document_id","case_document_load_date","case_document_num_build","case_document_publ_date","case_document_result_date","case_hear_date","case_id","case_id_region","case_regbasenum","case_user_doc_court","case_user_doc_validity_date","case_user_document_num","case_year","case_year_entry","case_year_result","id","timestamp","txt_exist"'

for m in {01,02,03,04,05,06,07,08,09,10,11,12} ;
  echo $m ;
  stack run -- ../fields-spec.yaml ../data/2022-$m* \
    | jq -r "del(.case_user_document_text_tag) | [.[$KEYS]] | @csv" \
    | xz -c -3 -T2 > 2022-$m.meta.csv.xz ;
end
```

```fish
for m in {01,02,03,04,05,06,07,08,09,10,11,12} ;
  echo $m ;
  stack run -- ../fields-spec.yaml ../data/2022-$m* \
    | jq -r '[.id, .case_user_document_text_tag] | @csv' \
    | xz -c -3 -T2 > 2022-$m.text.csv.xz ;
end
```
