#!/usr/bin/env bash

PSQL='psql -v ON_ERROR_STOP=1 frodus'


for yyyy in {2015,2016,2017,2018,2019,2020,2021} ; do
for q in {1,2,3,4} ; do
echo "`date --rfc-3339=s` $yyyy-$q"
FILE=text-$yyyy-$q.tsv.xz
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
