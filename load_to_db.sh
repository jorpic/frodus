#!/usr/bin/env bash

set -o pipefail

DATA_FILES="$@"

PSQL='psql -v ON_ERROR_STOP=1 frodus'
TABLE=raw_props_`date +%s`

echo "### Load properties"

$PSQL <<EOF
  create table $TABLE(id text not null, data json not null);
EOF

time \
  ./convert.py \
    --format tsv \
    --skip-duplicates \
    --except case_user_document_text_tag \
    $DATA_FILES \
  | $PSQL -c "copy $TABLE from stdin"

cd db
raw_table=$TABLE time \
  j2 -e config insert_props.sql.j2 config.yaml \
  | $PSQL
cd -


$PSQL <<EOF
  drop table $TABLE;
EOF


echo "### Load texts"
TABLE=raw_texts_`date +%s`

$PSQL <<EOF
  create table $TABLE(id text not null, data json not null);
EOF

time \
  ./convert.py \
    --format tsv \
    --skip-duplicates \
    --only case_user_document_text_tag \
    $DATA_FILES \
  | $PSQL -c "copy $TABLE from stdin"

cd db
raw_table=$TABLE time \
  j2 -e config insert_texts.sql.j2 config.yaml \
  | $PSQL
cd -

$PSQL <<EOF
  drop table $TABLE;
EOF
