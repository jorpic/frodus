#!/usr/bin/env bash

set -o pipefail

DATA_FILES="$@"
PSQL='psql -v ON_ERROR_STOP=1 frodus'


TABLE=raw_data_`date +%s`
$PSQL <<EOF
  create table $TABLE(
    id text not null,
    data json not null,
    txt json not null);
EOF

../extract.py $DATA_FILES \
  | $PSQL -c "copy $TABLE from stdin"

raw_table=$TABLE \
  j2 -e config load_data.sql.j2 config.yaml \
  | $PSQL

$PSQL  -c "drop table $TABLE"
