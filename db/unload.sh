#!/usr/bin/env bash

PSQL='psql -v ON_ERROR_STOP=1 frodus'


pg_dump --schema-only --no-owner frodus > schema.sql

pg_dump --data-only \
  --exclude-table='case_text*' \
  --exclude-table=case_common_event_m2 \
  --exclude-table=u_common_case_defendant_m \
  --exclude-table=case_common_parts_m2_search \
  frodus \
    | xz -zc > case_props.sql.xz

pg_dump --data-only \
  --table=case_common_event_m2 \
  --table=u_common_case_defendant_m \
  --table=case_common_parts_m2_search \
  frodus \
    | xz -zc > case_arrays.sql.xz

for yyyy in {2015,2016,2017,2018,2019,2020,2021} ; do
for q in {1,2,3,4} ; do
echo "`date --rfc-3339=s` $yyyy-$q"
FILE=case_text-$yyyy-$q.tsv.xz
$PSQL <<EOF | xz -z > $FILE
  \copy ( \
    select t.* \
      from case_props p, case_text t \
      where \
        p.id = t.doc_id \
        and extract('year' from case_common_doc_result_date) = $yyyy \
        and extract('quarter' from case_common_doc_result_date) = $q \
    ) to stdout;
EOF
ls -sh $FILE
done
done
