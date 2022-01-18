#!/usr/bin/env bash

set -o pipefail

DATA_FILES="$@"
PSQL='psql -v ON_ERROR_STOP=1 frodus'


echo "### Extract TSV"
PROPS_TMP=$(mktemp /tmp/props.XXXXXX)
TEXT_TMP=$(mktemp /tmp/text.XXXXXX)
../extract.py --props $PROPS_TMP --text $TEXT_TMP $DATA_FILES


echo "### Load properties"
PROPS_TABLE=raw_props_`date +%s`
$PSQL <<EOF
  create table $PROPS_TABLE(id text not null, data json not null);
EOF

$PSQL -c "copy $PROPS_TABLE from stdin" < $PROPS_TMP

raw_table=$PROPS_TABLE \
  j2 -e config insert_props.sql.j2 config.yaml \
  | $PSQL

$PSQL  -c "drop table $PROPS_TABLE"
rm $PROPS_TMP


echo "### Load texts"
TEXT_TABLE=raw_text_`date +%s`
$PSQL <<EOF
  create table $TEXT_TABLE(id text not null, data json not null);
EOF

$PSQL -c "copy $TEXT_TABLE from stdin" < $TEXT_TMP

raw_table=$TEXT_TABLE \
  j2 -e config insert_texts.sql.j2 config.yaml \
  | $PSQL

$PSQL -c "drop table $TEXT_TABLE"
rm $TEXT_TMP
