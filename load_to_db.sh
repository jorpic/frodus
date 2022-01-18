#!/usr/bin/env bash

set -o pipefail

DATA_FILES="$@"

PSQL='psql -v ON_ERROR_STOP=1 frodus'
TABLE=raw_data_`date +%s`

$PSQL <<EOF
  drop table if exists $TABLE;
  create table $TABLE(id text not null, data json not null);
EOF

time \
  ./convert.py \
    --format tsv \
    --skip-duplicates \
    --except case_user_document_text_tag \
    $DATA_FILES \
  | $PSQL -c "copy $TABLE from stdin"

# FIXME: table name in env params
cd db
raw_table=$TABLE time \
  j2 -e config transform.sql.j2 config.yaml \
  | $PSQL
cd -


$PSQL <<EOF
  drop table if exists $TABLE;
EOF
